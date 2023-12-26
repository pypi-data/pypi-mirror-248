#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from aiearth.core import env
from . import g_var
from .client import Endpoints
from .error import AIEError, AIEErrorCode

global initialized_watch_dog
initialized_watch_dog = False


def _get_token_file_path():
    return os.environ.get('AIE_AUTH_TOKEN_FILE', '/home/jovyan/.jupyter/aie/token')


class _TokenFileChangedEventHandler(FileSystemEventHandler):

    def on_any_event(self, event):
        token_file_path = _get_token_file_path()
        if not os.path.isfile(token_file_path):
            return
        with open(token_file_path) as token_file:
            token = token_file.read()
            if token and len(token.strip()) > 0:
                original_token = os.environ.get(g_var.JupyterEnv.TOKEN)
                if env.get_log_level() == g_var.LogLevel.DEBUG_LEVEL:
                    print(f"Token changed detected, from {original_token} to {token.strip()}")
                os.environ[g_var.JupyterEnv.TOKEN] = token.strip()


def _get_inject_token():
    global initialized_watch_dog
    token_file_path = _get_token_file_path()
    if os.path.isfile(token_file_path) and not initialized_watch_dog:
        # start a watch dog on file change
        _observer = Observer()
        _observer.schedule(_TokenFileChangedEventHandler(), os.path.dirname(token_file_path), recursive=True)
        _observer.start()
        initialized_watch_dog = True

        with open(token_file_path) as token_file:
            token = token_file.read().strip()
        if token and len(token) > 0:
            os.environ[g_var.JupyterEnv.TOKEN] = token.strip()
            return token
        else:
            return os.environ.get(g_var.JupyterEnv.TOKEN)
    else:
        return os.environ.get(g_var.JupyterEnv.TOKEN)


class Authenticate(object):
    class ClientId(object):
        USER_STD = "user_std"
        ALIYUN_JUPYTER = "aliyun_jupyter"

    @staticmethod
    def getClientEnvironment():
        if os.getenv(g_var.JupyterEnv.TOKEN) is not None:
            return Authenticate.ClientId.ALIYUN_JUPYTER
        else:
            return Authenticate.ClientId.USER_STD

    @staticmethod
    def __displayAuthPromt():
        print("请将以下地址粘贴到Web浏览器中，访问授权页面，并将个人token粘贴到输入框中")
        print("\t", Endpoints.AUTH_PORTAL_PAGE)

    @staticmethod
    def __getTokenFromJupyter():
        # token = os.getenv(g_var.JupyterEnv.TOKEN)
        token = _get_inject_token()
        if token is None:
            raise AIEError(AIEErrorCode.ENVIRONMENT_INIT_ERROR,
                           "云平台环境token获取失败")
        return token

    @staticmethod
    def auth(token=None, access_key_id=None, access_key_secret=None, access_key_security_token=None):
        """
        authentication
        :param token: AI earth granted token, check https://engine-aiearth.aliyun.com/#/utility/auth-token for more
        :param access_key_id: aliyun accessKey id, check https://help.aliyun.com/zh/ram/?spm=a2c4g.11186623.0.0.44326ecf21XEUf
        :param access_key_secret: aliyun accessKey secret, check above link for more
        :param access_key_security_token: aliyun accessKey STS security token, check above link for more; None if you do not use STS
        :return: None
        """
        client_id = Authenticate.getClientEnvironment()

        cred = {}
        cred["client_id"] = client_id
        if token is not None:
            cred["token"] = token
        elif access_key_id and access_key_secret:
            token = Authenticate.__get_token_by(access_key_id, access_key_secret,
                                                security_token=access_key_security_token)
            cred["token"] = token
        else:
            if client_id == Authenticate.ClientId.ALIYUN_JUPYTER:
                token = Authenticate.__getTokenFromJupyter()
                cred["token"] = token
            else:
                Authenticate.__displayAuthPromt()
                token = input("个人token: ")
                cred["token"] = token

        g_var.set_var(g_var.GVarKey.Authenticate.CLIENT_ID, cred["client_id"])
        g_var.set_var(g_var.GVarKey.Authenticate.TOKEN, cred["token"])

    @staticmethod
    def getCurrentUserToken():
        if not g_var.has_var(g_var.GVarKey.Authenticate.CLIENT_ID):
            raise AIEError(AIEErrorCode.ENVIRONMENT_INIT_ERROR,
                           "客户端ID获取失败，请先调用 aie.Authenticate() 进行授权")

        client_id = g_var.get_var(g_var.GVarKey.Authenticate.CLIENT_ID)
        token = ""
        if client_id == Authenticate.ClientId.ALIYUN_JUPYTER:
            token = Authenticate.__getTokenFromJupyter()
        else:
            if not g_var.has_var(g_var.GVarKey.Authenticate.TOKEN):
                raise AIEError(AIEErrorCode.ENVIRONMENT_INIT_ERROR,
                               "个人token获取失败，请先调用 aie.Authenticate() 进行授权")
            token = g_var.get_var(g_var.GVarKey.Authenticate.TOKEN)
        return token

    @staticmethod
    def __get_token_by(access_key_id, access_key_secret, security_token=None, force_create=False,
                       expected_hours_before_expired=24):
        from alibabacloud_tea_openapi import models
        from alibabacloud_aiearth_engine20220609.client import Client
        from alibabacloud_aiearth_engine20220609.models import GetUserTokenRequest
        from alibabacloud_aiearth_engine20220609.models import GetUserTokenResponse
        config = models.Config(
            access_key_id=access_key_id, access_key_secret=access_key_secret, security_token=security_token,
            region_id=Endpoints.OPENAPI_REGION_ID, endpoint=Endpoints.OPENAPI_ENDPOINT)

        client = Client(config)

        get_user_token = GetUserTokenRequest()
        get_user_token.force_create = force_create
        get_user_token_resp: GetUserTokenResponse = client.get_user_token(get_user_token)
        token = get_user_token_resp.body.token
        expired_at_ts = get_user_token_resp.body.expired_at / 1000.

        current_ts = datetime.now().timestamp()
        if expired_at_ts - current_ts < expected_hours_before_expired * 3600.:
            get_user_token = GetUserTokenRequest()
            get_user_token.force_create = True
            get_user_token_resp: GetUserTokenResponse = client.get_user_token(get_user_token)
            return get_user_token_resp.body.token
        else:
            return token
