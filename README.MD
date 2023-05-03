This is a boilerplate for web-backends written in Python using starlette and sqlalchemy.

## usage

copy/clone this repo

```
python -m venv .venv
python source .venv/bin/activate
python pip install -r requirements.txt
```

## example routing
```
from src.controllers.base import BaseController
class ExampleController(BaseController):
    # define instance name
    instance_name = 'example'

    def make_routes(self):
        # path base: controller endpoint
        # routes : list[tuple[str, str, callable]]
        #   -> route endpoint, httpMethod, controller method to forward the request to
        path_base = '/example'
        routes = [
            ("/", "GET", self.index)
            ("/user", "GET", self.user_data)
            ]

    def index(self, request):
        return self.response('ok', 200)


    def user_data(self, request):
        return self.response({'user':'ExampleUser'}, 200)

```
call like: host:port/endpoint/route
eg: localhost:8000/example/ or localhost:8000&/example/user


## Test email on Error in development:
enviroment/development.env
```
export MAIL_SERVER='localhost'
export MAIL_PORT=1025
export MAIL_USER='somemail@sth.com' # no need for real email in development
export MAIL_PASS='' # not needed for development
export ADMIN_MAIL='admin@mail.lol' # no need for real email in development
```

```
python -m smtpd -n -c DebugginServer localhost:1025
```

and Trigger an error

## Future:
- install script

