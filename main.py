import asyncio
from pprint import pprint

from async_db_manager import AsyncDataBaseManager
from auth_manager import AuthManager


async def main():
    adbm = AsyncDataBaseManager()
    authm = AuthManager()
    con = await adbm.connect_to_db()
    username, password = input("Username and Password: ").split(" ")
    user_id = await authm.login_in_profile(con, username, password)
    print(user_id)
    # await adbm.create_note(con, (
    # 'Note 1', 'This is the content of note 1', '2023-01-01 00:00:00', '2023-01-01 00:00:00', 1))
    # notes = await adbm.return_all_notes(con)
    await con.close()

if __name__ == "__main__":
    asyncio.run(main())
