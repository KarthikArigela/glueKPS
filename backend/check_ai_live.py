import asyncio
from pydantic import BaseModel, Field

from app.services.ai_adapter import OpenAIResponsesAdapter
from app.services.ai_telemetry import record_ai_operation
from app.database import async_session_maker

class WeatherReport(BaseModel):
    city: str
    temperature_celsius: float
    summary: str = Field(description="One-sentence weather overview")
    clothing_recommendations: list[str]

async def main():
    print("🤖 Initializing AI Adapter...")
    adapter = OpenAIResponsesAdapter()
    print(f"📡 Configured Base URL: {adapter.base_url}")
    print(f"🧠 Configured Model: {adapter.model}")
    prompt = "What is the weather like in Tokyo right now?"
    system_prompt = "You are a helpful travel assistant. Output accurate structured weather data."
    print("\n⏳ Sending request to AI model...")
    try:
        result, latency_ms, raw_text = await adapter.generate_structured(
            prompt=prompt,
            system_prompt=system_prompt,
            response_model=WeatherReport
        )
        print("\n🎉 Live AI Call Successful!")
        print(f"⏱️ Latency: {latency_ms:.2f} ms")
        print(f"📊 Parsed Pydantic Output:\n{result.model_dump_json(indent=2)}")

        # Log operation into Supabase DB
        print("\n💾 Recording AI Telemetry in Supabase PostgreSQL...")
        async with async_session_maker() as session:
            db_record = await record_ai_operation(
                session=session,
                provider="openai_responses",
                model=adapter.model,
                prompt=prompt,
                response=raw_text,
                latency_ms=latency_ms,
            )
            print(f"✅ Saved to DB! Operation ID: {db_record.id}")
    except Exception as e:
        print("\n❌ Live AI Call Failed!")
        print(f"Error details: {e}")

if __name__ == "__main__":
    asyncio.run(main())