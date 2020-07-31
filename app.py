import flask
from flask import render_template
from flaskext.mysql import MySQL
app = flask.Flask(__name__)
#development mode
app.config['DEBUG'] = True
#Database Configuration
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'coronadb'
mysql.init_app(app)

@app.route("/", methods=['GET'])
def testing_app():
    #return "<h1>Testing Flask Application</h1>"
    data = ['Bhavana','Urmila','Deven', 'Mrinal','Sneha']
    return render_template("home.html", data=data)

@app.route("/home", methods=['GET'])
def home_corona_page():
    con = mysql.connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM corona_details;")
    rows = cur.fetchall()
    row_data =[]
    for row in rows:
        d = {'id':row[0], 'age':row[1], 'name':row[2]}
        if row[4] == 1 and row[5] ==1:
            d['cf'] = "Yes"
        elif row[4] == 1 and row[5] == 0:
            d['cf'] = "Cough"
        elif row[4] == 0 and row[5] ==1:
            d['cf'] = "Fever"
        else:
            d['cf'] = "No"
        if row[6] == 1:
            d['breath'] = "Yes"
        else:
            d['breath'] = "No"
        if row[3] == 1 and row[7] == 1 and row[8] == 1 and row[9] == 1:
            d['od'] = "Yes"
        elif row[3] == 1 and row[7] == 0 and row[8] == 0 and row[9] == 0:
            d['od'] = "HBP"
        elif row[3] == 1 and row[7] == 1 and row[8] == 0 and row[9] == 0:
            d['od'] = "HBP & Diabetes"
        elif row[3] == 1 and row[7] == 0 and row[8] == 1 and row[9] == 0:
            d['od'] = "HBP & Lungs Problem"
        elif row[3] == 1 and row[7] == 0 and row[8] == 0 and row[9] == 1:
            d['od'] = "HBP & Heart Problem"
        elif row[3] == 0 and row[7] == 1 and row[8] == 0 and row[9] == 0:
            d['od'] = "Diabetes"
        elif row[3] == 0 and row[7] == 1 and row[8] == 1 and row[9] == 0:
            d['od'] = "Diabetes & Lung problem"
        elif row[3] == 0 and row[7] == 1 and row[8] == 0 and row[9] == 1:
            d['od'] = "Diabetes & Heart problem"
        elif row[3] == 0 and row[7] == 0 and row[8] == 1 and row[9] == 0:
            d['od'] = "Lung Problem"
        elif row[3] == 0 and row[7] == 0 and row[8] == 1 and row[9] == 1:
            d['od'] = "Lung and Heart Problem"
        elif row[3] == 0 and row[7] == 0 and row[8] == 0 and row[9] == 1:
            d['od'] = "Heart Problem"
        else:
            d['od'] = "No"
        if row[10]==1:
            d['travel'] = "Yes"
        else:
            d['travel']="No"
        if row[11]=="1":
            d['pd'] = "Doctor/Police"
        else:
            d['pd']="Civilian"
        if row[12]==1:
            d['covid']="Yes"
        else:
            d['covid']="No"
        d['status']=row[13]
        row_data.append(d)
    cur.close()
    con.close()
    return render_template("corona_home.html", data=row_data)

#run the flask application
app.run()