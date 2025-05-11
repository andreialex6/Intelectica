from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# ADO.NET converted for pyodbc
connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=tcp:intelectica-ip.database.windows.net,1433;"
    "Database=ip_database;"
    "Uid=admin_ip;"
    "Pwd=Intelectica1!;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

def get_connection():
    return pyodbc.connect(connection_string)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?", (username, password))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({"status": "success", "message": "Login successful", "username": row.Username, "permissions": row.Permissions_Tier}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirm = data.get("confirm")
    role = data.get("role")

    if not all([username, email, password, confirm, role]):
        return jsonify({"status": "error", "message": "Missing fields"}), 400
    if password != confirm:
        return jsonify({"status": "error", "message": "Passwords do not match"}), 400

    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM Users WHERE Username = ?", username)
        if cursor.fetchone()[0] > 0:
            return jsonify({"status": "error", "message": "Username already exists"}), 400

        if role == "profesor":
            tier = 2
        elif role == "elev":
            tier = 3
        elif role == "parinte":
            tier = 4

        cursor.execute("""
            INSERT INTO Users (Username, Email, Password, Permissions_Tier)
            VALUES (?, ?, ?, ?)
        """, (username, email, password, tier))

        cursor.execute("SELECT Id FROM Users WHERE Username = ?", (username,))
        row = cursor.fetchone()
        if row is None:
            return jsonify({"status": "error", "message": "Failed to retrieve user ID"}), 500

        user_id = int(row[0])

        if role == "elev":
            cursor.execute("INSERT INTO Elevi (Id, Username, Nume, Prenume) VALUES (?, ?, '', '')", (user_id, username))
        elif role == "parinte":
            cursor.execute("INSERT INTO Parinti (Id, Username, Nume, Prenume, CopilId) VALUES (?, ?, '', '', NULL)", (user_id, username))
        else:
            return jsonify({"status": "error", "message": "Invalid role"}), 400

        conn.commit()
        return jsonify({"status": "error", "message": "Account created successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Registration failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

# Connect and query
# try:
#     conn = pyodbc.connect(connection_string)
#     cursor = conn.cursor()

#     cursor.execute("SELECT Id, Username, Email, Permissions_Tier FROM Users")
#     for row in cursor.fetchall():
#         print(row)

#     conn.close()
# except Exception as e:
#     print("Connection failed:", e)
