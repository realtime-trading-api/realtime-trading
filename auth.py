"""
보안 및 인증 (Authentication Layer)
- 비밀번호 해싱 및 JWT 토큰 검증 처리
"""

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta  # 시간을 다루기 위해 추가
from database import get_db
import models
import os from dotenv import load_dotenv# .env 파일의 내용 불러오기

load_dotenv()# 이제 직접 문자열을 쓰지 않고 환경 변수에서 가져옵니다

# JWT 서명 설정
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"

# 비밀번호 암호화 컨텍스트 (argon2 알고리즘 사용)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# 토큰 추출을 위한 OAuth2 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 로그인 성공시 토큰 생성
def create_access_token(data: dict):
  
    to_encode = data.copy()
    # 토큰 만료 시간 설정: 현재 시간 + 15분
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    
    # 설정된 SECRET_KEY로 암호화하여 토큰 발행
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    """토큰 해독 후 현재 로그인한 유저 정보를 반환하는 의존성 함수"""
    try:
        # JWT 토큰 해독 및 유저네임(sub) 추출
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        # sub 없을 경우
        if username is None:
            raise HTTPException(status_code=401, detail="인증 정보가 유효하지 않습니다.")

        # DB에서 해당 유저 조회 (비동기 방식)
        query = select(models.User).where(models.User.username == username)
        result = await db.execute(query)
        user = result.scalars().first()

        # 유저가 존재하지 않을 경우 401 에러 발생
        if not user:
            raise HTTPException(status_code=401, detail="존재하지 않는 사용자입니다.")

        return user
        
    except JWTError:
        # 토큰 만료 또는 변조 시 401 에러 반환
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰")