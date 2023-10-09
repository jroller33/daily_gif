import requests
from urllib.parse import urlencode
import json
from random import randint
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import make_msgid
from hidden import api_key, email_sender, email_receivers, email_password

search_term = "funny"
url = 'https://api.giphy.com/v1/gifs/search?'
params = {
    'api_key' : api_key,
    'q'       : search_term,
    'lang'    : 'en'
}
url += urlencode( params )
r = requests.get( url )
result = r.json()
i = randint(0, len(result['data'])-1)
rand_result = result['data'][i]
url = rand_result['images']['original']['url']
gif = requests.get(url)

# -------------------------------------------------------------------------------

subject = "Daily GIF"
body = f"""
<html>
    <head></head>
    <body>

    <img src=f"{gif}" alt="GIF">

    </body>
</html>

"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = ", ".join(email_receivers)
em['Subject'] = subject
em.set_content(body)


context = ssl.create_default_context()

# Log in and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receivers, em.as_string())
