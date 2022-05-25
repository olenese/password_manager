from re import I, S
from unittest.util import _count_diff_all_purpose
import requests
import hashlib
from flask_login import login_required, current_user
from .security import decrypt
from .models import Logins
from concurrent.futures import ThreadPoolExecutor, as_completed


shadictionary = {}

def getpass(userid):
    # Gets the passwords from the user.
    print(userid)
    passwords = Logins.query.filter_by(userID=userid).all()

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
    with ThreadPoolExecutor(max_workers=4) as executor:
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
        return response.content.decode('UTF-8').split('\r\n')
    else :
            print( 'No matches found')

def checkpasswords(output):
    # Checks the return from checkpwn against the shadictionary.
    headers = []
    for id, sha in checkdict.items():
        headers.append(sha[:5])    
    realhash = []
    for line in output:
        for head in headers:
                realhash.append(head+line.split(':')[0])
    print(shadictionary)
    for k, v in shadictionary.items():
        for line in realhash:
            if v == line:
                return k
            else:
                return None

def is_pwned(password):
    password_hash = hashlib.sha1(password.encode('UTF-8')).digest().hex().upper()
    # For obvious security reasons, the pwnedpasswords API only accepts the first
    # five characters of the hash, so they are never aware of the actual password.
    # They return a list of partial matches, that we can use to compare against 
    # the full passowrd hash defined above.
    # ref: https://haveibeenpwned.com/API/v3#SearchingPwnedPasswordsByRange
    lookup_token = password_hash[:5]
    url = 'https://api.pwnedpasswords.com/range/' + lookup_token
    response = requests.get(url)

    # The request was not successful, let's not assume the worst,
    # though we could return a non-boolean value to indicate that
    # testing the password was unsuccessful.
    if response.status_code != 200:
        return False
    
    partial_matches = response.content.decode('UTF-8').split('\r\n')

    for match in partial_matches:
        partial_hash = match.split(':')[0]
        pwned_hash = lookup_token + partial_hash

        if pwned_hash == password_hash:
            return True
    
    return False
