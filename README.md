# script-omnichannel-notifications
Script on omnichannel notifications using SMTP, Twilio SMS, and Discord/Slack connections

## Transactional Email via SMTP

Use `emailSMTP.py` to send transactional emails through any SMTP provider, including **SendGrid** and **AWS SES**.

### Install dependency

```bash
pip install python-dotenv
```

The script automatically loads credentials from `.env` using `python-dotenv`.

### 1) Create a `.env` file

```dotenv
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your_smtp_password_or_api_key
SMTP_SENDER_EMAIL=no-reply@yourdomain.com
SMTP_SENDER_NAME=Your App
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

Required variables:
- `SMTP_HOST`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_SENDER_EMAIL`

Optional variables:
- `SMTP_PORT` (default `587`)
- `SMTP_SENDER_NAME` (default `Notifications`)
- `SMTP_USE_TLS` (default `true`)
- `SMTP_USE_SSL` (default `false`)

### 2) Run the script

```bash
python3 emailSMTP.py
```

By default, `emailSMTP.py` contains an example call in the `__main__` block. Update the recipient, subject, and message there to send your transactional email.

