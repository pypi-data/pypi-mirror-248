import asyncio

from . import physical_layer
from serial.tools.list_ports import comports


async def autodetect():
    tasks = []
    for port in comports():
        tasks.append(asyncio.create_task(detect(port.device)))
    await asyncio.gather(*tasks)
    return [t.result() for t in tasks if t.result()]


async def detect(port):
    for mode in ('H', 'S'):
        try:
            res = await asyncio.wait_for(_detect_port(port, mode), 3)
        except Exception:
            continue
        else:
            return res
    return None


async def _detect_port(port, mode):
    reader, writer = await physical_layer.serial_line(port, mode)
    params = None
    async for raw_frame in physical_layer.frame_iterator(reader):
        params = {
            'port': port,
            'mode': mode,
            'sep': '\t' if '\t' in raw_frame else ' '
        }
        break
    writer.close()
    await writer.wait_closed()
    return params
