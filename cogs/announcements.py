import discord
from discord.ext import commands
import sys, asyncio
import perms, onoff
sys.path.append('../utils')
from constants import DESTICON, CHANNELS, RAIDIMG, GAMBITIMG, TRIALSIMG, NFALLIMG, CRUCIMG, CLNSERVERS




'''
COMMANDS LIST:
- reset
- clanreward
'''
class AnnouncementsCog:
    
    def __init__(self, bot):
        self.bot = bot
        self.lvl = 5 # required permission to use commmands below
    

    # Function helps admin set up the various information
    # and guides for the Destiny 2 weekly reset.
    @commands.command(pass_context=True)
    async def reset(self, ctx):
        
        if not onoff.check('announcements',CLNSERVERS['Ex Aspera Ad Astra']):
            return
        
        if not perms.check(ctx.message.author, self.lvl):
            await self.bot.say(ctx.message.author +\
            ', You do not have permission to use this command.')
            return
        val4 = val5 = 'n'

        try:
            # Questions/Responses
            await self.bot.say('I sent you a private message <@'+\
              str(ctx.message.author.id)+'> about setting up the **Weekly Reset**.')
            
            await self.bot.send_message(ctx.message.author, 'The following '+\
                     'questions will help you set up the **Weekly Reset** message. '+\
                     'simply dont respond to the prompts - after 2mins, the command will quit.')
            
            await self.bot.send_message(ctx.message.author, 'Enter the date of this reset: ')
            val1 = await self.bot.wait_for_message(timeout=120.0, author=ctx.message.author)
            #Check for reply
            if val1 == None:
                await self.bot.say('<@'+str(ctx.message.author.id)+'> you did not '+\
                                   'respond in time. Please try the command again.')
                return
            
            await self.bot.send_message(ctx.message.author, 'Enter url for weekly reset image: ')
            val2 = await self.bot.wait_for_message(timeout=120.0, author=ctx.message.author)
            #Check for reply
            if val2 == None:
                await self.bot.say('<@'+str(ctx.message.author.id)+'> you did not '+\
                                   'respond in time. Please try the command again.')
                return
        
            await self.bot.send_message(ctx.message.author, 'Enter url for reset guide (general): ')
            val3 = await self.bot.wait_for_message(timeout=120.0, author=ctx.message.author)
            #Check for reply
            if val3 == None:
                await self.bot.say('<@'+str(ctx.message.author.id)+'> you did not '+\
                                   'respond in time. Please try the command again.')
                return
            
            # Optional information
            await self.bot.send_message(ctx.message.author, 'Want to include raid challenge video[yes/no]?: ')
            res = await self.bot.wait_for_message(timeout=120.0, author=ctx.message.author)

            if (res.content).lower() == 'yes':
                await self.bot.send_message(ctx.message.author, 'Input video url: ')
                val4 = await self.bot.wait_for_message(timeout=120.0, author=ctx.message.author)
            else:
                if (res.content).lower() != 'no':
                    await self.bot.say('<@'+str(ctx.message.author.id)+'> you did not '+\
                                   'respond in time. Please try the command again.')
                    return
            
            await self.bot.send_message(ctx.message.author, 'Want to include nightfall video[yes/no]?: ')
            res = await self.bot.wait_for_message(timeout=120.0, author=ctx.message.author)
            
            if (res.content).lower() == 'yes':
                await self.bot.send_message(ctx.message.author, 'Input video url: ')
                val5 = await self.bot.wait_for_message(timeout=120.0, author=ctx.message.author)
            else:
                if (res.content).lower() != 'no':
                    await self.bot.say('<@'+str(ctx.message.author.id)+'> you did not '+\
                                    'respond in time. Please try the command again.')
                    return
                                    
            val6 = []
            val7 = []
            val8 = []
            # Additional information to include - not standard reset
            while(True):
                await self.bot.send_message(ctx.message.author, 'Anything else this week?[yes/no]: ')
                res = await self.bot.wait_for_message(timeout=120.0, author=ctx.message.author)
                
                if (res.content).lower() == 'yes':
                    val6.append(True)
                    await self.bot.send_message(ctx.message.author, 'Title: ')
                    val7.append((await self.bot.wait_for_message(timeout=120.0, author=ctx.message.author)).content)
                    await self.bot.send_message(ctx.message.author, 'Url for guide/info: ')
                    val8.append((await self.bot.wait_for_message(timeout=120.0, author=ctx.message.author)).content)
                else:
                    val6.append(False)
                    break

            desc = 'Check out this [Weekly Reset Guide]('+val3.content+') for more info'
            embed = discord.Embed(title=':high_brightness: __**Everything you need '+\
                    'to know, right here!**__ :high_brightness:', description=desc, color=1234123)
            embed.set_author(name='Destiny 2', icon_url=DESTICON)

            # Add in any optional fields requested
            if val4 != 'n':
                if val5 != 'n':
                    embed.add_field(name="Raid Challenge Video",
                                    value='[Challenge]('+val4.content+') video')
                else:
                    embed.add_field(name="Raid Challenge Video",
                                    value='[Challenge]('+val4.content+') video', inline=False)
            if val5 != 'n':
                if val4 != 'n':
                    embed.add_field(name="Nightfall Video",
                                    value='[Nightfall]('+val5.content+') video')
                else:
                    embed.add_field(name="Nightfall Video",
                                    value='[Nightfall]('+val5.content+') video', inline=False)

            # Add in additional fields not standars to regular weekly reset
            i = 0;
            while(val6[i]):
                embed.add_field(name=val7[i], value='**'+val8[i]+'**!')
                i = i + 1

            # Finish embedded messaged
            embed.set_image(url=val2.content)
            embed.set_footer(text='Ex Aspera Ad Astra', icon_url=DESTICON)
            
            await self.bot.send_message(ctx.message.author, "Here is your message:")
            await self.bot.send_message(ctx.message.author,'**Weekly Reset: '+val1.content+'**', embed=embed)
            await self.bot.send_message(ctx.message.author, "type **confirm** or **cancel**")
            res = await self.bot.wait_for_message(timeout=120.0, author=ctx.message.author)
            if (res.content).lower() == 'confirm':
                await self.bot.send_message(ctx.message.author, "Reset has been posted to #weekly-events-and-reset")
                await self.bot.send_file(self.bot.get_channel(CHANNELS['WEEKLYRESETCHNL']), './img/weeklyReset.png')
                await asyncio.sleep(4)
                await self.bot.send_message(self.bot.get_channel(CHANNELS['WEEKLYRESETCHNL']),
                          '@everyone **Weekly Reset: '+val1.content+'**', embed=embed)
            else:
                await self.bot.send_message(ctx.message.author, "Message **cancelled**.")
        except:
            err = '**::SOMETHING WENT WRONG::**\n**Error**: Request caused 404 error \n'
            err = 'Check your links, when it asks for a video link, and reset guide link, '
            err = 'an image link, etc., you must provide a full URL.\n'
            await self.bot.send_message(ctx.message.author, err)


                                    
    # Send an announcement to the weekly-reset channnel
    # command requires 1 of 4 arguments: raid, nightfall
    # crucible, or trials.
    @commands.command(pass_context=True)
    async def clanreward(self, ctx, arg=None):
        
        if not onoff.check('announcements',CLNSERVERS['Ex Aspera Ad Astra']):
            return
        
        # ERROR CHECKING: Must be Admin
        if not perms.check(ctx.message.author, self.lvl):
            await self.bot.say(ctx.message.author +\
            ', You do not have permission to use this command.')
            return
        
        if arg != None:
            # some variables to make things easy
            engram = 'http://exo-boost.com/images/stories/virtuemart/product/legenary.png'
            chnl = self.bot.get_channel(CHANNELS['ANNOUNCEMENTSCHNL'])
            
            msg = '@everyone **New Clan Reward Incoming**'
            desc = '**New Clan Rewards** available from **Hawthorne**! \U0001f603 '
            embed = discord.Embed(title="", description=desc, color=000000)
            embed.set_author(name='Clan Engrams', icon_url=engram)
            
            # Customize embed based on arg value
            if arg.lower() == 'raid':
                embed.add_field(name='__Leviathan Raid__',value='Complete ')
                embed.add_field(name='__Reward__',value='Luminous Engram :crossed_swords: ')
                embed.set_image(url=RAIDIMG)

            elif arg.lower() == 'crucible':
                embed.add_field(name='__Crucible__',value='Complete')
                embed.add_field(name='__Reward__',value='Luminous Engram :crossed_swords: ')
                embed.set_image(url=CRUCIMG)
            
            elif arg.lower() == 'nightfall':
                embed.add_field(name='__Nightfall__',value='Complete')
                embed.add_field(name='__Reward__',value='Luminous Engram :crossed_swords: ')
                embed.set_image(url=NFALLIMG)

            elif arg.lower() == 'trials':
                embed.add_field(name='__Trials of the Nine__',value='Complete')
                embed.add_field(name='__Reward__',value='Luminous Engram :crossed_swords: ')
                embed.set_image(url=TRIALSIMG)

            elif arg.lower() == 'gambit':
                embed.add_field(name='__Gambit__',value='Complete')
                embed.add_field(name='__Reward__',value='Luminous Engram :crossed_swords: ')
                embed.set_image(url=GAMBITIMG)
            
            else:
                err =' :x:  argument not valid. Must be (raid, nightfall, trials, or crucible).'
                await self.bot.say(ctx.message.author.mention+err)
                return

            # confirm to user and finish embed
            conf = ':white_check_mark: Reward message initiated'
            await self.bot.say(ctx.message.author.mention+conf)
            embed.set_footer(text='Ex Aspera Ad Astra | Clan Reward',icon_url=DESTICON)
            await self.bot.send_message(chnl,msg, embed=embed)
            
        # ERROR CHECKING: Command requires argument
        else:
            err =' :x:  command requires argument (raid, nightfall, trials, or crucible).'
            await self.bot.say(ctx.message.author.mention+err)



    # Posts the announcement.png image to #announcements
    @commands.command(pass_context=True)
    async def announce(self, ctx):

        if not onoff.check('announcements',CLNSERVERS['Ex Aspera Ad Astra']):
            return

        if not perms.check(ctx.message.author, self.lvl):
            await self.bot.say(ctx.message.author +\
            ', You do not have permission to use this command.')
            return
        
        chnl = self.bot.get_channel(CHANNELS['ANNOUNCEMENTSCHNL'])
        await self.bot.send_file(chnl,'./img/announcements.png')
        await self.bot.say(ctx.message.author.mention + ", Announcement image has been posted to "+ chnl.mention)



# set the cog up
def setup(bot):
    bot.add_cog(AnnouncementsCog(bot))







