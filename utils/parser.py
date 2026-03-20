from bs4 import BeautifulSoup
import re


def parse_login_page(html: str):
    soup = BeautifulSoup(html, "html.parser")

    lt_tag = soup.find("input", {"name": "lt"})
    execution_tag = soup.find("input", {"name": "execution"})
    salt_tag = soup.find("input", {"name": "pwdEncryptSalt"}) or soup.find("input", {"id": "pwdEncryptSalt"}) or soup.find("input", {"name": "encryptSalt"})

    lt = lt_tag.get("value", "") if lt_tag else ""
    execution = execution_tag.get("value", "") if execution_tag else ""
    salt = salt_tag.get("value", "") if salt_tag else ""

    # 兼容在脚本中的 salt
    if not salt:
        match = re.search(r'pwdEncryptSalt\s*[:=]\s*["\']([A-Za-z0-9]+)["\']', html)
        if match:
            salt = match.group(1)

    if not execution:
        match = re.search(r'execution\s*[:=]\s*["\']([A-Za-z0-9\-_.]+)["\']', html)
        if match:
            execution = match.group(1)

    # lt 有时可能为空字符串，登录仍然有效
    if salt == "":
        raise ValueError("登录页面缺少 pwdEncryptSalt")

    return lt, execution, salt
