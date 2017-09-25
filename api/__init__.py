from apistar import Include
from .instruments import instrument_routes

routes = [
    Include('/instruments', instrument_routes)
]