from fastapi import APIRouter , status

from src.app.application.use_cases.userUseCases import RegisterUserCase , LoginUseCase
from src.app.adapters.api.schemas.serializers import UserRegisterIn , UserSessionCode , UserLoginIn , UserProfile
from src.app.adapters.hashEncrypt import BcryptHashEncrypt
from src.app.adapters.api.dependencies.repository import UserRepositoryDep as RepositoryDep
from src.app.adapters.api.dependencies.auth import UserDep , AuthDep

router = APIRouter(
    prefix="/account",
    tags=["account"]
)

@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSessionCode
)
async def registerView(userData : UserRegisterIn , repository : RepositoryDep , auth : AuthDep ):
    """register an user and return his session code"""
    user = await RegisterUserCase(repository,BcryptHashEncrypt).execute(userData.model_dump())
    repository.session.commit()
    token = auth.create_user_token(user.id)
    return UserSessionCode(detail="created", session_id=token)

@router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    response_model=UserSessionCode
)
async def loginView(user_data : UserLoginIn , repository : RepositoryDep , auth : AuthDep):
    """login an user"""
    user_id = LoginUseCase(repository , BcryptHashEncrypt).execute(user_data.model_dump())
    session_code = auth.create_user_token(user_id)
    return UserSessionCode(detail="logated", session_id=session_code)

@router.get(
    '/me/',
    status_code=status.HTTP_200_OK,
    response_model=UserProfile
)
async def profileView(user : UserDep):
    """user profile view"""
    return UserProfile(name = user.name , email = user.email)
