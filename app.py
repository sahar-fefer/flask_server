from flask import Flask, jsonify, request, make_response, render_template, redirect, json
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'realtor'

mysql = MySQL(app)


@app.route('/')
def Home():
    return 'HOME'


@app.route('/apartments', methods=['GET'])
def getApartments():
    cur = mysql.connection.cursor()
    cur.execute('''Select * from apartments where status = "approved" and availability  = "available"''')
    results = cur.fetchall()
    return jsonify(results)


@app.route('/apartments/<apartment_id>/images', methods=['GET'])
def getApartmentImages(apartment_id):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT url FROM images WHERE apartment_id = (%s)''' % (apartment_id))
    results = cur.fetchall()
    return jsonify(results)


@app.route('/<user_id>', methods=['GET'])
def getApartmentsUser(user_id):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM apartments WHERE user_id = (%s)''' % (user_id))
    results = cur.fetchall()
    return jsonify(results)

@app.route('/apartments/rent_or_sale', methods=['GET'])
def getRentSaleApartments():
    sale = getSaleApartments()
    rent = getRentApartments()
    print('sale', sale)
    print('rent', rent)
    print({"rent": rent, "sale": sale})
    return {"rent": rent, "sale": sale}

def getSaleApartments():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT COUNT(*) as sale FROM apartments where status = 'approved' and availability = 'available' and sale_status = 'sale';''')
    results = cur.fetchall()
    return results[0][0]

def getRentApartments():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT COUNT(*) as rent FROM apartments where status = 'approved' and availability = 'available' and sale_status = 'rent';''')
    results = cur.fetchall()
    return results[0][0]

@app.route('/cities', methods=['GET'])
def getCities():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM cities''')
    results = cur.fetchall()
    return jsonify(results)


@app.route('/cities/<id>', methods=['GET'])
def getCity(id):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM cities WHERE id = (%s)''' % (id))
    results = cur.fetchall()
    return jsonify(results)


@app.route('/cities/withApartments', methods=['GET'])
def allCitiesWithApartments():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT C.id, C.name FROM cities C JOIN apartments A on A.city_id = C.id group by C.id;''')
    results = cur.fetchall()
    return jsonify(results)

@app.route("/users/login", methods=['POST', 'OPTIONS'])
def login():
    user_data = request.get_json()
    email = user_data['email']
    password = user_data['password']
    if email and password:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password,))
        user = cursor.fetchone()
        if user:
            res = make_response('send a cookie')
            user_ditails = {'id': user[0], 'first_name': user[2]}
            print('json.dumps', json.dumps(user_ditails))
            res.set_cookie('auth', str(user_ditails), max_age = 60 * 60 * 24 * 365 * 2)
            return res
        else:
            return 'Incorrect username/password!'
    else:
        return 'nooo'

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=4040, debug=True)

app.run()