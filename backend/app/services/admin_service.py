from typing import Dict, Any
from fastapi import HTTPException, status
from ..repositories.admin_repository import AdminRepository


class AdminService:
    def __init__(self, db: Any):
        # db is expected to be a cursor (DictCursor)
        self.db = db
        self.admin_repo = AdminRepository()

    def verify_admin(self, password: str) -> Dict:
        """관리자 비밀번호 확인 (토큰 발급 없음)."""
        if not self.admin_repo.verify_password(self.db, password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="비밀번호가 일치하지 않습니다."
            )

        return {
            "status": "success",
            "message": "인증 성공"
        }

    def change_password(self, current_password: str, new_password: str) -> Dict:
        admin = self.admin_repo.get_admin(self.db)
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="관리자 계정이 존재하지 않습니다."
            )

        if not self.admin_repo.verify_password(self.db, current_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="현재 비밀번호가 일치하지 않습니다."
            )

        self.admin_repo.update_password(self.db, admin.get('id'), new_password)

        return {
            "status": "success",
            "message": "비밀번호가 변경되었습니다."
        }