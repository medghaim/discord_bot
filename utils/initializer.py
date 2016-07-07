import json
from discord.ext import commands
from collections import namedtuple

def get_json():
	with open('credentials.json') as file:
		return json.load(file)

def get_credentials():
	###CONSTRUCTING bot.credentials ATTRIBUTE -- THESE ARE IMMUTABLE VALUES (const; cannot be changed)
	##Step 1: Creating named tuples used to construct bot.credentials - 1) ADD NEW CRED ATTR and 2) CREATE NEW NAMED TUPLE
	Credentials = namedtuple('Credentials', ['token', 'imgur', 'reddit', 'youtube']) 
	Imgur = namedtuple('Imgur', ['id', 'secret'])
	Reddit = namedtuple('Reddit', ['id', 'secret'])
	YouTube = namedtuple('Youtube', ['key', 'id', 'secret'])

	##Step 2: Create instances of the named tuples - 3) CREATE NEW INSTANCE OF NAMED TUPLE
	credentials = get_json() #reads the json file
	imgur = Imgur(credentials['imgur']['id'], credentials['imgur']['secret'])
	reddit = Reddit(credentials['reddit']['id'], credentials['reddit']['secret']) 
	youtube = YouTube(credentials['youtube']['key'], credentials['youtube']['id'], credentials['youtube']['secret'])

	##Step 3: Dynamically adding .credentials attr to bot. 4) ADD NEW INSTANCE OF NEW NAMED TUPLE HERE
	return Credentials(credentials['bot']['token'], imgur, reddit, youtube)

def init_modules(bot, modules):
	success = ''
	failure = ''
	for mod in modules:
		try:
			bot.load_extension(mod)
			success += '\t{}\n'.format(mod)
		except Exception as e:
			exc = '{}: {}'.format(type(e).__name__, e)
			failure += ('{} - {}'.format(mod, exc))

	if(len(success) > 0):
		print('MODULES LOADED: \n{}'.format(success))
	if(len(failure) > 0):
		print('MODULE ERRORS:\n{}'.format(failure))