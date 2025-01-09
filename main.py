# 遍历工作流运行记录并删除前一天之前的历史记录
for repo in repos_data:
    repo_name = repo["name"]
    repo_owner = repo["owner"]["login"]

    # 获取工作流运行历史记录的 API URL
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/runs"
    
    # 获取工作流运行记录
    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code != 200:
        print(f"无法获取 {repo_name} 仓库的工作流记录，错误信息: {data.get('message', '未知错误')}")
        continue

    # 打印每个仓库的工作流记录数量，确认是否返回了工作流记录
    print(f"仓库 {repo_name} 的工作流记录数量: {len(data.get('workflow_runs', []))}")

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
                print(f"删除工作流记录失败: {run_id}, 错误: {delete_response.status_code}, 错误信息: {delete_response.json()}")
