import logging
import unittest
import time
import os
import pyotp
import uuid
import email
import imaplib
import mailbox
from bs4 import BeautifulSoup
import requests

from testconfig import config
from testframework import base
# from testframework.email_verification import email_verification

class BaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)

        self.env_url = config['main']['env_url']
        self.validation_email = config['main']['validation_email']
        self.validation_email_password = config['main']['validation_email_password']
        self.organization_1 = self.random_value()
        self.organization_2 = self.random_value()
        #user_1 info
        self.user_1  = config['main']['user_1_username']
        self.user_1_password = config['main']['user_1_password']
        self.user_1_applicationid = config['main']['user_1_applicationid']
        self.user_1_secret = config['main']['user_1_secret']
        # user_2 info
        self.user_2  = config['main']['user_2_username']
        self.user_2_password = config['main']['user_2_password']
        self.user_2_applicationid = config['main']['user_2_applicationid']
        self.user_2_secret = config['main']['user_2_secret']

        self.totp_secret = config['main']['totp_secret']


    def setUp(self):
        self._testID = self._testMethodName
        self._startTime = time.time()
        self._logger = logging.LoggerAdapter(logging.getLogger('itsyouonline_testsuite'),{'testid': self.shortDescription() or self._testID})
        self.lg('Testcase %s Started at %s' % (self._testID, self._startTime))
        self.client_1 = base.Client(self.env_url)
        self.client_2 = base.Client(self.env_url)
        self.client_1.oauth.login_via_client_credentials(client_id=self.user_1_applicationid,client_secret=self.user_1_secret)
        self.client_2.oauth.login_via_client_credentials(client_id=self.user_2_applicationid,client_secret=self.user_2_secret)

    def random_value(self, size=10):
        value = ''
        n = (size/32) or 1
        if (size % 32) > 0:
            n+=1
        for i in range(n):
            value += str(uuid.uuid4()).replace('-', '')
        return value[:size]

        # return str(str(uuid.uuid4())+str(uuid.uuid4())).replace('-', '')[0:size]

    def get_totp_code(self, secret):
        totp = pyotp.TOTP(secret)
        GAuth_code = totp.now()
        return GAuth_code

    def get_valid_phonenumber(self):
        r = requests.get('http://receive-sms-now.com/')
        self.assertEqual(r.status_code, 200, 'cannot reach [receive-sms-now.com] website')
        html = r.content
        html = BeautifulSoup(html, "html.parser")
        html = html.find_all('a')
        numbers =  [x.string for x in html if '+' in x.string]
        links =  [x['href'] for x in html if '+' in x.string]
        self.assertGreater(numbers, 0, 'cannot find any virtual number')
        self.assertGreater(numbers, 0, 'cannot find any virtual number link')
        for i, number in enumerate(numbers):
            if number[1] == '3':
                self.validation_number = number
                self.validation_number_link = links[i]
                break
        else:
            self.validation_number = numbers[0]
            self.validation_number_link = links[0]

        return self.validation_number

    def get_mobile_verification_code(self):
        r = requests.get('http://receive-sms-now.com/'+self.validation_number_link)
        self.assertEqual(r.status_code, 200, 'cannot reach virtual number page')
        html = r.content
        html = BeautifulSoup(html, "html.parser")
        rows = html.find_all('table')[1].find_all('tr')[1:]
        self.assertGreater(rows, 0, 'cannot find messages content')
        for row in rows:
            sms_info =  [x.string for x in row.find_all('td')]
            sms_date = sms_info[1]
            sms_message = sms_info[2]
            if 'To verify your phonenumber on itsyou.online enter the code' in sms_message and 'seconds' in sms_date:
                code = sms_message[sms_message.find('code')+5: sms_message.find('code')+11]
                return code
        else:
            return False


    def UserValidateEmail(self):
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(self.validation_email, self.validation_email_password)
        mail.select('itsyouonline')
        result, data = mail.search(None, 'ALL')
        latest_email_id = data[0].split()[-1]
        result, email_data = mail.fetch(latest_email_id, '(UID BODY[TEXT])')
        raw_email = email_data[0][1]
        soup = BeautifulSoup(raw_email, "html.parser")
        validation_link = [x.string for x in soup.find_all('a', href=True)][-1]
        validation_link = validation_link.replace('=3D', '=').replace('=\r\n', '')
        r = requests.get(validation_link)
        self.assertEqual(r.status_code, 200, 'cannot open verification link')
        return r

    def tearDown(self):
        """
        Environment cleanup and logs collection.
        """
        if hasattr(self, '_startTime'):
            executionTime = time.time() - self._startTime
        self.lg('Testcase %s ExecutionTime is %s sec.' % (self._testID, executionTime))

    def lg(self, msg):
        self._logger.info(msg)

    def SetTotp(self, username):
        self.lg('Set totp code, should succeed with 204')
        totpcode = self.get_totp_code(self.totp_secret)
        data = {"totpcode":totpcode, "totpsecret":self.totp_secret}
        response = self.client_1.api.EditTotp(data, username)
        self.assertEqual(response.status_code, 204)

    def DeleteAllUserEmails(self, username):
        self.lg('Delete all user\'s emails, should fail with 409')
        response = self.client_1.api.GetEmailAddresses(username)
        self.assertEqual(response.status_code, 200)
        labels = [x['label'] for x in response.json()]
        for i in range(0, len(labels)-1):
            response = self.client_1.api.DeleteEmailAddress(labels[i], username)
            self.assertEqual(response.status_code, 204)

    def DeleteAllUserPhonenumbers(self, username):
        self.lg('Delete all user\'s phonenumbers, should fail with 409')
        response = self.client_1.api.GetUserPhoneNumbers(username)
        self.assertEqual(response.status_code, 200)
        labels = [x['label'] for x in response.json()]
        print labels
        for label in labels:
            response = self.client_1.api.DeleteUserPhonenumber(label, username ,query_params={'force':'true'})
            self.assertEqual(response.status_code, 204)

    def DeleteAllUserAddresses(self, username):
        self.lg('Delete all user\'s addresses, should fail with 409')
        response = self.client_1.api.GetUserAddresses(username)
        self.assertEqual(response.status_code, 200)
        labels = [x['label'] for x in response.json()]
        for label in labels:
            response = self.client_1.api.DeleteUserAddress(label, username)
            self.assertEqual(response.status_code, 204)

    def DeleteAllUserBankAccounts(self, username):
        self.lg('Delete all user\'s bank accounts , should fail with 409')
        response = self.client_1.api.GetUserBankAccounts(username)
        self.assertEqual(response.status_code, 200)
        labels = [x['label'] for x in response.json()]
        for label in labels:
            response = self.client_1.api.DeleteUserBankAccount(label, username)
            self.assertEqual(response.status_code, 204)

    def DeleteAllUserPublicKeys(self, username):
        self.lg('Delete all user\'s publickeys, should fail with 409')
        response = self.client_1.api.GetUserPublicKeys(username)
        self.assertEqual(response.status_code, 200)
        labels = [x['label'] for x in response.json()]
        for label in labels:
            response = self.client_1.api.DeleteUserPublicKey(label, username)
            self.assertEqual(response.status_code, 204)

    def DeleteAllUserDigitalWallet(self, username):
        self.lg('Delete all user\'s digital wallet , should fail with 409')
        response = self.client_1.api.GetUserDigitalWallets(username)
        self.assertEqual(response.status_code, 200)
        labels = [x['label'] for x in response.json()]
        for label in labels:
            response = self.client_1.api.DeleteUserDigitalWallet(label, username)
            self.assertEqual(response.status_code, 204)

    def DeleteAllUserRegistries(self, username):
        self.lg('Delete all user\'s registries, should fail with 409')
        response = self.client_1.api.GetRegistries(username)
        self.assertEqual(response.status_code, 200)
        keys = [x['Key'] for x in response.json()]
        for key in keys:
            response = self.client_1.api.DeleteRegistry(key, username)
            self.assertEqual(response.status_code, 204)

    def DeleteAllUserApiKeys(self, username):
        self.lg('Delete all user\'s apikeys, should fail with 409')
        response = self.client_1.api.ListAPIKeys(username)
        self.assertEqual(response.status_code, 200)
        labels = [x['label'] for x in response.json()[1:]]
        for label in labels:
            response = self.client_1.api.DeleteAPIkey(label, username)
            self.assertEqual(response.status_code, 204)
