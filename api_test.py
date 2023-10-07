import json

import global_vars.vars as g

g.init()

f = open('creds.json')
creds = json.load(f)

g.crunchyroll.login(creds['username'], creds['password'])

if g.crunchyroll.logged_in == True:
	print('Logged in')
else:
	print('Failed to login')
