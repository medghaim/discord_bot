import discord
from discord.ext import commands

import wikipedia
from imgurpython import ImgurClient
#import gdata.youtube 			 --- BROKEN ----
#import gdata.youtube.service

#yt_service = gdata.youtube.service.YouTubeService()

class Internet():
	def __init__(self, bot):
		self.bot = bot

	@commands.group(invoke_without_command=True, aliases=['g'])
	async def google(self, search_str : str, num_links = 0):
		"""Simple google search for you!"""
		url = 'https://www.google.com/#q='+"+".join(search_str.split())
		if num_links == 0:
			await self.bot.say(url)
		elif num_links > 0:
			await self.bot.say('parsing '+str(num_links)+' links')

	@google.command(name='img', aliases=['i', 'imgs','images','image'])
	async def _img(self, search_str : str, num_links = 0):
		"""Searches google images for you!"""
		await self.bot.say('https://www.google.com/search?tbm=isch&q='+"+".join(search_str.split()))

	@google.command(name='maps', aliases=['m', 'map'])
	async def _maps(self, search_str: str):
		"""Searches google maps for you!"""
		await self.bot.say('https://www.google.com/maps/place/{}'.format("+".join(search_str.split())))

	@commands.command(aliases=['yt'])
	async def youtube(self, search_str : str, num_links = 0):
		"""Searches youtube for you!"""
		url = 'https://www.google.com/#q='+"+".join(search_str.split())
		if num_links == 0:
			await self.bot.say(url)
		elif num_links > 0:
			await self.bot.say('parsing '+str(num_links)+' links')

		

	@commands.command(aliases=['sound', 'sc'])
	async def soundcloud(self, search_str : str, num_links = 0):
		"""Searches soundcloud for you!"""
		url = 'https://www.google.com/#q='+"+".join(search_str.split())
		if num_links == 0:
			await self.bot.say(url)
		elif num_links > 0:
			await self.bot.say('parsing '+str(num_links)+' links')


	@commands.command()
	async def reddit(self, search_str : str, num_links = 0):
		""" Searches reddit for you! """
		url = 'REDDIT'+"+".join(search_str.split())
		if num_links == 0:
			await self.bot.say(url)
		elif num_links > 0:
			await self.bot.say('parsing '+str(num_links)+' links')

		
	@commands.command()
	async def imgur(self, search_str : str, num_links = 0):
		""" Searches imgur for you!"""
		client = ImgurClient(self.bot.credentials.imgur.id, self.bot.credentials.imgur.secret)
		
		#out = '' 
		if num_links == 0:
			await self.bot.say('url')
		elif num_links > 0:
			await self.bot.say('parsing '+str(num_links)+' links')

	@commands.command()
	async def wiki(self, search_str : str):
		"""Searches Wikipedia with the supplied string"""
		page = wikipedia.page(search_str)
		await self.bot.say(page.url)

	@commands.command()
	async def tv(self, search_str : str):
		"""Searches primewire for you!"""
		await self.bot.say('http://www.primewire.ag/index.php?search_keywords={}'.format("+".join(search_str.split())))

	@commands.command()
	async def track(self, *track_nums : str):
		""" Tracks multiple packages. """
		await self.bot.say('https://www.17track.net/en/track?nums='+",".join(track_nums))



def setup(bot):
	bot.add_cog(Internet(bot))

