# µHTTP Session

Session support for µHTTP

Sessions are implemented as [Javascript Web Signatures](https://datatracker.ietf.org/doc/html/rfc7515). Which means that:

1. Sessions are stored in the client's browser.
2. Sessions are not secret.
3. Sessions cannot be tempered with.

### Installation

µHTTP Session is on [PyPI](https://pypi.org/project/uhttp-session/).

```bash
pip install uhttp-session
```

### Usage

First, you must set the secret key as an environment variable:

```bash
export APP_SECRET='<your secret key goes here>'
```

Don't have one?

```bash
python -c 'import secrets; print(secrets.token_hex())'
```

Then:

```python
from uhttp import App, Response
from uhttp_session import session

app = App()
app.mount(session())

@app.post('/login')
def login(request):
    request.state['session']['user'] = request.form.get('user', 'john')
    return Response(302, headers={'location': '/'})

@app.get('/')
def account(request):
    if 'user' not in request.state['session']:
        return 401
    else:
        return f'Hello, {request.state["session"]["user"]}!'
```

### License

Released under the MIT license.
