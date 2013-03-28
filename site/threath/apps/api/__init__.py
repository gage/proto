from piston.emitters import Emitter
from api.emitters import CustomEmitter
Emitter.unregister('json')
Emitter.register('json', CustomEmitter, 'application/json; charset=utf-8')