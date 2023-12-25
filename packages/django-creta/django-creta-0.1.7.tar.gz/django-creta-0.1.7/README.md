# django-creta

## 1. Installation

The preferred installation method is directly from pypi:

```bash
# Create promgen setting directory.
$ pip install -U django-creta
```

## 2. Quickstart

In ``settings.py``:

```python
INSTALLED_APPS = [
    ...,
    'creta'
]
```

2. In ``urls.py``:

```python
from django.urls import path, include

urlpatterns = [
    ...,
    path('creta/', include('creta.urls')),
]
```

3. Run ``python manage.py migrate``
Create the models.
```bash
$ python manage.py migrate
```

4. Import gateway
```python
from creta.gateway import creta_sdk

# get_nfts
result = creta_sdk.get_nfts(address="0x628fD709BFa7fe68af024852893Ef615104445Ee", page=1)

# get_nft
result = creta_sdk.get_nft(token_id="10106")

# get_nft_transactions_by_user
result = creta_sdk.get_nft_transactions_by_user(address="0x628fD709BFa7fe68af024852893Ef615104445Ee")

# get_nft_transactions_by_nft
result = creta_sdk.get_nft_transactions_by_nft(token_id="10103")

# create_nft
result = creta_sdk.create_nft(
    address="0x628fD709BFa7fe68af024852893Ef615104445Ee",
    nft_type=1,
    name="NFT name",
    attributes=[
        {
            "trait_type": "Level",
            "value": 1
        }
    ],
    image_url="https://cf.dev.superclubs.io/media/club/advertisement/8f4ee8fd-8c79-4004-aad7-88c3edbdf4ef/20230907/20230907T040903.jpg",
)
# get_nft_status
result = creta_sdk.get_nft_status(request_id="3c52f871-1a01-47f3-8a9e-045d2767aab9")

# update_nft
result = creta_sdk.update_nft(
    tokenId="10106",
    nftType=3,
    name="Club 20",
    attributes=[{"trait_type": "Level", "value": 20}])
```

6. Test SDK
```bash
$ python manage.py test -v 2
```

## 3. Configuration
1.settings.py
```python
import environ

env = environ.Env()

...

# Creta Configuration
CRETA_GATEWAY_HOST = env('CRETA_GATEWAY_HOST')
CRETA_APP_ID = env('CRETA_APP_ID')
CRETA_API_KEY = env('CRETA_API_KEY')
CRETA_SECRET_KEY = env('CRETA_SECRET_KEY')
```

## 4. Update Package

In ``setup.cfg``, upgrade version
```
[metadata]
name = django-creta
version = x.x.x
...
```

Build package
```bash
$ python setup.py sdist bdist_wheel
```

Deploy package
```bash
$ twine upload --verbose dist/django-creta-x.x.x.tar.gz
```

## The MIT License

Copyright (c) 2023 Runners Co., Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
