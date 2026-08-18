import time
from typing import TypeVar, Protocol
from pydantic import BaseModel
from openai import AsyncOpenAI
from app.config import settings

T = TypeVar("T", bound=BaseModel)

class AIAdapter(Protocol):
    async def generate_structured(
        self,
        prompt: str,
        system_prompt: str,
        response_model: type[T]
    ) -> tuple[T, float]:
        """Generates a structured Pydantic object to enable any AI Model Usage rather than Tightly coupled with one model provider only ."""
        ...

class OpenAIResponsesAdapter:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL or "gpt-5.6-luna"
        self.base_url = settings.OPENROUTER_BASE_URL

        self.client = AsyncOpenAI(
            api_key=self.api_key or "dummy-key-for-dev",
            base_url=self.base_url,
            timeout=30.0,
        )

    async def generate_structured(
        self,
        prompt: str,
        system_prompt: str,
        response_model: type[T]
        ) -> tuple[T, float, str]:
        """Calls client.responses.parse and returns parsed Pydantic model + latency."""
        
        start_time = time.perf_counter()

        response = await self.client.responses.parse(
            model=self.model,
            instructions=system_prompt,
            input=prompt,
            reasoning={"effort": "low"},
            text_format=response_model,
        )

        latency_ms = (time.perf_counter() - start_time) * 1000.0

        parsed_result: T = response.output_parsed
        raw_text = response.output_text or "{}"
        return parsed_result, latency_ms, raw_text
