from flask import Flask, render_template, request
import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import csv

app = Flask(__name__)

# ---------------- LOGIN CREDENTIALS ----------------
USERNAME = "admin"
PASSWORD = "1234"

# ---------------- LOGIN PAGE ----------------
@app.route('/')
def home():
    return render_template("login.html")

# ---------------- LOGIN CHECK ----------------
@app.route('/login', methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == USERNAME and password == PASSWORD:
        return render_template("dashboard.html")
    return "Invalid Login"

# ---------------- DASHBOARD ROUTE ----------------
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

# ---------------- FACE RECOGNITION SETUP ----------------
path = "images"
images = []
classNames = []

# Load images and names
if os.path.exists(path):
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv2.imread(f"{path}/{cl}")
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
else:
    print(f"Folder '{path}' does not exist!")

# Encode all faces
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if encodes:
            encodeList.append(encodes[0])
    return encodeList

encodeListKnown = findEncodings(images)

# ---------------- MARK ATTENDANCE ----------------
def markAttendance(name):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    attendance_folder = os.path.join(BASE_DIR, "attendance")
    os.makedirs(attendance_folder, exist_ok=True)
    file_path = os.path.join(attendance_folder, "attendance.csv")

    now = datetime.now()
    time = now.strftime("%H:%M:%S")

    # Always append to CSV
    with open(file_path, "a") as f:
        f.write(f"{name},{time}\n")

# ---------------- CAMERA / FACE RECOGNITION ----------------
@app.route('/camera')
def camera():
    cap = cv2.VideoCapture(0)
    recognized_name = None
    error_message = None

    while True:
        success, img = cap.read()
        if not success:
            continue

        small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        faces = face_recognition.face_locations(small)
        encodes = face_recognition.face_encodings(small, faces)

        for encodeFace, faceLoc in zip(encodes, faces):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            if len(faceDis) == 0:
                continue

            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                recognized_name = classNames[matchIndex].upper()
                markAttendance(recognized_name)
                break
            else:
                error_message = "Record not found for this face!"
                break

        if recognized_name or error_message:
            break

        cv2.imshow("Camera", img)
        if cv2.waitKey(1) == 27:  # ESC to quit
            error_message = "Camera closed by user!"
            break

    cap.release()
    cv2.destroyAllWindows()

    return render_template("attendance.html", name=recognized_name, error=error_message)

# ---------------- VIEW ATTENDANCE RECORDS ----------------
@app.route('/attendance_records')
def attendance_records():
    records = []
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "attendance", "attendance.csv")

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    records.append({"name": row[0], "time": row[1]})
    else:
        return "No attendance records found yet."

    return render_template("attendance_records.html", records=records)

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run()