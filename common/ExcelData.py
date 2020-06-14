from utils.ExcelUtil import ExcelReader
from common.ExcelConfig import DataConfig


class Data:
    def __init__(self, testcase_file, sheet_name):
        # 1、使用excel工具类，获取结果list
        self.reader = ExcelReader(testcase_file, sheet_name)

    def get_run_data(self):
        """
        根据是否运行列==y，获取执行测试用例
        :return:
        """
        run_list = list()
        for line in self.reader.data():
            if str(line[DataConfig().is_run]).lower() == 'y':
                run_list.append(line)
        # print(run_list)
        return run_list


if __name__ == '__main__':
    Data("../data/testdata.xlsx", "美多商城接口测试").get_run_data()

"""
# 1、使用excel工具类，获取结果list
reader = ExcelReader("../data/testdata.xlsx", "美多商城接口测试")
# print(reader.data())
# 2、列是否运行内容，y
read_list = reader.data()
run_list = list()
for line in read_list:
    if line['是否运行'] == 'y':
        run_list.append(line)
print(run_list)
# 3、保存要执行结果，放到新的列表。
"""