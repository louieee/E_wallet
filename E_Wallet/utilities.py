import json
import os
import smtplib
import socket
from datetime import timedelta

from decouple import config
from django.contrib import auth
from django.utils import timezone
import pyotp
from django.template.loader import render_to_string
from django.utils.datetime_safe import datetime
from django.utils.html import strip_tags


def send_mail(user, title, message, to, code=None, attachments=None, data=None):
	try:
		sender = config('SENDER_EMAIL')
		password = config('SENDER_PASSWORD')
		server = smtplib.SMTP(f"{config('SERVER')}: {config('PORT')}")
		server.starttls()
		server.login(sender, password)
		msg_list = str(message).split('.')
		context = {"message": msg_list, "subject": title, "user": user}
		if code is not None:
			context['code'] = code
		if data is not None:
			context['data'] = data

		html_message = render_to_string('Account/mailer.html', context=context)
		plain_message = strip_tags(html_message)
		# The email body for recipients with non-HTML email clients.
		body_text = plain_message
		# The HTML body of the email.
		body_html = html_message
		charset = "utf-8"
		from email.mime.multipart import MIMEMultipart
		msg = MIMEMultipart('mixed')
		# Add subject, from and to lines.
		msg['Subject'] = title
		msg['From'] = f"{config('APP_NAME')}<{config('SENDER_EMAIL')}>"
		if not isinstance(to, list):
			msg['To'] = to
		msg_body = MIMEMultipart('alternative')
		from email.mime.text import MIMEText
		textpart = MIMEText(body_text.encode(charset), 'plain', charset)
		htmlpart = MIMEText(body_html.encode(charset), 'html', charset)
		# Add the text and HTML parts to the child container.
		msg_body.attach(textpart)
		msg_body.attach(htmlpart)
		# Define the attachment part and encode it using MIMEApplication.
		msg.attach(msg_body)

		if attachments is not None:
			from email.mime.application import MIMEApplication
			for i in attachments:
				att = MIMEApplication(open(i['filename'], 'rb').read())
				att.add_header('Content-Disposition', 'attachment', filename=i['filename'])
				if os.path.exists(i['filename']):
					pass
				else:
					pass
				msg.attach(att)
		server.sendmail(f'{sender}', msg['to'], msg.as_string())
		server.quit()
	except (socket.gaierror, smtplib.SMTPAuthenticationError) as e:
		print(e)


def get_token():
	token = pyotp.TOTP(pyotp.random_base32()).now()
	return token


def prepare_cache_key(email):
	from Account.models import Cache
	pin = get_token()
	key_ = f"{email}_{pin}"
	if Cache.get(key_) is None:
		return pin, key_
	prepare_cache_key(email)


def send_verification_mail(email, type_, return_page=None, new_email=None):
	from Account.models import User, Cache
	user = User.objects.get(email=email)
	key_ = prepare_cache_key(email)
	data = json.dumps({"pin": key_[0], "return_page": return_page, 'code': key_[1], "email": new_email}, )
	key = key_[1]
	Cache.set(key, data)
	message = f"The number below is your pin for your {str(type_).lower()} " \
			  f"verification. This pin will last for {config('CACHE_EXPIRY')} minutes."
	if new_email:
		send_mail(user=user, title=f'{str(type_).title()}',
				  message=message, to=new_email, code=key_[0])
	else:
		send_mail(user=user, title=f'{str(type_).title()}',
				  message=message, to=email, code=key_[0])
		return


def lock(email, request=None):
	from Account.models import User
	user = User.objects.get(email=email)
	multiplier = user.multiplier
	trial = user.trial
	if request:
		auth.logout(request)
	if trial < 2:
		user.trial = trial + 1
		user.save()
		return
	elif trial == 2:
		user.multiplier = multiplier + 1
		user.trial = 1
		user.lock_time = datetime.now() + timedelta(minutes=(multiplier+1))
		user.save()
		return


def open_lock(email, final=None):
	from Account.models import User
	user = User.objects.get(email=email)
	if user.lock_time is None:
		return
	user.trial = 0
	user.lock_time = None
	if final:
		user.multiplier = 0
	user.save()
	return


def check_lock(user):
	if user.lock_time is None:
		return None
	print(user.lock_time.strftime("%b %d %Y %H:%M:%S"))
	print(datetime.now().strftime("%b %d %Y %H:%M:%S"))
	seconds = int((user.lock_time - datetime.now()).total_seconds())
	print(seconds)
	if seconds <= 0:
		return None
	if 0 < seconds < 60:
		return f'{seconds} seconds'
	elif 60 <= seconds < 3600:
		return f'{seconds} minute(s), {seconds % 60} second(s)'
	elif 3600 <= seconds < 86400:
		return f'{seconds // 3600} hour(s)'
	else:
		return f'{seconds // 86400} day(s)'


def get_countries():
	return 'Afghanistan', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua And Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia And Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic Of', 'Cook Islands', 'Costa Rica', "Cã”Te D'Ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guinea', 'Guyana', 'Haiti', 'Heard Island And Mcdonald Islands', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic Of', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People'S Republic Of", 'Korea, Republic Of', 'Kuwait', 'Kyrgyzstan', "Lao People'S Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libyan Arab Jamahiriya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, The Former Yugoslav Republic Of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States Of', 'Moldova, Republic Of', 'Monaco', 'Mongolia', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'Netherlands Antilles', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Rã‰Union', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Helena', 'Saint Kitts And Nevis', 'Saint Lucia', 'Saint Pierre And Miquelon', 'Saint Vincent And The Grenadines', 'Samoa', 'San Marino', 'Sao Tome And Principe', 'Saudi Arabia', 'Senegal', 'Serbia And Montenegro', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia And South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Svalbard And Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province Of China', 'Tajikistan', 'Tanzania, United Republic Of', 'Thailand', 'Timor', 'Togo', 'Tokelau', 'Tonga', 'Trinidad And Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks And Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis And Futuna', 'Western Sahara', 'Yemen', 'Zimbabwe'


def flash(request, message, status):
	"""
	This function sets the variables for the alert on a page.
	:param request: The HTTP request
	:param message: The message to be displayed on the alert bar.
	:param status: The status e.g warning, success or danger
	:param icon: The icon to be displayed
	:return: it returns nothing
	"""
	request.session['message'] = message
	request.session['status'] = status
	return


def display(request):
	"""
	This function returns the message for an alert.
	:param request: HTTP request
	:return: This returns a list containing the message, the status and the icon.
	"""
	if 'message' in request.session:
		message = request.session['message']
		status = request.session['status']
		del request.session['message'], request.session['status']
		return {"message": message, "status": status}
	return None


def check_unn_email(email):
	extracts = str(email).lower().split('@')
	if extracts[1] != 'unn.edu.ng':
		return None
	remaining = extracts[0].split('.')
	if remaining.__len__() < 2:
		return None
	if remaining.__len__() > 1 and str(remaining[1]).isdigit():
		return None
	first_name = remaining[0]
	if remaining.__len__() == 2:
		last_name = remaining[1]
		return first_name, last_name, ''
	if remaining.__len__() == 3:
		last_name = remaining[1]
		reg_no = remaining[2]
		return first_name, last_name, reg_no, ''


import csv
import json


# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath):
	# create a dictionary
	data = []

	# Open a csv reader called DictReader
	with open(csvFilePath, encoding='utf-8') as csvf:
		csvReader = csv.DictReader(csvf)

		# Convert each row into a dictionary
		# and add it to data
		for rows in csvReader:
			# Assuming a column named 'No' to
			# be the primary key
			data.append(rows['name'])

	# Open a json writer, and use the json.dumps()
	# function to dump data
	return data


# Call the make_json function

banks = make_json(config('BANK_DIR'))