from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.authentication import JWTAuthentication

from main.models import Folder
from .serializers import TokenObtainLifetimeSerializer


class TokenObtainView(TokenViewBase):
	"""
    Extend token obtain view to include extended serializer for user ID
    """
	serializer_class = TokenObtainLifetimeSerializer

	def post(self, request, *args, **kwargs):
		"""
		On user login, check if user root container exists, create it if not
		"""
		resp = super().post(request, *args, **kwargs)
		user_id, user_name = resp.data.get('userId', None), resp.data.get('userName', None)

		if user_id and user_name:
			try:
				Folder.objects.get(owner_id=user_id, name=user_name)
			except Folder.DoesNotExist:
				Folder.objects.create(owner_id=user_id, name=user_name)

		return resp


class TokenCheckPairView(APIView):
	permission_classes = ()
	authentication_classes = ()

	@staticmethod
	def get(request, *args, **kwargs):
		authenticator = JWTAuthentication()

		authed = authenticator.authenticate(request)

		if authed:
			resp = Response({'status': 'success'})
		else:
			resp = Response({'status': 'error'})

		return resp