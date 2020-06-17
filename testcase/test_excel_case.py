import os
import re
import json
import pytest
import allure
from config import Conf
from config.Conf import ConfigYaml
from common.ExcelData import Data
from utils.LogUtil import my_log
from common.ExcelConfig import DataConfig
from common import Base
from utils.RequstsUtil import Request
from utils.AssertUtil import AssertUtil

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

# 初始化dataconfig
data_key = DataConfig


# 2、测试用例方法，参数化运行
class TestExcel:
    def run_api(self, url, method, params=None, header=None, cookie=None):
        """
        发送请求api
        :return:
        """
        # 2）.接口请求
        request = Request()
        # params 转义json
        # 验证params有没有内容
        if len(str(params).strip()) is not 0:
            params = json.loads(params)
        # method post/get
        if str(method).strip().lower() == 'get':
            res = request.get(url, json=params, headers=header, cookies=cookie)
        elif str(method).strip().lower() == 'post':
            res = request.post(url, json=params, headers=header, cookies=cookie)
        else:
            log.error("错误请求method: %s" % method)
        return res

    def run_pre(self, pre_case):
        url = ConfigYaml().get_conf_url() + pre_case[data_key.url]
        method = pre_case[data_key.method]
        params = pre_case[data_key.params]
        headers = pre_case[data_key.headers]
        cookies = pre_case[data_key.cookies]

        # 判断headers,cookies是否存在，json转义，无需
        header = Base.json_param(headers)
        cookie = Base.json_param(cookies)
        res = self.run_api(url, method, params, header)
        print("前置用例执行：%s" % res)
        return res

    # 1）.初始化信息，url,data
    @pytest.mark.parametrize('case', run_list)
    def test_run(self, case):
        # run_list第1个用例，用例，key获取values
        url = ConfigYaml().get_conf_url() + case[data_key.url]

        case_id = case[data_key.case_id]
        case_model = case[data_key.case_model]
        case_name = case[data_key.case_name]
        pre_exec = case[data_key.pre_exec]
        method = case[data_key.method]
        params_type = case[data_key.params_type]
        params = case[data_key.params]
        expect_result = case[data_key.expect_result]
        headers = case[data_key.headers]
        cookies = case[data_key.cookies]
        code = case[data_key.code]
        db_verify = case[data_key.db_verify]

        # 2.增加Headers
        # 3.增加cookies
        # 4.发送请求
        if pre_exec:
            # 前置测试用例
            pre_case = data_init.get_case_pre(pre_exec)
            print("前置条件信息为：%s" % pre_case)
            pre_res = self.run_pre(pre_case)
            headers, cookies = self.get_correlation(headers, cookies, pre_res)
        # 1.判断headers是否存在，json转义，无需
        header = Base.json_param(headers)
        cookie = Base.json_param(cookies)
        res = self.run_api(url, method, params=params, header=header, cookie=cookie)
        print("测试用例执行：%s" % res)

        # allure
        # sheet名称  feature 一级标签
        allure.dynamic.feature(sheet_name)
        # 模块   story 二级标签
        allure.dynamic.story(case_model)
        # 用例ID+接口名称  title
        allure.dynamic.title(case_id + case_name)
        # 请求URL  请求类型 期望结果 实际结果描述
        desc = "<font color='red'>请求URL111: </font> {}<Br/>" \
               "<font color='red'>请求类型222: </font>{}<Br/>" \
               "<font color='red'>期望结果: </font>{}<Br/>" \
               "<font color='red'>实际结果: </font>{}".format(url, method, expect_result, res)
        allure.dynamic.description(desc)

        # 断言验证
        # 状态码，返回结果内容，数据库相关的结果的验证
        assert_util = AssertUtil()
        assert_util.assert_code(int(res['code']), code)
        # 返回结果内容
        assert_util.assert_in_body(str(res["body"]), str(expect_result))
        Base.assert_db("db_1", res["body"], db_verify)



    def get_correlation(self, headers, cookies, pre_res):
        """
        关联
        :param headers:当前用例的请求头
        :param cookies:当前用例的cookies
        :param pre_res:前置用例执行后返回的结果
        :return:
        """
        # 验证是否有关联
        headers_para, cookies_para = Base.params_find(headers, cookies)
        # 有关联，执行前置用例，获取结果
        if len(headers_para):
            headers_data = pre_res['body'][headers_para[0]]
            # 结果替换
            headers = Base.res_sub(headers, headers_data)
        if len(cookies_para):
            cookies_data = pre_res['body'][cookies_para[0]]
            # 结果替换
            cookies = Base.res_sub(cookies, cookies_data)

        return headers, cookies


# TestExcel().test_run()
if __name__ == '__main__':
    # pytest.main(['-s', 'test_excel_case.py'])

    report_path = Conf.get_report_path() + os.sep + "result"
    report_html_path = Conf.get_report_path() + os.sep + "html"
    pytest.main(["-s", "test_excel_case.py", "--alluredir", report_path])
    Base.allure_report(report_path, report_html_path)


    # 动态关联
    # 1、验证前置条件
    # if pre_exec:
    # pass
    # 2、找到执行用例
    # 3、发送请求，获取前置用例结果
    # 发送获取前置测试用例，用例结果
    # 数据初始化，get/post，重构
    # 4、替换Headers变量
    # 5、请求发送
    # str1 = '{"Authorization": "JWT ${token}$"}'
    # pattern = re.compile('\${(.*)}\$')
    # re_res = pattern.findall(str1)
    # print(re_res[0])
    # #     #2、根据内容token，查询 前置条件测试用例返回结果token = 值
    # token = "123"
    # #     #3、根据变量结果内容，替换
    # res = re.sub(pattern, token, str1)
    # print(res)

    # 1、查询，公共方法
    # 2、替换，公共方法
    # 3、验证请求中是否${}$，返回${}$内容，公共方法
    # 4、关联方法
