import os
import pytest
from config import Conf
from config.Conf import ConfigYaml
from common.ExcelData import Data
from utils.LogUtil import my_log
from common.ExcelConfig import DataConfig
# 1、初始化信息
# 1）.初始化测试用例文件
case_file = os.path.join(Conf.get_data_path(), ConfigYaml().get_excel_file())
# 2）.测试用例sheet名称
sheet_name = ConfigYaml().get_excel_sheet()
# 3）.获取运行测试用例列表
data_init = Data(case_file, sheet_name)
run_list = data_init.get_run_data()
# 4）.日志
log = my_log()


# 2、测试用例方法，参数化运行
class TestExcel:
    # 1）.初始化信息，url,data
    def test_run(self):
        data_key = DataConfig
        # run_list第1个用例，用例，key获取values
        url = ConfigYaml().get_conf_url() + run_list[0][data_key.url]
        print(url)

TestExcel().test_run()
    # 2）.接口请求