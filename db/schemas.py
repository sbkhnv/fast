import os

from pydantic import BaseModel
from typing import Optional


class RegisterUser(BaseModel):
    id: Optional[int]
    first_name: str
    last_name: str
    username: str
    password: str
    email: str
    address_id: Optional[int]


class LoginUser(BaseModel):
    username: str
    password: str


class CityModel(BaseModel):
    id: Optional[int]
    name: str


class AddressModel(BaseModel):
    id: Optional[int]
    city_id: Optional[int]
    name: str


class LessonModel(BaseModel):
    id: Optional[int]
    title: str
    description: str
    homework: str


class ModuleModel(BaseModel):
    id: Optional[int]
    name: str
    description: str
    lesson_id: Optional[int]


class CourseModel(BaseModel):
    id: Optional[int]
    name: str
    description: str
    module_id: Optional[int]
    price: Optional[int]


class PayTypeModel(BaseModel):
    id: Optional[int]
    type: str


class PayModel(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    amount: Optional[float]
    course_id: Optional[int]
    type: Optional[int]


class JwtModel(BaseModel):
    authjwt_secret_key: str = '192ba1860ccd8dcb1577983848289f3792e3c896fd7df9277a773d39d2c9e291'
