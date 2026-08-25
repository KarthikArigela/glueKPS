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
        self.model = settings.OPENROUTER_MODEL
        self.base_url = settings.OPENROUTER_BASE_URL

        if not self.api_key:
            raise ValueError("AI API key is missing in .env! Please configure OPENROUTER_API_KEY.")
        
        if "openrouter.ai" in self.base_url:
            self.provider_name = "openrouter"
        elif "openai.com" in self.base_url:
            self.provider_name = "openai"
        else:
            self.provider_name = self.base_url.split("//")[-1].split("/")[0]

        self.client = AsyncOpenAI(
            api_key=self.api_key,
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
