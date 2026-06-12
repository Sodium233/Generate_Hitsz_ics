from playwright.sync_api import Playwright, sync_playwright
from config import CONFIG
import json

def get_state(page):
    if page.url.endswith("/authentication/main"):
        return "logged_in"
    elif page.url.endswith("/authserver/login?service=http%3A%2F%2Fjw.hitsz.edu.cn%2FcasLogin"):
        return "need_login"
    elif page.url.endswith("authserver/reAuthCheck/reAuthLoginView.do?isMultifactor=true&service=http%3A%2F%2Fjw.hitsz.edu.cn%2FcasLogin"):
        return "need_2fa"
    else:
        return "unknown"

def accessScheduleData(playwright: Playwright) -> None:
    context = playwright.chromium.launch_persistent_context(
        user_data_dir="./browser_data",
        channel="msedge",
        headless=True,
    )
    page = context.new_page()
    print("1", flush=True)
    page.goto(CONFIG["base_url"], wait_until="networkidle")
    print("URL:", page.url, flush=True)
    print("2", page.url, flush=True)
    page.locator(".towlg_tybox").click()
    print("3", page.url, flush=True)
    # 状态机，判断当前页面状态，决定下一步操作
    while True:
        state = get_state(page)
        print("当前页面状态:", state, flush=True)
        if state == "logged_in":
            print("登陆成功")
            break
        elif state == "need_login":
            # 需要输入账号密码
            print("需要登录，正在输入账号密码")
            page.locator("#username").fill(CONFIG["account"]["username"])
            page.locator("#password").fill(CONFIG["account"]["password"])
            page.locator("#rememberMe").check()
            page.locator("a#login_submit").click()
            page.wait_for_load_state()
            continue
        elif state == "need_2fa":
            # 需要2fa验证
            print("需要2FA验证，正在处理2FA验证")
            page.locator("#getDynamicCode").click()
            code = input("请输入2FA验证码: ")
            page.locator("#dynamicCode").fill(code)
            page.locator("#userNameDiv #reAuthSubmitBtn").click()

            if (page.locator("button.trust-device-sub-btn").count()>0):
                page.locator("button.trust-device-sub-btn").click()
                print("已信任当前设备")
            page.wait_for_url(
                "**/authentication/main"
            )
            continue;
                
        else:
            print("未知页面状态，无法继续操作")
            context.close()
            return None

    # ---------------------
    data = {
        "xn": CONFIG["schedule"]["xn"],
        "xq": CONFIG["schedule"]["xq"],
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

    with open(CONFIG["output"]["schedule_file"], "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=4)