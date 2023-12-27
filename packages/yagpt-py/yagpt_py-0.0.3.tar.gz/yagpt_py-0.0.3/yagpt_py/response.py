import requests
import json
from typing import Optional

class Response():
    
    """
    Generating a request and returning a response from the YandexGPT API.
    """
    
    def __init__(self, token, id, message):
        
        self.token = token
        self.id = id
        self.message = message
    
    def getResponse(
        self,
        system_message: Optional[str] = None,
        max_tokens: Optional[int] = 2000,
        stream: Optional[bool] = False,
        temperature: Optional[float] = 0.6,
    ) -> None:
        
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "x-folder-id": f"{self.id}",
        }

        data = {
            "modelUri": f"gpt://{self.id}/yandexgpt-lite",
            "completionOptions": {
                "stream": stream,
                "temperature": temperature,
                "maxTokens": max_tokens,
            },
            "messages": [
                {"role": "system", "text": f"{system_message}"},
                {"role": "user", "text": f"{self.message}"},
            ],
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        return response.text
