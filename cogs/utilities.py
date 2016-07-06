from discord.ext import commands

from cogs.utils import output, math #Helpers

class Utilities():
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def math(self, ctx, expr : str):
		"""Evaluates a math expression"""
		#await self.bot.delete_message(ctx.message)
		await output.speak(self.bot, '{} = {}'.format(expr, math.eval_expr(expr)))
		

def setup(bot):
	bot.add_cog(Utilities(bot))