import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

'''
def _read_bool_env(var_name: str, default: bool = False) -> bool:
	value = os.getenv(var_name)
	if value is None:
		return default
	return value.strip().lower() in {"1", "true", "yes", "on"}
'''

def send_email(to: str, subject: str, message: str, html: str | None = None) -> None:
	"""Send a transactional email using SMTP credentials from .env."""
	smtp_host = os.getenv("SMTP_HOST")
	smtp_port = os.getenv("SMTP_PORT", "587")  # Default to 587 if not set
	smtp_username = os.getenv("SMTP_USERNAME")
	smtp_password = os.getenv("SMTP_PASSWORD")
	smtp_use_tls = os.getenv("SMTP_USE_TLS", "True").strip().lower() in {"1", "true", "yes", "on"}
	smtp_use_ssl = os.getenv("SMTP_USE_SSL", "False").strip().lower() in {"1", "true", "yes", "on"}
	sender_email = os.getenv("SMTP_SENDER_EMAIL")
	sender_name = os.getenv("SMTP_SENDER_NAME", "Zindua LMS")

	required = {
		"SMTP_HOST": smtp_host,
		"SMTP_USERNAME": smtp_username,
		"SMTP_PASSWORD": smtp_password,
		"SMTP_SENDER_EMAIL": sender_email,
	}
	missing = [name for name, value in required.items() if not value]
	if missing:
		raise ValueError(f"Missing required .env variables: {', '.join(missing)}")

	msg = EmailMessage()
	msg["Subject"] = subject
	msg["From"] = formataddr((sender_name, sender_email))
	msg["To"] = to
	msg["Message-ID"] = make_msgid()
	msg.set_content(message)
	if html:
		msg.add_alternative(html, subtype="html")

	try:
		port = int(smtp_port)
	except ValueError as exc:
		raise ValueError("SMTP_PORT must be a valid number") from exc

	if smtp_use_ssl:
		with smtplib.SMTP_SSL(smtp_host, port) as server:
			server.login(smtp_username, smtp_password)
			server.send_message(msg)
		return

	with smtplib.SMTP(smtp_host, port) as server:
		if smtp_use_tls:
			server.starttls()
		server.login(smtp_username, smtp_password)
		server.send_message(msg)


if __name__ == "__main__":
	# Example usage
	send_email(
		to="cyrilmichino@gmail.com",
		subject="Test Transactional Email",
		message="This is a transactional email sent via SMTP.",
		html="<p>This is a <strong>transactional</strong> email sent via SMTP.</p>",
	)