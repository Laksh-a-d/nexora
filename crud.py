from sqlalchemy.orm import Session
import models, schemas
from cloudinary_config import cloudinary  # make sure this file exists
import cloudinary.uploader

# ---------- Users ----------
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_users(db: Session):
    return db.query(models.User).all()



# ----------------------change passwword-------------------------


# ---------- Reports ----------
def create_report(db: Session, report: schemas.ReportCreate, image_path: str):
    db_report = models.Report(
        location=report.location,
        landmark=report.landmark,
        size=report.size,
        content_type=report.content_type,
        description=report.description,
        image_path=image_path,
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def get_reports(db: Session):
    return db.query(models.Report).all()

def update_report_status(db: Session, report_id: int, status: bool):
    db_report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if db_report:
        db_report.status = status
        db.commit()
        db.refresh(db_report)
    return db_report

def upload_image_to_cloudinary(file) -> str:
    result = cloudinary.uploader.upload(file, folder="billboard_reports/")
    return result["secure_url"]


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_report(db: Session, report: schemas.ReportCreate, image_path: str, user_id: int = None):
    db_report = models.Report(
        location=report.location,
        landmark=report.landmark,
        size=report.size,
        content_type=report.content_type,
        description=report.description,
        image_path=image_path,
        status="pending",   # ✅ Always start as pending
        user_id=user_id
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def get_reports(db: Session):
    return db.query(models.Report).all()

def get_report_by_id(db: Session, report_id: int):
    return db.query(models.Report).filter(models.Report.id == report_id).first()

def update_report_status(db: Session, report: models.Report, status: str):
    report.status = status
    db.commit()
    db.refresh(report)
    return report

def get_reports_by_user(db: Session, user_id: int):
    return db.query(models.Report).filter(models.Report.user_id == user_id).all()

def update_password(db: Session, username: str, new_password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        user.password = new_password
        db.commit()
        db.refresh(user)
        return user
    return None


def create_report(db: Session, report: schemas.ReportCreate, image_path: str, user_id: int = None):
    db_report = models.Report(
        location=report.location,
        landmark=report.landmark,
        size=report.size,
        content_type=report.content_type,
        description=report.description,
        image_path=image_path,
        status="pending",
        user_id=user_id
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report