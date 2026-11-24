from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.envelope import ApiResponse
from core.exceptions import AppException
from core.security import verify_password, get_password_hash, create_access_token
from models.entities import User
from schemas.dtos import RegisterRequest, LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=ApiResponse[TokenResponse], status_code=status.HTTP_201_CREATED)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise AppException(code="ERR_AUTH_004", message="Email này đã được đăng ký", status_code=409)
    
    user = User(
        email=req.email,
        hashed_password=get_password_hash(req.password),
        full_name=req.full_name,
        role=req.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    token = create_access_token({"sub": str(user.id), "role": user.role, "email": user.email})
    return ApiResponse.ok(TokenResponse(
        access_token=token,
        user_id=str(user.id),
        role=user.role,
        full_name=user.full_name
    ))

@router.post("/login", response_model=ApiResponse[TokenResponse])
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise AppException(code="ERR_AUTH_002", message="Email hoặc mật khẩu không chính xác", status_code=401)
    
    if not user.is_active:
        raise AppException(code="ERR_AUTH_005", message="Tài khoản đã bị vô hiệu hóa", status_code=403)
        
    token = create_access_token({"sub": str(user.id), "role": user.role, "email": user.email})
    return ApiResponse.ok(TokenResponse(
        access_token=token,
        user_id=str(user.id),
        role=user.role,
        full_name=user.full_name
    ))
