# File: main.py
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Path, Query
from sqlalchemy.orm import Session
import os
import models, schemas, crud
from database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware

# ----- Cloudinary Import -----
from cloudinary_config import cloudinary
import cloudinary.uploader

# Initialize app
app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=engine)

# Allow Flutter frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # ⚠️ In production, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload directory (fallback)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------- Helper Function --------------------
def upload_image_to_cloudinary(file) -> str:
    """
    Upload image to Cloudinary and return secure URL
    """
    result = cloudinary.uploader.upload(file, folder="billboard_reports/")
    return result["secure_url"]

# -------------------- USER AUTH --------------------
@app.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user.username)
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful!", "user_id": db_user.id}

# -------------------- REPORTS --------------------
# POST: Create report (with Cloudinary image upload)
@app.post("/reports", response_model=schemas.ReportResponse)
async def create_report(
    location: str = Form(...),
    landmark: str = Form(None),
    size: str = Form(None),
    content_type: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Upload image
    image_url = upload_image_to_cloudinary(image.file)

    # Prepare report (user_id is optional / None)
    report_data = schemas.ReportCreate(
        location=location,
        landmark=landmark,
        size=size,
        content_type=content_type,
        description=description,
        user_id=None
    )

    return crud.create_report(db=db, report=report_data, image_path=image_url)

# GET: Fetch all reports (Admin view)
@app.get("/reports", response_model=list[schemas.ReportResponse])
def get_reports(db: Session = Depends(get_db)):
    return crud.get_reports(db)

# GET: Fetch reports for a specific user (still optional)
@app.get("/reports/user/{username}", response_model=list[schemas.ReportResponse])
def get_reports_by_username(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_reports_by_user(db, db_user.id)

# -------------------- UPDATE REPORT STATUS --------------------
@app.put("/reports/{report_id}", response_model=schemas.ReportResponse)
def update_report_status(
    report_id: int = Path(..., description="ID of the report to update"),
    status_update: dict = None,
    db: Session = Depends(get_db),
):
    if status_update is None or "status" not in status_update:
        raise HTTPException(status_code=400, detail="Status is required")

    report = crud.get_report_by_id(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    new_status = status_update["status"].lower()
    if new_status not in ["approved", "rejected", "pending"]:
        raise HTTPException(
            status_code=400, detail="Status must be approved, rejected, or pending"
        )

    return crud.update_report_status(db=db, report=report, status=new_status)
# ----------------------------------------------for the fetching the reprort stats--------

@app.get("/reports/status")
def get_reports_by_status(
    status: str = Query(..., description="Status filter: approved, rejected, pending"),
    db: Session = Depends(get_db)
):
    status = status.lower()
    if status not in ["approved", "rejected", "pending"]:
        raise HTTPException(status_code=400, detail="Invalid status. Choose approved, rejected, or pending.")
    return db.query(models.Report).filter(models.Report.status == status).all()


# --------------------change in password----------------------

@app.post("/change-password")
def change_password(request: schemas.ChangePassword, db: Session = Depends(get_db)):
    """
    Change password for a user
    """
    db_user = crud.get_user(db, request.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found ❌")
    
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match ❌")
    
    updated_user = crud.update_password(db, request.username, request.new_password)
    if updated_user:
        return {"message": "Password updated successfully ✅"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update password ❌")