from discord.ext import commands

from utils import output
from utils import math

class Utilities():
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def math(self, expr : str):
		"""Evaluates a math expression"""
		#await self.bot.delete_message(ctx.message)
		await output.speak(self.bot, '{} = {}'.format(expr, math.eval_expr(expr)))
		

def setup(bot):
	bot.add_cog(Utilities(bot))