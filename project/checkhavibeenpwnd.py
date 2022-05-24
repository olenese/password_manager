from re import I, S
import requests
import hashlib
from flask_login import login_required, current_user
from .security import decrypt
from .models import Logins
from concurrent.futures import ThreadPoolExecutor, as_completed



def getpass():
    # Gets the passwords from the user.
    passwords = Logins.query.filter_by(userID=current_user.id).all()
    shadictionary = {}
    for password in passwords:
        decrypted = decrypt(password.password)
        passwordid = password.id
        sha = hashlib.sha1(decrypted.encode('utf-8'))
        encryptedsha=sha.digest()
        encryptedsha = encryptedsha.hex()
        shadictionary.update({passwordid:encryptedsha.upper()})
    concurrency(shadictionary)

processes = []
def concurrency(shadictionary):
    # Checks the passwords in a thread pool.
    with ThreadPoolExecutor(max_workers=30) as executor:
        for id, sha in shadictionary.items():
            processes.append(executor.submit(checkpwn, id, sha))
    for process in as_completed(processes):
        output = process.result()
        if output:
            checkpasswords(output)
        else:
            print('No results found.')


checkdict = {}
def checkpwn(id, sha):
    # Checks the password against the havibeenpwnd api.
    checkdict.update({id:sha})
    url = 'https://api.pwnedpasswords.com/range/' + sha[:5]
    response = requests.get(url)
    if response.status_code == 200:
        output = response.text
        return output
    else:
        return None

def checkpasswords(output):
    # Checks the return from checkpwn against the shadictionary.
    for line in output.splitlines():
        hash, count = line.split(':')
        if hash in checkdict.values():
            print(f'{hash} was found {count} times.')
 


"""
shadictionary = {}
def checkpwn(luring):
    passwords = luring
    for password in passwords:
        decrypted = decrypt(password.password)
        passwordid = password.id
        sha = hashlib.sha1(decrypted.encode('utf-8'))
        encryptedsha=sha.digest()
        encryptedsha = encryptedsha.hex()
        shadictionary.update({passwordid:encryptedsha.upper()})
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
                print(k)
                return k

processes = []
            
with ThreadPoolExecutor(max_workers=10) as executor:
    for id, password in shadictionary.items():    
        processes.append(executor.submit(updatemerakidevices, serial, coordinates))

                #if head+i == v:
                #    print(f'Password {k} is pwned')

    #for i in response:
    #    if i.split(':')[0] == shadictionary[v]:
    #        print(i, shadictionary[k])
"""