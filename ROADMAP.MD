PYTHON API/WEBAPP BACKEND TEMPLATE
using starlette/sqlalchemy/pytest

Just coding a boilerplate for later reuses.
-> main branch will just be:
[x] Backend
[x] Routes
[x] Responses
[x] DataBase
[X] Logging

-> user branch will include
[ ] UserModel, UserRoles
[ ] decorators for roles on routes

#############################
ROADMAP
(02-05-2023)
[x] add Database including Tests
[x] add logging
	[x] fix: logger.info not working
	[x] add: File Logger
    [x] add: mail Logger
[x] add error handling
[x] add email (for extended error handling/notification)

Todo:
[x] db.session lookup error
[x] import controllers from module

(03-05-2023)
[x] better app.config
[x] cleanup todos
[x] fix file-logger
[x] request logger

(04-05-2023)
[WIP] configparser more file formats
	[ ] .ini
	[x] .json
	[ ] .toml/.yaml
[X] rework error handling
