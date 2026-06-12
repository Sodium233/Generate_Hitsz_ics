# PlaywrightDemo

这是一个基于 Python + Playwright 的课程表抓取与 ICS 导出工具。

## 功能简介

- 登录教务系统并抓取课表数据
- 将课程表保存为 JSON
- 生成可导入的 ICS 日历文件

## 项目结构

- `main.py`：程序入口
- `accessSchedule.py`：抓取课程表数据
- `utils/generate_ics.py`：将 JSON 转为 ICS
- `config.example.py`：配置模板
- `data/`：保存抓取结果与生成的日历文件
- `browser_data/`：Chromium 持久化浏览器数据

## 快速开始

1. 安装依赖

   ```bash
   python -m pip install -U pip
   python -m pip install -r requirements.txt
   python -m playwright install
   ```

2. 配置账号信息

   复制 `config.example.json` 为 `config.json`，并填写你的用户名、密码和学年学期信息：
   可以删除掉作为示例的 `schedule.examplae.json` ， `schedule.example.ics` ， 和 `config.example.json`

3. 运行程序

   ```bash
   python main.py
   ```

4. 输出结果

   - `data/schedule.json`
   - `data/schedule.ics`

## 注意事项

- 请不要把真实的 `config.json` 提交到版本控制。
- 如果登录过程需要二次验证（2FA），程序会在终端中提示输入验证码。
- 生成的课程表文件可能包含个人隐私信息，请谨慎处理。
