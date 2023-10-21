import flet as ft
from async_db_manager import AsyncDataBaseManager
from auth_manager import AuthManager
import asyncio


class MyApp:
    def __init__(self, page: ft.Page):
        self.login_page = page
        self.dbManager = AsyncDataBaseManager()
        self.adbm = AuthManager()
        self.con = None
        self.current_user = None

        asyncio.gather(self.initialize_db_con(), self.set_up_login_page())


    async def initialize_db_con(self):
        self.con = await self.dbManager.connect_to_db()

    async def set_up_login_page(self):
        self.login_page.window_width = 500

        # Initialize controls
        self.greeting_textfield = ft.Text("Welcome to Based Notes", size=24)
        self.username_field = ft.TextField(label="Username")
        self.password_field = ft.TextField(label="Password")
        self.login_button = ft.ElevatedButton(text='Login', on_click=self.on_login_button_click)
        self.registration_textfield = ft.Text("Want to Register?")
        self.register_button = ft.ElevatedButton(text='Register', on_click=self.on_register_button_click)

        # Create containers
        self.col_greeting = ft.Container(margin=10, content=self.greeting_textfield)
        self.col_login = ft.Container(border=ft.border.all(1, ft.colors.ORANGE),
                                      content=ft.Column(
                                          controls=[self.username_field, self.password_field, self.login_button],
                                          horizontal_alignment=ft.CrossAxisAlignment.CENTER), border_radius=10,
                                      padding=10)
        self.col_reg = ft.Container(content=ft.Column(controls=[self.registration_textfield, self.register_button],
                                                      horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    border_radius=10,
                                    padding=10)

        # Create main column and container
        self.basic_col = ft.Column(controls=[self.col_greeting, self.col_login, self.col_reg],
                                   horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.basic_container = ft.Container(border=ft.border.all(1, ft.colors.ORANGE), padding=50,
                                            content=self.basic_col,
                                            border_radius=10,
                                            alignment=ft.alignment.center, expand=True)

        # Add main container to page
        await self.login_page.add_async(self.basic_container)

    async def check_login_input(self):
        username, password = None, None
        if self.username_field.value is None:
            self.username_field.error_text = 'Please, enter username'
            await self.login_page.update_async()
        else:
            username = self.username_field.value

        if self.password_field.value is None:
            self.password_field.error_text = 'Please, enter password'
            await self.login_page.update_async()
        else:
            password = self.password_field.value

        return username, password

    async def on_login_button_click(self, e):
        username, password = await self.check_login_input()
        if username is not None and password is not None:
            self.username_field.value = ''
            self.password_field.value = ''
            await self.login_page.update_async()

        user_id = await self.adbm.login_in_profile(self.con, username, password)
        if user_id == -1:
            print('No such user') # create an alert that there is no such user
        else:
            self.current_user = await self.dbManager.get_user_by_id(self.con, user_id)
            print(self.current_user)

    async def on_register_button_click(self, e):
        print('Register...')


async def main(page: ft.Page):
    myApp = MyApp(page)


asyncio.run(ft.app_async(target=main))
