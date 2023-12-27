from typing import Optional

class Messages:

    '''
    Requesting and verifying message data of YandexGPT API.
    '''
    
    def __init__(self, system_message_text, user_message_text):
        
        self.system_message_text = system_message_text
        self.user_message_text = user_message_text

    def system(system_message: Optional[str] = None) -> None:
        return system_message

    def user(self):
        if not self.message_text:
            raise TypeError("It is necessary to specify a message.")
        else:
            return self.message_text