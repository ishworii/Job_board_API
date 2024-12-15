import random
from datetime import datetime

import requests

# API base URL
BASE_URL = "http://localhost:8000/api"

job_titles = [
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "Python Developer",
    "React Developer",
    "UI/UX Designer",
    "Content Writer",
    "Digital Marketing Specialist",
    "Project Manager",
    "QA Engineer",
    "DevOps Engineer",
    "Mobile App Developer",
    "Business Analyst",
    "HR Manager",
    "Sales Executive",
    "Customer Support Representative",
    "SEO Specialist",
    "System Administrator",
    "Database Administrator",
    "IT Support Engineer"
]

locations = [
    "Kathmandu, Bagmati",
    "Lalitpur, Bagmati",
    "Bhaktapur, Bagmati",
    "Pokhara, Gandaki",
    "Birgunj, Madhesh",
    "Biratnagar, Province 1",
    "Butwal, Lumbini",
    "Dharan, Province 1",
    "Bharatpur, Bagmati",
    "Remote, Nepal"
]

categories = [
    "Software Development",
    "IT & Networking",
    "Design & Creative",
    "Sales & Marketing",
    "Customer Service",
    "Content & Writing",
    "Management",
    "Human Resources",
    "Digital Marketing",
    "Quality Assurance"
]

companies = [
    "Cotiviti Nepal",
    "Leapfrog Technology",
    "Deerwalk Services",
    "F1Soft International",
    "Cloud Factory",
    "Fusemachines Nepal",
    "Info Developers",
    "Yomari Information Services",
    "Asterdio Inc",
    "Bits Innovation"
]

salary_ranges = [
    "NPR 30,000 - 50,000",
    "NPR 50,000 - 80,000",
    "NPR 80,000 - 120,000",
    "NPR 120,000 - 150,000",
    "NPR 150,000 - 200,000",
    "As per experience",
    "Negotiable"
]

def setup_authentication():
    """Create an employer account and get access token"""
    # First try to register
    register_data = {
        "email": "employer@example.com",
        "password": "password123",
        "name": "John Doe",
        "role": "employer"
    }

    try:
        # Try to register first
        register_response = requests.post(f"{BASE_URL}/register", json=register_data)
        if register_response.status_code not in [200, 400]:  # 400 means user exists
            print(f"Registration failed: {register_response.text}")
            return None

        # Get token regardless of registration (either new user or existing)
        token_response = requests.post(
            f"{BASE_URL}/token",
            data={
                "username": register_data["email"],
                "password": register_data["password"]
            }
        )

        if token_response.status_code == 200:
            return token_response.json()["access_token"]
        else:
            print(f"Failed to get token: {token_response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error in authentication: {e}")
        return None

def create_job(token, job_data):
    """Create a job using the API"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/jobs/",
            json=job_data,
            headers=headers
        )
        if response.status_code == 200:
            print(f"Successfully created job: {job_data['title']}")
        else:
            print(f"Failed to create job: {job_data['title']}")
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error creating job: {e}")

def generate_description(title, company):
    return f"""
We are seeking a talented {title} to join our team at {company}. 

Key Responsibilities:
- Design, develop, and maintain software solutions
- Collaborate with cross-functional teams
- Write clean, efficient, and maintainable code
- Participate in code reviews and technical discussions

Requirements:
- 3+ years of relevant experience
- Strong problem-solving skills
- Excellent communication abilities
- Bachelor's degree in Computer Science or related field

We offer:
- Competitive salary
- Health insurance
- 401(k) matching
- Flexible work hours
- Professional development opportunities
"""


def main():
    # Get access token
    token = setup_authentication()
    if not token:
        print("Failed to get access token")
        return

    print("Successfully got access token")
    
    # Create 20 jobs
    for i in range(20):
        company = random.choice(companies)
        salary = random.choice(salary_ranges)
        job_data = {
            "title": random.choice(job_titles),
            "description": generate_description(job_titles[i], company),
            "category": random.choice(categories),
            "location": random.choice(locations),
        }
        create_job(token, job_data)

if __name__ == "__main__":
    main()

