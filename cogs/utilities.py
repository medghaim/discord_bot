from discord.ext import commands
from cogs.utils import output
from cogs.utils import math

class Utilities():
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def math(self, expr : str):
		""" Evaluates a math expression """
		await output.speak(self.bot, math.eval_expr(expr))
		#await output.speak(self.bot, ", ".join(args))
		

def setup(bot):
	bot.add_cog(Utilities(bot))