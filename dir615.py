#/usr/bin/env python3

from bs4 import BeautifulSoup
import requests

dir615_url = 'http://192.168.1.1'
username = 'xxxxx'
password = '*****'
form_url = 'url to the google form which has only two text fields one for ssid and another for wpa key'

print('logging in to router')
requests.post(dir615_url + '/login.cgi',data={'username':username, 'password':password, 'submit.htm?login.htm':'Send'})
print('getting pass page')
response = requests.get(dir615_url + '/wlan_basic.htm')
soup = BeautifulSoup(response.content, 'html.parser')
input_passphrase = soup.find('input', {'name':'pskValue'})
passphrase = input_passphrase['value']
input_ssid = soup.find('input', {'name':'ssid'})
ssid = input_ssid['value']

fields_to_submit = [ssid, passphrase]

print('fetching google form')

response = requests.get(form_url)
soup = BeautifulSoup(response.content, 'html.parser')
form = soup.find('form')
post_url = form['action']

payload = {}
i = 0
for input in form.find_all('input', {'type':'text'}):
  payload[input['name']] = fields_to_submit[i]
  i+=1

for input in form.find_all('input', {'type':'hidden'}):
  payload[input['name']] = input['value']
print(post_url)
print(payload)

print('submitting to google form')
requests.post(post_url, data=payload)
print('all done')
