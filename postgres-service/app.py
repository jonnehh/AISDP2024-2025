from flask import Flask, request, jsonify
import psycopg2
from db import get_db_connection

app = Flask(__name__)


@app.route('/add_medicine', methods=['POST'])
def add_medicine():
    data = request.json
    medicine_name = data.get("medicine_name")  # 获取药品名称
    function = data.get("function")  # 获取药品用途
    dosage_time = data.get("dosage_time")  # 获取服药时间

    if not medicine_name or not function or not dosage_time:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # 插入数据到数据库
    cursor.execute("INSERT INTO medicines (name, info, dosage_time) VALUES (%s, %s, %s)", 
                   (medicine_name, function, dosage_time))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Medicine added successfully"}), 201


@app.route('/medicines', methods=['GET'])
def get_medicines():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, info,dosage_time FROM medicines")
    medicines = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify([{"name": name, "info": info, "dosage_time":dosage_time} for name, info, dosage_time in medicines])

@app.route('/delete_medicine/<string:medicine_name>', methods=['DELETE'])
def delete_medicine(medicine_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicines WHERE name = %s", (medicine_name,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"Deleted {medicine_name} successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6050)
