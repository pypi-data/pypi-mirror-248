from .config import routes as config
from .flow import routes as flow
from .flows import routes as flows
from .index import routes as index

routes = [*config, *flow, *flows, *index]
