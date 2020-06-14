from config.Conf import ConfigYaml
from utils.MysqlUtil import Mysql


# 1、定义init_db
def init_db(db_alias):
    # 2、初始数据化信息，通过配置
    db_info = ConfigYaml().get_db_conf_info(db_alias)
    host = db_info["db_host"]
    user = db_info["db_user"]
    password = db_info["db_password"]
    db_name = db_info["db_name"]
    charset = db_info["db_charset"]
    port = int(db_info["db_port"])
    # 3、初始化mysql对象
    conn = Mysql(host, user, password, db_name, charset, port)
    return conn
