from fastapi import status, HTTPException
from typing import Literal


async def http_404_not_found_user():
    """
    Raise exception - not found user
    """

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Не удалось найти пользователя"
    )


async def http_400_not_right_password_or_login():
    """
    Raise exception - not right password or login
    """

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Неправильный логин или пароль"
    )


async def http_400_error_create_user():
    """
    Raise exception - error with create a new user
    """

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Неудалось создать пользователя"
    )


def http_404_not_right_token(token: Literal["token", "refresh_token"]):
    """
    Raise exception - not right token
    """

    detail_message: str = "Не действительный токен"
    if token == "refresh_token":
        detail_message = "Не верный refresh токен"

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail_message
    )


async def http_406_error_update_user():
    """
    Raise exception - error update user
    """

    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Не удалось обновить информацию о пользователе"
    )


async def http_400_error_with_update_password_user():
    """
    Raise exception with update user password
    """ 

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Не удалось обновить пароль"
    )


async def http_400_error_delete_user():
    """
    Raise exception with delete user
    """

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Не удалось удалить пользователя"
    )