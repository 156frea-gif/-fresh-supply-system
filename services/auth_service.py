from sqlalchemy.orm import Session
from models.user import UserModel
from schemas.user_schema import UserCreate, UserLogin
from fastapi import HTTPException, status

class AuthService:
    @staticmethod
    def register_user(db: Session, user_data: UserCreate):
        existing = db.query(UserModel).filter(UserModel.username == user_data.username).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="اسم المستخدم مسجل مسبقاً."
            )
        if user_data.role not in ["admin", "manager", "worker"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="الصلاحية غير صالحة. الصلاحيات المتاحة: admin, manager, worker"
            )
        new_user = UserModel(
            username=user_data.username,
            password=user_data.password,
            role=user_data.role
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def login_user(db: Session, login_data: UserLogin):
        user = db.query(UserModel).filter(UserModel.username == login_data.username).first()
        if not user or user.password != login_data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="اسم المستخدم أو كلمة المرور غير صحيحة."
            )
        return {"message": "تم تسجيل الدخول بنجاح", "username": user.username, "role": user.role}
