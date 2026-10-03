"""Optional Gemini integration. Core CyberDesk remains functional without it."""
import httpx
from app.core.config import get_settings

class AIError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

async def assist(prompt: str, context: str | None) -> tuple[str, str]:
    settings = get_settings()
    if not settings.gemini_api_key:
        raise AIError(503, "AI assistant is not configured. Core CyberDesk features remain available.")
    model = settings.gemini_model
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    system = (
        "You are CyberDesk's cybersecurity learning assistant. "
        "Teach defensively and safely. Do not provide instructions for malware, credential theft, "
        "real-target scanning, persistence, or arbitrary code execution. Keep explanations suitable "
        "for a university cybersecurity student."
    )
    if context:
        system += f"\nLearning context:\n{context}"
    payload = {"system_instruction": {"parts": [{"text": system}]}, "contents": [{"parts": [{"text": prompt}]}]}
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(url, params={"key": settings.gemini_api_key}, json=payload)
    except httpx.HTTPError:
        raise AIError(502, "AI provider could not be reached.")
    if response.status_code >= 400:
        raise AIError(502, "AI provider returned an error.")
    data = response.json()
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    answer = "".join(p.get("text", "") for p in parts).strip()
    if not answer:
        raise AIError(502, "AI provider returned no usable answer.")
    return answer, model
