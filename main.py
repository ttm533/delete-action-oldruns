import os
import requests
from datetime import datetime, timedelta

# 获取 GitHub Token
access_token = os.getenv('MY_ACCESS_TOKEN')
if not access_token:
    raise ValueError("环境变量 MY_ACCESS_TOKEN 未设置！")

# 计算24小时前的时间戳
time_limit = datetime.utcnow() - timedelta(hours=24)
time_limit_timestamp = int(time_limit.timestamp())

# 获取所有仓库的工作流运行记录
url = "https://api.github.com/repos/{repo_owner}/{repo_name}/actions/runs"
headers = {"Authorization": f"Bearer {access_token}"}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    raise Exception(f"获取仓库信息失败: {response.json().get('message', '未知错误')}")

data = response.json()

# 遍历工作流运行记录并删除24小时以前的记录
for run in data['workflow_runs']:
    run_timestamp = run['created_at']
    run_time = datetime.strptime(run_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    
    if run_time < time_limit:
        delete_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/runs/{run['id']}"
        delete_response = requests.delete(delete_url, headers=headers)
        
        if delete_response.status_code == 204:
            print(f"成功删除仓库 {repo_name} 的工作流记录: {run['id']}")
        else:
            print(f"删除仓库 {repo_name} 的工作流记录失败: {run['id']}")
