# MailMe

Send emails straight from your CLI!

## How to use

Clone the repo:

```bash
git clone https://github.com/aiadam36/MailMe.git
cd MailMe
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the `.env`:

```bash
cp .env.example .env
```

And then fill your credentials and recipient addresses

> we also supports `Cc`, `Bcc`, `Reply-To` and attachment!

After that, run any of this command:

```bash
cp email.txt.example email.txt # Use our email template (Easiest)
```

Or

```bash
touch email.txt # If you wanna write them yourself
```

To change the email subject and content, simply edit the `email.txt` (If you used `touch`, refer below!)

And then run `python3 main.py` to send them

### How to write the email (Especially if you used `touch`)

The script (`main.py`) parse email exactly like these:

- **Line 1** is subject
- **Line 2** is a separator
- **Line 3+** is the email body

> For subject and email body, you can always leave them blank if you don't want any, but **line 2** must always be blank

> If any of these requirements are not satisfied, the script will print an error and won't send

### Example email

This is example of valid `email.txt`:

```
Sample Message

Hello,

Lorem ipsum style placeholder email content for testing purposes

Thank you.
```

#### Breakdown

- `Sample Message` is the subject

- Between `Sample Message` and `Hello,` is the separator

- `Hello,` to `Thank you.` is basically the email body

> **fyi**, we handle linebreak automatically by injecting `\n` starting from **line 3** and so on

## Contributing

Feel free to fork and open a PR
