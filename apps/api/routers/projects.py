import uuid
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from core.database import get_db
from core.envelope import ApiResponse
from core.exceptions import AppException
from core.security import decode_access_token
from models.entities import Project, Phase, Task, PhaseGate
from schemas.dtos import OnboardingRequest, ProjectResponse, PhaseSummary

router = APIRouter(prefix="/projects", tags=["Projects & Roadmap"])

def get_current_user_id(authorization: str = Header(...)) -> uuid.UUID:
    if not authorization.startswith("Bearer "):
        raise AppException(code="ERR_AUTH_001", message="Thiếu token Bearer", status_code=401)
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    return uuid.UUID(payload["sub"])

@router.post("/onboarding", response_model=ApiResponse[ProjectResponse])
def onboarding(req: OnboardingRequest, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    # Create Project
    project = Project(
        user_id=user_id,
        title=req.title,
        domain=req.domain,
        target_skills=req.target_skills,
        summary=req.description,
        status="ACTIVE"
    )
    db.add(project)
    db.flush()

    # Generate standard template phases for Web + AI
    template_phases = [
        ("Giai đoạn 1: Thiết kế Cơ sở Dữ liệu & Kiến trúc REST API", "Thiết lập schema PostgreSQL, pgvector, ORM và API Contract."),
        ("Giai đoạn 2: Xây dựng Module Xác thực & Phân quyền bảo mật", "Triển khai JWT auth, RBAC và các Middleware bảo vệ endpoint."),
        ("Giai đoạn 3: Tích hợp AI Chatbot & Xử lý Thời gian thực", "Dựng SSE streaming, LLM Gateway và kết nối WebSocket."),
        ("Giai đoạn 4: Hoàn thiện Frontend & Trải nghiệm Người dùng", "Xây dựng giao diện Next.js, quản trị trạng thái, kết nối API."),
        ("Giai đoạn 5: Tối ưu hóa, Kiểm thử & Đóng gói Docker", "Kiểm thử đơn vị, đo tải và viết tài liệu bảo vệ đồ án.")
    ]

    phases_res = []
    for idx, (title, desc) in enumerate(template_phases, 1):
        phase = Phase(
            project_id=project.id,
            order_index=idx,
            title=title,
            description=desc,
            is_unlocked=(idx == 1)
        )
        db.add(phase)
        db.flush()

        # Create Gate
        gate = PhaseGate(
            phase_id=phase.id,
            status="OPEN" if idx == 1 else "LOCKED"
        )
        db.add(gate)

        # Create template tasks
        t1 = Task(phase_id=phase.id, title=f"Nghiên cứu & Thiết kế {title}", criteria="Hoàn thành tài liệu thiết kế", status="TODO")
        t2 = Task(phase_id=phase.id, title=f"Hiện thực mã nguồn {title}", criteria="Code chạy và có test pass", status="TODO")
        db.add_all([t1, t2])

        phases_res.append(PhaseSummary(
            id=phase.id,
            order_index=phase.order_index,
            title=phase.title,
            description=phase.description,
            is_unlocked=phase.is_unlocked
        ))

    db.commit()
    db.refresh(project)

    return ApiResponse.ok(ProjectResponse(
        id=project.id,
        title=project.title,
        domain=project.domain,
        target_skills=project.target_skills,
        status=project.status,
        ugi_score=project.ugi_score,
        phases=phases_res
    ))

@router.get("/{project_id}", response_model=ApiResponse[ProjectResponse])
def get_project(project_id: uuid.UUID, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise AppException(code="ERR_PROJ_001", message="Dự án không tồn tại", status_code=404)
    
    phases_res = [
        PhaseSummary(
            id=p.id,
            order_index=p.order_index,
            title=p.title,
            description=p.description,
            is_unlocked=p.is_unlocked
        ) for p in project.phases
    ]

    return ApiResponse.ok(ProjectResponse(
        id=project.id,
        title=project.title,
        domain=project.domain,
        target_skills=project.target_skills,
        status=project.status,
        ugi_score=project.ugi_score,
        phases=phases_res
    ))
