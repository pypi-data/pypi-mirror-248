import os
import time
import jwt
from uhttp import App, Response


def session():
    app = App()


    @app.startup
    def set_secret(state):
        state.setdefault('secret', os.getenv('APP_SECRET', 'dev'))


    @app.before
    def get_token(request):
        session = request.cookies.get('session')
        if session and session.value:
            try:
                request.state['session'] = jwt.decode(
                    jwt=session.value,
                    key=request.state['secret'],
                    algorithms=['HS256']
                )
            except jwt.exceptions.PyJWTError:
                request.state['session'] = {'exp': 0}
                raise Response(400)
        else:
            request.state['session'] = {}


    @app.after
    def set_token(request, response):
        if session := request.state.get('session'):
            session.setdefault('exp', int(time.time()) + 604800)
            response.cookies['session'] = jwt.encode(
                payload=session,
                key=request.state['secret'],
                algorithm='HS256'
            )
            response.cookies['session']['expires'] = time.strftime(
                '%a, %d %b %Y %T GMT', time.gmtime(session['exp'])
            )
            response.cookies['session']['samesite'] = 'Lax'
            response.cookies['session']['httponly'] = True
            response.cookies['session']['secure'] = True

    return app
