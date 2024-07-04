import requests
import json

# Configuration
openai_api_key = ''
jira_url = ''
jira_api_token = ''
jira_username = ''
project_key = ''
issue_type = ''

# Function to generate issue summary and description using OpenAI
def generate_issue_details(prompt):
    headers = {
        'Authorization': f'Bearer {openai_api_key}',
        'Content-Type': 'application/json'
    }
    data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            'max_tokens': 100
        }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    response_data = response.json()
    return response_data['choices'][0]['message']['content']

# Prompt for OpenAI to generate issue details
prompt = """
Generate a Jira issue summary and description for creating a database connection. The description should include user story and acceptance criteria.
"""

# Generate issue details
issue_details = generate_issue_details(prompt).split('\n', 1)
summary = issue_details[0].strip()
description = issue_details[1].strip()

# Jira API payload
jira_payload = {
    'fields': {
        'project': {
            'key': project_key
        },
        'summary': summary,
        'description': description,
        'issuetype': {
            'name': issue_type
        }
    }
}

# Function to create an issue in Jira
def create_jira_issue(payload):
    url = f'{jira_url}/rest/api/2/issue'
    auth = (jira_username, jira_api_token)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, auth=auth, headers=headers, json=payload)
    return response.json()

# Create the Jira issue
jira_response = create_jira_issue(jira_payload)
print(jira_response)
