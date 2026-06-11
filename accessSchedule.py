from playwright.sync_api import Playwright, sync_playwright
import os
import config
import json

def accessScheduleData(playwright: Playwright) -> None:
    context = playwright.chromium.launch_persistent_context(
        user_data_dir="./browser_data",
        channel="chrome",
        headless=True,
    )
    page = context.new_page()
    print("1", flush=True)
    page.goto(config.BASE_URL, wait_until="networkidle")
    print("URL:", page.url, flush=True)
    print("2", page.url, flush=True)
    page.locator(".towlg_tybox").click()
    print("3", page.url, flush=True)
    # 判断是否已经跳转到了教务系统的主页
    if page.url.endswith("/authentication/main"):
        print("已登录，无需输入账号密码")
    else:
        # 需要输入账号密码
        page.get_by_role("textbox", name="Please enter student ID/work").fill(config.USERNAME)
        page.get_by_role("textbox", name="Please enter Password").fill(config.PASSWORD)
        page.locator("#rememberMe").check()
        page.get_by_role("link", name="Login", exact=True).click()

        if page.url.endswith("/authentication/main"):
            print("登录成功")
        else:
            # 需要2fa验证
            page.get_by_role("button", name="Obtain").click()
            page.get_by_role("textbox", name="enter").click()
            code = input("请输入2FA验证码: ")
            page.get_by_role("textbox", name="enter").fill(code)
            page.get_by_role("button", name="Sign in").click()
            page.locator("button").filter(has_text="Trust this device").click()
            page.get_by_text("知道了").click()

    # ---------------------
    data = {
        "xn": config.XN,
        "xq": config.XQ,
    }
    schedule = page.evaluate(
        """
        async (data) => {
            const response = await fetch(
                "/xszykb/queryxszykbzong",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": 
                        "application/x-www-form-urlencoded"
                    },
                    body: new URLSearchParams(data)
                }
            );
            return await response.json();
        }
        """,
     data)
    context.close()
    return schedule

def accessSchedule():
    with sync_playwright() as playwright:
        schedule = accessScheduleData(playwright)

    with open(config.SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=4)