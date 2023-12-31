# µHTTP Static

Static files support for µHTTP

In production, use [Unit](https://unit.nginx.org/) instead.

### Installation

µHTTP Static is on [PyPI](https://pypi.org/project/uhttp-static/).

```bash
pip install uhttp-static
```

### Usage

```python
from uhttp import App
from uhttp_static import send_file, static


app = App()
app.mount(static('assets'), '/assets')


@app.get('/')
def hello(request):
    return send_file('hello.html')
```

### License

Released under the MIT license.
