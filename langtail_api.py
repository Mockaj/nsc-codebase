# langtail_api.py
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LANGTAIL_WORKSPACE = os.getenv('LANGTAIL_WORKSPACE')
LANGTAIL_PROJECT = os.getenv('LANGTAIL_PROJECT')
LANGTAIL_ASSISTANT = os.getenv('LANGTAIL_ASSISTANT')
LANGTAIL_ENVIRONMENT = os.getenv('LANGTAIL_ENVIRONMENT')
LANGTAIL_API_KEY = os.getenv('LANGTAIL_API_KEY')

BASE_URL = 'https://api.langtail.com'

HEADERS = {
    'X-API-Key': LANGTAIL_API_KEY,
    'Content-Type': 'application/json'
}

def create_thread(metadata=None):
    url = f"{BASE_URL}/v2/threads"
    payload = {}
    if metadata:
        payload['metadata'] = metadata
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()

def delete_thread(thread_id):
    url = f"{BASE_URL}/v2/threads/{thread_id}"
    response = requests.delete(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def list_threads():
    url = f"{BASE_URL}/v2/threads"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def send_message(thread_id, messages):
    url = f"{BASE_URL}/{LANGTAIL_WORKSPACE}/{LANGTAIL_PROJECT}/{LANGTAIL_ASSISTANT}/{LANGTAIL_ENVIRONMENT}"
    payload = {
        'threadId': thread_id,
        'messages': messages,
        'stream': False
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()