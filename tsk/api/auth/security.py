import datetime

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta
from tsk.settings import settings
from typing import Annotated
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError


class Security:

    oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/create_token")

    def __init__(self):
        self.__api_secret_key: str = settings.get_auth_key
        self.__algorithm_crypt: str = "HS256"

        #Cryptography
        self.bcrypt_context = CryptContext(schemes=["bcrypt"], default='auto')

    def create_access_token(self, login: str, user_id: int, date_for_token_time: timedelta):
        """
        Create access token
        :param login:
        :param user_id:
        :param date_for_token_time:
        :return:
        """

        encode = {"sub": login, "id": user_id} #Data for token
        expires = datetime.datetime.utcnow() + date_for_token_time
        encode.update({"exp": expires}) #add time
        return jwt.encode(encode, self.__api_secret_key, algorithm=self.__algorithm_crypt)

    def decode_jwt_token(self, token: Annotated[str, Depends(oauth2_bearer)]):
        """
        Decode jwt_token
        :param token:
        :return:
        """

        try:
            #Decode token
            actual_data = jwt.decode(token=token, key=self.__api_secret_key, algorithms=self.__algorithm_crypt)
            user_login: str = actual_data.get("sub")
            user_id: int = actual_data.get("id")

            #Check data
            if (user_login is None) or (user_id is None):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователь не был найден!"
                )
            else:
                return {"user_id": user_id, "login": user_login}
        except JWTError as jwt_er:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Не удалось обработать ваш запрос"
            )