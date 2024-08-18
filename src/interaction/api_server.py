from interaction.api import Api
from interaction.button_hub import ButtonHub
from settings import Settings
from aiohttp import web
import asyncio


class ApiServer:
    def __init__(self, settings: Settings, buttonHub: ButtonHub):
        self.runner = None
        self.site = None
        self.loop = None
        self.settings = settings
        self.app = web.Application()
        api = Api(buttonHub)
        self.app.add_routes([
            web.get('/', api.home),
            web.get('/next', api.next),
            web.get('/back', api.back),
            web.get('/primary', api.primary),
            web.get('/secondary', api.secondary)
        ])

    def start(self):
        web.run_app(self.app, port=80)

    def start_bg(self):
        print("starting API server")
        self.runner = web.AppRunner(self.app)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.runner.setup())
        site = web.TCPSite(self.runner, '0.0.0.0', self.settings.api_port)
        loop.run_until_complete(site.start())
        loop.run_forever()
        self.loop = loop
        print("API server started")

    async def stop_bg(self):
        await self.runner.cleanup()