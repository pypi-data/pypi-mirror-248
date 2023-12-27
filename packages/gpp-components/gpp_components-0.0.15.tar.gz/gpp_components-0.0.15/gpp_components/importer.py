from .response import Response
import pandas as pd
import cx_Oracle as cx
import sqlalchemy as sqla


class Importer:
    def __init__(self, jsonStr) -> None:
        self.jsonStr = jsonStr

    """
    {
      "file_name": "Dragon_Deviation",
      "file_path": "\\\\xmncc4engdb07.dhcp.apac.dell.com\\APCC",
      "file_type": "Excel", 
      "file_extend":"xlsx",
      "row_split": "",
      "data_value": [],
      "host_name": "XMNCC4ENGDB010.dhcp.apac.dell.com:1521",
      "service_name":"mostpdb.apac.dell.com",
      "user_name": "MOST",
      "password": "MOST_2020",
      "db_type": "Oracle",
      "table_name": "test_import",
      "sheet_name": "Sheet1",
      "model": "append",
      "header": 0,
      "skiprows": 0,
      "mapping_data": [{"source": "Original Part", "column_name": "ORDERNUM"},{"source": "Deviation Part", "column_name": "QTY"}],
      "before_script": "",
      "after_script": ""
    }
    """

    def importData(self):
        obj = self.jsonStr
        table_data = Importer.loadFile(obj)
        # DB 操作
        res = Importer.executeDB(obj, table_data)
        print(res)
        if res:
            return Response(success=False, msg=str(res), data=[])
        else:
            return Response(success=True, data=[])

    def executeDB(obj, table_data):
        """
        obj:{
            "db_type": "SQL",
            "host_name": "xmncc4engdb04.dhcp.apac.dell.com:1433/PCWebsite",
            "user_name": "sa",
            "password": "k9efQV0uNJ)Zz3CZ",
            "before_script": "ddd",
            "after_script": "",
        }
        table_data:[{"ORDERNUM":"11111","QTY":"333"}]
        """
        db_type = obj["db_type"]
        table_name = obj["table_name"]
        model = obj["model"]
        before_script = obj["before_script"]
        after_script = obj["after_script"]
        try:
            conn = Importer.connDB(obj)
            if db_type == "Oracle":
                # connect DB
                cur = conn.cursor()
                if before_script:
                    cur.execute(before_script)
                if model == "Overall":
                    cur.execute(f"delete from {table_name}")

                rows = [tuple(x) for x in pd.DataFrame(table_data).values]
                columns = [x for x in pd.DataFrame(table_data).keys()]
                # 动态造insert 语句
                sql_str = Importer.rebuildSQL(table_name, columns)
                # rows:[(value1,value2)]
                cur.executemany(sql_str, rows)
                if after_script:
                    conn.execute(after_script)
                cur.close()
            elif db_type == "SQL":
                if before_script:
                    cur.execute(sqla.text(before_script))
                if model == "Overall":
                    model = "replace"
                table_data = pd.DataFrame(obj["data"])
                # table_data:DataFrame类型
                # if_exists：replace 替换原有数据/append 新增数据/fail 默认；创建一个表，目标表存在就失败
                # index:True 默认，新增一列索引
                table_data.to_sql(table_name, conn, if_exists=model, index=False)
                if after_script:
                    conn.execute(sqla.text(after_script))
            conn.commit()
            conn.close()
        except Exception as e:
            return str(e)

    # 连接DB
    def connDB(obj):
        """
        {
            "db_type": "Oracle",
            "host_name": "XMNCC4ENGDB010.dhcp.apac.dell.com:1521",
            "service_name":"mostpdb.apac.dell.com",
            "user_name": "MOST",
            "password": "MOST_2020"
        }
        """
        db_type = obj["db_type"]
        host_name = obj["host_name"]
        service_name = obj["service_name"]
        user_name = obj["user_name"]
        password = obj["password"]

        # 判断db
        if db_type == "Oracle":
            conn_str = f"{user_name}/{password}@{host_name}/{service_name}"
            conn = cx.connect(conn_str)
        elif db_type == "SQL":
            conn = sqla.create_engine(
                f"mssql+pymssql://{user_name}:{password}@{host_name}/{service_name}?charset=utf8"
            ).connect()

        return conn

    def rebuildSQL(table_name, columns):
        """
        table_name:
        columns:['ORDERNUM', 'QTY']
        output:
          insert into test_import(ORDERNUM,QTY)values(:1,:2)
        """
        # columns str
        col_str = ""
        # values str
        value_str = ""
        for j, key in enumerate(columns):
            col_str += key
            value_str += ":" + str((j + 1))
            # 最后一个不拼接','
            if j != len(columns) - 1:
                col_str += ","
                value_str += ","
        return f"insert into {table_name}({col_str}) values({value_str})"

    def loadFile(obj):
        """
        {
          file_name:xx,
          file_path:xx,
          file_extend:xx,
          file_type:xx,
          row_spilt:xx,
          quote:xx,
          data_value:xx,
          table_name:
          sheet_name:
          model:
          header:
          skiprows:
          mapping_data:[
            {
              source:
              column_name
            }
          ]
          ]
        }

        """

        file_type = obj["file_type"]
        if file_type == "Value":
            table_data = eval(obj["data_value"])
        else:
            file_name = obj["file_name"]
            file_extend = obj["file_extend"]
            file_name = f"{file_name}.{file_extend}"
            file_path = obj["file_path"]
            file_fullPath = f"{file_path}\\{file_name}"
            sheet_name = obj["sheet_name"]
            mapping_data = obj["mapping_data"]
            if obj["header"] == 0:
                header = obj["header"]
            else:
                header = None
            if obj["skiprows"] == 0:
                skiprows = obj["skiprows"]
            else:
                skiprows = None
            if file_type == "Excel":
                sheet_name_data = pd.read_excel(
                    file_fullPath,
                    sheet_name=sheet_name,
                    skiprows=skiprows,
                    header=header,
                )
            elif file_type == "CSV":
                sheet_name_data = pd.read_csv(
                    file_fullPath,
                    sheet_name=sheet_name,
                    header=header,
                    skiprows=skiprows,
                )
            elif file_type == "TXT":
                row_spilt = obj["row_spilt"]
                sheet_name_data = pd.read_csv(
                    file_fullPath,
                    skiprows=skiprows,
                    sep=row_spilt,
                )
            table_data = Importer.mergeData(sheet_name_data, mapping_data, header)
        return table_data

    def mergeData(sheet_name_data, mapping_data, header):
        """
        sheet_name_data:DataFrame Data
        mapping_data:[{"source":xx,"column_name":xx2}]
        """
        data1 = []
        columns = list(sheet_name_data.columns.tolist())
        if header != 0:
            columns = ["COL" + str(item + 1) for item in columns]
        for j in range(1, len(sheet_name_data)):
            dic1 = dict()
            for i in mapping_data:
                column_name = i["column_name"]
                source = i["source"]
                column_index = columns.index(source)
                if column_index != -1:
                    dic1[column_name] = str(sheet_name_data.iloc[j, column_index])
                else:
                    dic1[column_name] = None
            data1.append(dic1)
        return data1
