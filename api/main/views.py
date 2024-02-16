from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.

class UploadView(APIView):
	"""
	Handle file upload
	"""

	@staticmethod
	def post(request, *args, **kwargs):

		print('upload view req :', request.data)

		return Response({'status': 'success'})
