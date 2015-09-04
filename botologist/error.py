import logging
log = logging.getLogger(__name__)

from email.mime.text import MIMEText
import os
import pwd
import subprocess
import traceback


def send_email(email):
	p = subprocess.Popen(['/usr/sbin/sendmail', '-t', '-oi'],
		stdin=subprocess.PIPE)
	p.communicate(email.as_string().encode('utf-8'))


def format_error(message=None):
	long_msg = traceback.format_exc().strip()
	# should get the exception type and message
	medium_msg = long_msg.split('\n')[-1]
	short_msg = 'Uncaught exception'

	if isinstance(message, str):
		short_msg = message.split('\n')[0]
	medium_msg = '{} - {}'.format(short_msg, medium_msg)

	return medium_msg, long_msg


class ErrorHandler:
	def __init__(self, bot):
		self.bot = bot

	def handle_error(self, message=None):
		medium_msg, long_msg = format_error(message)

		log.exception(medium_msg)

		self.bot._send_msg(medium_msg, self.bot.get_admin_nicks())

		email = MIMEText(long_msg)
		user = pwd.getpwuid(os.getuid())[0]
		email['From'] = user
		email['To'] = user
		email['Subject'] = '[botologist] ' + medium_msg
		send_email(email)

		log.info('Sent email with exception information to %s', user)
