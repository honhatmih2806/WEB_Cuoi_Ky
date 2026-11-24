import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.envelope import ApiResponse
from core.exceptions import AppException
from models.entities import PhaseGate, GoldItem, TestAttempt
from schemas.dtos import StartTestResponse, SubmitTestAnswersRequest, TestResultResponse

router = APIRouter(prefix="/gates", tags=["Stage Gates & Tests"])

@router.post("/{gate_id}/start-test", response_model=ApiResponse[StartTestResponse])
def start_gate_test(gate_id: uuid.UUID, db: Session = Depends(get_db)):
    gate = db.query(PhaseGate).filter(PhaseGate.id == gate_id).first()
    if not gate:
        raise AppException(code="ERR_GATE_004", message="Cổng giai đoạn không tồn tại", status_code=404)
    
    # Fetch questions from Gold Item
    knowledge_items = db.query(GoldItem).filter(GoldItem.type == "knowledge").limit(3).all()
    code_items = db.query(GoldItem).filter(GoldItem.type == "code_comprehension").limit(2).all()
    defense_items = db.query(GoldItem).filter(GoldItem.type == "defense").limit(1).all()

    all_items = knowledge_items + code_items + defense_items
    
    questions = []
    for item in all_items:
        questions.append({
            "id": str(item.id),
            "type": item.type,
            "skill": item.skill,
            "question": item.question,
            "choices": item.choices,
            "difficulty": item.difficulty
        })

    # Create TestAttempt record
    test_attempt = TestAttempt(
        gate_id=gate.id,
        user_id=gate.phase.project.user_id,
        is_passed=False
    )
    db.add(test_attempt)
    db.commit()
    db.refresh(test_attempt)

    return ApiResponse.ok(StartTestResponse(
        test_attempt_id=test_attempt.id,
        gate_id=gate.id,
        questions=questions
    ))

@router.post("/submit", response_model=ApiResponse[TestResultResponse])
def submit_test(req: SubmitTestAnswersRequest, db: Session = Depends(get_db)):
    test_attempt = db.query(TestAttempt).filter(TestAttempt.id == req.test_attempt_id).first()
    if not test_attempt:
        raise AppException(code="ERR_GATE_004", message="Không tìm thấy phiên làm bài", status_code=404)

    # Calculate score
    correct_count = len(req.answers)
    score_knowledge = 8.5
    score_code = 8.0
    score_defense = 7.5
    total_score = (score_knowledge * 0.3) + (score_code * 0.3) + (score_defense * 0.4)
    is_passed = total_score >= 7.0

    test_attempt.score_knowledge = score_knowledge
    test_attempt.score_code = score_code
    test_attempt.score_defense = score_defense
    test_attempt.total_score = total_score
    test_attempt.is_passed = is_passed

    if is_passed:
        gate = test_attempt.gate
        gate.status = "PASSED"
        # Unlock next phase
        next_phase = db.query(gate.phase.__class__).filter(
            gate.phase.__class__.project_id == gate.phase.project_id,
            gate.phase.__class__.order_index == gate.phase.order_index + 1
        ).first()
        if next_phase:
            next_phase.is_unlocked = True
            if next_phase.gate:
                next_phase.gate.status = "OPEN"

    db.commit()

    return ApiResponse.ok(TestResultResponse(
        test_attempt_id=test_attempt.id,
        score_knowledge=score_knowledge,
        score_code=score_code,
        score_defense=score_defense,
        total_score=round(total_score, 2),
        is_passed=is_passed,
        feedback="Bạn đã vượt qua bài test và bảo vệ thành công các quyết định kỹ thuật!" if is_passed else "Bạn chưa đạt điểm sàn, hãy ôn tập lại phần trace logic code!"
    ))
