import asyncio
import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from schemas.dtos import DefenseTurnRequest

router = APIRouter(prefix="/defense", tags=["Defense Session & SSE"])

@router.post("/turns/stream")
async def stream_defense_turn(req: DefenseTurnRequest):
    """
    Streaming phản hồi của AI Giám khảo phản biện qua giao thức Server-Sent Events (SSE).
    """
    async def event_generator():
        prefix = "🤖 [AI Giám Khảo]: "
        response_text = (
            f"Tôi đã ghi nhận giải thích của bạn về: '{req.student_reply[:60]}...'. "
            "Quyết định dùng giải pháp này rất hợp lý trong điều kiện tải bình thường. "
            "Tuy nhiên, nếu hệ thống có 10,000 người dùng đồng thời và kết nối mạng bị rớt giữa chừng, "
            "bạn sẽ thiết kế cơ chế Retry và Idempotency Key ở tầng API như thế nào để tránh trừ tiền 2 lần?"
        )
        
        yield f"data: {json.dumps({'token': prefix})}\n\n"
        await asyncio.sleep(0.1)

        words = response_text.split(" ")
        for word in words:
            yield f"data: {json.dumps({'token': word + ' '})}\n\n"
            await asyncio.sleep(0.04)

        yield f"data: {json.dumps({'done': True, 'rubric_hint': 'Cần trả lời rõ về Idempotency Header và Atomic Database Transaction'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
