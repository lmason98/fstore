from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from azure_storage.main import AzureStorage
from .models import Folder, Blob
from .serializers import FolderSerializer, BlobSerializer


az_storage = AzureStorage()


class BaseAPIView(APIView):

	def get_folder(self, name):
		try:
			if name == '/':
				folder = Folder.objects.get(owner_id=self.request.user.id, name=self.request.user.username)
			else:
				# Get last folder name
				name = list(filter(lambda v: v != '', name.split('/')))[-1]
				folder = Folder.objects.get(owner_id=self.request.user.id, name=name)
		except Folder.DoesNotExist:
			folder = None

		return folder


class FolderView(BaseAPIView):

	def get(self, request, *args, **kwargs):
		"""
		Gets a list of folders and files with parent location
		"""
		location = request.GET.get('location')

		folder = self.get_folder(location)

		if folder:
			filter_args = {
				'owner_id': request.user.id,
				'parent': folder,
			}
			folders = FolderSerializer(Folder.objects.filter(**filter_args), many=True).data
			blobs = BlobSerializer(Blob.objects.filter(**filter_args), many=True).data
			resp = {'status': 'success', 'objects': folders + blobs, 'options': self.get_folder_options()}
		else:
			resp = {'status': 'error', 'message': 'Folder not found'}

		return Response(resp)

	def get_folder_options(self):
		"""
		Gets folder names owned by current user for copy/move select options
		"""
		folders = Folder.objects.filter(owner_id=self.request.user.id)
		return [{'value': f.id, 'text': f.option_name()} for f in folders]

	def post(self, request, *args, **kwargs):
		"""
		Create new folder
		"""
		folder_name = request.data.get('name')
		location = request.data.get('location')

		folder = self.get_folder(location)

		if folder:
			if not location:
				resp = {'status': 'error', 'message': 'Missing parent folder.'}
			elif Folder.objects.filter(owner_id=self.request.user.id, name=folder_name).count() > 0:
				resp = {'status': 'error', 'message': 'This folder already exists.'}
			else:
				data = {
					'owner_id': request.user.id,
					'parent': folder,
					'name': request.data['name'],
				}

				Folder.objects.create(**data)
				resp = {'status': 'success', 'message': 'New folder created.'}
		else:
			resp = {'status': 'error', 'message': 'Folder not found'}

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
			resp = {'status': 'error', 'message': 'Folder not found.'}
		elif not file_data:
			resp = {'status': 'error', 'message': 'Missing file.'}
		elif file_data.size > 1024 * 1024 * 5:
			resp = {'status': 'error', 'message': 'File too large. (Max 5 MB)'}
		else:
			data = {
				'owner_id': request.user.id,
				'parent': location,
				'name': self.validate_name_count(location, str(file_data)),
				'size': file_data.size
			}

			blob = Blob.objects.create(**data)
			print('pre upload')
			blob.upload(file_data)

			resp = {'status': 'success', 'message': f'Successfully uploaded {str(file_data)}'}

		return Response(resp)

	def patch(self, request, *args, **kwargs):
		"""
		Copy or move a file
		"""
		obj_id = kwargs.get('id')
		location = request.data.get('location')
		copy = request.data.get('copy')

		if location:
			try:
				dest_folder = Folder.objects.get(owner_id=request.user.id, id=location)
			except Folder.DoesNotExist:
				return {'status': 'error', 'message': 'Folder not found.'}

			try:
				blob = Blob.objects.get(owner_id=request.user.id, id=obj_id)

				data = {
					'owner_id': request.user.id,
					'parent': dest_folder,
					'name': self.validate_name_count(dest_folder, blob.name),
					'size': blob.size
				}

				new_blob = Blob.objects.create(**data)
				az_storage.copy_file(request.user, blob.path_name(), new_blob.path_name())

				# Move, delete original file
				if not copy:
					blob.delete()  # This also deletes blob in az storage
					message = 'Successfully moved file!'
				else:
					message = 'Successfully copied file!'

				resp = {'status': 'success', 'message': message}

			except Blob.DoesNotExist:
				resp = {'status': 'error', 'message': 'File not found.'}
		else:
			resp = {'status': 'error', 'message': 'No location provided.'}

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

	def validate_name_count(self, location, name):
		split_name = name.split('.')
		existing = Blob.objects.filter(owner_id=self.request.user.id,
									   parent=location,
									   name__startswith=split_name[0],
									   name__endswith=split_name[1]).count()

		if existing > 0:
			name = f'{split_name[0]}({existing}).{split_name[1]}'

		return name
