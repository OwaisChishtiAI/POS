import mysql.connector
from flask import Flask, json, jsonify, request
from flask_cors import CORS
from datetime import datetime
from dateutil import parser

app = Flask(__name__)
CORS(app)

"""
ADMIN APIsa and Functions START
"""
@app.route("/admin_login_write", methods=['POST'])
def admin_login_write_fn():
    data = request.form.to_dict()
    print("#####################################", data)
    admin_login_write_db(data)
    return "0"

def admin_login_write_db(data):
    keys = ""
    vals = []
    for key, val in data.items():
        keys = keys + key + ", "
        vals.append(val)
    vals = tuple(vals)
    print(keys)
    sql = "INSERT INTO login ({0}) VALUES (%s, %s, %s);".format(keys[:-2])
    print("@@@@@@@@@@@@@", (sql, vals))
    cursor, db = connect.pointer()
    cursor.execute(sql, vals)
    db.commit()

@app.route("/admin_login_read", methods=['POST'])
def admin_login_read_fn():
    data = request.form.to_dict()
    user_email = data.get('user_email')
    data = admin_login_read_db(user_email)
    print("#####################################", data)
    return jsonify(data) 

def admin_login_read_db(user_email):
    cursor = connect.pointer()[0]
    if user_email:
        sql = "SELECT * FROM login WHERE username = '{}'".format(user_email.strip())
    else:
        sql = "SELECT * FROM login"
    print(sql)
    cursor.execute(sql)

    myresult = cursor.fetchall()
    data = []
    keys = ['username', 'password', 'admin_status']
    for each in myresult:
        json_data = {}
        each = list(each)
        each.pop(0)
        for x,y in zip(keys, each):
            json_data[x] = y
        data.append(json_data)
    return data

@app.route("/admin_emp_salary_write", methods=['POST'])
def admin_emp_salary_write_fn():
    data = request.form.to_dict()
    print("#####################################", data)
    admin_emp_salary_write_db(data)
    return "0"

def admin_emp_salary_write_db(data):
    keys = ""
    vals = []
    for key, val in data.items():
        keys = keys + key + ", "
        vals.append(val)
    vals = tuple(vals)
    print(keys)
    sql = "INSERT INTO emp_salary ({0}) VALUES (%s, %s, %s, %s, %s);".format(keys[:-2])
    print("@@@@@@@@@@@@@", (sql, vals))
    cursor, db = connect.pointer()
    cursor.execute(sql, vals)
    db.commit()

@app.route("/admin_emp_salary_read", methods=['POST'])
def admin_emp_salary_read_fn():
    data = request.form.to_dict()
    user_email = data.get('user_email')
    data = admin_emp_salary_read_db(user_email)
    print("#####################################", data)
    return jsonify(data) 

def admin_emp_salary_read_db(user_email):
    cursor = connect.pointer()[0]
    if user_email:
        sql = "SELECT * FROM emp_salary WHERE agent_id = '{}'".format(user_email.strip())
    else:
        sql = "SELECT * FROM emp_salary"
    print(sql)
    cursor.execute(sql)

    myresult = cursor.fetchall()
    data = []
    keys = ['agent_id', 'salary', 'com_b_15', 'com_a_15', 'X_15']
    for each in myresult:
        json_data = {}
        each = list(each)
        # each.pop(0)
        for x,y in zip(keys, each):
            json_data[x] = y
        data.append(json_data)
    return data

@app.route("/admin_emp_salary_update", methods=['POST'])
def admin_emp_salary_update_fn():
    data = request.form.to_dict()
    print("EDIT #####################################", data)
    admin_emp_salary_update_db(data)
    return jsonify(data)

def admin_emp_salary_update_db(data):
    keys = ""
    vals = []
    # data['timestamp'] = parser.parse(data['timestamp'])
    # print("$$$$$$$", type(data['timestamp']), data['timestamp'])
    for key, val in data.items():
        keys = keys + key + ", "
        vals.append(val)
    keys = keys[:-2]
    vals = tuple(vals)
    sql = "UPDATE emp_salary SET "
    for i in range(len(data.values())-1):
        # if not list(data.keys())[i] == "order_id":
        sql = sql + "{0} = '{1}', ".format(list(data.keys())[i], list(data.values())[i])
    sql = sql[:-2] + " "
    sql = sql + "WHERE {0} = '{1}'".format("agent_id", data['agent_id'])
    print(sql)
    # print("@@@@@@@@@@@@@", (sql, vals))
    cursor, db = connect.pointer()
    cursor.execute(sql)

    db.commit()

@app.route("/admin_emp_salary_delete", methods=['POST'])
def admin_emp_salary_delete_fn():
    agent_id = request.form.to_dict()['agent_id']
    admin_emp_salary_delete_db(agent_id)
    return jsonify({"OK" : "200"})

def admin_emp_salary_delete_db(agent_id):
    sql = "DELETE FROM emp_salary WHERE agent_id = '{0}'".format(agent_id)
    print("DELETE: ", sql)
    cursor, db = connect.pointer()
    cursor.execute(sql)

    db.commit()

@app.route("/admin_read_sales", methods=['POST'])
def admin_read_sales_fn():
    data = request.form.to_dict()
    from_date = data.get('from_date')
    to_date = data.get('to_date')
    agent_id = data.get('agent_id')
    if from_date:
        if to_date:
            print("Dates Provided")
            data = admin_read_sales_by_date(from_date, to_date)
    else:
        print("Dates NOT Provided")
        data = admin_read_sales_db()
    print(len(data), data)
    return jsonify(data)

def admin_read_sales_by_date(from_date, to_date):
    cursor = connect.pointer()[0]
    sql = "SELECT * FROM emp_sales WHERE timestamp BETWEEN '{0}' AND '{1}'".format(from_date, to_date)
    print(": ", sql)
    cursor.execute(sql)
    myresult = cursor.fetchall()
    data = []
    keys = ["timestamp","agent_name","order_id","client_name","contact","email_id","total_tariff","deposit","profit","driver_pay","payment_method","pickup_date","no_of_vehicles","pickup","booking_status","agreement","agent_notes","jt_link","agent_id"]
    for each in myresult:
        json_data = {}
        each = list(each)
        each.pop(0)
        for x,y in zip(keys, each):
            json_data[x] = y
        data.append(json_data)
    return data

def admin_read_sales_db():
    cursor = connect.pointer()[0]
    cursor.execute("SELECT * FROM emp_sales")

    myresult = cursor.fetchall()
    data = []
    keys = ["timestamp","agent_name","order_id","client_name","contact","email_id","total_tariff","deposit","profit","driver_pay","payment_method","pickup_date","no_of_vehicles","pickup","booking_status","agreement","agent_notes","jt_link","agent_id"]
    for each in myresult:
        json_data = {}
        each = list(each)
        each.pop(0)
        for x,y in zip(keys, each):
            json_data[x] = y
        data.append(json_data)
    return data

@app.route("/admin_emp_salary_search", methods=['POST'])
def admin_emp_salary_search_fn():
    data = request.form.to_dict()
    figures = admin_emp_salary_search_db(data)
    return jsonify([figures])

def admin_emp_salary_search_db(data):
    months = {"January" : 1,"February" : 2,"March" : 3,"April" : 4,"May" : 5,"June" : 6,"July" : 7,"August" : 8,"September" : 9,"October" : 10,"November" : 11,"December" : 12}
    cursor = connect.pointer()[0]
    month = int(months[data['sal_month']])
    year = data['sal_year']
    sql = "SELECT * FROM emp_time WHERE '{0}-{1}-01' <= end_time AND end_time < '{2}-{3}-01' AND agent_id = '{4}'".format(str(year), str(month), str(year), str(month+1), data['agent_id'])
    print("SEARCH: ", sql)
    cursor.execute(sql)
    days = cursor.fetchall()
    no_of_days = len(days)
    print(days, no_of_days)
    sql2 = "SELECT * FROM emp_sales WHERE '{0}-{1}-01' <= timestamp AND timestamp < '{2}-{3}-01' AND agent_id = '{4}'".format(str(year), str(month), str(year), str(month+1), data['agent_id'])
    print("sql2: ", sql2)
    cursor.execute(sql2)
    sales = cursor.fetchall()
    print(sales)
    total_tarrif = []
    for each_sale in sales:
        total_tarrif.append(int(each_sale[7]))
    
    total_tarrif = sum(total_tarrif)
    print("Total Sales: ", total_tarrif)
    sql3 = "SELECT * FROM emp_salary WHERE agent_id = '{}'".format(data['agent_id'])
    cursor.execute(sql3)
    sal_com = cursor.fetchall()
    print("EMP SALARY: ", sal_com)
    sal_com = sal_com[0]
    salary = int(sal_com[1])
    com_b = int(sal_com[2])
    com_a = int(sal_com[3])
    thresh = int(sal_com[4])
    print(data['agent_id'], salary, com_b, com_a, thresh)
    salary = salary / 25
    salary = salary * no_of_days
    if total_tarrif <= thresh:
        commision = (total_tarrif//100) * com_b
    else:
        commision = (total_tarrif//100) * com_a
    print("#################################################################################################")
    print({"agent_id": data['agent_id'], "salary": salary, 'commision': commision, 'total': salary+commision})
    return {"agent_id": data['agent_id'], "days": no_of_days, "salary": salary, 'commision': commision, 'total': salary+commision}

@app.route("/admin_write_expense", methods=['GET', 'POST'])
def admin_write_expense_fn():
    data = request.form.to_dict()
    print("#####################################", data)
    admin_write_expense_db(data)
    return "0"

def admin_write_expense_db(data):
    data['timestamp'] = datetime.strptime(data['timestamp'], '%m/%d/%Y, %H:%M:%S %p')
    keys = ""
    vals = []
    for key, val in data.items():
        keys = keys + key + ", "
        vals.append(val)
    vals = tuple(vals)
    print(keys)
    sql = "INSERT INTO expenses ({0}) VALUES (%s, %s, %s);".format(keys[:-2])
    print("@@@@@@@@@@@@@", (sql, vals))
    cursor, db = connect.pointer()
    cursor.execute(sql, vals)
    db.commit()

@app.route("/admin_read_expense", methods=['POST'])
def admin_read_expense_fn():
    data = request.form.to_dict()
    from_date = data.get('from_date')
    to_date = data.get('to_date')
    # agent_id = data.get('agent_id')
    if from_date:
        if to_date:
            print("Dates Provided")
            data = admin_read_expense_db_by_date(from_date, to_date)
    else:
        print("Dates NOT Provided")
        data = admin_read_expense_db()
    print(len(data), data)
    return jsonify(data)

def admin_read_expense_db_by_date(from_date, to_date):
    cursor = connect.pointer()[0]
    sql = "SELECT * FROM expenses WHERE timestamp BETWEEN '{0}' AND '{1}'".format(from_date, to_date)
    print(": ", sql)
    cursor.execute(sql)
    myresult = cursor.fetchall()
    data = []
    keys = ['expense_id', 'timestamp', 'exp_name', 'exp_amt']
    for each in myresult:
        json_data = {}
        each = list(each)
        # each.pop(0)
        for x,y in zip(keys, each):
            json_data[x] = y
        data.append(json_data)
    return data

def admin_read_expense_db():
    cursor = connect.pointer()[0]
    cursor.execute("SELECT * FROM expenses")

    myresult = cursor.fetchall()
    data = []
    keys = ['expense_id', 'timestamp', 'exp_name', 'exp_amt']
    for each in myresult:
        json_data = {}
        each = list(each)
        # each.pop(0)
        for x,y in zip(keys, each):
            json_data[x] = y
        data.append(json_data)
    return data

@app.route("/admin_update_expense", methods=['POST'])
def admin_update_expense_fn():
    data = request.form.to_dict()
    print("EDIT #####################################", data)
    admin_update_expense_db(data)
    return jsonify(data)

def admin_update_expense_db(data):
    keys = ""
    vals = []
    data['timestamp'] = parser.parse(data['timestamp'])
    # print("$$$$$$$", type(data['timestamp']), data['timestamp'])
    for key, val in data.items():
        keys = keys + key + ", "
        vals.append(val)
    keys = keys[:-2]
    vals = tuple(vals)
    sql = "UPDATE expenses SET "
    sql = sql + "exp_name = '{0}', exp_amt = '{1}'".format(data['exp_name'], data['exp_amt'])
    # sql = sql[:-2] + " "
    sql = sql + " WHERE {0} = '{1}'".format("expense_id", data['expense_id'])
    print(sql)
    # print("@@@@@@@@@@@@@", (sql, vals))
    cursor, db = connect.pointer()
    cursor.execute(sql)

    db.commit()

@app.route("/admin_partners_write", methods=['POST'])
def admin_partners_write_fn():
    data = request.form.to_dict()
    print("#####################################", data)
    admin_partners_write_db(data)
    return "0"

def admin_partners_write_db(data):
    keys = ""
    vals = []
    for key, val in data.items():
        keys = keys + key + ", "
        vals.append(val)
    vals = tuple(vals)
    print(keys)
    sql = "INSERT INTO partners ({0}) VALUES (%s, %s);".format(keys[:-2])
    print("@@@@@@@@@@@@@", (sql, vals))
    cursor, db = connect.pointer()
    cursor.execute(sql, vals)
    db.commit()

@app.route("/admin_partner_read", methods=['POST'])
def admin_partner_read_fn():
    data = request.form.to_dict()
    user_email = data.get('user_email')
    data = admin_partner_read_db(user_email)
    print("#####################################", data)
    return jsonify(data) 

def admin_partner_read_db(user_email):
    cursor = connect.pointer()[0]
    if user_email:
        sql = "SELECT * FROM partners WHERE agent_id = '{}'".format(user_email.strip())
    else:
        sql = "SELECT * FROM partners"
    print(sql)
    cursor.execute(sql)

    myresult = cursor.fetchall()
    data = []
    keys = ['partner_id','agent_id', 'salary']
    for each in myresult:
        json_data = {}
        each = list(each)
        # each.pop(0)
        for x,y in zip(keys, each):
            json_data[x] = y
        data.append(json_data)
    return data

@app.route("/admin_partner_update", methods=['POST'])
def admin_partner_update_fn():
    data = request.form.to_dict()
    print("EDIT #####################################", data)
    admin_partner_update_db(data)
    return jsonify(data)

def admin_partner_update_db(data):
    keys = ""
    vals = []
    # data['timestamp'] = parser.parse(data['timestamp'])
    # print("$$$$$$$", type(data['timestamp']), data['timestamp'])
    for key, val in data.items():
        keys = keys + key + ", "
        vals.append(val)
    keys = keys[:-2]
    vals = tuple(vals)
    sql = "UPDATE partners SET "
    # for i in range(len(data.values())-1):
        # if not list(data.keys())[i] == "order_id":
    sql = sql + "agent_id = '{0}', salary = '{1}'".format(data['agent_id'], data['salary'])
    sql = sql + "WHERE {0} = '{1}'".format("partner_id", data['partner_id'])
    print(sql)
    # print("@@@@@@@@@@@@@", (sql, vals))
    cursor, db = connect.pointer()
    cursor.execute(sql)

    db.commit()

@app.route("/admin_expenses_delete", methods=['POST'])
def admin_expenses_delete_fn():
    expense_id = request.form.to_dict()['expense_id']
    admin_expenses_delete_db(expense_id)
    return jsonify({"OK" : "200"})

def admin_expenses_delete_db(expense_id):
    sql = "DELETE FROM expenses WHERE expense_id = '{0}'".format(expense_id)
    print("DELETE: ", sql)
    cursor, db = connect.pointer()
    cursor.execute(sql)

    db.commit()

@app.route("/admin_partners_delete", methods=['POST'])
def admin_partners_delete_fn():
    partner_id = request.form.to_dict()['partner_id']
    admin_partners_delete_db(partner_id)
    return jsonify({"OK" : "200"})

def admin_partners_delete_db(partner_id):
    sql = "DELETE FROM partners WHERE partner_id = '{0}'".format(partner_id)
    print("DELETE: ", sql)
    cursor, db = connect.pointer()
    cursor.execute(sql)

    db.commit()

@app.route("/admin_profit_search", methods=['POST'])
def admin_profit_search_fn():
    data = request.form.to_dict()
    figures = admin_profit_search_db(data)
    return jsonify(figures)

def admin_profit_search_db(data):
    months = {"January" : 1,"February" : 2,"March" : 3,"April" : 4,"May" : 5,"June" : 6,"July" : 7,"August" : 8,"September" : 9,"October" : 10,"November" : 11,"December" : 12}
    cursor = connect.pointer()[0]
    month = int(months[data['sal_month']])
    year = data['sal_year']
    revenue = int(data['revenue'])
    sql = "SELECT * FROM expenses WHERE '{0}-{1}-01' <= timestamp AND timestamp < '{2}-{3}-01'".format(str(year), str(month), str(year), str(month+1))
    print("SEARCH SQL: ", sql)
    cursor.execute(sql)
    total_expenses = cursor.fetchall()
    print("total_expenses: ", total_expenses)
    total_expenses_li = []
    for each in total_expenses:
        total_expenses_li.append(int(each[3]))
    total_expenses_li = sum(total_expenses_li)
    print("Total Expenses: ", total_expenses_li)
    total_profit = revenue - total_expenses_li
    sql2 = "SELECT * FROM partners"
    cursor.execute(sql2)
    partners = cursor.fetchall()
    figures = []
    for every in partners:
        figures.append({"revenue": revenue, "total_expenses": total_expenses_li, "total_profit": total_profit, "agent_id": every[1],\
            "partner_share": (int(every[2])/100) * total_profit })
    print("figures: ", figures)
    return figures


"""
ADMIN APIs and Functions END ------------------------------------------------------------------------------------------------------->
                             ------------------------------------------------------------------------------------------------------->
                             ------------------------------------------------------------------------------------------------------->
                             ------------------------------------------------------------------------------------------------------->
"""

@app.route("/write", methods=['GET', 'POST'])
def write_fn():
    data = request.form.to_dict()
    print("#####################################", data)
    insert_db(data)
    return "0"

@app.route("/write_time", methods=['GET', 'POST'])
def write_time_fn():
    data = request.form.to_dict()
    print("#####################################", data)
    insert_db_time(data)
    return "0"

@app.route("/read", methods=['POST'])
def read_fn():
    data = request.form.to_dict()
    from_date = data.get('from_date')
    to_date = data.get('to_date')
    agent_id = data.get('agent_id')
    if from_date:
        if to_date:
            print("Dates Provided")
            data = read_db_by_date(from_date, to_date, agent_id)
    else:
        print("Dates NOT Provided")
        data = read_db(agent_id)
    print(len(data))
    return jsonify(data)

@app.route("/read_time", methods=['POST'])
def read_time_fn():
    data = request.form.to_dict()
    from_date = data.get('from_date')
    to_date = data.get('to_date')
    agent_id = data.get('agent_id')
    if from_date:
        if to_date:
            print("Dates Provided")
            data = read_db_time_by_date(from_date, to_date, agent_id)
    else:
        print("Dates NOT Provided")
        data = read_db_time(agent_id)
    print(len(data), data)
    return jsonify(data)

@app.route("/read_by_date", methods=['POST'])
def read_by_date_fn():
    data = request.form.to_dict()
    from_date = data['from_date']
    to_date = data['to_date']
    data = read_db_by_date(from_date, to_date)
    return jsonify(data)

@app.route("/delete", methods=['POST'])
def delete_fn():
    order_id = request.form.to_dict()['order_id']
    agent_id = request.form.to_dict()
    agent_id = agent_id.get('agent_id')
    if not agent_id:
        agent_id = 'null'
    print(type(order_id), len(order_id), order_id)
    delete_db(order_id, agent_id)
    return jsonify({"OK" : "200"})

@app.route("/update", methods=['POST'])
def update_fn():
    data = request.form.to_dict()
    print("EDIT #####################################", data)
    update_db(data)
    return jsonify(data)

@app.route("/login", methods=['POST'])
def login_fn():
    data = request.form.to_dict()
    print("LOGIN #####################################", data)
    admin = login(data)
    print("ADMIN: ", admin)
    return jsonify({'status' : admin}) # status : admin, emp, unk

class Connect:
    def __init__(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ag_car_db",
        )
        self.db = mydb
        self.cursor = self.db.cursor()
    
    def pointer(self):
        return (self.cursor, self.db)

    def fields(self):
        return ["timestamp","agent_name","order_id","client_name","contact","email_id","total_tariff","deposit","profit","driver_pay","payment_method","pickup_date","no_of_vehicles","pickup","booking_status","agreement","agent_notes","jt_link"]

def read_db(agent_id):
    cursor = connect.pointer()[0]
    cursor.execute("SELECT * FROM emp_sales WHERE agent_id = '{}'".format(agent_id))

    myresult = cursor.fetchall()
    data = []
    keys = connect.fields()
    for each in myresult:
        json_data = {}
        each = list(each)
        each.pop(0)
        for x,y in zip(keys, each):
            json_data[x] = y
        data.append(json_data)
    return data

def read_db_time(agent_id):
    cursor = connect.pointer()[0]
    cursor.execute("SELECT * FROM emp_time WHERE agent_id = '{}'".format(agent_id))

    myresult = cursor.fetchall()
    print("######################", myresult)
    data = []
    keys = ['start_time', 'end_time', 'agent_id']
    for each in myresult:
        json_data = {}
        each = list(each)
        # each.pop(0)
        for x,y in zip(keys, each):
            json_data[x] = y
        data.append(json_data)
    return data

def read_db_by_date(from_date, to_date, agent_id):
    cursor = connect.pointer()[0]
    sql = "SELECT * FROM emp_sales WHERE timestamp BETWEEN '{0}' AND '{1}' AND agent_id = '{2}'".format(from_date, to_date, agent_id)
    print(": ", sql)
    cursor.execute(sql)
    myresult = cursor.fetchall()
    data = []
    keys = connect.fields()
    for each in myresult:
        json_data = {}
        each = list(each)
        each.pop(0)
        for x,y in zip(keys, each):
            json_data[x] = y
        data.append(json_data)
    return data

def read_db_time_by_date(from_date, to_date, agent_id):
    cursor = connect.pointer()[0]
    sql = "SELECT * FROM emp_time WHERE start_time BETWEEN '{0}' AND '{1}' AND agent_id = '{2}'".format(from_date, to_date, agent_id)
    print(": ", sql)
    cursor.execute(sql)
    myresult = cursor.fetchall()
    data = []
    keys = ['start_time', 'end_time', 'agent_id']
    for each in myresult:
        json_data = {}
        each = list(each)
        # each.pop(0)
        for x,y in zip(keys, each):
            json_data[x] = y
        data.append(json_data)
    return data
    

def login(data):
    cursor = connect.pointer()[0]
    sql = "SELECT admin_status FROM login WHERE username = '{0}' AND password = '{1}'".format(data['username'], data['password'])
    print(sql)
    cursor.execute(sql)
    admin = cursor.fetchall()
    if admin:
        admin = admin[0][0]
        if admin:
            admin = 'admin'
        else:
            admin = 'emp'
    else:
        admin = 'null'
    return admin

def insert_db(data):
    keys = ""
    vals = []
    data['timestamp'] = datetime.strptime(data['timestamp'], '%m/%d/%Y, %H:%M:%S %p')
    for key, val in data.items():
        keys = keys + key + ", "
        vals.append(val)
    vals = tuple(vals)
    print(keys)
    sql = "INSERT INTO emp_sales ({0}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);".format(keys[:-2])
    print("@@@@@@@@@@@@@", (sql, vals))
    cursor, db = connect.pointer()
    cursor.execute(sql, vals)

    db.commit()

def insert_db_time(data):
    keys = ""
    vals = []
    data['start_time'] = datetime.strptime(data['start_time'], '%m/%d/%Y, %H:%M:%S %p')
    data['end_time'] = datetime.strptime(data['end_time'], '%m/%d/%Y, %H:%M:%S %p')
    for key, val in data.items():
        keys = keys + key + ", "
        vals.append(val)
    vals = tuple(vals)
    sql = "INSERT INTO emp_time ({0}) VALUES (%s, %s, %s);".format(keys[:-2])
    print("@@@@@@@@@@@@@", (sql, vals))
    cursor, db = connect.pointer()
    cursor.execute(sql, vals)

    db.commit()

def delete_db(order_id, agent_id):
    sql = "DELETE FROM emp_sales WHERE order_id = '{0}' AND agent_id = '{1}'".format(order_id, agent_id)
    print("DELETE: ", sql)
    cursor, db = connect.pointer()
    cursor.execute(sql)

    db.commit()

def update_db(data):
    keys = ""
    vals = []
    data['timestamp'] = parser.parse(data['timestamp'])
    print("$$$$$$$", type(data['timestamp']), data['timestamp'])
    for key, val in data.items():
        keys = keys + key + ", "
        vals.append(val)
    keys = keys[:-2]
    vals = tuple(vals)
    sql = "UPDATE emp_sales SET "
    for i in range(len(data.values())-1):
        if not list(data.keys())[i] == "order_id":
            sql = sql + "{0} = '{1}', ".format(list(data.keys())[i], list(data.values())[i])
    sql = sql[:-2] + " "
    sql = sql + "WHERE {0} = '{1}' AND agent_id = '{2}'".format("order_id", data['order_id'], data['agent_id'])
    print(sql)
    # print("@@@@@@@@@@@@@", (sql, vals))
    cursor, db = connect.pointer()
    cursor.execute(sql)

    db.commit()

if __name__ == "__main__":
    connect = Connect()
    app.run(debug=True)
    # admin_profit_search_db({'revenue': '500000', 'sal_month': 'September', 'sal_year': '2021'})
