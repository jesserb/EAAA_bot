import discord
from discord.ext import commands
import sys, asyncio
import perms, onoff
sys.path.append('../utils')
from constants import CLANLOGOBLK, CLANICONWHT, VERSION, CLNSERVERS
import functions as f


'''
COMMANDS LIST:
- help
'''
class HelpCog:
    
    def __init__(self, bot):
        self.bot = bot
        self.lvl = 5 # some comands sensitive here


    @commands.command(pass_context=True)
    async def help(self, ctx, *args):
        
        if not onoff.check('help',CLNSERVERS['Ex Aspera Ad Astra']):
            return
        
        if len(args) == 0:
            ttl = 'Ex Aspera Ad Astra Bot Commands'
            desc, roster, gr, D2, other = f.Help_Gen()
            embed = discord.Embed(title=ttl, description=desc, color=0xD6D6D6)
            embed.set_author(name='EAAA | Version '+VERSION, icon_url=CLANICONWHT)
            embed.add_field(name='**roster commands**', value=roster , inline=False)
            embed.add_field(name='**guidedroles commands**', value=gr , inline=False)
            embed.add_field(name='**Destiny 2 Commands**', value=D2 , inline=False)
            embed.add_field(name='**other commands**', value=other , inline=False)
            embed.set_image(url=CLANLOGOBLK)
            embed.set_footer(text='Ex Aspera Ad Astra Bot Commands',icon_url=CLANICONWHT)
            await self.bot.send_message(ctx.message.channel, embed=embed)

        else:
            if args[0].lower() == 'roster':
                desc, r1, r2, r3, r4, r5 = f.Help_Roster()
                embed = discord.Embed(title='Roster Commands', description=desc, color=0xD6D6D6)
                embed.set_author(name='EAAA | Version '+VERSION, icon_url=CLANICONWHT)
                embed.add_field(name=':beginner:  **roster add**', value=r1 , inline=False)
                embed.add_field(name=':beginner:  **roster add gt**', value=r2 , inline=False)
                embed.add_field(name=':beginner:  **roster add gt**', value=r3 , inline=False)
                embed.add_field(name=':beginner:  **roster show**', value=r4 , inline=False)
                embed.add_field(name=':beginner:  **roster @user**', value=r5 , inline=False)
                embed.set_image(url=CLANLOGOBLK)
                embed.set_footer(text='Ex Aspera Ad Astra Bot Roster Commands',icon_url=CLANICONWHT)
                await self.bot.send_message(ctx.message.channel, embed=embed)
            
            
            if args[0].lower() == 'guidedroles':
                desc, gr1, gr2 = f.Help_Guidedroles()
                embed = discord.Embed(title='Guided Roles Commands', description=desc, color=0xD6D6D6)
                embed.set_author(name='EAAA | Version '+VERSION, icon_url=CLANICONWHT)
                embed.add_field(name=':beginner:  **guidedroles add**', value=gr1 , inline=False)
                embed.add_field(name=':beginner:  **guidedroles**', value=gr2 , inline=False)
                embed.set_image(url=CLANLOGOBLK)
                embed.set_footer(text='Ex Aspera Ad Astra Bot guidedroles Commands',icon_url=CLANICONWHT)
                await self.bot.send_message(ctx.message.channel, embed=embed)
            
            
            if args[0].lower() == 'destiny':
                desc, d1, d2, d3, d4 = f.Help_Destiny()
                embed = discord.Embed(title='Destiny 2 Commands', description=desc, color=0xD6D6D6)
                embed.set_author(name='EAAA | Version '+VERSION, icon_url=CLANICONWHT)
                embed.add_field(name=':beginner:  **guardian**', value=d1 , inline=False)
                embed.add_field(name=':beginner:  **underbelly**', value=d2 , inline=False)
                embed.add_field(name=':beginner:  **leviathan**', value=d3 , inline=False)
                embed.add_field(name=':beginner:  **guides**', value=d4 , inline=False)
                embed.set_image(url=CLANLOGOBLK)
                embed.set_footer(text='Ex Aspera Ad Astra Bot Destiny 2 Commands',icon_url=CLANICONWHT)
                await self.bot.send_message(ctx.message.channel, embed=embed)


            if args[0].lower() == 'other':
                desc, o1, o2, o3 = f.Help_Other()
                embed = discord.Embed(title='Other Commands', description=desc, color=0xD6D6D6)
                embed.set_author(name='EAAA | Version '+VERSION, icon_url=CLANICONWHT)
                embed.add_field(name=':beginner:  **congrats**', value=o1 , inline=False)
                embed.add_field(name=':beginner:  **poll**', value=o2 , inline=False)
                embed.add_field(name=':beginner:  **tally**', value=o3 , inline=False)
                embed.set_image(url=CLANLOGOBLK)
                embed.set_footer(text='Ex Aspera Ad Astra Bot Other Commands',icon_url=CLANICONWHT)
                await self.bot.send_message(ctx.message.channel, embed=embed)


            if args[0].lower() == 'admin':
                if ctx.message.channel.name == 'admin-chat' or ctx.message.channel.name == 'admin-testing'\
                    or ctx.message.channel.name == 'eaaa-bug-reporting':
                    if  perms.check(ctx.message.author, self.lvl):
                        desc, roster, radmin, announce, reg, other = f.Help_Admin()
                        embed = discord.Embed(title='Admin ONLY Commands', description=desc, color=0xD6D6D6)
                        embed.set_author(name='EAAA | Version '+VERSION, icon_url=CLANICONWHT)
                        embed.add_field(name=':beginner:  **roster commands**', value=roster , inline=False)
                        embed.add_field(name=':beginner:  **rosteradmin commands**', value=radmin , inline=False)
                        embed.add_field(name=':beginner:  **announcement commands**', value=announce , inline=False)
                        embed.add_field(name=':beginner:  **registration commands**', value=reg , inline=False)
                        embed.add_field(name=':beginner:  **administrative commands**',value=other,inline=False)
                        embed.set_image(url=CLANLOGOBLK)
                        embed.set_footer(text='Ex Aspera Ad Astra Bot Other Commands',icon_url=CLANICONWHT)
                        await self.bot.send_message(ctx.message.channel, embed=embed)
                else:
                    await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(HelpCog(bot))





