import config
import accessSchedule
import utils.generate_ics as ics_gen

def main():
    # 访问教务系统获取课表数据
    accessSchedule.accessSchedule()
    # 生成课表ICS文件
    ics_gen.generate_ics_from_json(config.SCHEDULE_FILE, config.FIRST_DAY, output_path=config.SCHEDULE_FILE.replace(".json", ".ics"))
    print(f"课表已保存到 {config.SCHEDULE_FILE} 和 {config.SCHEDULE_FILE.replace('.json', '.ics')}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"错误: {e}")
