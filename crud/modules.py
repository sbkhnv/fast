from fastapi import APIRouter
from db.database import Session, ENGINE
from db.schemas import ModuleModel
from db.models import Modules, Lesson, User
from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT


session = Session(bind=ENGINE)
module_router = APIRouter(prefix="/modules")


@module_router.get("/")
async def get_modules(Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        modules = session.query(Modules).all()
        context = [
            {
                "id": module.id,
                "name": module.name,
                "description": module.description,
                "lesson": {
                    'id': module.lson.id,
                    'title': module.lson.title,
                    'description': module.lson.description,
                    'homework': module.lson.homework
                    }
            }
            for module in modules
        ]

        return jsonable_encoder(context)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')


@module_router.get("/{id}")
async def get_modules(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        module = session.query(Modules).filter(Modules.id == id).first()
        context = [
            {
                "id": module.id,
                "name": module.name,
                "description": module.description,
                "lesson": {
                    'id': module.lson.id,
                    'title': module.lson.title,
                    'description': module.lson.description,
                    'homework': module.lson.homework
                    }
            }
        ]

        return jsonable_encoder(context)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')


@module_router.post('/create')
async def create_module(module: ModuleModel, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        check_module = session.query(Modules).filter(Modules.id == module.id).first()
        if check_module:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Module already exists")

        module_data = Modules(
            id=module.id,
            name=module.name,
            description=module.description,
            lesson_id=module.lesson_id
        )
        session.add(module_data)
        session.commit()

        context = {
            "msg": "Module created",
            "id": module_data.id,
            "name": module_data.name,
            "description": module_data.description,
            "lesson": {
                'id': module_data.lson.id,
                'title': module_data.lson.title,
                'description': module_data.lson.description,
                'homework': module_data.lson.homework
            } if module_data.lson else None
        }

        return HTTPException(status_code=status.HTTP_201_CREATED, detail=context)
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="only admins can create modules")


@module_router.put('/{id}')
async def update_module(id: int, module: ModuleModel, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        check = session.query(Modules).filter(Modules.id == id).first()
        check_new_id = session.query(Modules).filter(Modules.id == module.id).first()
        lesson_id = session.query(Lesson).filter(Lesson.id == module.lesson_id).first()
        if check:
            if lesson_id:
                if check_new_id is None or check_new_id.id == id:
                    for key, value in module.dict().items():
                        setattr(check, key, value)
                        session.commit()

                    data = {
                        "code": 200,
                        "message": "Module updated",
                        "detail": {
                            "id": check.id,
                            "name": check.name,
                            "description": check.description,
                            "lesson": {
                                'id': check.lson.id,
                                'title': check.lson.title,
                                'description': check.lson.description,
                                'homework': check.lson.homework
                            }
                        }
                    }

                    return jsonable_encoder(data)

                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Module uchun bu id allaqachon ishlatilgan")
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday id ga ega dars yo'q")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="malumot topilmadi!")
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can access this endpoint")


@module_router.delete("/{id}")
async def delete_module(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        modul = session.query(Modules).filter(Modules.id == id).first()
        if modul:
            session.delete(modul)
            session.commit()
            return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Module deleted")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can")
