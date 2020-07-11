import smtplib, ssl
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendEmail(parsersResults):
    sender_email = "avi256.b@gmail.com"
    receiver_email = "abondalapati1@student.gsu.edu"
    password = "lnsegqymwulszgpp"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Parser daily report :" + str(datetime.datetime.utcnow().date())
    message["From"] = sender_email
    message["To"] = receiver_email

    tableValuesContent = ""
    tableHeaderContent = "<thead><tr><th>Market Name</th><th>product descriptions</th><th>product reviews</th><th>vendor profiles</th><th>vendor ratings</th></tr></thead>"

    for market in parsersResults.keys():
        marketValues = parsersResults.get(market)
        tableValuesContent += "<tr><td>" + market + "</td><td>" + marketValues["productDescriptions"] + "</td><td>" + \
                              marketValues["productRatings"] + "</td><td>" + marketValues[
                                  "vendorProfiles"] + "</td><td>" + marketValues["vendorRatings"] + "</td></tr>"

    tableContent = "<table >" + tableHeaderContent + "<tbody>" + tableValuesContent + "</tbody>" + "</table>"

    html = """\
    <html>
    <head>
    <style>
    table {
      font-family: arial, sans-serif;
      border-collapse: collapse;
      width: 70%;
    }

    td, th {
      border: 1px solid #dddddd;
      text-align: left;
      padding: 8px;
    }

    tr:nth-child(even) {
      background-color: #dddddd;
    }
    </style>
    </head>
      <body>
        <p>Hi All,</p>
        <br>
        <p> the below counts are the number of records inserted into parsed database.</p><br> 

        """ + tableContent + """<br>
            Thanks.
      </body>
    </html>
    """

    # Turn these into html MIMEText objects
    part = MIMEText(html, "html")
    # Add HTML parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part)
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email.split(","), message.as_string()
        )