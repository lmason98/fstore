from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class BaseAPICase(APITestCase):
	""" Base test case for api tests """

	def setUp(self):
		# Create new user
		self.user = User.objects.create(email='test@gmail.com', username='testuser')
		self.user.set_password('testtest')
		self.user.save()

		# Login test client
		self.client.login(username='testuser', password='testtest')
		self.do_auth()

	def tearDown(self):
		self.user.delete()
		self.token = None
		self.refresh_token = None

	def do_auth(self):
		url = '/api/auth/token/obtain'
		resp = self.query_api(self.client.post, url, data={'username': 'testuser', 'password': 'testtest'})

		self.token = resp.data.get('access')
		self.refresh_token = resp.data.get('refresh')
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

		return resp

	@staticmethod
	def query_api(method, url, data=None, file=False):
		""" Api query wrapper """
		if data is not None:
			if not file:
				response = method(url, data, format='json')
			else:
				response = method(url, data)
		else:
			response = method(url)

		return response


class APIAuthCase(BaseAPICase):
	""" This tests authorization with the api """
	def test_do_auth_success(self):
		response = self.do_auth()

		self.assertEqual(response.data.get('status'), 'success')
		self.assertEqual(response.data.get('userId'), self.user.id)
		self.assertEqual(response.data.get('message'), f'Successfully logged in {self.user.username}')

	def test_login_fail_username(self):
		url = '/api/auth/token/obtain'
		response = self.query_api(self.client.post, url, data={'username': 'testt', 'password': 'test'})

		self.assertEqual(response.data.get('status'), 'error')
		self.assertEqual(response.data.get('message'), 'No account with this username exists.')

	def test_login_fail_password(self):
		url = '/api/auth/token/obtain'
		response = self.query_api(self.client.post, url, data={'username': 'testuser', 'password': 'test'})

		self.assertEqual(response.data.get('status'), 'error')
		self.assertEqual(response.data.get('message'), f'Invalid password for {self.user.username}')

	def test_check_auth(self):
		url = '/api/auth/token/check'
		response = self.query_api(self.client.get, url)

		self.assertEqual(response.data.get('status'), 'success')

	def test_auth_refresh(self):
		url = '/api/auth/token/refresh'
		resp = self.query_api(self.client.post, url, {'refresh': self.refresh_token})

		self.assertNotEqual(resp.data.get('access'), self.token)
		self.assertNotEqual(resp.data.get('refresh'), self.refresh_token)
