import requests
from app.config import notion_api, notion_db_id

headers = {
    "Authorization": f"Bearer {notion_api}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

notion_url = "https://api.notion.com/v1"


def get_tasks():
    # fetch all the tasks from the notion database
    url = f"{notion_url}/databases/{notion_db_id}/query"

    try:
        response = requests.post(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Failed to fetch tasks: {str(e)}"

    data = response.json()
    pages = data.get("results", [])

    task_list = []

    for page in pages:
        props = page.get("properties", {})

        title_data = props.get("Name", {}).get("title", [])
        if len(title_data) > 0:
            task_name = title_data[0].get("plain_text", "Untitled Task")
        else:
            task_name = "Untitled Task"

        status_data = props.get("Status", {}).get("status")
        if status_data:
            task_status = status_data.get("name", "No status")
        else:
            task_status = "No status"

        date_data = props.get("Due date", {}).get("date") or props.get("Due Date", {}).get("date")
        if date_data:
            due_date = date_data.get("start")
        else:
            due_date = None

        task_list.append({
            "id": page.get("id"),
            "name": task_name,
            "status": task_status,
            "due_date": due_date,
        })

    return task_list


def create_task(name, due_date=None):
    url = f"{notion_url}/pages"

    properties = {
        "Name": {"title": [{"text": {"content": name}}]}
    }

    if due_date:
        properties["Due date"] = {"date": {"start": due_date}}

    body = {
        "parent": {"database_id": notion_db_id},
        "properties": properties,
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=10)
        response.raise_for_status()
        new_page_id = response.json().get("id")
        return {"success": True, "id": new_page_id, "name": name}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Failed to create task: {str(e)}"}


def update_task_status(page_id, new_status):
    url = f"{notion_url}/pages/{page_id}"

    properties = {
        "Status": {"status": {"name": new_status}}
    }

    body = {
        "properties": properties
    }

    try:
        response = requests.patch(url, headers=headers, json=body, timeout=10)
        response.raise_for_status()
        return {"success": True, "id": page_id, "status": new_status}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Failed to update task: {str(e)}"}


def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,precipitation,weather_code",
        "timezone": "auto",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch the weather: {str(e)}"}

    current = response.json().get("current", {})

    return {
        "temperature": current.get("temperature_2m"),
        "precipitation": current.get("precipitation"),
        "weather_code": current.get("weather_code"),
    }