from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_HOST'] = 'localhost:3306'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'realtor'

mysql = MySQL(app)


@app.route('/')
def Home():
    return 'HOME'


@app.route('/apartments', methods=['GET'])
# def getApartments():
#     cur = mysql.connection.cursor()
#     cur.execute('''SELECT * FROM apartments''')
#     results = cur.fetchall()
#     return jsonify(results)

def getApartments():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM apartments''')
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


####### not working #######
@app.route('/<user_id>/<status>', methods=['GET'])
def getApartmentsUserByStatus(user_id, status):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM apartments WHERE user_id = (%s) AND status = (%s)''' % (user_id, status))
    results = cur.fetchall()
    return jsonify(results)


####### send only sale apartments #######
# @app.route('/apartments/rent_or_sale', methods=['GET'])
# def getRentSaleApartments():
#     saleApartments = getSaleApartments()
#     rentApartments = getRentApartments()
#     return saleApartments

###### not working - try to join two arrs to one #######
# @app.route('/apartments/rent_or_sale', methods=['GET'])
# def getRentSaleApartments():
#     saleApartments = getSaleApartments()
#     rentApartments = getRentApartments()
#     rentSaleApartments = {rentApartments + saleApartments}
#     return rentSaleApartments

###### working #######
# def getSaleApartments():
#     cur = mysql.connection.cursor()
#     cur.execute('''SELECT COUNT(*) as sale FROM apartments where status = 'approved' and availability = 'available' and sale_status = 'sale';''')
#     results = cur.fetchall()
#     return jsonify(results)
#
# def getRentApartments():
#     cur = mysql.connection.cursor()
#     cur.execute('''SELECT COUNT(*) as rent FROM apartments where status = 'approved' and availability = 'available' and sale_status = 'rent';''')
#     results = cur.fetchall()
#     return jsonify(results)

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


# @app.route('/bla')
# def bla():
#     cur = mysql.connection.cursor()
#     cur.execute('''SELECT * FROM users''')
#     rv = cur.fetchall()
#     return str(rv)

# @app.route('/<user>')
# def hello_user(user):
#     return "Hello {}!".format(user)
#
# @app.route('/len/<word>')
# def len_count(word):
#     return 'word len = {}#'.format(str(len(word)))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

app.run()

# print('hello!')
