from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List

from schemas import ApplicationResponse
from auth import validate_user_token, security
from database import get_db
from models import Grant, Application, Document, User
import logging
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/grants", tags=["grants"])
logger = logging.getLogger(__name__)


@router.post("/{grant_id}/apply", response_model=ApplicationResponse)
@validate_user_token
async def apply_for_grant(
    grant_id: int,
    current_user: int = None,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security),  # used to show auth header in the API docs
):
    # Validate grant existence
    grant = db.query(Grant).filter(Grant.id == grant_id).first()
    if not grant:
        raise HTTPException(status_code=404, detail="Grant not found")
    logger.info("Grant found in the DB")

    # Create a new application
    try:
        application = Application(
            user_id=current_user, grant_id=grant_id, status="submitted"
        )
        db.add(application)
        db.commit()
        db.refresh(application)
        logger.info(
            f"Application submitted successfully by user {current_user} for grant {grant_id}"
        )
    except IntegrityError as e:
        logger.error(
            f"Failed to submit application due to a unique constraint: {str(e)}"
        )
        raise HTTPException(
            status_code=400, detail="You have already applied for this grant."
        )
    except Exception as e:
        logger.error(f"Failed to submit application: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to submit application")

    # Handle file uploads to S3
    document_paths = []
    for file in files:
        if file.content_type not in ["application/pdf", "application/msword"]:
            raise HTTPException(status_code=400, detail="Invalid file type")

        # Generate a unique file name for S3 (you could use UUID, timestamp, etc.)
        object_name = f"{grant_id}/{current_user}/{file.filename}"
        # Not implemented
        # s3_file_url = upload_file_to_s3(file.file, S3_BUCKET_NAME, object_name)
        s3_file_url = "s3_url"

        document = Document(application_id=application.id, document_url=s3_file_url)
        db.add(document)
        document_paths.append(s3_file_url)

    db.commit()
    logger.info(f"Documents uploaded successfully for application ID {application.id}")
    return {"message": "Application submitted successfully"}


def upload_file_to_s3(file, bucket_name, object_name) -> str:
    # not implemented
    pass


@router.post("/add")
async def create_dummy_data(db: Session = Depends(get_db)):
    user = User(
        id=1,
        username="Test",
        email="test@test.com",
        hashed_password="test",
        role="User",
    )
    grant = Grant(id=1, title="New1", description="Test", category="Test", created_by=1)
    db.add(user)
    db.add(grant)
    db.commit()
    return "data created"
