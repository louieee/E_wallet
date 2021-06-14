from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# This is the user model
from django.utils import timezone


class User(AbstractUser):
	profile_picture = models.ImageField(upload_to='profile_pic')

	def __str__(self):
		return self.username

	def cards(self):
		return Card.objects.filter(wallet__user=self)

	def add_card(self, **kwargs):
		card = Card.objects.create(kwargs)
		card.wallet.user = self
		card.save()

	def fund_sources(self):
		return Source.objects.filter(wallet__user=self, type=Source.Choice.funding)

	def withdrawal_channels(self):
		return Source.objects.filter(wallet__user=self, type=Source.Choice.withdrawal)

	def add_source(self, **kwargs):
		source = Source.objects.create(kwargs)
		source.wallet.user = self
		source.save()


class Source(models.Model):
	class Choice:
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
	first_digits = models.CharField(max_length=5, default='')
	last_digits = models.CharField(max_length=5, default='')
	cvv = models.CharField(max_length=4, default='')
	expiry_date = models.DateField()
	wallet = models.ForeignKey('Wallet.Wallet', on_delete=models.CASCADE)

	def expired(self):
		return self.expiry_date < timezone.now()
