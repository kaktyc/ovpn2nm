#!env python

import os
import sys
import re
from BeautifulSoup import BeautifulSoup as BS

if len(sys.argv) < 2:
    sys.exit('Usage: %s client.ovpn' % sys.argv[0])

if not os.path.exists(sys.argv[1]):
    sys.exit('ERROR: Could not open file %s' % sys.argv[1])

f = open(sys.argv[1], 'r')

config = open("client.conf", 'w')
ta = open("ta.key", 'w')  # tls-auth
ca = open("ca.crt", 'w')  # ca
key = open("client.key", 'w')  # key
cert = open("client.crt", 'w')  # cert

config_addon = """ 
ca ca.crt
cert client.crt
key client.key
tls-auth ta.key 1 
"""

# remove all comments
f_ovpn = "".join([l for l in f.readlines() if not l.startswith('#')])
f.close()

# replace dash in tag 'tls-auth' for easy parsing
f_ovpn = re.sub("tls-auth>", "tlsauth>", f_ovpn)

# remove 'key-direction' directive
f_ovpn = re.sub("key-direction 1", "", f_ovpn)

ovpn = BS(f_ovpn)

ta.write(ovpn.tlsauth.contents[0].strip())
ovpn.tlsauth.decompose()
ta.close()

ca.write(ovpn.ca.contents[0].strip())
ovpn.ca.decompose()
ca.close()

key.write(ovpn.key.contents[0].strip())
ovpn.key.decompose()
key.close()

cert.write(ovpn.cert.contents[0].strip())
ovpn.cert.decompose()
cert.close()

config.write(str(ovpn).strip())
config.write(config_addon)
config.close()
