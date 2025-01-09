import os
import requests

def fetch_data():
    token = os.getenv('MY_ACCESS_TOKEN')
    if not token:
        raise ValueError("环境变量 MY_ACCESS_TOKEN 未设置！")
    
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://api.github.com/user"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print("用户信息:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"获取用户信息失败: {e}")

def main():
    print("运行 Python 脚本...")
    fetch_data()

if __name__ == "__main__":
    main()
