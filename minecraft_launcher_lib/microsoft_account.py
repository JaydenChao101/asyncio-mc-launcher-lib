# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2025 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
# This file is part of asyncio-minecraft-launcher-lib (https://github.com/JaydenChao101/asyncio-mc-lancher-lib)
# Copyright (c) 2025 JaydenChao101 <jaydenchao@proton.me> and contributors
#This part of the code is licensed under the MIT License.

from minecraft_launcher_lib.microsoft_types import AuthorizationTokenResponse, XBLResponse, XSTSResponse, MinecraftAuthenticateResponse, MinecraftStoreResponse, MinecraftProfileResponse, CompleteLoginResponse
from minecraft_launcher_lib.exceptions import AccountNotOwnMinecraft
import urllib.parse
import requests
import logging



__AUTH_URL__ = "https://login.live.com/oauth20_authorize.srf"
__TOKEN_URL__ = "https://login.live.com/oauth20_token.srf"
CLIENT_ID = "00000000402b5328"
REDIRECT_URI = "https://login.live.com/oauth20_desktop.srf"
__SCOPE__ = "service::user.auth.xboxlive.com::MBI_SSL"

class LoggingSetting:
    def __init__(self, level: int = logging.INFO, filename: str = None, enable_console: bool = False):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)

        formatter = logging.Formatter("%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")

        if enable_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        if filename:
            file_handler = logging.FileHandler(filename)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

async def get_login_url() -> str:
    """
    Generate a login url.\\
    For a more secure alternative, use :func:`get_secure_login_data`


    :return: The url to the website on which the user logs in
    """
    parameters = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "response_mode": "query",
        "scope": __SCOPE__,
    }
    url = urllib.parse.urlparse(__AUTH_URL__)._replace(query=urllib.parse.urlencode(parameters)).geturl()
    logging.info(f"Login url: {url}")
    return url

async def extract_code_from_url(url: str) -> str:
    """
    Extract the code from the redirect url.

    :param url: The redirect url
    :return: The code
    """
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    if "code" not in query_params:
        raise ValueError("No code found in the URL")
    return query_params["code"][0]

async def get_ms_token(code: str) -> AuthorizationTokenResponse:
    """
    Get the Microsoft token using the code from the login url.

    :param code: The code from the login url
    :return: The Microsoft token
    """
    data = {
        "client_id": CLIENT_ID,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "scope": __SCOPE__,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(__TOKEN_URL__, data=data, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    logging.info(f"Microsoft token response: {data}")
    return data

async def get_xbl_token(ms_access_token: str) -> XBLResponse:
    payload = {
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName": "user.auth.xboxlive.com",
            "RpsTicket": ms_access_token
        },
        "RelyingParty": "http://auth.xboxlive.com",  # 注意这里
        "TokenType": "JWT"
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post("https://user.auth.xboxlive.com/user/authenticate", json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    logging.info(f"Xbox Token response: {data}")
    return data

async def get_xsts_token(xbl_token: str) -> XSTSResponse:
    """
    Get the XSTS token using the Xbox Live token.

    :param xbl_token: The Xbox Live token
    :return: The XSTS token
    """
    payload = {
        "Properties": {
            "SandboxId": "RETAIL",
            "UserTokens": [xbl_token]
        },
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT"
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post("https://xsts.auth.xboxlive.com/xsts/authorize", json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    logging.info(f"XSTS Token response: {data}")
    return data

async def get_minecraft_access_token(xsts_token: str, uhs: str) -> MinecraftAuthenticateResponse:
    """
    Get the Minecraft access token using the XSTS token and user hash.

    :param xsts_token: The XSTS token
    :param uhs: The user hash
    :return: The Minecraft access token
    """
    identity_token = f"XBL3.0 x={uhs};{xsts_token}"
    payload = {"identityToken": identity_token}
    headers = {"Content-Type": "application/json"}
    resp = requests.post("https://api.minecraftservices.com/authentication/login_with_xbox", json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    logging.info(f"Minecraft access token response: {data}")
    return data

async def have_minecraft(access_token : str) -> bool:
    """
    Check if the user owns Minecraft using the access token.

    :param access_token: The Minecraft access token
    :return: True if the user owns Minecraft, Raise AccountNotOwnMinecraft otherwise
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get("https://api.minecraftservices.com/entitlements/mcstore", headers=headers)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("items"):
        raise AccountNotOwnMinecraft()
    return True

async def get_minecraft_profile(access_token: str) -> MinecraftProfileResponse:
    """
    Get the Minecraft profile using the access token.

    :param access_token: The Minecraft access token
    :return: The Minecraft profile
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get("https://api.minecraftservices.com/minecraft/profile", headers=headers)
    resp.raise_for_status()
    return resp.json()

async def get_minecraft_player_attributes(access_token :str) -> MinecraftProfileResponse:
    """
    Get the Minecraft player attributes.

    :return: The Minecraft player attributes
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get("https://api.minecraftservices.com/minecraft/profile/attributes", headers=headers)
    resp.raise_for_status()
    return resp.json()

async def login_minecraft():
    import webbrowser
    webbrowser.open_new_tab(await get_login_url())
    url = input("Please open the URL in your browser and paste the redirect URL here: ")
    code = await extract_code_from_url(url)
    ms_token = await get_ms_token(code)
    xbl_token = await get_xbl_token(ms_token["access_token"])
    xsts_token = await get_xsts_token(xbl_token["Token"])
    uhs = xbl_token["DisplayClaims"]["xui"][0]["uhs"]
    minecraft_token = await get_minecraft_access_token(xsts_token["Token"], uhs)
    await have_minecraft(minecraft_token["access_token"])
    return {
        "access_token": minecraft_token["access_token"],
        "refresh_token": ms_token["refresh_token"],
        "expires_in": ms_token["expires_in"],
        "uhs": uhs,
        "xsts_token": xsts_token["Token"],
        "xbl_token": xbl_token["Token"]
    }

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(login_minecraft())
    print(result)
