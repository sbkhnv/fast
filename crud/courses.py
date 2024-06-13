from fastapi import APIRouter
from db.database import Session, ENGINE
from db.schemas import CourseModel
from db.models import Courses, Modules, User
from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT


session = Session(bind=ENGINE)
course_router = APIRouter(prefix="/courses")


@course_router.get("/")
async def get_courses(Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        courses = session.query(Courses).all()
        data = [
            {
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "price": course.price,
                "module": {
                    "id": course.modl.id,
                    "name": course.modl.name,
                    "description": course.modl.description,
                    "lesson": {
                            'id': course.modl.lson.id,
                            'title': course.modl.lson.title
                      }
                }
            }
            for course in courses
        ]
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')


@course_router.get("/{id}")
async def get_courses(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        course = session.query(Courses).filter(Courses.id == id).first()
        data = {
                "id": course.id,
                "name": course.name,
                "description": course.description,
                "price": course.price,
                "module": {
                    "id": course.modl.id,
                    "name": course.modl.name,
                    "description": course.modl.description,
                    "lesson": {
                            'id': course.modl.lson.id,
                            'title': course.modl.lson.title,
                            'description': course.modl.lson.description,
                            'homework': course.modl.lson.homework
                      }
                }
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')


@course_router.post("/create")
async def create_course(course: CourseModel, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        check = session.query(Courses).filter(Courses.id == course.id).first()
        if check:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This course already exists")

        new_course = Courses(
            id=course.id,
            name=course.name,
            description=course.description,
            module_id=course.module_id,
            price=course.price
        )
        session.add(new_course)
        session.commit()

        context = {
                "message": "Course created successfully",
                "id": new_course.id,
                "name": new_course.name,
                "description": new_course.description,
                "price": new_course.price,
                "module": {
                    "id": new_course.modl.id,
                    "name": new_course.modl.name,
                    "description": new_course.modl.description,
                    "lesson": {
                            'id': new_course.modl.lson.id,
                            'title': new_course.modl.lson.title,
                            'description': new_course.modl.lson.description,
                            'homework': new_course.modl.lson.homework
                      }
                }
                if new_course.modl else None
                if new_course.modl.lson else None
        }
        return HTTPException(status_code=status.HTTP_201_CREATED, detail=context)
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Admins can create new courses.")


@course_router.put("/{id}")
async def update_course(id: int, course: CourseModel, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        check = session.query(Courses).filter(Courses.id == id).first()
        check_new_id = session.query(Courses).filter(Courses.id == course.id).first()
        check_module = session.query(Modules).filter(Modules.id == course.module_id).first()
        if check:
            if check_new_id is None or check_new_id.id == course.id:
                if check_module:
                    for key, value in course.dict().items():
                        setattr(check, key, value)
                        session.commit()
                    data = {
                            "code": 200,
                            "message": "Course updated successfully",
                            "detail": {
                                     "id": check.id,
                                     "name": check.name,
                                     "description": check.description,
                                     "price": check.price,
                                     "module": {
                                            "id": check.modl.id,
                                            "name": check.modl.name,
                                            "description": check.modl.description,
                                            "lesson": {
                                                'id': check.modl.lson.id,
                                                'title': check.modl.lson.title,
                                                'description': check.modl.lson.description,
                                                'homework': check.modl.lson.homework
                                                }
                                         }
                                }
                            }
                    return jsonable_encoder(data)
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Module id is not created")
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Berilgan yangi id da malumot mavjud!")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="malumot topilmadi")
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only admins can access this')


@course_router.delete("/{id}")
async def delete_course(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        item = session.query(Courses).filter(Courses.id == id).first()
        if item:
            session.delete(item)
            session.commit()
            return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Course deleted successfully")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course does not exist")
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You not have permission to delete this course")
