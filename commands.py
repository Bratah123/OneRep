from discord.ext import commands

from utility import one_rep_max_percentages, weight_to_plates


class Commands(commands.Cog, name="commands"):
    """
    A cog class that will handle all the commands of this bot
    """

    def __init__(self, bot):
        self._bot = bot

    @commands.command(name="1rm", pass_context=True)
    async def one_rep_max(self, ctx):
        """
        Given a weight, return all their percentages from 10-100% incrementing by 5%
        Additionally provide the amount of weight plates onto the bar
        :param ctx:
        :return:
        """
        args = ctx.message.content.split()
        if len(args) < 2:
            await ctx.send("Please provide all necessary arguments: !1rm <weight>")
            return

        weight = args[1]

        if not weight.isdecimal():
            await ctx.send("Please provide a valid weight number in lbs.")
            return

        weight_in_int = int(weight)
        weight_percentages = one_rep_max_percentages(weight_in_int)  # There should be 19 weights in total
        message = f"```\nWeight Percentages for {weight}"
        index = 0
        for i in range(10, 105, 5):
            # looping through 10-100% incrementing by 5% each iteration
            if weight_percentages[index] < 45.0:  # This way we don't show a weight where its lighter than the bar
                index += 1
                continue
            message += f"\n{i}%: {weight_percentages[index]} -> {weight_to_plates(weight_percentages[index])}"
            index += 1
        message += "```"

        await ctx.send(message)

    @commands.command(name="plates", pass_context=True)
    async def plates(self, ctx):
        """
        Given a weight, return the human readable english form of that to load onto a barbell
        :param ctx:
        :return:
        """
        args = ctx.message.content.split()
        if len(args) < 2:
            await ctx.send("Please provide all necessary arguments: !plates <weight>")
            return

        weight = args[1]

        if not weight.isdecimal():
            await ctx.send("Please provide a valid weight number in lbs.")
            return

        weight_in_int = int(weight)
        await ctx.send(weight_to_plates(weight_in_int))


def setup(bot):
    bot.add_cog(Commands(bot))
