import os
import sys
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app, students

client = TestClient(app)

def test_get_students_all():
    response = client.get("/students")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["code"] == "SV001"
    assert data[1]["code"] == "SV002"
    assert data[2]["code"] == "SV003"

def test_get_students_filters():
    response = client.get("/students?keyword=nguyen")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["code"] == "SV001"

    response = client.get("/students?keyword=SV002")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["code"] == "SV002"

    response = client.get("/students?keyword=c@gmail.com")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["code"] == "SV003"

    response = client.get("/students?min_age=20")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    response = client.get("/students?max_age=20")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    response = client.get("/students?keyword=gmail&min_age=18&max_age=22")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

def test_get_student_detail():
    response = client.get("/students/1")
    assert response.status_code == 200
    assert response.json()["code"] == "SV001"

    response = client.get("/students/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

def test_create_student_success():
    initial_len = len(students)
    payload = {
        "code": "SV004",
        "name": "Pham Van D",
        "email": "d@gmail.com",
        "age": 21
    }
    response = client.post("/students", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 4
    assert data["code"] == "SV004"
    assert len(students) == initial_len + 1
    students.pop()

def test_create_student_validation():
    payload = {
        "code": "SV001",
        "name": "Nguyen Dupe",
        "email": "dupe@gmail.com",
        "age": 20
    }
    response = client.post("/students", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Mã học viên đã tồn tại"

    payload = {
        "code": "SV004",
        "name": "   ",
        "email": "d@gmail.com",
        "age": 21
    }
    response = client.post("/students", json=payload)
    assert response.status_code == 422

    payload = {
        "code": "SV004",
        "name": "Pham Van D",
        "email": "",
        "age": 21
    }
    response = client.post("/students", json=payload)
    assert response.status_code == 422

    payload = {
        "code": "SV004",
        "name": "Pham Van D",
        "email": "d@gmail.com",
        "age": 0
    }
    response = client.post("/students", json=payload)
    assert response.status_code == 422

def test_update_student():
    payload = {
        "code": "SV003_NEW",
        "name": "Le Van C Updated",
        "email": "c_new@gmail.com",
        "age": 19
    }
    response = client.put("/students/3", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "SV003_NEW"
    assert data["name"] == "Le Van C Updated"

    payload = {
        "code": "SV003_NEW",
        "name": "Le Van C Updated 2",
        "email": "c_new@gmail.com",
        "age": 19
    }
    response = client.put("/students/3", json=payload)
    assert response.status_code == 200

    payload = {
        "code": "SV001",
        "name": "Le Van C Dupe",
        "email": "c_new@gmail.com",
        "age": 19
    }
    response = client.put("/students/3", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Mã học viên đã tồn tại"

    response = client.put("/students/999", json=payload)
    assert response.status_code == 404

def test_delete_student():
    initial_len = len(students)
    response = client.delete("/students/2")
    assert response.status_code == 200
    assert response.json()["message"] == "Xóa học viên thành công"
    assert len(students) == initial_len - 1

    response = client.delete("/students/999")
    assert response.status_code == 404

def run_tests():
    try:
        test_get_students_all()
        test_get_students_filters()
        test_get_student_detail()
        test_create_student_success()
        test_create_student_validation()
        test_update_student()
        test_delete_student()
        print("Success")
    except AssertionError as e:
        sys.exit(1)
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
