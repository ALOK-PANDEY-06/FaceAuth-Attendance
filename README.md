# FaceAuth Attendance System

FaceAuth Attendance is a **Face Recognition Based Attendance System** that automatically detects faces and records attendance in real time.
This project is designed to reduce manual attendance and improve accuracy using computer vision.

## Features

* Face detection and recognition
* Automatic attendance marking
* CSV-based attendance storage
* Simple login system
* Web interface using Flask
* Duplicate attendance prevention

## Technologies Used

* Python
* OpenCV
* Face Recognition Library
* Flask
* HTML & CSS
* CSV (Database)

## How the System Works

1. The system scans faces using the webcam.
2. It matches the detected face with stored images.
3. If the face is recognized, attendance is automatically recorded.
4. The attendance is saved in the CSV file with date and time.

## Project Structure

FaceAuth-Attendance
│
├── app.py
├── templates
├── static
├── attendance.csv
├── images
└── README.md

## Installation & Setup

1. Clone the repository
2. Install required libraries

pip install -r requirements.txt

3. Run the project

python app.py

4. Open in browser

http://localhost:5000

## Future Improvements

* Database integration (MySQL / MongoDB)
* Admin dashboard
* Cloud deployment
* Multiple classroom support

## Author

Alok Pandey
B.Tech CSE Student
