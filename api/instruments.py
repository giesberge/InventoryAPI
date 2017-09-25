from apistar import Route, Response
from db.models import Instrument
from apistar.backends.sqlalchemy_backend import Session


def create_instrument(session: Session, name: str):
    instrument = Instrument.create(model_name=name)
    instrument.save(session)
    return {'name': instrument._id}


def edit_instrument(record_id: int, name: str):
    return Instrument.api_edit()


def list_instrument(session: Session):
    res = session.query(Instrument).all()
    return [{'name': instr.model_name,
             'id': instr._id
             } for instr in res]


instrument_routes = [
    Route('/', 'GET', list_instrument),
    Route('/', 'POST', create_instrument),
    Route('/{record_id}', 'PUT', edit_instrument),
    Route('/{record_id}', 'DELETE', Instrument.api_delete)
]