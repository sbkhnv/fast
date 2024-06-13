from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import status, Depends
from db.database import Session, ENGINE
from db.models import User, Address
from db.schemas import RegisterUser
from werkzeug import security
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

ax_router = APIRouter(prefix='/users_api')
session = Session(bind=ENGINE)


@ax_router.get('/')
async def user_list(Authentiztion: AuthJWT=Depends()):

    try:
        Authentiztion.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:

        users = session.query(User).all()
        context = [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "username": user.username,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser,
                "address": {
                    "id": user.adr.id,
                    "name": user.adr.name,
                    "city": {
                        "id": user.adr.cities.id,
                        "name": user.adr.cities.name
                    }
                }
            }
            for user in users
        ]
        return jsonable_encoder(context)

    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="only admin has permission")


@ax_router.get('/{id}')
async def user_one(id:int, Authentiztion: AuthJWT=Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        user = session.query(User).filter(User.id == id).first()

        context_1 = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "username": user.username,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser,
                "address": {
                    "id": user.adr.id,
                    "name": user.adr.name,
                    "city": {
                        "id": user.adr.cities.id,
                        "name": user.adr.cities.name
                    }
                }
            }

        return jsonable_encoder(context_1)

    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='only admin has permission')


@ax_router.post('/create')
async def create(user: RegisterUser, Authentiztion: AuthJWT=Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        username = session.query(User).filter(User.username == user.username).first()
        if username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bunday foydalanuvchi mavjud boshqa yarating')

        email = session.query(User).filter(User.email == user.email).first()
        if email or username is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bunday foydalanuvchi royxatdan otgan')

        new_user = User(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
            password=security.generate_password_hash(user.password),
            address_id=user.address_id
        )

        session.add(new_user)
        session.commit()
        user_x = new_user
        context_2 = [
            {
                "id": user_x.id,
                "first_name": user_x.first_name,
                "last_name": user_x.last_name,
                "email": user_x.email,
                "username": user_x.username,
                "is_active": user_x.is_active,
                "is_superuser": user_x.is_superuser,
                "address": {
                    "id": user_x.adr.id,
                    "name": user_x.adr.name,
                    "city": {
                        "id": user_x.adr.cities.id,
                        "name": user_x.adr.cities.name
                    }
                } if user_x.adr else None
            }
        ]
        raise HTTPException(status_code=status.HTTP_201_CREATED, detail=context_2)

    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="only admin has permission")


@ax_router.put('/{id}')
async def update(id: int, user: RegisterUser, Authentiztion: AuthJWT=Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        adr = session.query(Address).filter(Address.id == user.address_id).first()
        user_check = session.query(User).filter(User.id == id).first()
        id_check = session.query(User).filter(User.id == user.id).first()
        if user_check:
            if adr:
                if id_check is None or id == user.id:
                    for key, value in user.dict().items():
                        setattr(user_check, key, value)
                        session.commit()
                    user_x = user_check
                    data = {
                          "id": user_x.id,
                          "first_name": user_x.first_name,
                          "last_name": user_x.last_name,
                          "email": user_x.email,
                          "username": user_x.username,
                          "is_active": user_x.is_active,
                          "is_superuser": user_x.is_superuser,
                          "address": {
                            "id": user_x.adr.id,
                            "name": user_x.adr.name,
                            "city": {
                                "id": user_x.adr.cities.id,
                                "name": user_x.adr.cities.name
                            }
                          }
                    }
                    return jsonable_encoder(data)
                return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='berilgan id malumotga ega')
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Berilgan manzil id mavjud emas!')
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User topilmadi!')
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="only admin has permission")


@ax_router.delete('/{id}')
async def delete(id: int, Authentiztion: AuthJWT=Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        x = session.query(User).filter(User.id == id).first()
        if x:
            session.delete(x)
            session.commit()

            return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='deleted')

        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='only admin has permission')
