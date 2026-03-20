import json
import logging
from client import JWClient
import config
import utils.generate_ics as ics_gen
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def main():
    import sys
    client = JWClient()

    if len(sys.argv) > 1 and sys.argv[1] in ("clear", "--clear", "--clear-cookies"):
        client.clear_cookies()
        print("已清理本地 cookies")
        return

    try:
        schedule = client.fetch_schedule()
    except Exception as e:
        logging.warning("首次拉取课表失败，尝试登录后重试: %s", e)
        client.login()
        schedule = client.fetch_schedule()

    print("获得第"+config.XN+"学年第"+config.XQ+"学期的课表数据")
    # 将数据保存到本地文件
    with open(config.SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=4)

    ##生成课表ICS文件
    ics_gen.generate_ics_from_json(config.SCHEDULE_FILE, config.FIRST_DAY, output_path=config.SCHEDULE_FILE.replace(".json", ".ics"))
    print(f"课表已保存到 {config.SCHEDULE_FILE} 和 {config.SCHEDULE_FILE.replace('.json', '.ics')}")
if __name__ == "__main__":
    main()
