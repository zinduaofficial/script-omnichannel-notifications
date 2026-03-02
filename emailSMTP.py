import argparse
import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr, make_msgid


def parse_bool(value: str | None, default: bool) -> bool:
	if value is None:
		return default
	return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def get_provider_defaults(provider: str, region: str | None):
	provider = (provider or "custom").lower()
	if provider == "sendgrid":
		return {
			"host": "smtp.sendgrid.net",
			"port": 587,
			"use_tls": True,
			"use_ssl": False,
			"username": "apikey",
		}
	if provider == "ses":
		ses_host = f"email-smtp.{region}.amazonaws.com" if region else None
		return {
			"host": ses_host,
			"port": 587,
			"use_tls": True,
			"use_ssl": False,
			"username": None,
		}
	return {
		"host": None,
		"port": 587,
		"use_tls": True,
		"use_ssl": False,
		"username": None,
	}


def resolve_config(args):
	provider_defaults = get_provider_defaults(args.provider, args.region or os.getenv("SMTP_REGION"))

	host = args.host or os.getenv("SMTP_HOST") or provider_defaults["host"]
	port = args.port or int(os.getenv("SMTP_PORT", provider_defaults["port"]))
	username = args.username or os.getenv("SMTP_USERNAME") or provider_defaults["username"]
	password = args.password or os.getenv("SMTP_PASSWORD")
	from_email = args.from_email or os.getenv("SMTP_FROM_EMAIL")
	from_name = args.from_name or os.getenv("SMTP_FROM_NAME")

	use_tls = args.use_tls
	if use_tls is None:
		use_tls = parse_bool(os.getenv("SMTP_USE_TLS"), provider_defaults["use_tls"])

	use_ssl = args.use_ssl
	if use_ssl is None:
		use_ssl = parse_bool(os.getenv("SMTP_USE_SSL"), provider_defaults["use_ssl"])

	if not host:
		raise ValueError("SMTP host is required. Pass --host or set SMTP_HOST.")
	if not username:
		raise ValueError("SMTP username is required. Pass --username or set SMTP_USERNAME.")
	if not password:
		raise ValueError("SMTP password is required. Pass --password or set SMTP_PASSWORD.")
	if not from_email:
		raise ValueError("Sender email is required. Pass --from-email or set SMTP_FROM_EMAIL.")
	if use_ssl and use_tls:
		raise ValueError("Choose one of SSL or TLS, not both.")

	return {
		"host": host,
		"port": port,
		"username": username,
		"password": password,
		"from_email": from_email,
		"from_name": from_name,
		"use_tls": use_tls,
		"use_ssl": use_ssl,
	}


def build_message(args, from_email: str, from_name: str | None):
	message = EmailMessage()
	message["From"] = formataddr((from_name or "", from_email))
	message["To"] = ", ".join(args.to)
	if args.cc:
		message["Cc"] = ", ".join(args.cc)
	if args.bcc:
		message["Bcc"] = ", ".join(args.bcc)
	if args.reply_to:
		message["Reply-To"] = args.reply_to
	message["Subject"] = args.subject
	message["Message-Id"] = make_msgid()

	if args.text and args.html:
		message.set_content(args.text)
		message.add_alternative(args.html, subtype="html")
	elif args.html:
		message.set_content("This is an HTML email. Please use an HTML capable client.")
		message.add_alternative(args.html, subtype="html")
	else:
		message.set_content(args.text)

	return message


def send_email(args):
	config = resolve_config(args)
	msg = build_message(args, config["from_email"], config["from_name"])

	recipients = list(args.to)
	if args.cc:
		recipients.extend(args.cc)
	if args.bcc:
		recipients.extend(args.bcc)

	if config["use_ssl"]:
		with smtplib.SMTP_SSL(config["host"], config["port"], timeout=30) as smtp:
			smtp.login(config["username"], config["password"])
			smtp.send_message(msg, from_addr=config["from_email"], to_addrs=recipients)
		return

	with smtplib.SMTP(config["host"], config["port"], timeout=30) as smtp:
		smtp.ehlo()
		if config["use_tls"]:
			smtp.starttls()
			smtp.ehlo()
		smtp.login(config["username"], config["password"])
		smtp.send_message(msg, from_addr=config["from_email"], to_addrs=recipients)


def build_parser():
	parser = argparse.ArgumentParser(
		description="Send transactional emails via SMTP (AWS SES, SendGrid, or custom provider)."
	)
	parser.add_argument("--provider", choices=["custom", "ses", "sendgrid"], default="custom")
	parser.add_argument("--region", help="AWS region for SES host auto-generation.")

	parser.add_argument("--host", help="SMTP host (e.g. smtp.sendgrid.net).")
	parser.add_argument("--port", type=int, help="SMTP port (usually 587 for TLS, 465 for SSL).")
	parser.add_argument("--username", help="SMTP username.")
	parser.add_argument("--password", help="SMTP password / API key.")
	parser.add_argument("--from-email", help="Sender email address.")
	parser.add_argument("--from-name", help="Sender display name.")

	parser.add_argument("--use-tls", dest="use_tls", action="store_true", default=None)
	parser.add_argument("--no-use-tls", dest="use_tls", action="store_false")
	parser.add_argument("--use-ssl", dest="use_ssl", action="store_true", default=None)
	parser.add_argument("--no-use-ssl", dest="use_ssl", action="store_false")

	parser.add_argument("--to", nargs="+", required=True, help="One or many recipients.")
	parser.add_argument("--cc", nargs="+", help="CC recipients.")
	parser.add_argument("--bcc", nargs="+", help="BCC recipients.")
	parser.add_argument("--reply-to", help="Reply-To email address.")
	parser.add_argument("--subject", required=True, help="Email subject.")
	parser.add_argument("--text", default="", help="Plain text body.")
	parser.add_argument("--html", help="HTML body.")
	return parser


def main():
	parser = build_parser()
	args = parser.parse_args()

	if not args.text and not args.html:
		parser.error("You must provide at least one body: --text or --html")

	send_email(args)
	print(f"Email sent successfully to {', '.join(args.to)}")


if __name__ == "__main__":
	main()
