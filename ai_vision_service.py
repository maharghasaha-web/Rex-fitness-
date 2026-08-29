import json
import logging
from typing import Dict, Any, Optional
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIVisionService:
    """
    Handles Multimodal AI Vision requests (supporting Google Gemini Vision / OpenAI GPT-4o).
    Provides structured JSON responses and fallback heuristics for offline development/testing.
    """
    
    @staticmethod
    async def analyze_image_with_gemini(
        image_base64: Optional[str],
        image_url: Optional[str],
        system_prompt: str,
        user_prompt: str
    ) -> Optional[Dict[str, Any]]:
        """Calls Gemini 1.5 Flash/Pro Vision API if API key is configured."""
        if not settings.GEMINI_API_KEY:
            return None
        
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
            
            parts = [{"text": f"{system_prompt}\n\n{user_prompt}"}]
            if image_base64:
                parts.append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": image_base64
                    }
                })
            
            payload = {
                "contents": [{"parts": parts}],
                "generationConfig": {
                    "response_mime_type": "application/json",
                    "temperature": 0.2
                }
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    text_content = result["candidates"][0]["content"]["parts"][0]["text"]
                    return json.loads(text_content)
                else:
                    logger.warning(f"Gemini API returned status {response.status_code}: {response.text}")
        except Exception as e:
            logger.error(f"Error calling Gemini Vision API: {e}")
        return None
