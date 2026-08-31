from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional

from backend.app.config import get_db
from backend.app.models.sql_models import UserSQL, RoleSQL, ProgramSQL
from backend.app.utils.auth_utils import hash_password, verify_password, create_access_token, get_current_user_payload
from backend.app.models.oop_models import Student, Admin

router = APIRouter(prefix="/auth", tags=["Authentication & Security"])

class RegisterSchema(BaseModel):
    full_name: str
    email: str
    password: str
    registration_number: str  # MANDATORY LPU Registration Number
    role_name: str = "STUDENT" # STUDENT or ADMIN
    program_id: Optional[int] = 1

class LoginSchema(BaseModel):
    email: str
    password: str
    registration_number: Optional[str] = None # Checked if provided

class OAuthLoginSchema(BaseModel):
    provider: str # google, apple, facebook
    email: str
    full_name: str
    registration_number: str # MANDATORY for LPU students

@router.post("/register")
def register_user(reg_in: RegisterSchema, db: Session = Depends(get_db)):
    if not reg_in.registration_number or not reg_in.registration_number.strip():
        raise HTTPException(status_code=400, detail="LPU Registration Number is strictly mandatory.")

    existing = db.query(UserSQL).filter(UserSQL.email == reg_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email address is already registered.")

    existing_reg = db.query(UserSQL).filter(UserSQL.registration_number == reg_in.registration_number.strip()).first()
    if existing_reg:
        raise HTTPException(status_code=400, detail="LPU Registration Number is already linked to another account.")

    role = db.query(RoleSQL).filter(RoleSQL.role_name == reg_in.role_name.upper()).first()
    if not role:
        role = RoleSQL(role_name=reg_in.role_name.upper())
        db.add(role)
        db.commit()
        db.refresh(role)

    pwd = hash_password(reg_in.password)
    user = UserSQL(
        full_name=reg_in.full_name,
        email=reg_in.email,
        hashed_password=pwd,
        role_id=role.role_id,
        program_id=reg_in.program_id,
        registration_number=reg_in.registration_number.strip()
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.email, "user_id": user.user_id, "role": role.role_name})
    prog_name = user.program.program_name if user.program else "B.Tech Computer Science & Engineering"
    oop_user = Student(user.user_id, user.full_name, user.email, user.registration_number, prog_name)

    return {
        "message": "Registration successful",
        "access_token": token,
        "token_type": "bearer",
        "user_profile": oop_user.to_dict()
    }

@router.post("/login")
def login_user(login_in: LoginSchema, db: Session = Depends(get_db)):
    if db.query(UserSQL).count() == 0:
        try:
            from database.seed_data import seed_database
            seed_database()
        except Exception as e:
            print(f"[Auth Login Seed Warning] {e}")

    email_clean = login_in.email.strip().lower() if login_in.email else ""
    user = db.query(UserSQL).filter(UserSQL.email == email_clean).first()
    if not user and login_in.email:
        # Fallback: check case-insensitive match
        user = db.query(UserSQL).filter(UserSQL.email.ilike(email_clean)).first()

    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email address or password.")

    if login_in.registration_number and login_in.registration_number.strip():
        if user.registration_number and user.registration_number != login_in.registration_number.strip():
            raise HTTPException(status_code=401, detail="Provided Registration Number does not match university record.")

    role_name = user.role.role_name if user.role else "STUDENT"
    token = create_access_token({"sub": user.email, "user_id": user.user_id, "role": role_name})

    if role_name == "STUDENT":
        prog_name = user.program.program_name if user.program else "B.Tech Computer Science & Engineering"
        oop_user = Student(user.user_id, user.full_name, user.email, user.registration_number or "12204891", prog_name)
    else:
        oop_user = Admin(user.user_id, user.full_name, user.email, "School of Computer Science")

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_profile": oop_user.to_dict()
    }

@router.post("/oauth")
def oauth_social_login(oauth_in: OAuthLoginSchema, db: Session = Depends(get_db)):
    if not oauth_in.registration_number or not oauth_in.registration_number.strip():
        raise HTTPException(status_code=400, detail=f"LPU Registration Number is strictly required for {oauth_in.provider.title()} sign-in.")

    user = db.query(UserSQL).filter(UserSQL.email == oauth_in.email).first()
    if not user:
        role = db.query(RoleSQL).filter(RoleSQL.role_name == "STUDENT").first()
        user = UserSQL(
            full_name=oauth_in.full_name,
            email=oauth_in.email,
            hashed_password=hash_password("oauth_secure_pass"),
            role_id=role.role_id if role else 1,
            program_id=1,
            registration_number=oauth_in.registration_number.strip()
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token({"sub": user.email, "user_id": user.user_id, "role": "STUDENT"})
    prog_name = user.program.program_name if user.program else "B.Tech Computer Science & Engineering"
    oop_user = Student(user.user_id, user.full_name, user.email, user.registration_number, prog_name)

    return {
        "message": f"Successfully authenticated via {oauth_in.provider.title()}",
        "access_token": token,
        "token_type": "bearer",
        "user_profile": oop_user.to_dict()
    }

@router.get("/me")
def get_me(payload: dict = Depends(get_current_user_payload), db: Session = Depends(get_db)):
    user = db.query(UserSQL).filter(UserSQL.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": user.user_id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role.role_name if user.role else "STUDENT",
        "program": user.program.program_name if user.program else None,
        "registration_number": user.registration_number
    }
