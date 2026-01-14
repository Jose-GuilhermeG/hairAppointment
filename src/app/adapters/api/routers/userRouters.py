from fastapi import APIRouter , status , Body
from typing import Annotated
from logging import getLogger

from src.app.application.use_cases.userUseCases import RegisterUserCase , LoginUseCase , SetPasswordUseCase , ListUsersUseCase , UserDetailsUseCase , UpdateUserUseCase
from src.app.adapters.api.schemas.serializers import UserRegisterIn , UserSessionCode , UserLoginIn , UserProfile , SimpleResponse , UpdateUser
from src.app.adapters.hashEncrypt import BcryptHashEncrypt
from src.app.adapters.api.dependencies.repository import UserRepositoryDep as RepositoryDep
from src.app.adapters.api.dependencies.auth import UserIdDep , AuthDep , SessionIdDep

router = APIRouter(
    prefix="/account",
    tags=["account"]
)

logger = getLogger(__name__)

@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSessionCode
)
async def registerView(userData : UserRegisterIn , repository : RepositoryDep , auth : AuthDep ):
    """register an user and return his session code"""
    user = await RegisterUserCase(repository,BcryptHashEncrypt).execute(userData.model_dump())
    token = auth.create_user_token(user.id)
    logger.info("User Created")
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
    logger.info("User logated")
    return UserSessionCode(detail="logated", session_id=session_code)

@router.get(
    '/me/',
    status_code=status.HTTP_200_OK,
    response_model=UserProfile
)
async def profileView(user_id : UserIdDep , repository : RepositoryDep):
    """user profile view"""
    user = UserDetailsUseCase(repository).execute(user_id)
    return UserProfile(name = user.name , email = user.email)


@router.post(
    "/change-password/",
    status_code=status.HTTP_200_OK,
    response_model=SimpleResponse
)
async def change_password_view(repository : RepositoryDep,user_id : UserIdDep , auth : AuthDep,session_id : SessionIdDep, password : Annotated[str , Body(embed=True , min_length=1 , title="new password")]):
    """User change view """
    SetPasswordUseCase(repository ,BcryptHashEncrypt).execute(user_id , password)
    repository.session.commit()
    auth.add_token_to_deathlist(session_id)
    return SimpleResponse(detail="password change")

@router.get(
    "/users/",
    status_code=status.HTTP_200_OK,
    response_model=list[UserProfile]
)
async def list_users_view(repository : RepositoryDep):
    users = ListUsersUseCase(repository).execute()
    return [UserProfile(email=user.email , name = user.name) for user in users ]

@router.patch(
    "/me/",
    status_code=status.HTTP_200_OK,
    response_model=SimpleResponse
)
def update_user_view(user_id : UserIdDep, repository : RepositoryDep ,user_data : UpdateUser):
    UpdateUserUseCase(repository).execute(user_id,user_data.model_dump(exclude_unset=True))
    return SimpleResponse(detail="User updated")
