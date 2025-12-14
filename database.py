# database.py
import json
import mysql.connector
from mysql.connector import Error

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def get_connection():
    cfg = load_config()
    try:
        conn = mysql.connector.connect(
            host=cfg.get("host","localhost"),
            user=cfg.get("user","root"),
            password=cfg.get("password","suhas0041R"),
            database=cfg.get("database","network_scanner"),
            port=cfg.get("port",3306)
        )
        return conn
    except Error as e:
        print("Database Connection Error:", e)
        return None

def init_db():
    conn = get_connection()
    if conn:
        print("MySQL Database connected successfully.")
        conn.close()
    else:
        print("Failed to connect to MySQL. Check config.json and MySQL server.")

def save_scan(target, ports, result, timestamp):
    conn = get_connection()
    if not conn:
        print("Cannot save scan — no DB connection.")
        return False
    try:
        cursor = conn.cursor()
        query = "INSERT INTO scan_results (target, ports, result, timestamp) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (target, ports, ",".join(map(str, result)), timestamp))
        conn.commit()
        cursor.close()
        conn.close()
        print("Scan saved in MySQL DB.")
        return True
    except Exception as e:
        print("Error saving scan:", e)
        return False
