import sys
import urllib.parse
import requests
import webbrowser

# Constants
CLIENT_ID = "00000000402b5328"
REDIRECT_URI = "https://login.live.com/oauth20_desktop.srf"
OAUTH_SCOPE = "service::user.auth.xboxlive.com::MBI_SSL"

MS_TOKEN_URL = "https://login.live.com/oauth20_token.srf"
XBL_AUTH_URL = "https://user.auth.xboxlive.com/user/authenticate"
XSTS_AUTH_URL = "https://xsts.auth.xboxlive.com/xsts/authorize"
MC_LOGIN_URL = "https://api.minecraftservices.com/authentication/login_with_xbox"

def extract_code(redirect_url: str) -> str:
    """Extract the 'code' parameter from the redirect URL."""
    parsed = urllib.parse.urlparse(redirect_url)
    qs = urllib.parse.parse_qs(parsed.query)
    code = qs.get("code", [None])[0]
    if not code:
        raise ValueError("No 'code' parameter found in the URL")
    return code

def get_ms_token(code: str) -> str:
    """Exchange OAuth code for a Microsoft access token."""
    data = {
        "client_id": CLIENT_ID,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "scope": OAUTH_SCOPE,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(MS_TOKEN_URL, data=data, headers=headers)
    resp.raise_for_status()
    return resp.json()["access_token"]

def get_xbl_token(ms_access_token: str) -> (str, str):
    """Exchange Microsoft token for an Xbox Live token + user hash (uhs)."""
    payload = {
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName": "user.auth.xboxlive.com",
            "RpsTicket": ms_access_token
        },
        "RelyingParty": "http://auth.xboxlive.com",
        "TokenType": "JWT"
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(XBL_AUTH_URL, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    xbl_token = data["Token"]
    uhs = data["DisplayClaims"]["xui"][0]["uhs"]
    return xbl_token, uhs

def get_xsts_token(xbl_token: str) -> str:
    """Exchange Xbox Live token for an XSTS token."""
    payload = {
        "Properties": {
            "SandboxId": "RETAIL",
            "UserTokens": [xbl_token]
        },
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT"
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(XSTS_AUTH_URL, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()["Token"]

def get_minecraft_token(xsts_token: str, uhs: str) -> str:
    """Exchange XSTS token + user hash for a Minecraft access token."""
    identity_token = f"XBL3.0 x={uhs};{xsts_token}"
    payload = {"identityToken": identity_token}
    headers = {"Content-Type": "application/json"}
    resp = requests.post(MC_LOGIN_URL, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()["access_token"]

def main():
    webbrowser.open_new_tab("https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?client_id=00000000402b5328&response_type=code&redirect_uri=https:%2F%2Flogin.live.com%2Foauth20_desktop.srf&response_mode=query&scope=service%3A%3Auser.auth.xboxlive.com%3A%3AMBI_SSL")

    redirect_url = input("Please open the URL in your browser and paste the redirect URL here: ")
    try:
        print("[*] Extracting code from redirect URL...")
        code = extract_code(redirect_url)
        print(f"    code = {code}")

        print("[*] Requesting Microsoft access token...")
        ms_token = get_ms_token(code)
        print(f"    ms_access_token = {ms_token}")

        print("[*] Requesting Xbox Live token...")
        xbl_token, uhs = get_xbl_token(ms_token)
        print(f"    xbl_token = {xbl_token}")
        print(f"    user_hash (uhs) = {uhs}")

        print("[*] Requesting XSTS token...")
        xsts_token = get_xsts_token(xbl_token)
        print(f"    xsts_token = {xsts_token}")

        print("[*] Requesting Minecraft token...")
        mc_token = get_minecraft_token(xsts_token, uhs)
        print(f"    minecraft_access_token = {mc_token}")

        print("\nAll tokens retrieved successfully.")
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
