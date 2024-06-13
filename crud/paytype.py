from fastapi import APIRouter
from db.database import Session, ENGINE
from db.schemas import PayTypeModel
from db.models import PayType, User
from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT


session = Session(bind=ENGINE)
pyt_router = APIRouter(prefix="/pyt")


@pyt_router.get('/')
async def get_all_pay_types(Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        pyt_list = session.query(PayType).all()
        return jsonable_encoder(pyt_list)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,  detail='unauthorized')


@pyt_router.get('/{id}')
async def get_all_pay_types(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        pyt = session.query(PayType).filter(PayType.id == id).first()
        return jsonable_encoder(pyt)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')


@pyt_router.post('/create')
async def create_pay_type(pytype: PayTypeModel, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        check = session.query(PayType).filter(PayType.id == pytype.id).first()
        if check:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='PayType already exists')

        pay_type = PayType(
            id=pytype.id,
            type=pytype.type
        )
        session.add(pay_type)
        session.commit()
        return HTTPException(status_code=status.HTTP_201_CREATED, detail='PayType created successfully')
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only admins can')


@pyt_router.put('/{id}')
async def update_pay_type(id: int, pytype: PayTypeModel, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        check = session.query(PayType).filter(PayType.id == id).first()
        new_id = session.query(PayType).filter(PayType.id == pytype.id).first()
        if check:
            if new_id is not None or new_id.id == pytype.id:
                for key, value in pytype.dict().items():
                    setattr(new_id, key, value)
                    session.commit()
                data = {
                        "code": 200,
                        "message": "PayType updated successfully"
                }
                return jsonable_encoder(data)

            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="berilgan yangi id da malumot bor")

        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Malumot topilmadi!")
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only admins can update')


@pyt_router.delete('/{id}')
async def delete_pay_type(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        pyt = session.query(PayType).filter(PayType.id == id).first()
        if pyt:
            session.delete(pyt)
            session.commit()
            return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="PayType deleted successfully")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Malumot topilmadi!")
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only admins can delete')
