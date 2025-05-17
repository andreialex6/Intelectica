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
        elif role == "profesor":
            cursor.execute("INSERT INTO Profesori (Id, Username, Nume, Prenume) VALUES (?, ?, '', '')", (user_id, username))
        elif role == "admin":
            cursor.execute("INSERT INTO Admins (Id, Username) VALUES (?, ?)", (user_id, username))
        else:
            return jsonify({"status": "error", "message": "Rol necunoscut"}), 400


        conn.commit()
        return jsonify({"status": "error", "message": "Account created successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Registration failed: {str(e)}"}), 500
    
@app.route("/get_profesori", methods=["GET"])
def get_profesori():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Username, Nume, Prenume FROM Profesori")
        profesori = [
            {
                "id": row.Id,
                "username": row.Username,
                "nume_complet": f"{row.Nume} {row.Prenume}"
            }
            for row in cursor.fetchall()
        ]
        return jsonify(profesori), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Nu s-au putut prelua profesorii: {str(e)}"}), 500
    finally:
        conn.close()


@app.route("/create_clasa", methods=["POST"])
def create_clasa():
    data = request.json
    nume_clasa = data.get("nume_clasa")
    profesor_id = data.get("profesor_id")

    if not all([nume_clasa, profesor_id]):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Creare clasa
        cursor.execute("INSERT INTO Clase (Nume) VALUES (?)", (nume_clasa,))
        cursor.execute("SELECT Id FROM Clase WHERE Nume = ?", (nume_clasa,))
        row = cursor.fetchone()
        if row is None:
            return jsonify({"status": "error", "message": "Failed to retrieve class ID"}), 500

        clasa_id = int(row[0])

        # Asociere profesor - clasa
        cursor.execute("INSERT INTO Profesor_Clase (ProfesorId, ClasaId) VALUES (?, ?)", (profesor_id, clasa_id))

        conn.commit()
        return jsonify({"status": "success", "message": "Clasa creata cu succes"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Eroare la creare clasa: {str(e)}"}), 500

    finally:
        conn.close()

@app.route("/get_elevi", methods=["GET"])
def get_elevi():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Nume, Prenume FROM Elevi")
        elevi = [{"id": row.Id, "nume_complet": f"{row.Nume} {row.Prenume}"} for row in cursor.fetchall()]
        return jsonify(elevi), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Eroare la preluarea elevilor: {str(e)}"}), 500
    finally:
        conn.close()

@app.route("/get_clase", methods=["GET"])
def get_clase():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Nume FROM Clase")
        clase = [{"id": row.Id, "nume": row.Nume} for row in cursor.fetchall()]
        return jsonify(clase), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Eroare la preluarea claselor: {str(e)}"}), 500
    finally:
        conn.close()

@app.route("/add_student_to_class", methods=["POST"])
def add_student_to_class():
    data = request.json
    elev_id = data.get("elev_id")
    clasa_id = data.get("clasa_id")

    if not elev_id or not clasa_id:
        return jsonify({"status": "error", "message": "Date lipsă"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Elev_Clase (ElevId, ClasaId) VALUES (?, ?)", (elev_id, clasa_id))
        conn.commit()
        return jsonify({"status": "success", "message": "Elev adăugat cu succes"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Eroare la adăugare: {str(e)}"}), 500
    finally:
        conn.close()



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
