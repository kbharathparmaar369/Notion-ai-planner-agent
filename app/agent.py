from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.tools import tool
from app.config import groq_api_key
from app.tools import get_tasks, create_task, update_task_status, get_weather


@tool
def get_tasks_tool() -> str:
    """Get all current tasks from Notion. Returns list of tasks with id, name, status, and due date."""
    return str(get_tasks())


@tool
def create_task_tool(name: str, due_date: str = None) -> str:
    """Create a new task in Notion. Parameters: name (task title), due_date (optional, format YYYY-MM-DD)."""
    if due_date and due_date.lower() == "none":
        due_date = None
    return str(create_task(name, due_date))


@tool
def update_status_tool(page_id: str, new_status: str) -> str:
    """Update a task's status in Notion. Parameters: page_id (Notion page ID), new_status (e.g. 'Not started', 'In progress', 'Done')."""
    return str(update_task_status(page_id, new_status))


@tool
def get_weather_tool(latitude: float, longitude: float) -> str:
    """Get current weather for a location. Parameters: latitude (float), longitude (float)."""
    return str(get_weather(latitude, longitude))


tools = [get_tasks_tool, create_task_tool, update_status_tool, get_weather_tool]

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model="openai/gpt-oss-120b",
    temperature=0,
)

system_message = """You are a helpful daily planning assistant.
You help the user plan their day using their Notion tasks and the weather.

Rules:
- If the user lists tasks directly in their message, plan around those too, not just Notion tasks.
- Check the weather when it's relevant to the plan.
- If you are about to create or update something in Notion, first tell the user what you plan to do and ask for confirmation before calling the tool.
- Keep your final answer clear and short, like a real daily plan.
"""

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_message,
)


def run_agent(user_message: str) -> str:
    result = agent.invoke({"messages": [{"role": "user", "content": user_message}]})
    messages = result.get("messages", [])
    if messages:
        return messages[-1].content
    return "No response generated."