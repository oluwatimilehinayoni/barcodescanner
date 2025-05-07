from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # This enables requests from external frontends

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="posdb"
)

@app.route('/scan', methods=['POST'])
def scan_product():
    data = request.json
    barcode = data.get('barcode')

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT name, price, stock FROM products WHERE barcode = %s", (barcode,))
    product = cursor.fetchone()
    cursor.close()

    if product:
        return jsonify(product)
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
