from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient


class AzureStorage:

	url = "https://fstorelmason.blob.core.windows.net"
	credentials = DefaultAzureCredential()

	def __init__(self):
		self.client = BlobServiceClient(self.url, credential=self.credentials,
										)

	def create_container(self, container_name):
		"""
		Creates a container if it does not exist
		"""
		container = self.client.get_container_client(container=container_name)

		if not container.exists():
			container.create_container()

	def delete_container(self, container_name):
		container = self.client.get_container_client(container=container_name)

		if container.exists():
			container.delete_container()

	def get_container(self, container_name):
		container = self.client.get_container_client(container=container_name)

		if container.exists():
			return container

	def get_blob(self, user, filename):
		return self.client.get_blob_client(container=user.username, blob=filename)

	def upload_file(self, user, filename, file_data):
		blob = self.get_blob(user, filename)

		print('pre upload 2')
		blob.upload_blob(file_data)

	def download_file(self, user, filename):
		blob = self.get_blob(user, filename)
		file_data = blob.download_blob().readall()

		return file_data

	def delete_file(self, user, filename):
		blob = self.get_blob(user, filename)

		try:
			blob.delete_blob()
		except ResourceNotFoundError:
			pass

	def copy_file(self, user, filename, new_filename):
		source_blob = self.get_blob(user, filename)
		dest_blob = self.get_blob(user, new_filename)

		dest_blob.upload_blob_from_url(source_url=source_blob.url, overwrite=False)
