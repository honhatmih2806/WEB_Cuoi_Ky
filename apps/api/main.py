import time
from datetime import datetime
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from core.config import settings
from core.database import Base, engine
from core.envelope import ApiResponse
from core.exceptions import AppException
from routers import products, categories, bundles, orders, advisor

# Create Database tables automatically on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API chuyên nghiệp cho nền tảng thương mại điện tử kết hợp Apple iPhone & NVIDIA Silicon.",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Timing Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    return response

# Custom AppException Handler
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse.fail(
            code=exc.code,
            message=exc.message,
            details=exc.details
        ).model_dump()
    )

# Validation Error Handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    details = [{"field": ".".join(str(loc) for loc in err["loc"]), "msg": err["msg"]} for err in errors]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ApiResponse.fail(
            code="ERR_VAL_001",
            message="Dữ liệu gửi lên không đúng định dạng",
            details=details
        ).model_dump()
    )

# Global Unhandled Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ApiResponse.fail(
            code="ERR_SYS_002",
            message="Lỗi hệ thống nội bộ không xác định",
            details=str(exc)
        ).model_dump()
    )

# Include Routers
app.include_router(products.router, prefix=settings.API_V1_STR)
app.include_router(categories.router, prefix=settings.API_V1_STR)
app.include_router(bundles.router, prefix=settings.API_V1_STR)
app.include_router(orders.router, prefix=settings.API_V1_STR)
app.include_router(advisor.router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["System"])
def health_check():
    return ApiResponse.ok(data={
        "status": "HEALTHY",
        "service": "titan-silicon-api",
        "version": settings.VERSION,
        "database_url": settings.DATABASE_URL.split("@")[-1] if "@" in settings.DATABASE_URL else "sqlite",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.get("/", tags=["System"])
def root():
    return ApiResponse.ok(data={
        "store": "TITAN SILICON — Apple & NVIDIA Ecosystem Flagship",
        "docs_swagger": f"{settings.API_V1_STR}/docs",
        "status": "Online"
    })
