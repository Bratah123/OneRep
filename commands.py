import asyncio

import discord
from discord import Color
from discord.ext import commands

from database_functions import *
from utility import one_rep_max_percentages, weight_to_plates, percent

OWNER_ID = "207371595113562124"


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
        await ctx.send("```" + weight_to_plates(weight_in_int) + "```")

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
        args = ctx.message.content.split()
        client_id = str(ctx.author.id)
        name = ctx.author.name

        if len(args) >= 2:
            name = args[1]
            client_id_new = ""
            for c in name:
                if c.isdecimal():
                    client_id_new += c
            client_id = client_id_new
            if not user_exists(client_id):
                await ctx.send("This user does not exist or has not registered themselves.")
                return

        if not user_exists(client_id):
            print(f"User {client_id} is now being created...")
            create_new_profile(client_id)

        sbd_total = get_squat(client_id) + get_bench(client_id) + get_deadlift(client_id)

        profile_embed = discord.Embed(title=name + "'s Profile",
                                      colour=Color.teal(),
                                      description=f"SBD Total: {sbd_total}lbs"
                                      )
        profile_embed.add_field(name="Powerlifting",
                                value=f"[Squat]({get_squat_url(client_id)}): {get_squat(client_id)}lbs"
                                      f"\n[Bench Press]({get_bench_url(client_id)}): {get_bench(client_id)}lbs"
                                      f"\n[Deadlift]({get_deadlift_url(client_id)}): {get_deadlift(client_id)}lbs",
                                inline=False)

        profile_embed.add_field(name="Weightlifting",
                                value=f"[Clean and Jerk]({get_clean_and_jerk_url(client_id)}): "
                                      f"{get_clean_and_jerk(client_id)}lbs"
                                      f"\n[Snatch]({get_snatch_url(client_id)}): {get_snatch(client_id)}lbs",
                                inline=False)

        # Hard Coded Achievements for now
        profile_embed.add_field(name="Achievements",
                                value="**W.I.P.**", inline=False)
        await ctx.send(embed=profile_embed)

    @commands.command(name="set_profile", pass_context=True)
    async def set_profile(self, ctx):
        client_id = str(ctx.author.id)

        if not user_exists(client_id):
            await ctx.send("your profile is not set up yet, please do !profile.")
            return

        args = ctx.message.content.split()

        if len(args) < 4:
            await ctx.send("Please provide all necessary arguments: !set_profile <lift> <weight> <url_to_lift>\n"
                           "Possible Lifts: Squat, Bench, Deadlift, C&J, Snatch")
            return

        possible_lifts = ["squat", "bench", "deadlift", "c&j", "snatch", "clean_and_jerk"]

        lift = args[1]
        weight_str = args[2]
        url = args[3]
        # commence sanity checks
        if lift.lower() not in possible_lifts:
            await ctx.send("Please provide a valid lift type.\nPossible Lifts: Squat, Bench, Deadlift, C&J, Snatch")
            return

        if not weight_str.isdecimal():
            await ctx.send("Please provide a valid weight amount in lbs.")
            return

        if not url.startswith("http"):
            await ctx.send("Please provide a valid link to your lift.")
            return

        weight = int(weight_str)

        def check(reaction_, user_):
            return str(user_.id) == OWNER_ID and (str(reaction_.emoji) == '👍' or str(reaction_.emoji) == '👎')

        await ctx.send("Please wait for approval of lift!")

        try:
            reaction, user = await self._bot.wait_for('reaction_add', timeout=180.0, check=check)
            if str(reaction.emoji) == '👍':
                await ctx.send("lift approved, it should now appear in your profile!")
            else:
                await ctx.send("lift not approved, ask reviewer for reasons why")
                return
        except asyncio.TimeoutError:
            await ctx.send("no one approved of the lift in time.")

        DATABASE[client_id][lift.lower()] = weight
        DATABASE[client_id][lift.lower()+"_url"] = url

    @commands.command(name="save_db", pass_context=True)
    async def save(self, ctx):
        if str(ctx.author.id) != OWNER_ID:
            return
        try:
            save_db()
        except Exception as e:
            await ctx.send("error saving database, possible rollbacks: ", e)
        await ctx.send("Successfully saved the cached database")


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
