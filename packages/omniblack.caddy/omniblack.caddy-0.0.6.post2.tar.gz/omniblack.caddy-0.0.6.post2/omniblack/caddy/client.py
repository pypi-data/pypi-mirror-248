from __future__ import annotations
from json import dump, load
from pathlib import Path

from requests import HTTPError

try:
    from aiohttp import ClientResponseError, ClientSession
    from anyio.to_thread import run_sync

    from .unix import create_aiohttp
except ImportError:
    async_installed = False
else:
    async_installed = True


from .convert_json import convert
from .route import Site
from .unix import create_requests


def get_url(net_address, default_host):
    if net_address.startswith('unix/'):
        return net_address.replace('unix/', 'unix://')
    elif net_address.startswith('udp/'):
        raise TypeError('Upd sockets are not supported.')
    else:
        net_address = net_address.removeprefix('tcp/')
        if net_address.startswith(':'):
            net_address = default_host + net_address
        return f'http://{net_address}'


class Caddy:
    def __init__(
            self,
            *,
            caddy_file: Path = None,
            socket_path: Path = None,
            update_caddy_file=False,
            caddy_host='localhost',
            cwd: Path = None,
    ):
        if cwd is None:
            cwd = Path.cwd()

        if caddy_file is not None:
            caddy_file = cwd / caddy_file

        if not socket_path:
            with caddy_file.open() as file_obj:
                config = load(file_obj)

            try:
                listen = config['admin']['listen']
            except KeyError:
                raise TypeError(
                    'Caddyfile must have an admin unix socket configured',
                )

            if listen.startswith('unix/'):
                self.socket_path = str(cwd / listen.removeprefix('unix/'))
                self.base = 'unix://caddy'
            else:
                self.base = get_url(listen, caddy_host)
                self.socket_path = None

        else:
            self.socket_path = str(cwd / socket_path)

        self.requests = None
        self.update_caddy_file = update_caddy_file
        self.caddy_file = caddy_file
        self.cwd = cwd

    def url(self, path):
        return self.base + path

    def get(self, path, *args, **kwargs):
        return self.requests.get(self.url(path), *args, **kwargs)

    def post(self, path, *args, **kwargs):
        return self.requests.post(self.url(path), *args, **kwargs)

    def patch(self, path, *args, **kwargs):
        return self.requests.patch(self.url(path), *args, **kwargs)

    def add_site(self, site: Site):
        site_id = f'site_{site.name}'
        json = convert(site)
        json['@id'] = site_id

        try:
            resp = self.requests.patch(self.url(f'/id/{site_id}'), json=json)
            resp.raise_for_status()
        except HTTPError:
            url = self.url('/id/server/routes')
            resp = self.requests.post(url, json=json)
            resp.raise_for_status()

        if self.update_caddy_file:
            updated_resp = self.get('/config')
            updated_resp.raise_for_status()

            updated_config = updated_resp.json()

            with self.caddy_file.open('w') as file:
                dump(
                    updated_config,
                    file,
                    sort_keys=True,
                    indent=4,
                    ensure_ascii=False,
                )

    def __enter__(self):
        self.requests = create_requests(self.socket_path)

    def __exit__(self, exc_type, exc_value, traceback):
        if self.requests is not None:
            self.requests.close()
            self.requests = None


def load_config(file_path):
    with file_path.open() as file_obj:
        return load(file_obj)


def dump_config(file_path, config):
    with file_path.open('w') as file_obj:
        return dump(
            config,
            file_obj,
            sort_keys=True,
            indent=4,
            ensure_ascii=False,
        )


class AsyncCaddy:
    def __init__(
        self,
        *,
        base: str,
        aiohttp: ClientSession,
        cwd: Path,
        caddy_file: Path = None,
        update_caddy_file: bool = False,
    ):
        self.base = base
        self.aiohttp = aiohttp
        self.cwd = cwd
        self.caddy_file = caddy_file
        self.update_caddy_file = update_caddy_file

    @classmethod
    async def create(
        cls,
        *,
        caddy_file: Path = None,
        socket_path: Path = None,
        update_caddy_file=False,
        caddy_host='localhost',
        cwd=None,
    ):
        if cwd is None:
            cwd = await run_sync(Path.cwd)

        if not socket_path:
            config = await run_sync(load_config, cwd / caddy_file)

            try:
                listen = config['admin']['listen']
            except KeyError:
                raise TypeError(
                    'Caddyfile must have an admin unix socket configured',
                )

            if listen.startswith('unix/'):
                socket_path = str(cwd / listen.removeprefix('unix/'))
                base = 'unix://caddy'
            else:
                base = get_url(listen, caddy_host)

        elif isinstance(socket_path, Path):
            socket_path = str(cwd / socket_path)
            base = 'unix://caddy'

        aiohttp = create_aiohttp(socket_path)

        return cls(
            aiohttp=aiohttp,
            base=base,
            caddy_file=caddy_file,
            update_caddy_file=update_caddy_file,
            cwd=cwd,
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.aiohttp.close()

    def url(self, path):
        return self.base + path

    def get(self, path, *args, **kwargs):
        return self.aiohttp.get(self.url(path), *args, **kwargs)

    def post(self, path, *args, **kwargs):
        return self.aiohttp.post(self.url(path), *args, **kwargs)

    def patch(self, path, *args, **kwargs):
        return self.aiohttp.patch(self.url(path), *args, **kwargs)

    async def add_site(self, site: Site):
        site_id = f'site_{site.name}'
        json = convert(site)
        json['@id'] = site_id

        try:
            await self.patch(f'/id/{site_id}', json=json)
        except ClientResponseError:
            await self.patch('/id/server/routes', json=json)

        if self.update_caddy_file:
            async with self.get('/config') as resp:
                updated_config = await resp.json()

            await run_sync(dump_config, self.caddy_file, updated_config)


if not async_installed:
    del AsyncCaddy
