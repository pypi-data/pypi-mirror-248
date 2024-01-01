from typing import Any, Optional

from oryks_google_oauth import GoogleDriveScopes, GoogleOAuth
from pydantic import BaseModel


class GoogleDrive(BaseModel):
    """Provides methods for interacting with the Drive API.

    This class acts as an interface to the Drive API, providing methods for interacting with
    the Drive API.

    Attributes
    ----------
    client_secret_file: str
        The path to the json file containing your authentication information.
    """

    client_secret_file: Optional[str] = None
    authenticated: Optional[bool] = False
    drive_client: Optional[Any] = None

    def authenticate(self, client_secret_file: Optional[str] = None) -> None:
        """Authenticate the requests made to drive.

        Used to generate the credentials that are used when authenticating requests to drive.

        Parameters
        ----------
        client_secret_file: str
            The path to clients secret json file from Google

        Raises
        ------
        ValueError:
            When the client secrets file is not provided
        FileNotFoundError:
            When the secrets file path is not found
        """
        if client_secret_file:
            self.client_secret_file = client_secret_file
        if not self.client_secret_file:
            raise ValueError('The client secret file must be provided.')
        api_service_name: str = 'drive'
        api_version: str = 'v3'
        credentials_dir: str = '.drive_credentials'
        scopes: list[str] = [
            GoogleDriveScopes.metadata.value,
            GoogleDriveScopes.drive.value,
            GoogleDriveScopes.files.value,
            GoogleDriveScopes.activity.value,
        ]
        oauth: GoogleOAuth = GoogleOAuth(
            secrets_file=self.client_secret_file,
            scopes=scopes,
            api_service_name=api_service_name,
            api_version=api_version,
            credentials_dir=credentials_dir,
        )
        self.drive_client = oauth.authenticate_google_server()
        return self.drive_client
