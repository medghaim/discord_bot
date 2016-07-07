import discord
from discord.ext import commands
from utils import output

class Administration():
	def __init__(self, bot):
		self.bot = bot
	###
	### BEGIN VOTE FUNCTIONS
	###
	@commands.group(pass_context=True)
	async def vote(self, ctx):
		"""Initiates a vote."""
		if ctx.invoked_subcommand is None:
			await self.bot.say('Vote command {0.subcommand_passed} not recognized.'.format(ctx))

	@vote.command(name='kick')
	async def _kick(self, *mentions : str):
		""" Calls a vote to kick a member """
		pass

	@vote.command(name='ban')
	async def _ban(self, *args : str):
		""" Calls a vote to ban a member """ 
		pass

	@vote.command(name='unban')
	async def _unban(self, *mentions : str):
		""" Calls a vote to unban a member """
		pass

	@vote.command(name='mute')
	async def _mute(self, *args : str):
		""" Calls a vote to mute a member """
		pass

	@vote.command(name='unmute')
	async def _unmute(self, *mentions : str):
		""" Calls a vote to unmute a member """
		pass

	@vote.command(name='deafen')
	async def _deafen(self, *args : str):
		""" Calls a vote to deafen a member """
		pass

	@vote.command(name='undeafen')
	async def _undeafen(self, *mentions : str):
		""" Calls a vote to undeafen a member """
		pass
	###
	### END VOTE FUNCTIONS
	###

	@commands.command()
	async def kick(self, *mentions : discord.Member):
		""" Kicks the mentioned people """
		#CHECK PERMISSIONS 
		#RAISE EXCEPTIONS IF NECESSARY
		kicked = []
		for member in mentions:
			await self.bot.kick(member)
			kicked.append(member.name)
			
		if len(kicked) > 0:
			await output.speak(self.bot, 'Kicked: {}'.format(", ".join(kicked)))

	@commands.command(pass_context=True)
	async def ban(self, ctx, time, *members: discord.Member):
		""" Ban the mentioned members (temp ban optional) 
		You can specify a time (in mins) before listing members, to specify how long to ban them for!"""
		# Time is 'optional'- it will either be eval'd to a time, or a member (ie, no time specified).
		try:
			time = int(time)
			#await self.bot.say('{} banned for {} mins.'.format(', '.join([m.name for m in members]), time))
		except ValueError:
			converter = commands.MemberConverter(ctx, time)
			members = list(members)
			members.insert(0, converter.convert())  # Let this raise to be consistent with the type hinting conversion
			#await self.bot.say('{} banned indefinitely.'.format(', '.join([m.name for m in members])))

	@commands.command(pass_context=True)
	async def unban(self, ctx, *members : discord.Member):
		""" Unbans the mentioned people """
		for member in members:
			await self.bot.unban(ctx.message.server, member)

	@commands.command(pass_context=True)
	async def mute(self, ctx, time, *members: discord.Member):
		""" Mutes the mentioned people (temp mute optional) """
		try:
			time = int(time)
			await self.bot.say('{} muted for {} mins.'.format(', '.join([m.name for m in members]), time))
		except ValueError:
			converter = commands.MemberConverter(ctx, time) #time != int, thus it MUST be a member
			members = list(members)
			members.insert(0, converter, convert())
			await self.bot.say('{} muted indefinitely.'.format(', '.join([m.name for m in members])))

	@commands.command()
	async def unmute(self, *members : discord.Member):
		""" Unmutes the mentioned people """
		pass

	@commands.command(pass_context=True)
	async def deafen(self, ctx, time, *members: discord.Member):
		""" Deafens the mentioned people (temp deafen optional) """
		pass

	@commands.command()
	async def undeafen(self, *members : discord.Member):
		""" Undeafens the mentioned people"""
		
def find_member(mention, members):
	return discord.utils.find(lambda m: m.mention == mention, members)

def setup(bot):
	bot.add_cog(Administration(bot))
