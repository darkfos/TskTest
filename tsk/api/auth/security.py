import datetime

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta
from settings import settings
from typing import Annotated
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from api.exceptions.user_exception import *


class Security:

    oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/create_token")

    def __init__(self):
        self.__api_secret_key: str = settings.get_auth_key
        self.__api_secret_key_refresh: str = settings.get_refresh_key
        self.__algorithm_crypt: str = "HS256"

        #Cryptography
        self.bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

    def create_access_token(self, login: str, user_id: int, password: str, date_for_token_time: timedelta) -> dict:
        """
        Create access token
        :param login:
        :param user_id:
        :param date_for_token_time:
        :return:
        """

        encode = {"sub": login, "id": user_id, "password": password} #Data for token
        expires = datetime.datetime.utcnow() + date_for_token_time
        encode.update({"exp": expires}) #add time
        jwt_token = jwt.encode(encode, self.__api_secret_key, algorithm=self.__algorithm_crypt)

        #Refresh token
        encode_jwt_refresh = {"sub": login, "id": user_id, "password": password}
        encode_jwt_refresh.update({"exp": (datetime.datetime.utcnow() + timedelta(days=100))})
        jwt_refresh_token = jwt.encode(encode_jwt_refresh, key=self.__api_secret_key_refresh, algorithm=self.__algorithm_crypt)
        return ({"jwt_token": jwt_token, "token_type": "Bearer"}, jwt_refresh_token)

    def decode_jwt_token(self, token: Annotated[str, Depends(oauth2_bearer)], type_key: bool = False):
        """
        Decode jwt_token
        :param token:
        :return:
        """

        try:

            key = self.__api_secret_key
            if type_key == True:
                key = self.__api_secret_key_refresh

            #Decode token
            actual_data = jwt.decode(token=token, key=key, algorithms=self.__algorithm_crypt)
            user_login: str = actual_data.get("sub")
            user_id: int = actual_data.get("id")
            password: str = actual_data.get("password")

            #Check data
            if (user_login is None) or (user_id is None):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователь не был найден!"
                )
            else:
                return {"user_id": user_id, "login": user_login, "password": password}
        except JWTError as jwt_er:
            http_404_not_right_token(token="token")

    def get_new_token_by_refresh(self, refresh_token: str):
        """
        Get new acces token with help refresh token
        :param refresh_token:
        :return:
        """
        try:
            data = jwt.decode(token=refresh_token, key=self.__api_secret_key_refresh, algorithms=self.__algorithm_crypt)
            user_login: str = data.get("sub")
            password: str = data.get("password")
            user_id: int = data.get("id")

            if (user_login is None) or (password is None) or (user_id is None):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Не актуальные данные пользователя"
                )
            else:
                #Create new acces token
                encode = {"sub": user_login, "password": password, "id": user_id}
                encode.update({"exp": (datetime.datetime.utcnow() + timedelta(minutes=5))})
                access_token = jwt.encode(encode, key=self.__api_secret_key, algorithm=self.__algorithm_crypt)

                return access_token
        except JWTError as jwt_err:
            http_404_not_right_token(token="refresh_token")