from rest_framework.response import Response
from rest_framework.views import APIView

from azure_storage.main import AzureStorage
from .models import Folder, Blob
from .serializers import FolderSerializer, BlobSerializer

az_storage = AzureStorage()


class BaseAPIView(APIView):

	def get_folder(self, name):
		if name == '/':
			folder = Folder.objects.get(owner_id=self.request.user.id, name=self.request.user.username)
		else:
			# Get last folder name
			name = list(filter(lambda v: v != '', name.split('/')))[-1]
			folder = Folder.objects.get(owner_id=self.request.user.id, name=name)

		return folder


class FolderView(BaseAPIView):

	def get(self, request, *args, **kwargs):
		"""
		Gets a list of folders and files with parent location
		"""
		location = request.GET.get('location')

		print('location :', location.split('/'))

		filter_args = {
			'owner_id': request.user.id,
			'parent': self.get_folder(location),
		}
		folders = FolderSerializer(Folder.objects.filter(**filter_args), many=True).data
		blobs = BlobSerializer(Blob.objects.filter(**filter_args), many=True).data

		return Response({'status': 'success', 'objects': folders + blobs})

	def post(self, request, *args, **kwargs):
		"""
		Create new folder
		"""
		folder_name = request.data.get('name')
		location = request.data.get('location')

		if not location:
			resp = {'status': 'error', 'message': 'Missing parent folder.'}
		elif Folder.objects.filter(owner_id=self.request.user.id, name=folder_name).count() > 0:
			resp = {'status': 'error', 'message': 'This folder already exists.'}
		else:
			data = {
				'owner_id': request.user.id,
				'parent': self.get_folder(location),
				'name': request.data['name'],
			}

			Folder.objects.create(**data)
			resp = {'status': 'success', 'message': 'New folder created.'}

		return Response(resp)

	@staticmethod
	def delete(request, *args, **kwargs):
		"""
		Delete folder and all sub content
		"""
		obj_id = kwargs.get('id')

		try:
			Folder.objects.get(owner_id=request.user.id, id=obj_id).delete()
			resp = {'status': 'success', 'message': 'Folder deleted.'}
		except Folder.DoesNotExist:
			resp = {'status': 'error', 'message': 'Folder not found.'}

		return Response(resp)


class FileView(BaseAPIView):
	"""
	Handle file upload
	"""

	def post(self, request, *args, **kwargs):
		location = request.data.get('location')
		file = request.data.get('files')

		print('file :', file, type(file), f'size={file.size}')
		location = self.get_folder(location)

		print('parent folder :', location)

		if not location:
			resp = {'status': 'error', 'message': 'Missing parent folder.'}
		elif Blob.objects.filter(owner_id=self.request.user.id, parent=location, name=str(file)).count() > 0:
			resp = {'status': 'error', 'message': 'This file already exists.'}
		elif not file:
			resp = {'status': 'error', 'message': 'Missing file.'}
		else:
			data = {
				'owner_id': request.user.id,
				'parent': location,
				'name': str(file),
				'size': file.size,
			}
			# az_storage.upload_file(str(file), file)
			blob = Blob.objects.create(**data)

			resp = {'status': 'success', 'message': f'Successfully uploaded {str(file)}'}

		return Response(resp)

	@staticmethod
	def delete(request, *args, **kwargs):
		"""
		Delete file
		"""
		obj_id = kwargs.get('id')

		print('obj id :', obj_id)
		for b in Blob.objects.all():
			print('b :', b, b.id)

		try:
			Blob.objects.get(owner_id=request.user.id, id=obj_id).delete()
			resp = {'status': 'success', 'message': 'File deleted.'}
		except Blob.DoesNotExist:
			resp = {'status': 'error', 'message': 'File not found.'}

		return Response(resp)
