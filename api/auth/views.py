from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import TokenObtainLifetimeSerializer


class TokenObtainView(TokenViewBase):
	"""
    Extend token obtain view to include extended serializer for account ID
    """
	serializer_class = TokenObtainLifetimeSerializer


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