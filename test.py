#!/Users/gowtham/anaconda/bin/python
import json
import requests
import sys
import smtplib
import getopt
import time
from datetime import datetime,date

def get_quote(symbol):
    scrip = {}
    rsp = requests.get('https://finance.google.com/finance?q='+symbol+'&output=json')
    if rsp.status_code in (200,):

        # This magic here is to cut out various leading characters from the JSON 
        # response, as well as trailing stuff (a terminating ']\n' sequence), and then
        # we decode the escape sequences in the response
        # This then allows you to load the resulting string
        # with the JSON module.
        fin_data = json.loads(rsp.content[6:-2].decode('unicode_escape'))

        # print out some quote data
        #print('Current Price: {}'.format(fin_data['l']))
        scrip["cur"] = fin_data['l']
        #print('Opening Price: {}'.format(fin_data['op']))
        scrip["open"] = fin_data['op']
        #print('Today\'s Range Price: %s - %s' % (fin_data['lo'],fin_data['hi']))
        scrip["curhi"] = fin_data['hi']
        scrip["curlo"] = fin_data['lo']
        #print('Price/Earnings Ratio: {}'.format(fin_data['pe']))
        #print('52-week high: {}'.format(fin_data['hi52']))
        scrip["52hi"] = fin_data['hi52']
        #print('52-week low: {}'.format(fin_data['lo52']))
        scrip["52lo"] = fin_data['lo52']
        #print(fin_data)
        return scrip

def send_email(recipient, subject, body):

    gmail_user = "kuchbivr@gmail.com"
    gmail_pwd = "handl3bar"
    FROM = gmail_user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")


def main():

    opts, ign = getopt.getopt(sys.argv[1:], "abc")
    #print(opts)
    stock_reco = {}

    for line in open("reco.txt"):
        (scrip, reco_price) = line.split()
        stock_reco[scrip] = get_quote(scrip)
        stock_reco[scrip]["reco"] = reco_price

    while True:
        wday = datetime.now()

        sub = "Mail alert date %s-%s-%s" % (wday.day, wday.month, wday.year)
        bod = """<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>"""
        bod = ""
        for scrip in stock_reco.keys():
            bod += """ \nStock %s\n
            Share Price: %s
            Open Price: %s
            Recommended Price: %s \n
            """ % (scrip, stock_reco[scrip]["cur"], stock_reco[scrip]["open"], stock_reco[scrip]["reco"])

        send_email("trgowtham@gmail.com",sub, bod)

        if wday != 5 or wday != 6:
            #if wday.hour == 9 and  wday.min == 30:
            if wday.hour == 9 and  wday.min == 30:
                print(stock_reco)
        sys.exit(0)
        time.sleep(100)


    #for s in stock_reco.keys():
    #    send_email("kuchbivr@gmail.com", "handl3bar", "Test"
    

if __name__ == '__main__':
    main()
