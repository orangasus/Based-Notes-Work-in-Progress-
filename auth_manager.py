import asyncio

class AuthManager():
    async def login_in_profile(self, con, username, password):
        async with con.cursor() as cur:
            await cur.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
            user = (await cur.fetchone())
            if user is None:
                return -1
            return user[0]