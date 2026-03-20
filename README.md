# HIT 教务自动登录与课表获取

一个用于自动登录 HIT 统一身份认证并获取教务课表的 Python 脚本。

## 目录结构

- `main.py` — 程序入口
- `client.py` — 登录、cookie 管理、课表请求
- `config.py` — 账号、学年、学期、cookie 路径配置
- `encrypt/` — 密码加密 JS 逻辑与调用
- `utils/` — 登录页面解析、验证判断、验证码处理、生成 ICS
- `data/` — 存储 `cookies.json`、`schedule.json`、`schedule.ics`

## 快速使用

1. 安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

2. 填写 `config.py` 中的 `USERNAME`、`PASSWORD`、`XN`、`XQ`。
3. 运行：

```bash
python main.py
```

4. 重新运行时会复用 cookie：

```bash
python main.py
```

5. 如果需要清理 cookie：

```bash
python main.py clear
```

## 规范

- 注意 `data/cookies.json` 请勿泄露
- 注意 `config.py` 中账号密码请勿泄露

## 其他

- 登录失败时，程序会清理过期 cookie 并重新登录。
- 切换账号登陆请清理cookies
