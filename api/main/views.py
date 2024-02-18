from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Folder, Blob
from .serializers import FolderSerializer, BlobSerializer


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
	Handle file upload, download, delete, etc.
	"""

	content_types = {
		'txt': 'text/plain',
		'png': 'image/png',
		'jpg': 'image/jpg',
		'jpeg': 'image/jpg',
		'pdf': 'application/pdf',
	}

	def get(self, request, *args, **kwargs):
		"""
		Downloads a file
		"""
		obj_id = kwargs.get('id')

		try:
			blob = Blob.objects.get(owner_id=request.user.id, id=obj_id)
			ext = blob.name.split('.')[-1]
			file_data = blob.download()

			resp = HttpResponse(file_data, content_type=self.content_types[ext.lower()])
			resp['Content-Disposition'] = f'attachment; filename={blob.name}'
		except Blob.DoesNotExist:
			resp = Response({'status': 'error', 'message': 'File not found.'})

		return resp

	def post(self, request, *args, **kwargs):
		location = request.data.get('location')
		file_data = request.data.get('files')

		location = self.get_folder(location)

		if not location:
			resp = {'status': 'error', 'message': 'Missing parent folder.'}
		elif not file_data:
			resp = {'status': 'error', 'message': 'Missing file.'}
		else:
			data = {
				'owner_id': request.user.id,
				'parent': location,
				'name': str(file_data),
			}
			existing = Blob.objects.filter(**data).count()

			data['size'] = file_data.size
			if existing > 0:
				split_name = data['name'].split('.')
				data['name'] = f'{split_name[0]}({existing}).{split_name[1]}'

			blob = Blob.objects.create(**data)
			blob.upload(file_data)

			resp = {'status': 'success', 'message': f'Successfully uploaded {str(file_data)}'}

		return Response(resp)

	@staticmethod
	def delete(request, *args, **kwargs):
		obj_id = kwargs.get('id')

		try:
			Blob.objects.get(owner_id=request.user.id, id=obj_id).delete()
			resp = {'status': 'success', 'message': 'File deleted.'}
		except Blob.DoesNotExist:
			resp = {'status': 'error', 'message': 'File not found.'}

		return Response(resp)
