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
	async def vote_kick(self, *mentions : str):
		""" Calls a vote to kick a member """
		pass

	@vote.command(name='ban')
	async def vote_ban(self, *args : str):
		""" Calls a vote to ban a member """ 
		pass

	@vote.command(name='unban')
	async def vote_unban(self, *mentions : str):
		""" Calls a vote to unban a member """
		pass

	@vote.command(name='mute')
	async def vote_mute(self, *args : str):
		""" Calls a vote to mute a member """
		pass

	@vote.command(name='unmute')
	async def vote_unmute(self, *mentions : str):
		""" Calls a vote to unmute a member """
		pass

	@vote.command(name='deafen')
	async def vote_deafen(self, *args : str):
		""" Calls a vote to deafen a member """
		pass

	@vote.command(name='undeafen')
	async def vote_undeafen(self, *mentions : str):
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
		#await admin_utils.administrate('ban', self, ctx, time, members)
		await admin_utils.admin_do('ban', self.bot, ctx, members, time)

	@commands.command(pass_context=True)
	async def unban(self, ctx, *members : str):
		""" Unbans the mentioned people """
		await admin_utils.admin_undo('ban', self.bot, ctx, members)

	@commands.command(pass_context=True)
	async def mute(self, ctx, time, *members: discord.Member):
		""" Mutes the mentioned people (temp mute optional) """
		#await admin_utils.administrate('mute', self.bot, ctx, time, members, mute=True)
		await admin_utils.admin_do('mute', self.bot, ctx, members, time, mute=True) #True, we're DOING mute

	@commands.command(pass_context=True)
	async def unmute(self, ctx, *members : discord.Member):
		""" Unmutes the mentioned people """
		await admin_utils.admin_undo('mute', self.bot, ctx, members, mute=True) #True, we're UNDOING mute

	@commands.command(pass_context=True, aliases=['deaf'])
	async def deafen(self, ctx, time, *members: discord.Member):
		""" Deafens the mentioned people (temp deafen optional) """
		await admin_utils.admin_do('deafen', self.bot, ctx, members, time, deafen=True) #True, we're DOING deafen

	@commands.command(pass_context=True, aliases=['undeaf'])
	async def undeafen(self, ctx, *members : discord.Member):
		""" Undeafens the mentioned people"""
		await admin_utils.admin_undo('deafen', self.bot, ctx, members, deafen=True) #True, we're UNDOING deafen

	@commands.command(pass_context=True, aliases=['chmute', 'cmute'])
	async def chatmute(self, ctx, time, *members : discord.Member):
		""" Removes the messaging privilege of the specified members.self.bot
		Time optional for temp chat mute """
		await admin_utils.admin_do('chatmute', self.bot, ctx, members, time)

	@commands.command(pass_context=True, aliases=['chunmute', 'cunmute', 'chun', 'cun'])
	async def chatunmute(self, ctx, *members : discord.Member):
		""" Restors the messaging privilege of the specified members. """
		await admin_utils.admin_undo('chatmute', self.bot, ctx, members)

def setup(bot):
	bot.add_cog(Administration(bot))

