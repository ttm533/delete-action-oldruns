import os
import requests
from datetime import datetime, timedelta

# 从环境变量中获取必要信息
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

if not all([REPO_OWNER, REPO_NAME, ACCESS_TOKEN]):
    raise ValueError("环境变量 REPO_OWNER、REPO_NAME 或 ACCESS_TOKEN 未正确设置！")

# GitHub API 基础 URL
BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs"

# 获取一天前的时间
ONE_DAY_AGO = datetime.now() - timedelta(days=1)

def delete_workflow_runs():
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    # 获取所有工作流运行的记录
    response = requests.get(BASE_URL, headers=headers)
    if response.status_code != 200:
        raise Exception(f"获取工作流运行记录失败: {response.status_code}, {response.text}")

    runs = response.json().get("workflow_runs", [])
    print(f"找到 {len(runs)} 条工作流运行记录。")

    for run in runs:
        run_id = run["id"]
        run_created_at = datetime.strptime(run["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        if run_created_at < ONE_DAY_AGO:
            # 删除一天前的工作流运行记录
            delete_url = f"{BASE_URL}/{run_id}"
            delete_response = requests.delete(delete_url, headers=headers)
            if delete_response.status_code == 204:
                print(f"成功删除运行记录: {run_id}")
            else:
                print(f"删除运行记录失败: {run_id}, {delete_response.status_code}, {delete_response.text}")

if __name__ == "__main__":
    delete_workflow_runs()
