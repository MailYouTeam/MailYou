# MailYou

Send emails straight from your CLI!

## How to use

Clone the repo:

```bash
git clone https://github.com/aiadam36/MailYou.git
cd MailYou
```

Install dependencies:

```bash
pip install .
```

Configure the `.env`:

```bash
cp .env.example .env
```

And then fill your credentials and recipient addresses

> We also supports **Cc**, **Bcc**, **Reply-To** and attachment! Simply fill it in `.env` file

After that, run any of this command:

```bash
cp examples/email.txt email.txt # Use our plain text template
```

Or for an HTML email:

```bash
cp examples/email.html email.html # Use our HTML template
```

Or basically write your own from scratch:

```bash
touch email.txt  # plain text
touch email.html # HTML
```

The file extension determines how the email is sent: `.txt` sends as plain text, `.html` sends as HTML. Any other extension will produce an error

And then run `mailyou -t FILE` to send them

`FILE` is your email file name

> `mailyou --target FILE` is also valid

We use `-t` or `--target` to specify the path of the email file, so it's not necessary to name them all `email.txt` or `email.html`

### How to write the email (Especially if you used `touch`)

The script parses email files exactly like these:

- **Line 1** is the subject
- **Line 2** is a separator (must be blank)
- **Line 3+** is the email body

> For subject and email body, you can always leave them blank if you don't want any, but **line 2** must always be blank

If any of these requirements are not satisfied, the script will print an error and won't send

---

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
