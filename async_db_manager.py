import asyncio
import datetime

import aiosqlite


class AsyncDataBaseManager():

    async def connect_to_db(self):
        try:
            con = await aiosqlite.connect('sample_async.db')
            await self.create_users_db_if_needed(con)
            await self.create_notes_db_if_needed(con)
            await con.commit()
            return con
        except Exception as e:
            print('---> Failed to connect to DB -', e)

    async def create_notes_db_if_needed(self, con):
        async with con.cursor() as cur:
            await cur.execute("""CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created DATETIME NOT NULL,
        last_modified DATETIME NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users (id))""")
            await con.commit()

    async def create_users_db_if_needed(self, con):
        async with con.cursor() as cur:
            await cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(20) NOT NULL,
            password VARCHAR(20) NOT NULL,
            num_of_notes INTEGER NOT NULL)""")
            await con.commit()

    async def create_note(self, con, data):
        user_id = data[4]
        async with con.cursor() as cur:
            await cur.execute(
                "INSERT INTO notes(title, content, created, last_modified, user_id) VALUES(?, ?, ?, ?, ?)", data)
            await self.user_note_counter_increment(con, user_id)
            await con.commit()

    async def update_note(self, con, id, data):
        async with con.cursor() as cur:
            await cur.execute("UPDATE notes SET title=?, content=?, last_modified=? WHERE id=?",
                              data + (datetime.datetime.now(),) + (id,))
            await con.commit()

    async def delete_note(self, con, id):
        async with con.cursor() as cur:
            await cur.execute("SELECT user_id FROM notes WHERE id=?", (id,))
            user_id = (await cur.fetchone())[0]
            task_del = asyncio.create_task(cur.execute("DELETE FROM notes WHERE id=?", (id,)))
            await asyncio.gather(task_del, self.user_note_counter_decrement(con, user_id))
            await con.commit()

    async def return_note(self, con, id):
        async with con.cursor() as cur:
            await cur.execute("SELECT * FROM notes WHERE id=?", (id,))
            return await cur.fetchone()

    async def return_all_notes(self, con):
        async with con.cursor() as cur:
            results = await cur.execute("SELECT * FROM notes")
            return await results.fetchall()

    async def delete_all_notes_for_user(self, con, user_id):
        async with con.cursor() as cur:
            await cur.execute("DELETE FROM notes WHERE user_id=?", (user_id,))
            await con.commit()

    async def create_user(self, con, data):
        async with con.cursor() as cur:
            await cur.execute("INSERT INTO users (username, password, num_of_notes) VALUES (?, ?, ?)", data + (0,))
            await con.commit()

    async def update_user(self, con, data, id):
        async with con.cursor() as cur:
            await cur.execute("UPDATE users SET username=?, password=? WHERE id=?", data + (id,))
            await con.commit()

    async def delete_user(self, con, id):
        async with con.cursor() as cur:
            task_del_user = asyncio.create_task(cur.execute("DELETE FROM users WHERE id=?", (id,)))
            await asyncio.gather(task_del_user, self.delete_all_notes_for_user(con, id))
            await con.commit()

    async def get_user_by_id(self, con, id):
        async with con.cursor() as cur:
            await cur.execute("SELECT * FROM users WHERE id=?", (id,))
            return await cur.fetchone()

    async def user_note_counter_increment(self, con, user_id):
        async with con.cursor() as cur:
            await cur.execute("UPDATE users SET num_of_notes=num_of_notes+1 WHERE id=?", (user_id,))
            await con.commit()

    async def user_note_counter_decrement(self, con, user_id):
        async with con.cursor() as cur:
            await cur.execute("UPDATE users SET num_of_notes=num_of_notes-1 WHERE id=?", (user_id,))
            await con.commit()

    async def return_users_list(self, con):
        async with con.cursor() as cur:
            await cur.execute("SELECT * FROM users")
            return await cur.fetchall()
