from fastapi import APIRouter

presence_router = APIRouter(
    prefix="/presence",
    tags=["presence"]
)

@presence_router.get("/all")
async def get_all_presences():
    return {
        "message": "List of all presences",
        "presences": [
            {
                "id": 1,
                "student_id": 1,
                "date": "2026-01-01",
                "status": "present"
            },
            {
                "id": 2,
                "student_id": 2,
                "date": "2026-01-02",
                "status": "absent"
            },
            
        ]
    }
    

@presence_router.get("/{presence_id}")
async def get_presence_by_id(presence_id: int):
    return {
        "message": f"Presence with ID {presence_id}",
        "presence": {
            "id": presence_id,
            "student_id": 1,
            "date": "2026-01-01",
            "status": "present"
        }
    }


@presence_router.post("/create")
async def create_presence(presence: dict):
    return {
        "message": "Presence created successfully",
        "presence": presence
    }


@presence_router.put("/update/{presence_id}")
async def update_presence(presence_id: int, presence: dict):
    return {
        "message": f"Presence with ID {presence_id} updated successfully",
        "presence": presence
    }


@presence_router.delete("/delete/{presence_id}")
async def delete_presence(presence_id: int):
    return {
        "message": f"Presence with ID {presence_id} deleted successfully"
    }