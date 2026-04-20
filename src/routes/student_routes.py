from fastapi import APIRouter


student_router = APIRouter(
    prefix="/student",
    tags=["student"]
)

@student_router.get("/all")
async def get_student():
    return {
        "message": "List of all students",
        "students": [
            {
                "id": 1, 
                "name": "John Doe", 
                "age": 20, 
                "coach_id": 1,
                "plan": "Basic Plan",
                "role": "student"
            },
            {
                "id": 2, 
                "name": "Jane Smith", 
                "age": 22, 
                "coach_id": 2,
                "plan": "Premium Plan",
                "role": "student"
            },
            {
                "id": 3, 
                "name": "Alice Johnson", 
                "age": 19, 
                "coach_id": 1,
                "plan": "Basic Plan",
                "role": "student"
            }
            
        ]
    }


@student_router.get("/{student_id}")
async def get_by_id(student_id: int):
    return {"message": f"Details of student with ID {student_id}"}


@student_router.post("/create")
async def create_student(student: dict):
    return {"message": "Student created", "student": student}


@student_router.post("/register")
async def register_student(student: dict):
    return {"message": "Student registered", "student": student}


@student_router.put("/update/{student_id}")
async def update_student(student_id: int, student: dict):
    return {"message": f"Student with ID {student_id} updated", "student": student}


@student_router.delete("/delete/{student_id}")
async def delete_student(student_id: int):
    return {"message": f"Student with ID {student_id} deleted"}



@student_router.get("/all-students-by-coach/{coach_id}")
async def get_by_coach(coach_id: int):
    return {"message": f"all student by coach {coach_id}"}
