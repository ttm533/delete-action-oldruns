import os
import requests
import datetime

# 从环境变量获取 GitHub Token
access_token = os.getenv("ACCESS_TOKEN")
if not access_token:
    raise ValueError("环境变量 ACCESS_TOKEN 未设置！")

# GitHub API URL
api_url = "https://api.github.com"

# 获取当前时间（UTC时间）
current_time = datetime.datetime.utcnow()

# 设置请求头
headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/vnd.github.v3+json",
}

# 获取所有仓库的列表
repos_url = f"{api_url}/user/repos"  # 获取当前用户所有仓库
repos_response = requests.get(repos_url, headers=headers)
repos_data = repos_response.json()

if repos_response.status_code != 200:
    raise Exception(f"获取仓库信息失败: {repos_data.get('message', '未知错误')}")

# 遍历所有仓库，获取工作流运行记录
for repo in repos_data:
    repo_name = repo["name"]
    print(f"开始处理仓库: {repo_name}")
    
    # 获取该仓库的工作流运行记录
    runs_url = f"{api_url}/repos/{repo['owner']['login']}/{repo_name}/actions/runs"
    runs_response = requests.get(runs_url, headers=headers)
    runs_data = runs_response.json()

    if runs_response.status_code != 200:
        print(f"获取仓库 {repo_name} 的工作流记录失败: {runs_data.get('message', '未知错误')}")
        continue

    # 获取并删除 24 小时前的工作流记录
    for run in runs_data["workflow_runs"]:
        run_id = run["id"]
        created_at = run["created_at"]
        run_time = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
        time_diff = current_time - run_time
        # 如果工作流记录超过 24 小时则删除
        if time_diff > datetime.timedelta(hours=24):
            # 删除工作流记录
            delete_url = f"{api_url}/repos/{repo['owner']['login']}/{repo_name}/actions/runs/{run_id}"
            delete_response = requests.delete(delete_url, headers=headers)
            
            if delete_response.status_code == 204:
                print(f"成功删除仓库 {repo_name} 的工作流记录: {run_id}")
            else:
                print(f"删除仓库 {repo_name} 的工作流记录失败: {delete_response.status_code}")
