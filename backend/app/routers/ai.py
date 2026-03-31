from fastapi import APIRouter, HTTPException, Depends
from ..dependencies import get_openai_service
from ..models.models import BaseResponse

router = APIRouter(prefix="/api/v1/ai", tags=["AI Assistant"])


@router.post("/query")
async def process_ai_query(query: str, session_id: str, ai_service=Depends(get_openai_service)):
    """Ask the AI assistant a question about stocks or companies.
    session_id groups messages into a conversation so the AI remembers context.
    """
    try:
        response = await ai_service.process_query(query, session_id)
        message = response.get("message", "No response available") if isinstance(response, dict) else str(response)
        return BaseResponse(
            success=True,
            message=message,
            data={"query": query, "response": response}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")


@router.get("/examples")
async def get_ai_examples():
    """Return example questions for the AI assistant."""
    examples = [
        "Compare Apple and Microsoft stock performance",
        "What does NVIDIA do and why is it successful?",
        "Should I invest in Tesla right now?",
        "Explain Amazon's business model",
        "What are the risks of investing in tech stocks?",
        "Which companies have the highest revenue?",
        "Tell me about Apple's financial health",
        "What is technical analysis and how does it work?",
        "Compare the profitability of Google vs Meta",
        "What sectors are performing well this year?"
    ]
    return BaseResponse(success=True, message="Example queries", data={"examples": examples})


@router.get("/health")
async def ai_health_check(ai_service=Depends(get_openai_service)):
    """Check if the AI service is responsive."""
    try:
        test_response = await ai_service.process_query("Hello, are you working?", "health-check")
        return BaseResponse(
            success=True,
            message="AI service is healthy",
            data={"status": "ready", "test_response": test_response}
        )
    except Exception as e:
        return BaseResponse(
            success=False,
            message=f"AI service error: {str(e)}",
            data={"status": "error"}
        )
