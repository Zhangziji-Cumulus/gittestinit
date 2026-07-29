"""Git 错误诊断模块：解析 git stderr，给出中文说明和解决办法。"""

from dataclasses import dataclass


@dataclass
class ErrorAdvice:
    title: str        # 错误标题
    cause: str        # 原因说明
    solution: str     # 解决办法


# 按优先级排列的错误匹配规则
_RULES: list[tuple[str, ErrorAdvice]] = [
    (
        "fetch first",
        ErrorAdvice(
            title="远程有更新，需要先拉取",
            cause="远程仓库有你本地没有的提交，直接推送会被拒绝。",
            solution="先点击「⬇ 拉取」按钮拉取远程更新，如有冲突解决后再推送。",
        ),
    ),
    (
        "non-fast-forward",
        ErrorAdvice(
            title="非快进推送被拒绝",
            cause="本地和远程的历史不一致，无法直接推送。",
            solution="先点击「⬇ 拉取」合并远程更改，确认无误后再推送；确有必要时可用「强制推送」。",
        ),
    ),
    (
        "rejected",
        ErrorAdvice(
            title="推送被拒绝",
            cause="远程仓库拒绝了此次推送操作。",
            solution="先拉取远程更新，解决可能的冲突后重试；或检查分支保护规则。",
        ),
    ),
    (
        "Authentication failed",
        ErrorAdvice(
            title="认证失败",
            cause="用户名或密码/令牌不正确，或凭证已过期。",
            solution="检查远程仓库的访问凭证；如使用 HTTPS，需提供有效的个人访问令牌(PAT)；如使用 SSH，确认密钥已配置。",
        ),
    ),
    (
        "could not read Username",
        ErrorAdvice(
            title="需要登录凭证",
            cause="远程仓库需要身份验证，但未提供用户名。",
            solution="请配置 Git 凭证：运行 `git config --global credential.helper manager`，或改用 SSH 方式连接。",
        ),
    ),
    (
        "Permission denied (publickey)",
        ErrorAdvice(
            title="SSH 密钥权限不足",
            cause="SSH 公钥未添加到远程仓库账户，或密钥文件权限不正确。",
            solution="将本地 SSH 公钥 (~/.ssh/id_rsa.pub) 添加到 GitHub/GitLab 账户的 SSH Keys 设置中。",
        ),
    ),
    (
        "does not appear to be a git repository",
        ErrorAdvice(
            title="远程仓库地址无效",
            cause="远程仓库 URL 不正确，或远程服务器上不存在该仓库。",
            solution="检查远程地址是否正确：运行 `git remote -v` 查看；用「远程」标签页的「设置」按钮修正 URL。",
        ),
    ),
    (
        "refusing to merge unrelated histories",
        ErrorAdvice(
            title="拒绝合并不相关的历史",
            cause="两个仓库没有共同的提交历史，Git 默认拒绝合并。",
            solution="如确认要合并，在命令行执行 `git pull origin <分支> --allow-unrelated-histories`。",
        ),
    ),
    (
        "CONFLICT",
        ErrorAdvice(
            title="存在合并冲突",
            cause="拉取或合并时，本地和远程修改了同一文件的同一区域。",
            solution="在工作区找到冲突文件（标记了 <<<<<<< 的位置），手动选择保留的内容后暂存并提交。",
        ),
    ),
    (
        "Your local changes would be overwritten",
        ErrorAdvice(
            title="本地修改未提交，无法切换",
            cause="工作区有未提交的修改，切换分支或拉取会覆盖这些修改。",
            solution="先在工作区提交或暂存(stash)本地修改，再执行操作。",
        ),
    ),
    (
        "not a git repository",
        ErrorAdvice(
            title="不是 Git 仓库",
            cause="当前目录未初始化 Git 仓库，或 .git 目录缺失。",
            solution="使用「🆕 初始化」按钮初始化新仓库，或确认打开的目录正确。",
        ),
    ),
    (
        "failed to push some refs",
        ErrorAdvice(
            title="部分引用推送失败",
            cause="推送过程中部分分支或标签未能成功推送。",
            solution="查看上方详细日志定位具体原因，通常需要先拉取远程更新。",
        ),
    ),
    (
        "no remote",
        ErrorAdvice(
            title="未设置远程仓库",
            cause="当前仓库没有配置远程地址。",
            solution="在「远程」标签页点击「设置」按钮，输入远程仓库 URL。",
        ),
    ),
    (
        "pathspec",
        ErrorAdvice(
            title="文件路径未找到",
            cause="指定的文件路径在仓库中不存在或已删除。",
            solution="刷新工作区列表，确认文件路径正确后再操作。",
        ),
    ),
]


def analyze(stderr: str) -> ErrorAdvice | None:
    """分析 git 错误输出，返回中文诊断建议。无匹配时返回 None。"""
    if not stderr:
        return None
    for keyword, advice in _RULES:
        if keyword in stderr:
            return advice
    return None
