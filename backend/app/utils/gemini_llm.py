from google import genai
from app.config.env import settings

gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
