from langchain.agents import create_agent

from dotenv import load_dotenv
load_dotenv(override=True, dotenv_path="../.env")

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


agent = create_agent(
    model="openai:gpt-5-mini",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "서울의 날씨를 알여줘."}]}
)