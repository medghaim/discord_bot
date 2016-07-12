import discord
from discord.ext import commands
#from utils import admin_utils

from utils import admin_utils

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
	async def kick(self, *members : discord.Member):
		""" Kicks the mentioned people """
		if len(members) == 0:
			raise commands.MissingRequiredArgument('Must specify member(s) to kick.')

		kicked = []
		for member in members:
			await self.bot.kick(member)
			kicked.append(member.name)
			
		await self.bot.say_block('Kicked: {}'.format(", ".join(kicked)))

	@commands.command(pass_context=True)
	async def ban(self, ctx, time, *members: discord.Member):
		""" Ban the mentioned members (temp ban optional) 
		You can specify a time (in mins) before listing members, to specify how long to ban them for!"""
		# Time is 'optional'- it will either be eval'd to a time, or a member (ie, no time specified).
		await admin_utils.administrate('ban', self, ctx, time, members)

	@commands.command(pass_context=True)
	async def unban(self, ctx, *members : str):
		""" Unbans the mentioned people 
		if len(members) == 0:
			raise commands.MissingRequiredArgument('Must specify member(s) to unban.')

		bans = await self.bot.get_bans(ctx.message.server)
		for member in members:	#for each member
			try:
				unban = [m for m in bans if m.name.lower() == member.lower()][0] # match the FIRST member in bans
				await self.bot.unban(ctx.message.server, unban)
			except IndexError:
				await self.bot.say('Member \'{}\' not found.'.format(member))
		"""
		await admin_utils.deadministrate(members, 'unban')

	@commands.command(pass_context=True)
	async def mute(self, ctx, time, *members: discord.Member):
		""" Mutes the mentioned people (temp mute optional) """
		await admin_utils.administrate('mute', self, ctx, time, members, mute=True)

	@commands.command()
	async def unmute(self, *members : discord.Member):
		""" Unmutes the mentioned people """
		await admin_utils.deadministrate('unmute', self, members)

	@commands.command(pass_context=True)
	async def deafen(self, ctx, time, *members: discord.Member):
		""" Deafens the mentioned people (temp deafen optional) """
		await admin_utils.administrate('deafen', self, ctx, time, members, deafen=True)

	@commands.command()
	async def undeafen(self, *members : discord.Member):
		""" Undeafens the mentioned people"""
		await admin_utils.deadministrate('undeafen', self, members)

	@commands.command(pass_context=True, aliases=['chmute', 'cmute'])
	async def chatmute(self, ctx, time, *members : discord.Member):
		""" Removes the messaging privilege of the specified members.
		Time optional for temp chat mute """
		await admin_utils.administrate('chatmute', self, ctx, time, members)

	@commands.command(aliases=['chunmute', 'cunmute', 'chun', 'cun'])
	async def chatunmute(self, *members : discord.Member):
		""" Restors the messaging privilege of the specified members. """
		admin_utils.deadministrate('chatunmute', self, members)

def setup(bot):
	bot.add_cog(Administration(bot))

