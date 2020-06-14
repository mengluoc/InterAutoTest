import requests
from utils.LogUtil import my_log


class Request:
    def __init__(self):
        self.log = my_log("Requests")

    def requests_api(self, url, data=None, json=None, headers=None, cookies=None, method="get"):
        if method == "get":
            self.log.debug("发送get请求")
            r = requests.get(url, data=data, json=json, headers=headers, cookies=cookies)
        elif method == "post":
            self.log.debug("发送post请求")
            r = requests.post(url, data=data, json=json, headers=headers, cookies=cookies)
        # 获取结果内容
        code = r.status_code
        try:
            body = r.json()
        except Exception as e:
            body = r.text
        # 内容存到字典
        res = dict()
        res["code"] = code
        res["body"] = body
        return res

    # get/post方法
    def get(self, url, **kwargs):
        return self.requests_api(url, method="get", **kwargs)

    def post(self, url, **kwargs):
        return self.requests_api(url, method="post", **kwargs)


if __name__ == '__main__':
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTIwMzI1NjIsInVzZXJuYW1lIjoicHl0aG9uIiwiZW1' \
            'haWwiOiI5NTI2NzM2MzhAcXEuY29tIiwidXNlcl9pZCI6MX0.k97PPQI0RUcHqTk9gqBlxVRL0FPGNEoz4VOitySj1M4'
    headers = {'Authorization': 'JWT ' + token}
    url = "http://211.103.136.242:8064/user"
    request = Request()
    r = request.get(url, headers=headers)
    print(r)

    # method = 'post'
    # url = "http://211.103.136.242:8064/authorizations/"
    # data = {"username": "python", "password": "12345678"}
    # request = Request()
    # r = request.post(url, json=data)
    # print(r)
