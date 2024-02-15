from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

class TokenObtainLifetimeSerializer(TokenObtainPairSerializer):
	"""
	Extend jwt login response to include account id
	"""
	@staticmethod
	def validate(attrs):
		"""
		Custom validation for correct error response to frontend
		"""
		try:
			# Valid username
			user = User.objects.get(username__iexact=attrs.get('username'))

			if user.check_password(attrs.get('password')):
				# Valid credentials passed, return tokens and account id
				token = RefreshToken.for_user(user)
				data = {
					'refresh': str(token),
					'access': str(token.access_token),
					'userId': user.id,
					'message': f'Successfully logged in {user}',
					'status': 'success'
				}
			else:
				# Valid password but invalid username passed, return error message
				data = {'message': f'Invalid password for {user}', 'status': 'error'}

		except User.DoesNotExist:
			# Invalid username passed, return error message
			data = {'message': 'No account with this username exists.', 'status': 'error'}

		return data