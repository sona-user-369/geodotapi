from main import sio


@sio.on('join')
async def handle_leave(sid, *args, **kwargs):
    await sio.emit('lobby', 'User left')


@sio.on('left')
async def handle_leave(sid, *args, **kwargs):
    await sio.emit('lobby', 'User left')

