## Installation
Project is compatible with Python 3.8 or newer versions. By using [Starlette](https://www.starlette.io/) framework with [Uvicorn](https://www.uvicorn.org) combination.

### Install dependencies

```shell
pip install -r requirements.txt
```
### Apply database migrations

```shell
alembic upgrade head
```

### Run HTTP server
```shell
cd src/app
uvicorn api:app --reload
```

## Testing

### Run tests

```shell
pytest
```

### Integration tests via HTTP

Integration tests are in `tests.http`

_How to work with integration tests in [Pycharm](https://www.jetbrains.com/help/pycharm/http-client-in-product-code-editor.html)._
