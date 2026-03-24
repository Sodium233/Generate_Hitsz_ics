import json
import logging
import os
import requests
from encrypt.encrypt import encrypt_password
from utils.parser import parse_login_page
from utils.captcha_verification import choose_message_verification, choose_hit_verification
import config

LOGGER = logging.getLogger(__name__)

class JWClient:
    LOGIN_PAGE_URL = "https://ids.hit.edu.cn/authserver/login?service=http%3A%2F%2Fjw.hitsz.edu.cn%2FcasLogin"
    SCHEDULE_URL = "https://jw.hitsz.edu.cn/xszykb/queryxszykbzong"

    def __init__(self):
        self.session = requests.Session()
        self.base_url = config.BASE_URL
        self.session.headers.update({
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Origin': 'https://ids.hit.edu.cn',
            'Referer': 'https://ids.hit.edu.cn/authserver/reAuthCheck/reAuthLoginView.do?isMultifactor=true&service=http%3A%2F%2Fjw.hitsz.edu.cn%2FcasLogin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        })
        self._load_cookies()

    def _cookie_file_path(self):
        return getattr(config, 'COOKIE_FILE', 'cookies.json')

    def _load_cookies(self):
        cookie_file = self._cookie_file_path()
        if not os.path.exists(cookie_file):
            return
        try:
            with open(cookie_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
            LOGGER.info("已加载本地 cookie: %s", cookie_file)
        except Exception as exc:
            LOGGER.warning("读取 cookie 文件失败，忽略并继续登录: %s", exc)

    def _save_cookies(self):
        cookie_file = self._cookie_file_path()
        try:
            parent = os.path.dirname(cookie_file)
            if parent:
                os.makedirs(parent, exist_ok=True)
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            with open(cookie_file, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            LOGGER.info("已保存 cookie 到 %s", cookie_file)
        except Exception as exc:
            LOGGER.warning("保存 cookie 失败: %s", exc)

    def _delete_cookies(self):
        cookie_file = self._cookie_file_path()
        if os.path.exists(cookie_file):
            try:
                os.remove(cookie_file)
                LOGGER.info("已删除本地 cookie: %s", cookie_file)
            except Exception as exc:
                LOGGER.warning("删除 cookie 失败: %s", exc)

    def clear_cookies(self):
        self.session.cookies.clear()
        self._delete_cookies()


    def _fetch_login_page(self):
        resp = self.session.get(self.LOGIN_PAGE_URL, timeout=15)
        resp.raise_for_status()
        return resp.text

    def _submit_login(self, lt, execution, encrypted_pwd):
        form_data = {
            "username": config.USERNAME,
            "password": encrypted_pwd,
            "lt": lt,
            "execution": execution,
            "_eventId": "submit",
            "cllt": "userNameLogin",
            "dllt": "generalLogin",
        }
        resp = self.session.post(self.LOGIN_PAGE_URL, data=form_data, timeout=15)
        try:
            resp.raise_for_status()
        except Exception as e:
            LOGGER.error("登录请求失败: %s, 响应内容: %s", resp.status_code, resp.text[:200])
            raise
        return resp

    def login(self):
        try:
            html = self._fetch_login_page()
        except requests.HTTPError as exc:
            if exc.response is not None and exc.response.status_code in (401, 403):
                LOGGER.warning("登录页返回 %s，清理 cookie 后重试", exc.response.status_code)
                self.clear_cookies()
                html = self._fetch_login_page()
            else:
                LOGGER.error("登录页面获取失败")
                raise RuntimeError("登录页面获取失败，请检查网络") from exc
        except Exception as exc:
            LOGGER.error("登录页面获取失败")
            raise RuntimeError("登录页面获取失败，请检查网络") from exc

        try:
            lt, execution, salt = parse_login_page(html)
        except Exception as exc:
            LOGGER.error("登录页面解析失败")
            raise RuntimeError("登录页面解析失败，请检查页面结构") from exc

        try:
            encrypted_pwd = encrypt_password(config.PASSWORD, salt)
        except Exception as exc:
            LOGGER.error("密码加密失败")
            raise RuntimeError("密码加密失败，请确认 encrypt.js 可用") from exc

        try:
            resp = self._submit_login(lt, execution, encrypted_pwd)
        except requests.RequestException as exc:
            raise

        if "为了您的信息安全，需要进行身份认证" in resp.text:
            print("输入1使用HIT APP验证码认证，输入2使用手机短信验证码认证")
            choice = input("请输入选择：").strip()
            if choice == "1":
                ok = choose_hit_verification(self.session)
            else:
                ok = choose_message_verification(self.session)
            if not ok:
                raise RuntimeError("多因素认证失败，请重试")

        # 登录成功后访问 jw/casLogin，完成服务票据交换
        try:
            self.session.get("https://jw.hitsz.edu.cn/casLogin", timeout=15)
        except Exception:
            LOGGER.warning("登录后访问 jw/casLogin 失败，继续使用当前 session")

        self._save_cookies()
        print("登录成功")

    def fetch_schedule(self):
        data = {
            "xn": config.XN,
            "xq": config.XQ,
        }

        resp = self.session.post(self.SCHEDULE_URL, data=data, timeout=15)

        # 1️⃣ 先检查 HTTP 状态
        try:
            resp.raise_for_status()
        except Exception as e:
            LOGGER.error("课表请求失败: %s, 响应内容: %s", resp.status_code, resp.text[:200])
            raise

        # 2️⃣ 检查 Content-Type（防止拿到 HTML）
        content_type = resp.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            LOGGER.error("返回不是 JSON, Content-Type=%s, 内容=%s", content_type, resp.text[:200])
            raise RuntimeError("课表接口返回非 JSON（可能未登录或被重定向）")

        # 3️⃣ 再解析 JSON
        try:
            schedule = resp.json()
        except ValueError as exc:
            LOGGER.error("JSON 解析失败, 原始内容: %s", resp.text[:200])
            raise RuntimeError("课表响应 JSON 格式错误") from exc

        self._save_cookies()
        return schedule