from re import I, S
import requests
import hashlib
from .security import decrypt
from .models import Logins
import re
import argparse


def checkpwn():
    passwords = Logins.query.all()
    shadictionary = {}
    for password in passwords:
        decrypted = decrypt(password.password)
        passwordid = password.id
        sha = hashlib.sha1(decrypted.encode('utf-8'))
        encryptedsha=sha.digest()
        print(encryptedsha)
        encryptedsha = encryptedsha.hex()
        print(encryptedsha)
        shadictionary.update({passwordid:encryptedsha.upper()})
    print(shadictionary)
    response = []
    check_pass_api = 'https://api.pwnedpasswords.com/range/'
    api_key= '20252769e5c04f37ae9beeffc0496520'
    headers = []
    for k,v in shadictionary.items():
        headers.append(v[:5])
        header = v[:5]
        shortenedresponse = requests.get(check_pass_api+header)
        if shortenedresponse.status_code == 200:
            response.append(shortenedresponse.content.decode('UTF-8').split('\r\n'))
        else :
            print( 'No matches found')
    realhash = []
    for line in response:
        for item in line:
            for head in headers:
                realhash.append(head+item.split(':')[0])
    for k, v in shadictionary.items():
        for line in realhash:
            #print(line)
            if v == line:
                print('Password {} was found in the database'.format(k))


            

                #if head+i == v:
                #    print(f'Password {k} is pwned')

    #for i in response:
    #    if i.split(':')[0] == shadictionary[v]:
    #        print(i, shadictionary[k])
