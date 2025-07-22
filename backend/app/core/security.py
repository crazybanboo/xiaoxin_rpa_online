from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings


class JWTHandler:
    """JWT工具类 - 处理token生成、验证和解析"""
    
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(
        self, 
        subject: Union[str, Any], 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        生成访问token
        
        Args:
            subject: 用户标识符（通常是用户名或用户ID）
            expires_delta: 过期时间增量，如果为None则使用默认值
            
        Returns:
            str: JWT token字符串
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.access_token_expire_minutes
            )
            
        to_encode = {
            "exp": expire,
            "sub": str(subject),
            "type": "access"
        }
        encoded_jwt = jwt.encode(
            to_encode, 
            self.secret_key, 
            algorithm=self.algorithm
        )
        return encoded_jwt

    def create_refresh_token(self, subject: Union[str, Any]) -> str:
        """
        生成刷新token（有效期更长）
        
        Args:
            subject: 用户标识符
            
        Returns:
            str: JWT refresh token字符串
        """
        expire = datetime.utcnow() + timedelta(days=7)  # 7天有效期
        to_encode = {
            "exp": expire,
            "sub": str(subject),
            "type": "refresh"
        }
        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[str]:
        """
        验证token并提取用户信息
        
        Args:
            token: JWT token字符串
            
        Returns:
            Optional[str]: 用户标识符，token无效则返回None
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            username: str = payload.get("sub")
            if username is None:
                return None
            return username
        except JWTError:
            return None
        except Exception:
            return None

    def decode_token(self, token: str) -> Optional[dict]:
        """
        解码token获取完整载荷信息
        
        Args:
            token: JWT token字符串
            
        Returns:
            Optional[dict]: token载荷字典，解码失败返回None
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except JWTError:
            return None
        except Exception:
            return None

    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """
        使用刷新token生成新的访问token
        
        Args:
            refresh_token: 刷新token
            
        Returns:
            Optional[str]: 新的访问token，刷新失败返回None
        """
        try:
            payload = self.decode_token(refresh_token)
            if not payload or payload.get("type") != "refresh":
                return None
                
            username = payload.get("sub")
            if not username:
                return None
                
            return self.create_access_token(subject=username)
        except Exception:
            return None

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """生成密码哈希值"""
        return self.pwd_context.hash(password)


jwt_handler = JWTHandler()