# 使用说明

## 1. Fork 本项目

1. 访问本项目的 GitHub 页面。
2. 点击页面右上角的 **Fork** 按钮，将本项目复制到你的 GitHub 账户中。

## 2. 添加环境变量

为了能够正常使用本项目的功能，需要设置以下环境变量：

### 环境变量列表

- **MY_ACCESS_TOKEN**: 你的 GitHub 个人访问令牌（Personal Access Token）。该令牌需具有访问所有仓库和删除工作流记录的权限。可以在 GitHub 的设置页面中生成并复制该令牌。
- **MY_GITHUB_USER**: 你的 GitHub 用户名。此用户名用于定位你拥有的仓库。

### 设置环境变量

1. 打开你的仓库页面。
2. 点击页面右上角的 **Settings**。
3. 在左侧导航栏中选择 **Secrets and variables** → **Actions**。
4. 点击 **New repository secret** 按钮，添加以下两个环境变量：
   - **MY_ACCESS_TOKEN**: 输入你生成的 GitHub 个人访问令牌。
   - **MY_GITHUB_USER**: 输入你的 GitHub 用户名。

### 环境变量的权限

- **MY_ACCESS_TOKEN**: 必须具有以下权限：
  - [image](https://github.com/user-attachments/assets/7e540e75-5da4-47e9-b3bd-1dbe857a1d86)
  - ![image](https://github.com/user-attachments/assets/45c5e04b-19c6-4879-92cb-d862f4a6fe54)

- **MY_GITHUB_USER**: 需要提供你的 GitHub 用户名，用于标识你所有的仓库。

## 3. 开启 Action 的定时任务运行

1. 在仓库页面上选择 **Actions** 标签页
2. 运行“定时清理所有仓库24小时以前工作流历史记录”的工作流。
