from django.contrib.auth.models import User
from django.test import TestCase

from azure_storage.main import AzureStorage
from main.models import Folder, Blob

# Create your tests here.
az_storage = AzureStorage()

class MainTestCase(TestCase):
	"""
	Tests functionality with azure containers/files

	Set username to testuser to not create containers
	"""

	def test_azure_container_create_delete(self):

		user = User.objects.create(username='testuser1', email='t@g.com')

		self.assertIsNone(az_storage.get_container(user.username))
		folder = Folder.objects.create(owner=user, name=user.username)  # On root folder create, create azure container
		self.assertEqual(az_storage.get_container(user.username).container_name, user.username)
		folder.delete()  # On folder delete, delete azure container
		self.assertIsNone(az_storage.get_container(user.username))

	def test_azure_blob_upload_download(self):
		"""
		Blob in azure should be deleted when blob object is deleted
		"""
		file_data = b'Hello World!'

		user = User.objects.create(username='testuser2', email='t@g.com')
		folder = Folder.objects.create(owner=user, name=user.username)  # Create root folder
		blob = Blob.objects.create(owner=user, parent=folder, name='test.txt', size=len(file_data))

		blob.upload(file_data)  # Creates and uploads to az blob
		self.assertTrue(az_storage.get_blob(user, 'test.txt').exists())

		downloaded_file_data = blob.download()

		blob.delete()  # Deletes az blob as well
		self.assertFalse(az_storage.get_blob(user, 'test.txt').exists())

		folder.delete()

	def test_folder_path(self):

		user = User.objects.create(username='testuser', email='t@g.com')
		f1 = Folder.objects.create(owner=user, name='f1')
		f2 = Folder.objects.create(owner=user, name='f2', parent=f1)
		f3 = Folder.objects.create(owner=user, name='f3', parent=f2)

		self.assertTrue(f3.path(), 'f1/f2/f3/')
		self.assertTrue(f2.path(), 'f1/f2/')
		self.assertTrue(f1.path(), 'f1/')
