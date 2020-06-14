import json
import pytest
from utils.LogUtil import my_log


class AssertUtil:
    def __init__(self):
        self.log = my_log('AssertUtil')

    # 3、code相等:验证返回状态码
    def assert_code(self, code, expected_code):
        try:
            assert code == expected_code
            return True
        except:
            self.log.error('code error,code is %s,excepted_code is %s' % (code, expected_code))
            raise

    # 4、body相等:验证返回结果内容相等
    def assert_body(self, body, expected_body):
        try:
            assert body == expected_body
            return True
        except:
            self.log.error('body error,body is %s,expected_body is %s' % (body, expected_body))
            raise

    # 5、body包含:验证返回结果是否包含期望的结果
    def assert_in_body(self, body, expected_body):
        try:
            body = json.dumps(body)
            print(body)
            assert expected_body in body
            return True
        except:
            self.log.error("不包含或者body是错误，body is %s,expected_body is %s" % (body, expected_body))
            raise
