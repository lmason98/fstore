from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


class AzureStorage:

	url = "https://fstorelmason.blob.core.windows.net"
	credentials = DefaultAzureCredential()

	def __init__(self):
		self.client = BlobServiceClient(self.url, credential=self.credentials)

	def create_container(self, container_name):
		"""
		Creates a container if it does not exist
		"""
		container = self.client.get_container_client(container=container_name)

		if not container.exists():
			container.create_container()

	def upload_file(self, user, filename, file):
		blob_client = self.client.get_blob_client(container=user.username, blob=filename)
		blob_client.upload_blob(file)
