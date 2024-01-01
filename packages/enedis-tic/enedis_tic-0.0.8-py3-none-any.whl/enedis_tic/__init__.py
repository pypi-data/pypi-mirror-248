from .application_layer import peek
from .autodetect import autodetect, detect


class Tic:
    def __init__(self, device_path, mode, sep):
        self.device_path = device_path
        self.serial_number = None
        self.groups = {}
        self._mode = mode
        self._sep = sep

    @classmethod
    async def create(cls, device_path):
        params = await detect(device_path)
        if not params:
            raise RuntimeError(f'No tic found at {device_path}')
        return cls(device_path, params['mode'], params['sep'])

    async def async_update(self):
        self.groups = await peek(self.device_path, self._mode, self._sep)
        self.serial_number = self.groups.get("Adresse Secondaire du Compteur", self.groups.get("Adresse du compteur"))
        return self.groups

    @classmethod
    async def discover(cls):
        tics_params = await autodetect()
        return [cls(p['port'], p['mode'], p['sep']) for p in tics_params]
