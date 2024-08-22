from fastapi import HTTPException, status
from functools import wraps
from database import get_db
from sqlalchemy.orm import Session
from models import User
import logging
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

SECRET_KEY = "secret_key"
ALGORITHM = "HS256"

logger = logging.getLogger(__name__)

security = HTTPBearer()


def validate_user_token(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        logger.info("Authenticating the user token")
        # Not fully implemented
        credentials: HTTPAuthorizationCredentials = kwargs.get("credentials")
        token = credentials.credentials
        print(token)
        # db: Session = next(get_db())
        #
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is missing",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # try:
        #     token = token.split(" ")[1]  # Extract the token part after "Bearer"
        #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #     username = payload.get("sub")
        #     if username is None:
        #         raise HTTPException(
        #             status_code=status.HTTP_401_UNAUTHORIZED,
        #             detail="Invalid token",
        #             headers={"WWW-Authenticate": "Bearer"},
        #         )
        #     current_user = db.query(User).filter(User.username == username).first()
        #     if current_user is None:
        #         raise HTTPException(
        #             status_code=status.HTTP_401_UNAUTHORIZED,
        #             detail="User not found",
        #             headers={"WWW-Authenticate": "Bearer"},
        #         )
        #     kwargs["current_user"] = current_user  # Inject the user into the route
        # except JWTError:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Token is invalid",
        #         headers={"WWW-Authenticate": "Bearer"},
        #     )

        kwargs["current_user"] = 1  # Inject the user into the route
        logger.info("Authentication successful")
        return await f(*args, **kwargs)

    return decorated_function
