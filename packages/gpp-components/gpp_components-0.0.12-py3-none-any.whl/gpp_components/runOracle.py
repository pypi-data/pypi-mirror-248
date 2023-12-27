import cx_Oracle
from .response import Response
from copy import deepcopy


class RunOracle:
    def __init__(self, tns_config):
        self.tns_config = tns_config
        self.conn = False
        self.cursor = False
        self.qs = None
        self.connectOracle()
        pass

    def connectOracle(self):
        user = self.tns_config.get("user")
        password = self.tns_config.get("password")
        host = self.tns_config.get("host")
        service_name = self.tns_config.get("service_name")

        conn_str = f"{user}/{password}@{host}/{service_name}"  # ('system/system@172.24.0.64:1521/helowinXDB')

        try:
            self.conn = cx_Oracle.connect(conn_str)
        except Exception as e:
            return Response(False, "tns is not correct, connection fail !")

    def closeConnection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def runSql(self, sqlStr):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sqlStr)
            col = [x[0] for x in cursor.description]
            self.qs = deepcopy(cursor.fetchall())
        except cx_Oracle.DatabaseError as e:
            return Response(False, f"Problem in runSql: {e}")
        finally:
            self.closeConnection()
            if self.qs:
                data = []
                for i in self.qs:
                    data.append(dict(zip(col, i)))
                return data

    def runProc(self, sp_name, jsonStr):
        try:
            # user = self.tns_config.get("user")
            # password = self.tns_config.get("password")
            # host = self.tns_config.get("host")
            # service_name = self.tns_config.get("service_name")

            # conn_str = f"{user}/{password}@{host}/{service_name}"  # ('system/system@172.24.0.64:1521/helowinXDB')
            # conn = cx_Oracle.connect(conn_str)
            self.cursor = self.conn.cursor()
            v_output = self.cursor.var(cx_Oracle.CLOB)
            self.cursor.callproc(sp_name, [str(jsonStr), v_output])
            result = deepcopy(v_output.getvalue())
            return result
        except cx_Oracle.DatabaseError as e:
            return Response(False, f"Problem in runProc: {e}")
        finally:
            self.closeConnection()
            # cursor.close()
            # conn.close()

    def getTNS(self, dbJson):
        host_name = dbJson.get("host_name")
        port = dbJson.get("port")
        container = dbJson.get("container")
        tb_space = dbJson.get("tb_space")

        sqlStr = f"SELECT user_name, user_pwd FROM DB_CONFIG WHERE host_name = '{host_name}' AND port = {port} AND container = '{container}' AND tb_space = '{tb_space}'"

        rsp = self.runSql(sqlStr)
        user_name = rsp[0].get("USER_NAME")
        user_pwd = rsp[0].get("USER_PWD")

        result = {
            "user": user_name,
            "password": user_pwd,
            "host": host_name + ":" + str(port),
            "service_name": container,
        }
        return result
