from fastapi import APIRouter
from ..models.entities.coach_entity import CoachRegister


coach_router = APIRouter(
    prefix="/coach",
    tags=["coach"]
)



@coach_router.get("/all")
async def get_all():
    return {
        "message": "List of coach",
        "coaches": [
            {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "1234567890"
            },
            
            {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "phone": "0987654321"
            },
            
        ]
    }

@coach_router.put("/update/{coach_id}")
async def update(coach_id: int, coach: dict):
    return {"message": f"Coach with ID {coach_id} updated", "Coach": coach}

@coach_router.post("/register")
async def register(coach: CoachRegister):
    return {"message": "Coach registered successfully", "coach": coach}


@coach_router.delete("/delete/{coach_id}")
async def delete(coach_id: int):
    return {"message": f"Coach with ID {coach_id} deleted"}