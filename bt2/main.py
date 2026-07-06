from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, field_validator
from typing import List, Optional

app = FastAPI()

class Student(BaseModel):
    id: int
    code: str
    name: str
    email: str
    age: int

class StudentCreate(BaseModel):
    code: str
    name: str
    email: str
    age: int

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Tên không được rỗng')
        return v.strip()

    @field_validator('code')
    @classmethod
    def validate_code(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Mã không được rỗng')
        return v.strip()

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Email không được rỗng')
        return v.strip()

    @field_validator('age')
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('Tuổi phải lớn hơn 0')
        return v

class StudentUpdate(BaseModel):
    code: str
    name: str
    email: str
    age: int

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Tên không được rỗng')
        return v.strip()

    @field_validator('code')
    @classmethod
    def validate_code(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Mã không được rỗng')
        return v.strip()

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Email không được rỗng')
        return v.strip()

    @field_validator('age')
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('Tuổi phải lớn hơn 0')
        return v

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]

def find_student_by_id(student_id: int):
    for s in students:
        if s["id"] == student_id:
            return s
    return None

@app.get("/students", response_model=List[Student])
def get_students(
    keyword: Optional[str] = Query(None),
    min_age: Optional[int] = Query(None),
    max_age: Optional[int] = Query(None)
):
    filtered_students = students
    if keyword:
        keyword_lower = keyword.lower()
        filtered_students = [
            s for s in filtered_students
            if keyword_lower in s["name"].lower()
            or keyword_lower in s["code"].lower()
            or keyword_lower in s["email"].lower()
        ]
    if min_age is not None:
        filtered_students = [s for s in filtered_students if s["age"] >= min_age]
    if max_age is not None:
        filtered_students = [s for s in filtered_students if s["age"] <= max_age]
    return filtered_students

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    student = find_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student_in: StudentCreate):
    if any(s["code"].lower() == student_in.code.lower() for s in students):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã học viên đã tồn tại"
        )
    
    new_id = max([s["id"] for s in students]) + 1 if students else 1
    new_student = {
        "id": new_id,
        "code": student_in.code,
        "name": student_in.name,
        "email": student_in.email,
        "age": student_in.age
    }
    students.append(new_student)
    return new_student

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student_in: StudentUpdate):
    student = find_student_by_id(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    if any(s["code"].lower() == student_in.code.lower() and s["id"] != student_id for s in students):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã học viên đã tồn tại"
        )
    
    student["code"] = student_in.code
    student["name"] = student_in.name
    student["email"] = student_in.email
    student["age"] = student_in.age
    return student

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    student = find_student_by_id(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    students.remove(student)
    return {"message": "Xóa học viên thành công"}
