from discord.ext import commands

from utils import math

class Utilities():
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def math(self, expr : str):
		""" Evaluates a math expression. """
		await self.bot.say_block('{} = {}'.format(expr, math.eval_expr(expr)))
		

def setup(bot):
	bot.add_cog(Utilities(bot))