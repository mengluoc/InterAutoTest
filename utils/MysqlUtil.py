import pymysql
from utils.LogUtil import my_log


class Mysql:
    # 2、初始化数据，连接数据库，光标对象
    def __init__(self, host, user, password, database, charset='utf8', port=3306):
        self.log = my_log('MysqlUtil')
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset=charset,
            port=port
        )
        # 获取执行SQL语句的光标对象,       结果作为字典返回
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 创建查询、执行方法
    def fetchone(self, sql):
        # 单个查询
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def fetchall(self, sql):
        # 多个查询
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def exec(self, sql):
        # 执行
        try:
            if self.conn and self.cursor:
                self.cursor.execute(sql)
                self.conn.commit()      # 提交
        except Exception as ex:
            self.conn.rollback()        # 回滚
            self.log.error("Mysql 执行失败")
            self.log.error(ex)
            return False
        return True

    def __del__(self):
        # 关闭光标对象
        if self.cursor is not None:
            self.cursor.close()
        # 关闭连接对象
        if self.conn is not None:
            self.cursor.close()


if __name__ == '__main__':
    mysql = Mysql("211.103.136.242",
                  "test",
                  "test123456",
                  "meiduo",
                  charset="utf8",
                  port=7090)
    res = mysql.fetchall("select username,password from tb_users")
    # res = mysql.exec("update tb_users set first_name='python2' where username = 'python'")
    print(res)

"""
    conn = pymysql.connect(
        host="211.103.136.242",
        user='test',
        password='test123456',
        database="meiduo",
        charset="utf8",
        port=7090
    )
"""