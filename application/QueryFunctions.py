import pymysql.cursors
from config import Config


###This class have to add error handler

class TableOperationBySQL():

    def __init__(self, Config, table_name):
        self.Config = Config
        self.table_name = table_name

    #This function Begin Connection
    def begin_connection(self):
        connection = pymysql.connect(host=self.Config.host,
                                user=self.Config.user,
                                password=self.Config.password,
                                db=self.Config.db_name,
                                charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor)
        return connection

    #This function Close Connecotion
    def close_connection(self, connection):
        connection.close()
        
    #SELECT
    #SELECT patern 
    # 1.User search company conditions --> SELECT company id, company name, company text... FROM campanies WHERE time == 1hour and location == kanagawa...
    # 2.User click company link. --> 
    # 3.Company logged in homePage used by company name, password, company_id -->  
    # 4.Company click OUBOuserTable data by company_id --> 

    #ex)This function outputs "company_id, working_time, location" 
    def make_select_data_for_SQL(self, select_datas):
        #ex)select_datas = [company_id,warking_time,location]
        select_data_for_SQL = ",".join(select_datas)
        return select_data_for_SQL

    #ex)This function execute SELECT company_id, working_time, location WHERE company_id == 1 and working_time == 1hour ...
    def select(self, select_datas, condition_dict):
        #ex)select_datas = [company_id,warking_time,location]
        #ex)condition_dict = {company_name:panasonic, working_time:1hour, location:kanagawa ...}
        select_where_data = ""
        for key, value in condition_dict.items():
            select_where_data += f"{key} = {value} and "
        select_where_data = select_where_data[:-4]

        if select_datas == "*":
            sql = f"SELECT * FROM {self.table_name} WHERE {select_where_data}"
        else :
            select_data_for_SQL = self.make_select_data_for_SQL(select_datas)
            #Create SQL
            sql = f"SELECT {select_data_for_SQL} FROM {self.table_name} WHERE {select_where_data}"
        #Connection MySQL
        connection = self.begin_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
                return result
        finally:
            #Close connection
            self.close_connection(connection)
            print("select")
            print(sql)
        ###return result --> and jsonify({select_result:result})

    
    #INSERT
    #INSERT patern
    # Regist new company conditions 
    # Regist new identificate 
    # User insert new application data

    #ex)This function execute INSERT INTO companies (company_name,workingTime,salaryPerHour,salaryPerDay,salaryPerMounth,location) VALUES (Fujitsu,4hours,1000,6000,170000,Tokyo)
    def insert(self, condition_dict):
        #ex)condition_dict = {'company_name': 'Fujitsu', 'workingTime': '4hours', 'salaryPerHour': 1500, 'salaryPerDay': 9000, 'salaryPerMounth': 160000, 'location': 'Tokyo'}

        #Make SQL material
        insert_columns_for_SQL = ""
        insert_columns_values_for_SQL = ""
        for column_name, column_value in condition_dict.items():
            insert_columns_for_SQL += column_name + ","
            insert_columns_values_for_SQL += str(column_value) + ","
        #Remove last ","
        insert_columns_for_SQL = insert_columns_for_SQL[:-1]
        insert_columns_values_for_SQL = insert_columns_values_for_SQL[:-1]
        #Create SQL
        sql = f"INSERT INTO {self.table_name} ({insert_columns_for_SQL}) VALUES ({insert_columns_values_for_SQL})"
        #Connection MySQL
        connection = self.begin_connection()
        #Execute SQL and commit 
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
            connection.commit()
        finally:
            #Close connection
            self.close_connection(connection)
            print("insert")
            print(sql)


    #UPDATE
    #UPDATE patern
    # Company update company condition
    # User update yours condition

    #This function execute UPDATE test woriking_time = 1hour, location = Tokyo, salary = 500 WHERE company_name = daikin
    def update(self,where_data,update_data):
    #ex)where_data = {company_id: int} or {company_name: "daikin"}
    #ex)update_data =  {working_time:"1hours",location:"tokyo" }
        update_data_for_SQL = f"UPDATE {self.table_name} SET "
        where_data_for_SQL = f"WHERE {next(iter(where_data.keys()))} = {next(iter(where_data.values()))}"###this data is ok form
        for key, value in update_data.items():
            update_data_for_SQL += f" {key} = {value},"
            #result = UPDATE company_condition working_time = 1hour, location = tokyo, 
        sql = update_data_for_SQL[:-1] + " " + where_data_for_SQL
        #Connection MySQL
        connection = self.begin_connection()
        #Execute SQL and commit 
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
            connection.commit()
        finally:
            #Close connection
            self.close_connection(connection)
            print("update")
            print(sql)


    #DELETE
    #DELETE patern
    # Company delete yours conditions
    # Company delete all data
    # User delete yours application data
    
    #ex)This function execute DELETE FROM company_condition WHERE company_name ==  daikin
    def delete(self, identificate_data):
        #ex)identificate_data = { company_id : 1 }
        id = next(iter(identificate_data.keys()))
        value = next(iter(identificate_data.values()))
        sql = f"DELETE FROM {self.table_name} WHERE {id} = {value}"
        #Connection MySQL
        connection = self.begin_connection()
        #Execute SQL and commit 
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
            connection.commit()
        finally:
            #Close connection
            self.close_connection(connection)
            print("update")
            print(sql)
