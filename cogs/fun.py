from discord.ext import commands

class Fun():
	def __init__(self, bot):
		self.bot = bot

	@commands.group(invoke_without_command=True)
	async def mlg(self, name : str):
		""" Gamertag of the best of the best """
		await self.bot.say_block('xXx_69_{}_69_xXx420360noscopeblazeit'.format(name))

	@mlg.command(name='me', pass_context=True)
	async def _me(self, ctx):
		""" YOUR epicly awesome gamertag """
		await ctx.command.parent.callback(self, ctx.message.author.name)

def setup(bot):
	bot.add_cog(Fun(bot))