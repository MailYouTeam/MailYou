> [!WARNING]
> We're currently in development, so expect bugs to show up

# MailYou

Send emails straight from your CLI!

## Installation

**From PyPI:**

```bash
pip install mailyou
```

**From a GitHub Release** (wheel or tarball):

```bash
pip install mailyou-X.X.X-py3-none-any.whl
# or
pip install mailyou-X.X.X.tar.gz
```

## Configuration

MailYou reads SMTP settings from a config file at:

- **Linux/macOS:** `~/.config/mailyou/config.toml`
- **Windows:** `%APPDATA%\mailyou\config.toml`

Get the example config file:

```bash
curl -LsSO https://raw.githubusercontent.com/MailYouTeam/MailYou/refs/heads/master/config.toml.example
```

Copy and fill in your details:

```bash
# Linux and macOS
cp config.toml.example ~/.config/mailyou/config.toml
```

```cmd
# Windows
copy config.toml.example %APPDATA%\mailyou\config.toml
```

A minimal config looks like this:

```toml
[smtp]
server = "smtp.example.com"
port   = 587
user   = "john@example.com"
```

Your SMTP password is **not** stored in the config file — you will be prompted for it securely each time you run

## How to use

Start from one of the provided templates:

```bash
# plain text template
curl -LsSO https://raw.githubusercontent.com/MailYouTeam/MailYou/refs/heads/master/examples/email.txt

# HTML template
curl -LsSO https://raw.githubusercontent.com/MailYouTeam/MailYou/refs/heads/master/examples/email.html
```

Or write your own from scratch:

```bash
touch email.txt  # plain text
touch email.html # HTML
```

The file extension determines how the email is sent: `.txt` sends as plain text, `.html` sends as HTML. Any other extension will produce an error

Then send it:

```bash
mailyou email.txt --to jane@example.com
```

`mailyou` accepts the following options:

| Option              | Description                             |
|---------------------|-----------------------------------------|
| `FILE`              | Path to the email file (required)       |
| `--from SENDER`     | Override the sender address from config |
| `--to RECIPIENT`    | Recipient address — repeatable          |
| `--cc RECIPIENT`    | Cc address — repeatable                 |
| `--bcc RECIPIENT`   | Bcc address — repeatable                |
| `--reply-to SENDER` | Reply-To address — repeatable           |
| `--attach FILE`     | Path to an attachment — repeatable      |

**Examples:**

```bash
# Send to multiple recipients with a Cc and an attachment
mailyou email.txt --to jane@example.com --to bob@example.com --cc alice@example.com --attach report.pdf

# Override the sender shown to recipients
mailyou email.html --to jane@example.com --from "Support Team <support@example.com>"
```

### How to write the email

The email file format is the same for both `.txt` and `.html`:

- **Line 1** is the subject
- **Line 2** is a separator (must be blank)
- **Line 3+** is the email body

> For subject and email body, you can always leave them blank if you don't want any, but **line 2** must always be blank

If any of these requirements are not satisfied, `mailyou` will print an error and won't send

This structure is the same for both `.txt` and `.html` files. The only difference is that **line 3 onward is treated as raw HTML** when using a `.html` file

### Example plain text email

This is an example of a valid `email.txt`:

```
Sample Message

Hello,

Lorem ipsum style placeholder email content for testing purposes

Thank you.
```

### Example HTML email

This is an example of a valid `email.html`:

```
Sample Message

<html>
  <body>
    <p>Hello</p>
    <p>Lorem ipsum style placeholder email content for testing purposes</p>
    <p>Thank you</p>
  </body>
</html>
```

#### Breakdown (applies to both formats)

- **Line 1** `Sample Message` is the subject

- **Line 2** (blank) is the separator

- **Line 3+** is the body: plain text for `.txt`, raw HTML markup for `.html`

> **FYI**, for plain text emails we handle linebreaks automatically by injecting `\n` starting from **line 3** and so on. For HTML emails, your markup controls all formatting

## Contributing

We're restricting PR access, sorry.
