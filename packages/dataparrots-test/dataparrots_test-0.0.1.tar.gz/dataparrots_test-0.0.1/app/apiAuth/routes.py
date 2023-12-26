import requests
from pydantic import BaseModel, Field
from app.apiAuth import bp
from app import db, siwa
from app.models import User
from app.common import Result
from config import Config
from app.access_token import AccessToken
from flask_login import login_user, login_required, logout_user


class LoginVo(BaseModel):
    username: str = Field(description='用户名')
    password: str = Field(description='密码')


@bp.route('/login', methods=['POST'])
@siwa.doc(summary='登录', tags=['认证模块'], body=LoginVo)
def login(body: LoginVo):
    user = User.query.filter_by(username=body.username, is_delete=0).first()
    if user is None or not user.check_password(body.password):
        return Result.common(400, 'Incorrect username or password!')
    if user.user_status == 0:
        return Result.common(400, 'The current user is not available!')
    # todo
    # api_url = Config.API_ROOT + "/api/login_user"
    # token = AccessToken().get_access_token()
    # headers = {'Authorization': "Bearer {}".format(token)}
    # data = {
    #     'user_id': user.id
    # }
    # response = requests.post(api_url, json=data, headers=headers)
    # if response.json()['status'] != 0:
    #     return Result.common(400, 'Account abnormality, please contact the administrator!')
    login_user(user)
    # 响应前端数据
    data = {
        'username': user.username,
        'email': user.email,
        'might_like': user.might_like,
        'role': user.user_role
    }
    return Result.success(data)


@bp.route('/logout')
@siwa.doc(summary='登出', tags=['认证模块'])
@login_required
def logout():
    logout_user()
    return Result.success()


class ResetPasswordVo(BaseModel):
    username: str = Field(description='用户名')
    email: str = Field(description='邮箱')


@bp.route('/reset_password', methods=['POST'])
@siwa.doc(summary='重置密码发送邮箱', tags=['认证模块'], body=ResetPasswordVo)
def reset_password(body: ResetPasswordVo):
    user = User.query.filter_by(email=body.email, username=body.username, is_delete=0, user_status=1).first()
    if user:
        api_url = Config.API_ROOT + "/api/send_password_reset_mail"
        token = AccessToken().get_access_token()
        headers = {'Authorization': "Bearer {}".format(token)}
        data = {
            'user_id': user.id,
            'username': user.username,
            'domain': Config.LOCAL_DOMAIN,
            'token': user.get_reset_password_token()
        }
        response = requests.post(api_url, json=data, headers=headers)
        if response.json()['status'] == 0:
            return Result.common(200, 'Check your email for the instructions to reset your password')
        else:
            return Result.common(500, 'Failed to send password reset email!')
    return Result.common(400,'User does not exist or is invalid!')


class CommitPasswordVo(BaseModel):
    password: str = Field(description='密码')
    token: str = Field(description='token')


@bp.route('/commit_password', methods=['POST'])
@siwa.doc(summary='重置密码提交密码更新', tags=['认证模块'], body=CommitPasswordVo)
def commit_password(body: CommitPasswordVo):
    user = User.verify_reset_password_token(body.token)
    if user:
        user.set_password(body.password)
        db.session.commit()
        return Result.success()
    return Result.common(500,'The token has expired or the user does not exist!')