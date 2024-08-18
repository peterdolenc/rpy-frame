from aiohttp import web
from interaction.button_hub import ButtonHub


class Api():
    def __init__(self, buttonHub: ButtonHub):
        self.buttonHub = buttonHub
        pass
        
    def home(self, request):
        return web.Response(text="""
                <html>
                    <head><title>rpy-frame</title></head>
                    <body style="width: 400px;max-width: 400px;overflow-x: hidden !important;">
                        <h3>rpy-frame</h3>
                        <p><a href="/back"><button>back</button></a> &nbsp; <a href="/next"><button>next</button></a></p>
                        <p><a href="/primary"><button>primary</button></a> &nbsp; <a href="/secondary"><button>secondary</button></a></p>
                    </body>
                </html>
                """,
        content_type='text/html')
    
    def next(self, request):
        self.buttonHub.next_button_handler()
        return self.home(request)
    
    def back(self, request):
        self.buttonHub.back_button_handler()
        return self.home(request)
    
    def primary(self, request):
        self.buttonHub.switch_to_primary_handler()
        return self.home(request)
    
    def secondary(self, request):
        self.buttonHub.switch_to_secondary_handler()
        return self.home(request)

