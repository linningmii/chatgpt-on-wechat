import requests
import json

notion_secret = "secret_pgJr57yecFM9WWHqSZuH5oxN9xq9ZSsTttkj63XOn7g"

auth_token = f'Bearer ${notion_secret}'

headers = {
    'Authorization': auth_token,
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
}
database_id = '8ee5cba98c974c07830ec834ff1ce03e'

response = requests.get(f"https://api.notion.com/v1/databases/{database_id}", headers=headers)
page_response = requests.get(f"https://api.notion.com/v1/pages/d158eed7424547658ad9dde3131ac164")
print(response)