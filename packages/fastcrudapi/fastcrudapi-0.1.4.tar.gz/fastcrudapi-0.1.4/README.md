# fastcrudapi

<p align="center">
    <a href="https://fastcrudapi.lpthong90.com"><img src="https://fastcrudapi.lpthong90.com/img/logo.png" alt="FastCRUDAPI"></a>
</p>
<p align="center">
    <em>Super easy to generate CRUD api routes.</em>
</p>
<p align="center">
    <a href="https://github.com/lpthong90/fastcrudapi/actions?query=workflow%3ATest" target="_blank">
        <img src="https://github.com/lpthong90/fastcrudapi/workflows/Test/badge.svg" alt="Test">
    </a>
    <a href="https://github.com/lpthong90/fastcrudapi/actions?query=workflow%3APublish" target="_blank">
        <img src="https://github.com/lpthong90/fastcrudapi/workflows/Publish/badge.svg" alt="Publish">
    </a>
    <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/lpthong90/fastcrudapi" target="_blank">
        <img src="https://coverage-badge.samuelcolvin.workers.dev/lpthong90/fastcrudapi.svg" alt="Coverage">
    <a href="https://pypi.org/project/fastcrudapi" target="_blank">
        <img src="https://img.shields.io/pypi/v/fastcrudapi?color=%2334D058&label=pypi%20package" alt="Package version">
    </a>
    <a href="https://pypi.org/project/fastcrudapi" target="_blank">
        <img alt="Downloads" src="https://img.shields.io/pypi/dm/fastcrudapi?color=%2334D058" />
    </a>
</p>
<p align="center">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/fastcrudapi">
</p>


---

**Documentation**: <a href="https://fastcrudapi.lpthong90.dev" target="_blank">https://fastcrudapi.lpthong90.dev</a>

**Source  Code**: <a href="https://github.com/lpthong90/fastcrudapi" target="_blank">https://github.com/lpthong90/fastcrudapi</a>

---

The package helps to build CRUD APIs for models based on FastAPI.

## Installation
```bash
pip install fastcrudapi
```

## Basic Usage
```python
from fastapi import FastAPI
from fastcrudapi import CrudApiRouter
from pydantic import BaseModel

app = FastAPI()


class Book(BaseModel):
    id: int
    name: str


book_router = CrudApiRouter(
    prefix="/books",
    schema=Book,
)
app.include_router(book_router)
```