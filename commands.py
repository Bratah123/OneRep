from discord.ext import commands

from utility import one_rep_max_percentages, weight_to_plates, percent


class Commands(commands.Cog, name="commands"):
    """
    A cog class that will handle all the commands of this bot
    """

    def __init__(self, bot):
        self._bot = bot

    @commands.command(name="1rm", pass_context=True)
    async def one_rm(self, ctx):
        """
        Given a weight, return all their percentages from 10-100% incrementing by 5%
        Additionally provide the amount of weight plates onto the bar.
        :param ctx:
        :return:
        """
        await one_rep_max(ctx, True)

    @commands.command(name="percentages", aliases=['ps'], pass_context=True)
    async def percentage(self, ctx):
        """
        Only display the percentages and their corresponding weights without the details
        :param ctx:
        :return:
        """
        await one_rep_max(ctx, False)

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
        await ctx.send("```"+weight_to_plates(weight_in_int)+"```")

    @commands.command(name="warmup_for_pr", pass_context=True)
    async def warm_up_to_pr(self, ctx):
        args = ctx.message.content.split()
        if len(args) < 2:
            await ctx.send("Please provide all necessary arguments: !warmup_for_pr <weight>")
            return

        weight = args[1]

        if not weight.isdecimal():
            await ctx.send("Please provide a valid weight number in lbs.")
            return

        weight_in_int = int(weight)
        percentages_to_reps = {
            50: 8,
            60: 5,
            70: 3,
            80: 1,
            90: 1,
            100: 1,
        }
        message = f"```\nWarm up Program for PR Day\nWeight: {weight_in_int}\n"

        for percentage in percentages_to_reps:
            message += f"\n{percentage}%: {percent(weight_in_int, percentage)} for {percentages_to_reps[percentage]} " \
                       f"reps -> {weight_to_plates(percent(weight_in_int, percentage))}"

        message += "\n%105+ PR rep```"
        await ctx.send(message)

    @commands.command(name="profile", pass_context=True)
    async def profile(self, ctx):
        pass


async def one_rep_max(ctx, show_details=True):
    """
    Given a weight, return all their percentages from 10-100% incrementing by 5%
    Additionally provide the amount of weight plates onto the bar
    :param show_details:
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
        if show_details:
            message += f"\n{i}%: {weight_percentages[index]} -> {weight_to_plates(weight_percentages[index])}"
        else:
            message += f"\n{i}%: {weight_percentages[index]}"
        index += 1
    message += "```"

    await ctx.send(message)


def setup(bot):
    bot.add_cog(Commands(bot))
