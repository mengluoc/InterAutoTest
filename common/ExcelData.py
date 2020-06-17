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

    def get_case_list(self):
        """
        获取全部测试用例
        :return:
        """
        run_list = [line for line in self.reader.data()]
        # print(run_list)
        return run_list

    def get_case_pre(self, pre):
        """
        根据前置条件：从全部测试用例取到对应前置的测试用例
        :param pre:
        :return:
        """
        run_list = self.get_case_list()
        for line in run_list:
            if pre in dict(line).values():
                return line
        return None


if __name__ == '__main__':
    # Data("../data/testdata.xlsx", "美多商城接口测试").get_run_data()
    Data("../data/testdata.xlsx", "美多商城接口测试").get_case_list()






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