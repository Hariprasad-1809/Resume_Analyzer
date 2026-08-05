#!/bin/bash

# AI Resume Analysis API - Curl Examples

# Set the API base URL (update if different)
API_URL="http://localhost:8000/api/v1/ai/analyze"

# Example 1: Basic Analysis Request
echo "=== Example 1: Basic Analysis Request ==="
curl -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Full Stack Developer",
    "resume_data": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1-234-567-8900",
      "location": "San Francisco, CA",
      "summary": "Experienced software engineer with 5+ years in full-stack development",
      "experience": [
        {
          "company": "Tech Corp",
          "position": "Senior Backend Engineer",
          "duration": "2020-2024",
          "description": "Led Python backend development using FastAPI and PostgreSQL. Designed microservices architecture. Mentored 3 junior developers.",
          "achievements": [
            "Reduced API latency by 40%",
            "Implemented automated testing (95% coverage)",
            "Led migration to Kubernetes"
          ]
        },
        {
          "company": "StartupXYZ",
          "position": "Full Stack Engineer",
          "duration": "2018-2020",
          "description": "Built full-stack web applications using React and Node.js",
          "achievements": [
            "Built customer dashboard used by 10K+ users",
            "Implemented real-time notifications"
          ]
        }
      ],
      "skills": [
        "Python",
        "FastAPI",
        "React",
        "PostgreSQL",
        "Docker",
        "Git",
        "REST APIs",
        "Database Design"
      ],
      "education": [
        {
          "school": "State University",
          "degree": "BS Computer Science",
          "year": "2018",
          "gpa": "3.8"
        }
      ],
      "projects": [
        {
          "name": "E-commerce Platform",
          "description": "Built scalable e-commerce backend API",
          "technologies": ["Python", "FastAPI", "PostgreSQL"],
          "impact": "Served 100K+ concurrent users"
        }
      ]
    }
  }' | jq .

echo -e "\n"

# Example 2: Minimal Request
echo "=== Example 2: Minimal Request ==="
curl -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Backend Developer",
    "resume_data": {
      "name": "Jane Smith",
      "email": "jane@example.com",
      "skills": ["Python", "Django", "PostgreSQL"],
      "experience": [
        {
          "company": "TechCorp",
          "position": "Backend Developer",
          "duration": "2021-2024"
        }
      ]
    }
  }' | jq .

echo -e "\n"

# Example 3: Save Response to File
echo "=== Example 3: Saving Response to File ==="
curl -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Data Scientist",
    "resume_data": {
      "name": "Alice Johnson",
      "email": "alice@example.com",
      "skills": ["Python", "Machine Learning", "TensorFlow", "SQL"],
      "experience": [
        {
          "company": "DataCorp",
          "position": "ML Engineer",
          "duration": "2020-2024",
          "description": "Built machine learning pipelines for real-time predictions"
        }
      ]
    }
  }' -o analysis_response.json

echo "Response saved to analysis_response.json"
cat analysis_response.json | jq .

echo -e "\n"

# Example 4: Check Status Code and Headers
echo "=== Example 4: Detailed Response Information ==="
curl -i -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "DevOps Engineer",
    "resume_data": {
      "name": "Bob Wilson",
      "email": "bob@example.com",
      "skills": ["Kubernetes", "Docker", "AWS", "CI/CD"],
      "experience": [
        {
          "company": "CloudInc",
          "position": "DevOps Engineer",
          "duration": "2019-2024"
        }
      ]
    }
  }'

echo -e "\n"

# Example 5: Error Handling - Missing Required Field
echo "=== Example 5: Error Handling - Invalid Request ==="
curl -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Software Engineer",
    "resume_data": {}
  }' | jq .

echo -e "\n"

# Example 6: Timeout Handling - Long Request
echo "=== Example 6: With Timeout Handling ==="
curl --max-time 30 -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Architect",
    "resume_data": {
      "name": "Charlie Brown",
      "email": "charlie@example.com",
      "skills": ["System Design", "Microservices", "Cloud Architecture"],
      "experience": [
        {
          "company": "Enterprise Corp",
          "position": "Solutions Architect",
          "duration": "2015-2024",
          "description": "Designed enterprise-scale solutions for Fortune 500 companies"
        }
      ]
    }
  }' | jq .

echo -e "\n"

# Example 7: Using jq to Filter Specific Fields
echo "=== Example 7: Get Only Match Score and Summary ==="
curl -s -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "QA Engineer",
    "resume_data": {
      "name": "Diana Prince",
      "email": "diana@example.com",
      "skills": ["Selenium", "Test Automation", "JIRA"],
      "experience": [
        {
          "company": "QA Systems",
          "position": "QA Engineer",
          "duration": "2020-2024"
        }
      ]
    }
  }' | jq '{overall_match, summary}'

echo -e "\n"

# Example 8: Pretty Print JSON Response
echo "=== Example 8: Pretty Print Full Response ==="
curl -s -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Senior Software Engineer",
    "resume_data": {
      "name": "Eve Adams",
      "email": "eve@example.com",
      "skills": ["Python", "Java", "Scala", "Big Data", "Spark"],
      "experience": [
        {
          "company": "TechGiant",
          "position": "Senior Software Engineer",
          "duration": "2018-2024",
          "description": "Led team of 5 engineers. Built data processing pipelines."
        }
      ]
    }
  }' | jq '.'
