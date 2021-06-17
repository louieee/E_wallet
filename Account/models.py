from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# This is the user model
from django.utils import timezone


class User(AbstractUser):
	# this is the abstract user class which extends the normal user class and its attributes.
	profile_picture = models.ImageField(upload_to='profile_pic')

	def __str__(self):
		# this returns the name of the class
		return self.username

	def cards(self):
		# this returns all the user's cards
		return Card.objects.filter(wallet__user=self)

	def add_card(self, **kwargs):
		# this function helps a user to add card to his portfolio
		card = Card.objects.create(kwargs)
		card.wallet.user = self
		card.save()

	def fund_sources(self):
		# these are all the sources through which the user funds his wallet
		return Source.objects.filter(wallet__user=self, type=Source.Choice.funding)

	def withdrawal_channels(self):
		# these are all the accounts where the user withdraws money to
		return Source.objects.filter(wallet__user=self, type=Source.Choice.withdrawal)

	def add_source(self, **kwargs):
		# this function allows a user to add a new source be it, funding sources or withdrawal channels
		source = Source.objects.create(kwargs)
		source.wallet.user = self
		source.save()


class Source(models.Model):
	# this is the source class through which a user funds his wallet or withdraws from his wallet.
	class Choice:
		# this is a choice class for all fields regarding making a selection
		funding, withdrawal = range(2)
		source_type = (
			(funding, 'Funding'), (withdrawal, 'Withdrawal')
		)
		card, bank = range(2)
		source_channel = (
			(card, 'Card'), (bank, 'Bank')
		)

	type = models.PositiveSmallIntegerField(choices=Choice.source_type, default=Choice.funding)
	channel = models.PositiveSmallIntegerField(choices=Choice.source_channel, default=Choice.card)
	card = models.OneToOneField('Account.Card', on_delete=models.CASCADE, default=None, null=True, blank=True)
	bank_name = models.CharField(max_length=50, default=None, null=True, blank=True)
	account_number = models.CharField(max_length=50, default=None, null=True, blank=True)
	wallet = models.ForeignKey('Wallet.Wallet', on_delete=models.CASCADE)


class Card(models.Model):
	# this is a credit card class
	first_digits = models.CharField(max_length=5, default='')
	last_digits = models.CharField(max_length=5, default='')
	cvv = models.CharField(max_length=4, default='')
	expiry_date = models.DateField()
	wallet = models.ForeignKey('Wallet.Wallet', on_delete=models.CASCADE)

	def expired(self):
		# this function checks if a credit card is expired or not
		return self.expiry_date < timezone.now()
