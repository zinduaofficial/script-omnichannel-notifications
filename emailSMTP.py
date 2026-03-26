import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(dotenv_path=".env")




if __name__ == "__main__":
	# Example usage
	send_email(
		to="cyrilmichino@gmail.com",
		subject="Test Email",
		message="This is a test message from the SMTP script."
	)