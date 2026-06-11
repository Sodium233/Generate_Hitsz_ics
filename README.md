# HIT 教务自动登录与课表获取

一个用于自动登录 HIT 统一身份认证并获取教务课表的 Python 脚本。

## 目录结构

- `main.py` — 程序入口
- `client.py` — 登录、cookie 管理、课表请求
- `config.example.py` — 配置模板
- `config.py` — 本地实际配置文件（已加入 `.gitignore`）
- `encrypt/` — 密码加密 JS 逻辑与调用
- `utils/` — 登录页面解析、验证判断、验证码处理、生成 ICS
- `data/` — 存储 `cookies.json`、`schedule.json`、`schedule.ics`

## 快速使用

1. 安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

2. 复制配置模板并填写你的信息：

```bash
cp config.example.py config.py
```

3. 在 `config.py` 中填写 `USERNAME`、`PASSWORD`、`XN`、`XQ`。
4. 运行：

```bash
python main.py
```

5. 重新运行时会复用 cookie：

```bash
python main.py
```

6. 如果需要清理 cookie：

```bash
python main.py clear
```

## 规范

- 注意 `data/cookies.json` 请勿泄露
- 注意 `config.py` 已加入 `.gitignore`，不要提交本地账号密码

## 其他

- 登录失败时，程序会清理过期 cookie 并重新登录。
- 切换账号登录请清理 cookies
