from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from apistar.backends import sqlalchemy_backend
from db.models import Base
from api import routes


def welcome(name=None):
    if name is None:
        return {'message': 'Welcome to db Star!'}
    return {'message': 'Welcome to db Star, %s!' % name}


routes = routes + \
         [
             Include('/docs', docs_urls),
             Include('/static', static_urls)
         ]

# Configure database settings
settings = {
    "DATABASE": {
        "URL": "sqlite:///Test.db",
        "METADATA": Base.metadata
    }
}

app = App(routes=routes,
          settings=settings,
          commands=sqlalchemy_backend.commands,
          components=sqlalchemy_backend.components)

if __name__ == '__main__':
    app.main()
