import http.client
import json
import argparse

def github_activity(username):
    connection = http.client.HTTPSConnection("api.github.com")

    header = {
    'User-Agent': "PythonApp"
    }

    connection.request("GET", f"/users/{username}/events", headers=header)
    response = connection.getresponse()
    data = response.read().decode('utf-8')
    connection.close()

    print(f"User: {username}")

    if response.status == 404:
        print(f"Username {username} not found")
    elif response.status != 200:
        print(f"Error: {response.status}")

    events = json.loads(data)
    if not events:
        print("No user activity")
        return
    
    for event in events:
        event_type = event.get("type")
        repo_name = event.get("repo",{}).get("name")
        created_at = event.get("created_at")
        print(f"{created_at}: {event_type} in {repo_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('username', type=str, help='GitHub username')
    args = parser.parse_args()
    print('-'*40)
    github_activity(args.username)
    print('-'*40)