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

	@commands.command()
	async def tupac(self):
		""" What Tupac has to say about Biggie Smalls and Junior MAFIA """
		await self.bot.say_block('BIGGIE SMALLS AND JUNIOR M.A.F.I.A SOME MARK ASS BITCHES.')

def setup(bot):
	bot.add_cog(Fun(bot))