from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

def app_contenedor(request):
 print('Incoming request')
 return Response('<body> <h1>Esta es la aplicacion funcionando!</h1></body>')

if __name__ == '__main__':
 config = Configurator()
 config.add_route('app', '/')
 config.add_view(app_contenedor, route_name='app')
 app = config.make_wsgi_app()
 server = make_server('0.0.0.0', 5000, app)
 server.serve_forever()
