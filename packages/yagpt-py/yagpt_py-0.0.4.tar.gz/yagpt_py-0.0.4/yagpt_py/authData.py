class AuthData:

    '''
    Requesting and verifying authentication data of Yandex Cloud API.
    '''
    
    def __init__(self, iam_token, catalog_id) -> None:
        
        self.iam_token = iam_token
        self.catalog_id = catalog_id

    def Token(self) -> None:
        if not self.iam_token:
            raise TypeError("It is necessary to specify a IAM token.")
        else:
            return self.iam_token

    def CatalogID(self) -> None:
        if not self.catalog_id:
            raise TypeError("It is necessary to specify a Catalog ID.")
        else:
            return self.catalog_id