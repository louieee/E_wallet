from .models import User


# this allows the user to be authenticated using email and password
class EmailAuthBackend:
	def authenticate(self, request, username, password):
		try:
			user = User.objects.get(email=username)
			success = user.check_password(password)
			if success:
				return user
		except User.DoesNotExist:
			pass
		return None

	def get_user(self, uid):
		try:
			return User.objects.get(pk=uid)
		except:
			return None
