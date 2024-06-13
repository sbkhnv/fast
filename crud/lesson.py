from fastapi import APIRouter
from db.database import Session, ENGINE
from db.schemas import LessonModel
from db.models import Lesson, User
from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

session = Session(bind=ENGINE)
lesson_router = APIRouter(prefix="/lessons")


@lesson_router.get('/')
async def get_all_lessons(Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        lessons = session.query(Lesson).all()
        context = [
            {
                'id': lesson.id,
                'title': lesson.title,
                'description': lesson.description,
                'homework': lesson.homework
            }
            for lesson in lessons
        ]
        return jsonable_encoder(context)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')


@lesson_router.get('/{id}')
async def get_all_lessons(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        lesson = session.query(Lesson).filter(Lesson.id == id).first()
        context = [
            {
                'id': lesson.id,
                'title': lesson.title,
                'description': lesson.description,
                'homework': lesson.homework
            }

        ]
        return jsonable_encoder(context)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')


@lesson_router.post('/create')
async def create_lesson(lesson: LessonModel, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        lesson_check = session.query(Lesson).filter(Lesson.id == lesson.id).first()
        if lesson_check:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Lesson already exists")

        new_lesson = Lesson(
            id=lesson.id,
            title=lesson.title,
            description=lesson.description,
            homework=lesson.homework
        )
        session.add(new_lesson)
        session.commit()
        return HTTPException(status_code=status.HTTP_201_CREATED, detail="Lesson created successfully")
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create lessons")


@lesson_router.put('/{id}')
async def update_lesson(id: int, lesson: LessonModel, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        check_lesson = session.query(Lesson).filter(Lesson.id == id).first()
        check_new_id = session.query(Lesson).filter(Lesson.id == lesson.id).first()
        if check_lesson:
            if check_new_id is None or id == check_new_id.id:
                for key, value in lesson.dict().items():
                    setattr(check_lesson, key, value)
                    session.commit()
                    data = {
                        "code": 200,
                        "message": "Lesson updated successfully"
                    }
                    return jsonable_encoder(data)
            return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Berilgan yangi id da malumot bor!")

        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Malumot topilmadi!")
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can")


@lesson_router.delete('/{id}')
async def delete_lesson(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        check_lesson = session.query(Lesson).filter(Lesson.id == id).first()
        if check_lesson:
            session.delete(check_lesson)
            session.commit()
            data = {
                "code": 200,
                "message": "Lesson deleted successfully"
            }
            return jsonable_encoder(data)

        return HTTPException(status_code=status.HTTP_204_, detail="Malumot topilmadi!")
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied')
