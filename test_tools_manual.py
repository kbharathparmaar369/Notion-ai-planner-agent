from app.tools import get_tasks, create_task, update_task_status, get_weather

print("--- Testing get_tasks ---")
print(get_tasks())

print("\n--- Testing create_task ---")
result = create_task("Test task from script", "2026-10-10")
print(result)

print("\n--- Testing get_weather (example: Hubballi, India) ---")
print(get_weather(15.3647, 75.1240))