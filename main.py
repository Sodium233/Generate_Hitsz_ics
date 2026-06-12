from config import CONFIG
import utils.accessSchedule as accessSchedule
import utils.generate_ics as ics_gen

def main():
    # 访问教务系统获取课表数据
    accessSchedule.accessSchedule()
    # 生成课表ICS文件
    ics_gen.generate_ics_from_json(
        CONFIG["output"]["schedule_file"],
        CONFIG["schedule"]["first_day"],
        CONFIG["output"]["ics_file"]
    )
    print(f"课表已保存到 {CONFIG["output"]["schedule_file"]} 和 {CONFIG["output"]["ics_file"]}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"错误: {e}")
