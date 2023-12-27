# YandexGPT Python Library #

### What is this? 

### This library allows you work with YandexGPT using Python and implement it to your projects.

## Setup 

```Bash
pip install yagpt-py
```

## Usage 

```Python
import os
from yagpt_py.authData import AuthData
from yagpt_py.messages import Messages
from yagpt_py.response import Response

token = AuthData.Token = os.getenv('IAM_token')
folder_id = AuthData.CatalogID = os.getenv('catalog_id')

message = Messages.user = 'Tell me poem about misfit developer.'

response = Response(token, folder_id, message)

print(response.getResponse())
```