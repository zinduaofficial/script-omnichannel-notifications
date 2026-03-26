# script-omnichannel-notifications
Script on omnichannel notifications using SMTP, Twilio SMS, and Discord/Slack connections

## Transactional Email via SMTP

Use `emailSMTP.py` to send transactional emails through any SMTP provider, including **SendGrid** and **AWS SES**.

### Install dependency

```bash
pip install python-dotenv
```

The script automatically loads credentials from `.env` using `python-dotenv`.

### 1) Set environment variables

You can pass values by CLI flags, but env vars are easiest:

```bash
export SMTP_HOST="smtp.sendgrid.net"
export SMTP_PORT="587"
export SMTP_USERNAME="apikey"
export SMTP_PASSWORD="<SENDGRID_API_KEY>"
export SMTP_FROM_EMAIL="no-reply@yourdomain.com"
export SMTP_FROM_NAME="Your App"
export SMTP_USE_TLS="true"
```

### 2) Send a transactional email

```bash
python3 emailSMTP.py \
	--to customer@example.com \
	--subject "Welcome to our app" \
	--text "Your account has been created successfully."
```

### SendGrid quick example

```bash
python3 emailSMTP.py \
	--provider sendgrid \
	--password "<SENDGRID_API_KEY>" \
	--from-email "no-reply@yourdomain.com" \
	--to customer@example.com \
	--subject "Password reset" \
	--text "Use this code: 123456"
```

### AWS SES quick example

```bash
python3 emailSMTP.py \
	--provider ses \
	--region us-east-1 \
	--username "<SES_SMTP_USERNAME>" \
	--password "<SES_SMTP_PASSWORD>" \
	--from-email "verified@yourdomain.com" \
	--to customer@example.com \
	--subject "Order confirmed" \
	--html "<h1>Thank you</h1><p>Your order is confirmed.</p>"
```

### Optional flags

- `--cc user1@example.com user2@example.com`
- `--bcc audit@example.com`
- `--reply-to support@yourdomain.com`
- `--html "<p>...</p>"` for HTML body
- `--text "..."` for plain text body

