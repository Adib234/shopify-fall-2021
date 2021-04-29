from fastapi import APIRouter
router = APIRouter()


@router.get("/")
def read_root_route():
    return {"Hello": "Adib!"}
