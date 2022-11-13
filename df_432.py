# import all necessary modules
from flask import Flask
from flask import jsonify
import pyodbc as pyo

# establish connection to the Azure SQL DB using ODBC connector
titanic_sql_azure = (r"Driver={ODBC Driver 18 for SQL Server};Server=tcp:cf-432-sql-server.database.windows.net,"
                     r"1433;Database=CF_432;Uid=cf432432;Pwd={"
                     r"Neil432432!};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")


cnxn: pyo.Connection = pyo.connect(titanic_sql_azure)
crsr: pyo.Cursor = cnxn.cursor()

sql = "SELECT * FROM dbo.TITANIC"
crsr.execute(sql)

columns = [column[0] for column in crsr.description]
json_db = []

for row in crsr.fetchmany(10):
    json_db.append(dict(zip(columns, row)))

cnxn.close()

app = Flask(__name__)

# test if the api is established
# @app.route("/", methods=['GET'])
# def welcome():
#     return "Welcome to Python WebServices"

# api to get first 10 lines
@app.route("/gettenrows", methods=['GET'])
def topten():
    return jsonify({"topten": json_db})

if (__name__ == '__main__'):
    app.run()
