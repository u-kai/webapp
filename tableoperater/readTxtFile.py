# def fileToCreateTable(file_path)
with open("test2.txt" ,"r") as file:
    string = file.read()

slist = string.split()
number_of_primary_key = 0

while True:
    try:
        index = slist.index("1")
        slist.pop(index)
        number_of_primary_key += 1
    except ValueError:
        break
print(slist, number_of_primary_key)
table_name = "tests"
valueList = []
typeList = []
primary_key = 1
sql = f"CREATE table {table_name} ("
for i in range(0,len(slist),2):
    valueList.append(slist[i])
    typeList.append(slist[i + 1])
    sql += f"{slist[i]} {slist[i + 1]},"
    if i == 6:
        break
if primary_key is None:
    sql = sql + ")"
else :
    sql = f"{sql} primary key ("
    for primary_key_index in range(primary_key + 1):
        sql += f" {valueList[primary_key_index]},"
    sql = sql[:-1] + "))"

from application.QueryFunctions import TableOperationBySQL
from application.config import Config
t = TableOperationBySQL(Config, "myweb2")
print(sql)
t.executeSQL(sql)
    