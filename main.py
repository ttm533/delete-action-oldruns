import os
import requests
from datetime import datetime, timedelta

# 获取 GitHub Token
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
if not ACCESS_TOKEN:
    raise ValueError("环境变量 ACCESS_TOKEN 未设置！")

# 获取当前仓库的信息
repo_owner, repo_name = os.getenv("GITHUB_REPOSITORY").split("/")  # 自动获取当前仓库的拥有者和仓库名称

# 获取工作流运行历史记录的 API URL
url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/runs"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# 获取工作流运行记录
response = requests.get(url, headers=headers)
data = response.json()

if response.status_code != 200:
    raise Exception(f"GitHub API 请求失败: {data.get('message', '未知错误')}")

# 获取当前时间并计算前一天的时间
now = datetime.utcnow()
day_before = now - timedelta(days=1)

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
            print(f"成功删除工作流运行记录: {run_id}")
        else:
            print(f"删除工作流运行记录失败: {run_id}, 错误: {delete_response.status_code}")
