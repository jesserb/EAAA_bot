import discord
from discord.ext import commands
import sys, asyncio, onoff
sys.path.append('../utils')
from constants import DESTICON, CLANICONWHT, CLNSERVERS
import functions as f




'''
COMMANDS LIST:
- champions
'''
class ChampionsCog:
    
    def __init__(self, bot):
        self.bot = bot
        self.next = '\N{BLACK RIGHTWARDS ARROW}'
        self.stop = '\N{WHITE SQUARE BUTTON}'
        self.prev = '\N{LEFTWARDS BLACK ARROW}'

    @commands.command(pass_context=True)
    async def champions(self, ctx, *args):   

        # make some variables for large class calls
        roles = ctx.message.server.roles
        memb = ctx.message.author
        r = [self.stop]

        if len(args) == 0:
            # Get Roles
            found = False
            championRoles = []

            for role in roles:
                found = False
                for champ in role.name.split():
                    if champ.lower() == 'champion' or champ.lower() == 'champions': 
                        found = True
                if found:
                    championRoles.append(role.name)

            members = set(self.bot.get_all_members())
            champDict = {}
    
            for role in championRoles:
                champDict[role] = []
                list, champ = f.Get_Role_Members(members, role)
                for l in list:
                    champDict[role].append(l)

            output = []
            str = ''
            for k, v in champDict.items():
                str += '**'+k+'**\n'
                for m in v:
                    str += '× '+m+'\n'
                output.append(str)
            embed = discord.Embed(title="**CHAMPIONS**", description=output[0], color=0x000000)
            embed.set_thumbnail(url = CLANICONWHT)
            msg = await self.bot.send_message(ctx.message.channel, embed=embed)

            # Add reactions
            await self.bot.add_reaction(msg,self.stop)
            if len(output) > 1:
                r.append(self.next)
                await self.bot.add_reaction(msg,self.next)
                
            # get response
            res = await self.bot.wait_for_reaction(message=msg, timeout=60)




            # Begin pagination.
            # This while loop will handle viewing
            # of the champions command until the end
            try:
                while res.reaction.emoji != self.stop or res.user != memb:
                    
                    # NEXT page~~
                    if res.reaction.emoji == self.next and res.user == memb and f.available(self.next, r):
                        i += 1
                        r = []
                        txt = 'page '+ str(i+1)+'/'+pgs
                        embed = discord.Embed(title="**CHAMPIONS**", description=output[i], color=0x000000)
                        embed.set_footer(text=txt, icon_url=CLANICONWHT)
                        msg = await self.bot.edit_message(msg, embed=embed)
                        await self.bot.clear_reactions(msg)
                        
                        # Add reactions
                        await self.bot.add_reaction(msg,self.prev)
                        await self.bot.add_reaction(msg,self.stop)
                        if len(output) > i + 1:
                            r.append(self.next)
                            await self.bot.add_reaction(msg,self.next)
                        r.append(self.prev)
                
                    # PREV page~~
                    elif res.reaction.emoji == self.prev and res.user == memb and f.available(self.prev, r):
                        i -= 1
                        r = []
                        txt = 'page '+ str(i+1)+'/'+pgs
                        embed = discord.Embed(title="**CHAMPIONS**", description=output[i], color=0x000000)
                        embed.set_footer(text=txt,icon_url=CLANICONWHT)
                        msg = await self.bot.edit_message(msg, embed=embed)
                        await self.bot.clear_reactions(msg)
                        
                        # Add reactions
                        if i != 0:
                            r.append(self.prev)
                            await self.bot.add_reaction(msg,self.prev)
                        await self.bot.add_reaction(msg,self.stop)
                        await self.bot.add_reaction(msg,self.next)
                        r.append(self.next)
                    
                    # Un-approved emoji reaction
                    # or user other than memb & EAAA
                    else:
                        if res.user != self.eaaa and res.user != self.eaaat:
                            await self.bot.remove_reaction(msg, res.reaction.emoji, res.user)

                    # get next reaction based on current page.
                    if i == 0:
                        res = await self.bot.wait_for_reaction(message=msg, timeout=60)
    
                    elif i == len(output) - 1:
                        res = await self.bot.wait_for_reaction(message=msg, timeout=60)

                    else:
                        res = await self.bot.wait_for_reaction(message=msg, timeout=60)

                    # Timeout
                    if res is None:
                        break
            except:
                str = ''

            # wrap up pagination, clear all reactions to indicate end.
            # add end to footer and new desc/or first page
            await self.bot.clear_reactions(msg)
            embed = discord.Embed(title='', description=output[0], color=1234123)
            embed.set_author(name='Ex Aspera Ad Astra Roster: ', icon_url= CLANICONWHT)
            embed.set_footer(text='Session End',icon_url=CLANICONWHT)
            msg = await self.bot.edit_message(msg, embed=embed)
            return
        


# The setup fucntion below is neccesarry. Remember we give
# bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(ChampionsCog(bot))














