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
                    <body style="width: 500px">
                        <h3>rpy-frame</h4>
                        <p><a href="/back"><button>back</button></a> &nbsp; <a href="/next"><button>next</button></a></p>
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

