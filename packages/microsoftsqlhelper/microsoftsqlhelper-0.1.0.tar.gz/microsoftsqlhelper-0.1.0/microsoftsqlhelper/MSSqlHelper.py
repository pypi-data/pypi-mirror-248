from enum import Enum
import pyodbc
import json


class CommandType(Enum):
    StoredProcedure = 1
    CommandText = 2


class MSSqlHelper:
    @staticmethod
    def SelectRows(
        connectionString: str,
        cmdType: CommandType,
        cmdText: str,
        commandParameters: dict = None,
    ):
        typecmd = ""
        params = ""
        dt = []

        if cmdType == CommandType.StoredProcedure:
            typecmd = "EXEC "

        if commandParameters is not None and cmdType != CommandType.CommandText:
            for key, value in commandParameters.items():
                params += " " + str(key) + " =" + " " + str(value) + ","
            params = params[:-1]

        with pyodbc.connect(connectionString) as connection:
            with connection.cursor() as cursor:
                query = typecmd + cmdText + params + ";"
                cursor.execute(query)
                dt = cursor.fetchall()
        return dt

    @staticmethod
    def ExecuteNonQuery(
        connectionString: str,
        cmdType: CommandType,
        cmdText: str,
        commandParameters: dict = None,
    ):
        typecmd = ""
        params = ""

        if cmdType == CommandType.StoredProcedure:
            typecmd = "EXEC "

        if commandParameters is not None and cmdType != CommandType.CommandText:
            for key, value in commandParameters.items():
                params += " " + str(key) + " =" + " " + str(value) + ","
            params = params[:-1]

        with pyodbc.connect(connectionString) as connection:
            with connection.cursor() as cursor:
                query = typecmd + cmdText + params + ";"
                cursor.execute(query.strip())
                connection.commit()
                return cursor.rowcount

    @staticmethod
    def ExecuteReaderFieldByField(
        connectionString: str,
        cmdType: CommandType,
        cmdText: str,
        commandParameters: dict = None,
    ):
        typecmd = ""
        params = ""
        myList = []

        if cmdType == CommandType.StoredProcedure:
            typecmd = "EXEC "

        if commandParameters is not None and cmdType != CommandType.CommandText:
            for key, value in commandParameters.items():
                params += " " + str(key) + " =" + " " + str(value) + ","
            params = params[:-1]

        with pyodbc.connect(connectionString) as connection:
            with connection.cursor() as cursor:
                query = typecmd + cmdText + params + ";"
                cursor.execute(query.strip())
                for row in cursor:
                    for index in range(len(row)):
                        myList.append(
                            cursor.description[index][0] + ":" + str(row[index])
                        )
        return myList

    @staticmethod
    def ExecuteReaderJSON(
        connectionString: str,
        cmdType: CommandType,
        cmdText: str,
        commandParameters: dict = None,
    ):
        typecmd = ""
        params = ""
        myList = []

        if cmdType == CommandType.StoredProcedure:
            typecmd = "EXEC "

        if commandParameters is not None and cmdType != CommandType.CommandText:
            for key, value in commandParameters.items():
                params += " " + str(key) + " =" + " " + str(value) + ","
            params = params[:-1]

        with pyodbc.connect(connectionString) as connection:
            with connection.cursor() as cursor:
                query = typecmd + cmdText + params + ";"
                cursor.execute(query.strip())
                for row in cursor:
                    for index in range(len(row)):
                        myList.append(
                            cursor.description[index][0] + ":" + str(row[index])
                        )
                result = json.dumps(myList, default=str)
        return result
