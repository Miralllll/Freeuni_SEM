import requests
import base64

# GitHub personal access token and username
token = ''
username = ''

def update_bonus_file(repo_full_name):
    file_path = 'bonus.java'
    url = f'https://api.github.com/repos/gbochora/cs106a/contents/2023/midterm/session2/students/{repo_full_name}/problems/{file_path}'
    headers = {'Authorization': f'token {token}'}
    
    # Get current content of the file
    response = requests.get(url, headers=headers)
    content = response.json()
    
    if 'content' in content:
        decoded_content = base64.b64decode(content['content']).decode('utf-8')
        # Modify the content as needed
        # print(decoded_content)
        text_to_add = "ქულა: 0 \nმაქსიმალური ქულა: 0 \n"
        updated_content = text_to_add + decoded_content
        # print(updated_content)
        # Encode the updated content to base64
        encoded_content = base64.b64encode(updated_content.encode('utf-8')).decode('utf-8')
        
        # Prepare data for updating the file
        data = {
            "message": "Add text to bonus.java",
            "content": encoded_content,
            "sha": content['sha']
        }
        update_response = requests.put(url, headers=headers, json=data)
        if update_response.status_code == 200:
            print(f"Text added to {repo_full_name}/bonus.java")
        else:
            print(f"Failed to update {repo_full_name}/bonus.java")
    else:
        print(f"File {file_path} not found in {repo_full_name}")

def get_repository_names():
    url = 'https://api.github.com/repos/gbochora/cs106a/contents/2023/midterm/session2/students'
    headers = {'Authorization': f'token {token}'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repositories = [item['name'] for item in response.json() if item['type'] == 'dir']
        for repo_full_name in repositories:
            update_bonus_file(repo_full_name)
    else:
        print("Failed to fetch repositories.")

# Fetch repository names within the directory
repository_names = get_repository_names()
for repo_name in repository_names:
    print(repo_name)
