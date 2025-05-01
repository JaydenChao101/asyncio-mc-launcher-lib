from launcher_core import microsoft_account

async def main():
    # refresh my token
    token = await microsoft_account.refresh_minecraft_token("your-refresh_token","your_client_id")
    xbl_token = await microsoft_account.Login.get_xbl_token(token["access_token"])
    xsts_token = await microsoft_account.Login.get_xsts_token(xbl_token["Token"])
    minecraft_token = await microsoft_account.Login.get_minecraft_access_token(
        xsts_token["Token"],
        xsts_token["DisplayClaims"]["xui"][0]["uhs"]
    )
    print("Minecraft Access Token:", minecraft_token["access_token"])

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())