import os
from abc import ABC, abstractmethod
from totoapicontroller.TotoLogger import TotoLogger
from totoapicontroller.model.singleton import singleton
from google.cloud import secretmanager

class TotoConfig(ABC): 
    
    jwt_key: str
    
    def __init__(self) -> None:
        
        self.logger = TotoLogger(self.get_api_name())
        
        self.logger.log("INIT", "Loading Configuration..")
        
        self.jwt_key = self.access_secret_version("jwt-signing-key")
        
    
    @abstractmethod
    def get_api_name(self) -> str: 
        pass
    
    
    def access_secret_version(self, secret_id, version_id="latest"):
        """
        Retrieves a Secret on GCP Secret Manager
        """

        project_id = os.environ["GCP_PID"]

        # Create the Secret Manager client
        client = secretmanager.SecretManagerServiceClient()

        # Build the resource name of the secret version
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

        # Access the secret version
        response = client.access_secret_version(name=name)

        # Extract the secret payload
        payload = response.payload.data.decode("UTF-8")

        return payload
