import discord
from discord.ext import commands
from cogs.utils import output

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

	@commands.command()
	async def ban(self, *args : str):
		""" Bans the mentioned people (temp ban optional) """
		pass

	@commands.command()
	async def unban(self, *mentions : str):
		""" Unbans the mentioned people """
		pass

	@commands.command()
	async def mute(self, *args : str):
		""" Mutes the mentioned people (temp mute optional) """
		pass

	@commands.command()
	async def unmute(self, *mentions : str):
		""" Unmutes the mentioned people """
		pass

	@commands.command()
	async def deafen(self, *args : str):
		""" Deafens the mentioned people (temp deafen optional) """
		pass

	@commands.command()
	async def undeafen(self, *mentions : str):
		""" Undeafens the mentioned people"""
		
def setup(bot):
	bot.add_cog(Administration(bot))