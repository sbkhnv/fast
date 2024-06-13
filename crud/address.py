from fastapi import APIRouter
from db.database import Session, ENGINE
from db.schemas import AddressModel
from db.models import Address, City, User
from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT


session = Session(bind=ENGINE)
address_router = APIRouter(prefix="/address")


@address_router.get('/')
async def get_addresses(Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        addresses = session.query(Address).all()
        context = [
            {
                "id": address.id,
                "name": address.name,
                "city": {
                    "id": address.cities.id,
                    "name": address.cities.name
                }
            }
            for address in addresses
        ]

        return jsonable_encoder(context)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')


@address_router.get('/{id}')
async def get_addresses(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        address = session.query(Address).filter(Address.id ==id).first()
        context = [
            {
                "id": address.id,
                "name": address.name,
                "city": {
                    "id": address.cities.id,
                    "name": address.cities.name
                }
            }

        ]

        return jsonable_encoder(context)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')


@address_router.post('/create_address')
async def create_address(address: AddressModel, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        adr_check = session.query(Address).filter(Address.id == address.id).first()
        if adr_check:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Address is already registered")

        new_adr = Address(
            id=address.id,
            name=address.name,
            city_id=address.city_id
        )
        session.add(new_adr)
        session.commit()

        return HTTPException(status_code=status.HTTP_201_CREATED, detail="Address has been added")
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Only admins can create new addresses")


@address_router.put('/{id}')
async def update_address(id: int, address: AddressModel, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        adr_check = session.query(Address).filter(Address.id == id).first()
        new_id_check = session.query(Address).filter(Address.id == address.id).first()
        city_check = session.query(City).filter(City.id == address.city_id).first()
        if adr_check:
            if city_check:
                if new_id_check is None:
                    for key, value in address.dict().items():
                        setattr(adr_check, key, value)
                        session.commit()

                    data = {
                        "code": 200,
                        "message": "Address updated"
                    }
                    return jsonable_encoder(data)
                elif new_id_check.id == adr_check.id:
                    for key, value in address.dict().items():
                        setattr(adr_check, key, value)
                        session.commit()

                    data = {
                        "code": 200,
                        "message": "Address updated"
                    }
                    return jsonable_encoder(data)
                return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Berilgan id da malumot mavjud!")
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="berilgan city id mavjud emas!")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Malumot topilmadi")
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Only admins can edit this address')


@address_router.delete('/{id}')
async def delete_address(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        item = session.query(Address).filter(Address.id == id).first()
        if item:
            session.delete(item)
            session.commit()
            return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Deleted")

        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Malumot topilmadi")
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Only admins can delete this address")