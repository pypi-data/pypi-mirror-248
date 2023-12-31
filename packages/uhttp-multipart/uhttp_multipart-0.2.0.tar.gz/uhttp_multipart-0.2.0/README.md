# µHTTP Multipart

Multipart support for µHTTP

### Installation

µHTTP Multipart is on [PyPI](https://pypi.org/project/uhttp-multipart/).

```bash
pip install uhttp-multipart
```

### Usage

Only parse when required:

```python
from uhttp import App
from uhttp_multipart import parse_form

app = App()

@app.post('/')
def submit(request):
    form = parse_form(request.form)
```

Always parse `multipart/form-data` requests (middleware):

```python
from uhttp import App
from uhttp_multipart import multipart

app = App()
app.mount(mutipart())
```

The function `parse_form` (which is also used in the middleware) returns a `MultiDict`. Form fields are `str`, file fields are `BytesIO`.

### License

Released under the MIT license.
