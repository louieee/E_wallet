from django.db import models


# Create your models here.


class Wallet(models.Model):
	user = models.OneToOneField('Account.User', on_delete=models.CASCADE)
	beneficiaries = models.ManyToManyField('Wallet.Wallet')

	def deposit_transactions(self):
		return Transaction.objects.filter(type=Transaction.Choice.deposit, sender=self.user)

	def pending_deposits(self):
		return self.deposit_transactions().filter(status=Transaction.Choice.pending)

	def failed_deposits(self):
		return self.deposit_transactions().filter(status=Transaction.Choice.failed)

	def successful_deposits(self):
		return self.deposit_transactions().filter(status=Transaction.Choice.success)

	def withdrawal_transactions(self):
		return Transaction.objects.filter(type=Transaction.Choice.withdrawal, sender=self.user)

	def pending_withdrawals(self):
		return self.withdrawal_transactions().filter(status=Transaction.Choice.pending)

	def failed_withdrawals(self):
		return self.withdrawal_transactions().filter(status=Transaction.Choice.failed)

	def successful_withdrawals(self):
		return self.withdrawal_transactions().filter(status=Transaction.Choice.success)

	def transfer_transactions(self):
		return Transaction.objects.filter(type=Transaction.Choice.transfer, sender=self.user)

	def pending_transfers(self):
		return self.transfer_transactions().filter(status=Transaction.Choice.pending)

	def failed_transfers(self):
		return self.transfer_transactions().filter(status=Transaction.Choice.failed)

	def successful_transfers(self):
		return self.transfer_transactions().filter(status=Transaction.Choice.success)

	def received_transfers(self):
		return Transaction.objects.filter(type=Transaction.Choice.transfer, receiver=self.user,
										  status=Transaction.Choice.success)

	def total_deposits(self):
		return sum(x.total_amount() for x in self.successful_deposits())

	def total_sent_transfers(self):
		return sum(x.total_amount() for x in self.successful_transfers())

	def total_received_transfers(self):
		return sum(x.total_amount() for x in self.received_transfers())

	def total_withdrawals(self):
		return sum(x.total_amount() for x in self.successful_withdrawals())

	def account_balance(self):
		return self.total_deposits() + self.total_received_transfers() - self.total_sent_transfers() - self.total_withdrawals()


class Transaction(models.Model):
	class Choice:
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
		return self.amount - self.fee

	def confirm(self):
		self.status = self.Choice.success
		self.save()