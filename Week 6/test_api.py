import requests

# Base URL
BASE_URL = "http://127.0.0.1:5000"

# 1. Add a Course
course_data = {
    "course_name": "Math",
    "course_code": "MTH101"
}
response = requests.post(f"{BASE_URL}/course", json=course_data)
print("Add Course Response:", response.status_code, response.json())
