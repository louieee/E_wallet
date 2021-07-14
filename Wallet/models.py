from django.db import models


# Create your models here.
from django.db.models import Q


class Wallet(models.Model):
    # this is a wallet class where a user stores all his transaction details
    user = models.OneToOneField('Account.User', on_delete=models.CASCADE)
    beneficiaries = models.ManyToManyField('Wallet.Wallet', blank=True)

    def __str__(self):
        return f'{self.user.__str__()} wallet'

    def owner(self):
        return self.user.__str__()

    def transactions(self):
        return Transaction.objects.filter(Q(sender=self) | Q(receiver=self)).order_by('-id')

    def deposit_transactions(self):
        # this returns all the user's deposit transactions
        return Transaction.objects.filter(type=Transaction.Choice.deposit, sender=self).order_by('-id')

    def pending_deposits(self):
        # this returns all the user's deposit transactions that are still pending
        return self.deposit_transactions().filter(status=Transaction.Choice.pending)

    def failed_deposits(self):
        # this returns all the user's deposit transactions that failed
        return self.deposit_transactions().filter(status=Transaction.Choice.failed)

    def successful_deposits(self):
        # this returns all the user's deposit transactions that were successful.
        return self.deposit_transactions().filter(status=Transaction.Choice.success)

    def withdrawal_transactions(self):
        # this returns all the user's withdrawal transactions
        return Transaction.objects.filter(type=Transaction.Choice.withdrawal, sender=self).order_by('-id')

    def pending_withdrawals(self):
        # this returns all the user's withdrawal transactions that are still pending
        return self.withdrawal_transactions().filter(status=Transaction.Choice.pending)

    def failed_withdrawals(self):
        # this returns all the user's withdrawal transactions that are failed
        return self.withdrawal_transactions().filter(status=Transaction.Choice.failed)

    def successful_withdrawals(self):
        # this returns all the user's withdrawal transactions that were successful.
        return self.withdrawal_transactions().filter(status=Transaction.Choice.success)

    def transfer_transactions(self):
        # this returns all the user's transfer transactions
        return Transaction.objects.filter(type=Transaction.Choice.transfer, sender=self).order_by('-id')

    def pending_transfers(self):
        # this returns all the user's transfer transactions that are still pending
        return self.transfer_transactions().filter(status=Transaction.Choice.pending)

    def failed_transfers(self):
        # this returns all the user's transfer transactions that failed.
        return self.transfer_transactions().filter(status=Transaction.Choice.failed)

    def successful_transfers(self):
        # this returns all the user's transfer transactions that were successful.
        return self.transfer_transactions().filter(status=Transaction.Choice.success)

    def received_transfers(self):
        # this returns all the user's received transfer transactions
        return Transaction.objects.filter(type=Transaction.Choice.transfer, receiver=self,
                                          status=Transaction.Choice.success).order_by('-id')

    def total_deposits(self):
        # this sums up all the user's successful deposit transactions
        return sum(x.total_amount() for x in self.successful_deposits())

    def total_sent_transfers(self):
        # this sums up all the user's successful transfer transactions
        return sum(x.total_amount() for x in self.successful_transfers())

    def total_received_transfers(self):
        # this sums up all the user's received transfer transactions
        return sum(x.total_amount() for x in self.received_transfers())

    def total_withdrawals(self):
        # this sums up all the user's successful withdrawal transactions
        return sum(x.total_amount() for x in self.successful_withdrawals())

    def account_balance(self):
        # this calculates the user's current account balance
        return self.total_deposits() + self.total_received_transfers() - self.total_sent_transfers() - self.total_withdrawals()


class Transaction(models.Model):
    # this is thr user's transaction class
    class Choice:
        # this is the choice class for fields that require selections
        deposit, withdrawal, transfer = range(3)
        transaction_type = (
            (deposit, 'Deposit'), (withdrawal, 'Withdrawal'), (transfer, 'Transfer')
        )
        pending, success, failed = range(3)
        transaction_status = (
            (pending, 'Pending'), (success, 'Success'), (failed, 'Failed')
        )

    type = models.PositiveSmallIntegerField(choices=Choice.transaction_type, default=Choice.deposit)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sender = models.ForeignKey('Wallet.Wallet', on_delete=models.CASCADE, related_name='sender', )
    receiver = models.ForeignKey('Wallet.Wallet', on_delete=models.SET_NULL, related_name='receiver', default=None,
                                 null=True, blank=True)
    source = models.ForeignKey('Account.Source', on_delete=models.SET_NULL, default=None, null=True, blank=True)
    fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.PositiveSmallIntegerField(choices=Choice.transaction_status, default=Choice.pending)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def total_amount(self):
        # this returns the final amount after the transaction fee has been added.
        return self.amount + self.fee

    def confirm(self):
        # this function confirms that a transaction is successful
        self.status = self.Choice.success
        self.save()

    def save(self, *args, **kwargs):
        t = Transaction.objects.filter(id=self.id).first()
        if t is not None and t.amount != self.amount:
            print('amount changed')
        super(Transaction, self).save(*args, **kwargs)

