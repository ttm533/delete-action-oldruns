import os
import requests
from datetime import datetime, timedelta

# 获取 GitHub Token
ACCESS_TOKEN = os.getenv("MY_ACCESS_TOKEN")
if not ACCESS_TOKEN:
    raise ValueError("环境变量 MY_ACCESS_TOKEN 未设置！")

# 获取 GitHub 用户名（用于个人仓库）
GITHUB_USER = os.getenv("MY_GITHUB_USER")  # 设置为 GitHub 用户名
if not GITHUB_USER:
    raise ValueError("环境变量 MY_GITHUB_USER 未设置！")

# 获取所有仓库的 API URL（包括 fork 仓库）
repos_url = f"https://api.github.com/users/{GITHUB_USER}/repos?type=all&affiliation=owner,collaborator,organization_member"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# 获取用户的所有仓库
response = requests.get(repos_url, headers=headers)
repos_data = response.json()

if response.status_code != 200:
    raise Exception(f"获取仓库信息失败: {repos_data.get('message', '未知错误')}")

# 获取当前时间并计算前一天的时间
now = datetime.utcnow()
day_before = now - timedelta(days=1)

# 遍历仓库，删除每个仓库中过期的工作流历史记录
for repo in repos_data:
    repo_name = repo["name"]
    repo_owner = repo["owner"]["login"]

    # 获取工作流运行历史记录的 API URL
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/runs"
    
    # 获取工作流运行记录
    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code != 200:
        print(f"无法获取 {repo_name} 仓库的工作流记录")
        continue

    # 遍历工作流运行记录并删除前一天之前的历史记录
    for run in data.get("workflow_runs", []):
        run_date = datetime.strptime(run["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        
        # 如果工作流运行记录的时间早于前一天，则删除
        if run_date < day_before:
            run_id = run["id"]
            delete_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/runs/{run_id}"
            
            # 删除工作流运行记录
            delete_response = requests.delete(delete_url, headers=headers)
            
            if delete_response.status_code == 204:
                print(f"成功删除仓库 {repo_name} 的工作流记录: {run_id}")
            else:
                print(f"删除工作流记录失败: {run_id}, 错误: {delete_response.status_code}")
