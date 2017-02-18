import time
import random
import string
import names
import os
import requests
from bs4 import BeautifulSoup
import sys

filename = raw_input("[+]Enter the filename to save the usernames to (IE userlist.txt): ")
try:
    accountlist = open(filename,'w')
except IOError:
    sys.exit("[-]Invalid filename!")

number_of_accounts = raw_input("[+]Enter the number of accounts to create (IE 20): ")

delay = raw_input("[+]Enter how long to pause (IE 5): ")


base = 0

while int(base) < int(number_of_accounts):
    base += 1
    time.sleep(int(delay))
    with requests.Session() as c:


        fullName          = names.get_full_name()

        requesturl        = 'https://cp.adidas.com/web/eCom/en_US/accountcreate'
        regpage           = 'https://www.adidas.com/us/myaccount-register'

        FIRSTNAME         = fullName.split()[0]
        LASTNAME          = fullName.split()[1]
        MINAGECHECK       = 'true'
        _MINAGECHECK      = 'on'
        EMAIL             = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))+str(random.randint(1,100))+str('@grr.la')
        PASSWORD          = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(10))
        CONFIRMPASSWORD   = PASSWORD
        AMF               = 'true'
        _AMF              = 'on'
        TERMS             = 'true'
        _TERMS            = 'on'
        APP               = 'eCom'
        LOCALE            = 'en_US'
        DOMAIN            = ''
        CONSENTDATA1      = 'Sign me up for adidas emails, featuring exclusive offers, latest product info, news about upcoming events, and more. See our <a target="_blank" href="https://www.adidas.com/us/help-topics-privacy_policy.html">Privacy Policy</a> for details.'
        CONSENTDATA2      = ''
        CONSENTDATA3      = ''

        print "password: "    +str(PASSWORD)
        print "first name: "  +str(FIRSTNAME)
        print "last name: "   +str(LASTNAME)
        print "email   : "    +str(EMAIL)


        r = c.get('https://cp.adidas.com/web/eCom/en_US/loadcreateaccount').content
        soup = BeautifulSoup(r,'html.parser')
        CSRFTOKEN =  soup.find('input',{ 'name': 'CSRFToken' })['value']

        reg_data = dict(firstName = FIRSTNAME, lastName = LASTNAME, minAgeCheck = MINAGECHECK, _minAgeCheck = _MINAGECHECK, email = EMAIL, password = PASSWORD, confirmPassword = CONFIRMPASSWORD,amf = AMF, _amf = _AMF, terms = TERMS, _terms = _TERMS, app = APP, locale = LOCALE, domain = DOMAIN, consentData1 = CONSENTDATA1, consentData2 = CONSENTDATA2, consentData3 = CONSENTDATA3, CSRFToken = CSRFTOKEN  )
        regpost = c.post(requesturl, data=reg_data, headers={'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36","X-Requested-With":'XMLHttpRequest' })
        reg_status_code =  regpost.status_code
        if reg_status_code == 200:
            print "[+]Account " +str(base)+ " of " +str(number_of_accounts)+ " creation successful \n"
            accountlist.write(FIRSTNAME+":"+LASTNAME+":"+EMAIL+":"+PASSWORD+'\n')
        else:
            print "[+]Account creation unsuccessful \n"
            accountlist.close()
            sys.exit("[-]Error")


accountlist.close()
