from main import sio
from ..utils.helpers import cache

@sio.on('join')
async def handle_leave(sid, *args, **kwargs):
    cache[args[0]] = 1
    print('cool')
    await sio.emit('contactConnect', args[0])


@sio.on('left')
async def handle_leave(sid, *args, **kwargs):
    await sio.emit('contactDisconnect', args[0])

