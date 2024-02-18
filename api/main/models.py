from django.db import models
from django.conf import settings

from azure_storage.main import AzureStorage


az_storage = AzureStorage()

class CreateUpdatedMixin(models.Model):

	created_at = models.DateTimeField(blank=False, null=False, auto_now_add=True)
	updated_at = models.DateTimeField(blank=False, null=False, auto_now=True)
	class Meta:
		abstract = True


class Folder(CreateUpdatedMixin):
	"""
	Azure does not support hierarchical containers, they are stored as a flat list.
	This creates a hierarchical folder like storage system.
	"""
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	parent = models.ForeignKey('self', null=True, related_name='child_containers', on_delete=models.CASCADE)
	name = models.CharField(blank=False, null=False, max_length=255)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):

		# On create, if no parent (root) folder, create container in azure storage
		if not self.pk and not self.parent and self.owner.username != 'testuser':
			az_storage.create_container(self.name)

		super().save(*args, **kwargs)

	def delete(self, *args, **kwargs):

		# On user delete, delete container in azure storage
		az_storage.delete_container(self.name)

		super().delete(*args, **kwargs)

	def is_user_root(self):
		return self.owner.username == self.name

	def path(self):
		path = [self.name]

		cur = self
		while not cur.parent.is_user_root():
			cur = cur.parent
			path.append(cur.name)

		return '/'.join(list(reversed(path))) + '/'


class Blob(CreateUpdatedMixin):
	"""
	Corresponds to a blob stored in azure
	"""
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	parent = models.ForeignKey(Folder, null=False, related_name='child_files', on_delete=models.CASCADE)
	name = models.CharField(blank=False, null=False, max_length=255)
	size = models.IntegerField(blank=False, null=False)

	def delete(self, *args, **kwargs):
		az_storage.delete_file(self.owner, self.name)

		super().delete(*args, **kwargs)

	def upload(self, file_data):
		az_storage.upload_file(self.owner, self.path_name(), file_data)

	def download(self):
		file_data = az_storage.download_file(self.owner,  self.path_name())

		return file_data

	def path_name(self):
		"""
		Return pathname for the azure storage upload/download
		"""
		# If not root dir, add path to the name
		if not self.parent.is_user_root():
			name = self.parent.path() + self.name
		else:
			name = self.name

		return name
