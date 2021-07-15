import json
from datetime import timedelta

from decouple import config
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# This is the user model
from django.utils import timezone


class User(AbstractUser):
    # this is the abstract user class which extends the normal user class and its attributes.
    is_active = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pic')
    lock_time = models.DateTimeField(null=True)
    trial = models.SmallIntegerField(default=0)
    multiplier = models.SmallIntegerField(default=0)

    def __str__(self):
        # this returns the name of the class
        return f'{self.first_name} {self.last_name}'

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
        return Source.objects.filter(wallet__user=self, type=Source.Choice.withdrawal).order_by('-id')

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

    def __str__(self):
        # this returns the string representation of this class object
        if self.channel == self.Choice.card:
            return self.card.__str__()
        else:
            return self.bank_name


class Card(models.Model):
    # this is a credit card class
    first_digits = models.CharField(max_length=5, default='')
    last_digits = models.CharField(max_length=5, default='')
    cvv = models.CharField(max_length=4, default='')
    expiry_date = models.DateField()
    wallet = models.ForeignKey('Wallet.Wallet', on_delete=models.CASCADE)

    def __str__(self):
        # this returns the string representation of this class object
        return f'{self.first_digits} **** **** {self.last_digits}'

    def expired(self):
        # this function checks if a credit card is expired or not
        return 'Expired' if self.expiry_date < timezone.now().date() else 'Valid'


class Cache(models.Model):
    # this is a persistent storage to store data such as pins for later retrieval and deletion
    key = models.CharField(max_length=50, default='')
    data = models.TextField(default='{}')
    date_created = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    @staticmethod
    def set(key, data=None):
        # this method allows one to save data to the cache
        try:
            cache = Cache.objects.get(key=key)
            if data is not None:
                cache.data = data
                cache.save()
        except Cache.DoesNotExist:
            if data is not None:
                Cache.objects.create(key=key, data=data)
            else:
                Cache.objects.create(key=key)

    @staticmethod
    def get(key, object_=False):
        # this method allows one retrieve data from the cache and delete after use
        try:
            cache = Cache.objects.get(key=key)
            if cache.expired():
                cache.delete()
                return None
            if object_:
                return cache
            return json.loads(cache.data)
        except Cache.DoesNotExist:
            cache = Cache.objects.filter(key__istartswith=key).last()
            if cache is not None:
                if cache.expired():
                    cache.delete()
                    return None
                if object_:
                    return cache
                return json.loads(cache.data)
            else:
                return None

    @staticmethod
    def delete_(key):
        # this allows one to delete a particular cache instance
        try:
            cache = Cache.get(key=key, object_=True)
            if cache is not None:
                cache.delete()
            return
        except Cache.DoesNotExist:
            return

    def save(self, *args, **kwargs):
        # this method saves the cache instance
        if self.date_created is None:
            self.expiry_date = timezone.now() + timedelta(minutes=int(config('CACHE_EXPIRY')))
        super(Cache, self).save(*args, **kwargs)

    def expired(self):
        # this method checks if a cache instance has expired
        return self.expiry_date <= timezone.now()
