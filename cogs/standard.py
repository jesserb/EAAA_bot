import discord
from discord.ext import commands
from random import randint
import sys, asyncio, onoff
sys.path.append('../utils')
from constants import GUIDED_ROLES, GROLES, DORIANTALK, DESTICON, CHANNELS, CLNSERVERS
from functions import Get_Guided_Roles, Get_Role_Members, Guardian_Profile





'''
COMMANDS LIST:
- guardian
- congrats
- underbelly
'''
class StandardCog:
    
    def __init__(self, bot):
        self.bot = bot
    

    # This is a basic example of a call and response
    # command. You tell it do "this" and it does it.
    @commands.command(pass_context=True)
    async def guardian(self, ctx):
    
        if not onoff.check('guardian',CLNSERVERS['Ex Aspera Ad Astra']):
            return
        
        await self.bot.say('I sent you a private message <@'+str(ctx.message.author.id)+'> about setting up your Guardians profile.')
        
        msg = '**Guardian Profile initated by:** <@'+str(ctx.message.author.id)
        msg += '>\n\n Please answer the following questions **as described** to '
        msg += 'complete your guardian profile. \n\n**Note:** you must have a url '
        msg += 'for your guardian screenshot. If you do not know how to obtain such '
        msg += 'url, one option is to use **OneDrive**. Just upload your screenshot '
        msg += 'to OneDrive on Xbox (option is right there when viewing screenshots), '
        msg += 'navigate to [OneDrive](https://onedrive.live.com/about/en-us/), sign in '
        msg += 'using your xbox live credentials, select your image and click *"share"* '
        msg += 'to get a public link to your image. **One more step**, input that link '
        msg += 'into your browser, and select the image to go full-screen. **This is the '
        msg += 'image you want!**'
        
        await self.bot.send_message(ctx.message.author, msg)
        
        
        await self.bot.send_message(ctx.message.author, "What is the url to your Guardian Image?")
        img = await self.bot.wait_for_message(timeout=30.0, author=ctx.message.author)
        print(img)
        if img is None:
            await self.bot.say('<@'+str(ctx.message.author.id)+'> you did not respond in time. Please try the command again.')
            return
        
        await self.bot.send_message(ctx.message.author, "What is your guardian class, species, and power level? (send as a comma-seperated list, no spaces. For example: Warlock,Human,power")
        profile = await self.bot.wait_for_message(timeout=30.0, author=ctx.message.author)
        print(profile)
        if profile is None:
            await self.bot.say('<@'+str(ctx.message.author.id)+'> you did not respond in time. Please try the command again.')
            return
        
        #Check that user followed the directions
        if len((profile.content).split()) > 1:
            await self.bot.send_message(ctx.message.author, '<@'+str(ctx.message.author.id)+'> Your response is invalid, as it contained spaces. Please try again, and read the directions and follow the example provided.')
            return
    
        await self.bot.send_message(ctx.message.author, "Equiped Helmet?")
        helmet = await self.bot.wait_for_message(timeout=30.0, author=ctx.message.author)
        
        if helmet == None:
            await self.bot.say('<@'+str(ctx.message.author.id)+'> you did not respond in time. Please try the command again.')
            return

        await self.bot.send_message(ctx.message.author, "Equiped Gauntlets?")
        gauntlets = await self.bot.wait_for_message(timeout=30.0, author=ctx.message.author)

        if gauntlets == None:
            await self.bot.say('<@'+str(ctx.message.author.id)+'> you did not respond in time. Please try the command again.')
            return
        
        await self.bot.send_message(ctx.message.author, "Equiped Chest Armor?")
        chest = await self.bot.wait_for_message(timeout=30.0, author=ctx.message.author)

        if chest == None:
            await self.bot.say('<@'+str(ctx.message.author.id)+'> you did not respond in time. Please try the command again.')
            return

        await self.bot.send_message(ctx.message.author, "Equiped Leg Armor?")
        legs = await self.bot.wait_for_message(timeout=30.0, author=ctx.message.author)

        if legs == None:
            await self.bot.say('<@'+str(ctx.message.author.id)+'> you did not respond in time. Please try the command again.')
            return

        await self.bot.send_message(ctx.message.author, "Equiped Class Item?")
        classItem = await self.bot.wait_for_message(timeout=300.0, author=ctx.message.author)

        if classItem == None:
            await self.bot.say('<@'+str(ctx.message.author.id)+'> you did not respond in time. Please try the command again.')
            return

        await self.bot.send_message(ctx.message.author, "Equiped shaders? (send as comma-seperated list, no spaces. For example: shader1,shader2,shader3)?")
        shaders = await self.bot.wait_for_message(timeout=300.0, author=ctx.message.author)

        user = ctx.message.author.name
        grolesObj, groles = Get_Guided_Roles(ctx.message.author)

        desc, msg = Guardian_Profile(profile.content, helmet.content, gauntlets.content,
                                     chest.content, legs.content, classItem.content, shaders.content, groles, user)
        embed = discord.Embed(title='Guardian Profile', description=desc, color=1234123)
        embed.set_author(name=user, icon_url=DESTICON)
        embed.set_image(url=img.content)
        print(len(desc)+len(msg))
        print(msg)
        
        await self.bot.send_message(ctx.message.author, "Below is your guardian profile for review. If all looks good, reply with **'post it'**:")
        await self.bot.send_message(ctx.message.author,msg, embed=embed)
        res = await self.bot.wait_for_message(timeout=120.0, author=ctx.message.author)
        if res.content.lower() == 'post it':
                await self.bot.send_message(self.bot.get_channel(CHANNELS['GUARDIANCHNL']),msg, embed=embed)
        else:
            await self.bot.send_message(ctx.message.author, "**Guardian Profile not posted**. Please try again or @Admin for help.")



    @commands.command(pass_context=True)
    async def congrats(self, ctx, *args):
        
        if not onoff.check('congrats',CLNSERVERS['Ex Aspera Ad Astra']):
            return
        
        if len(ctx.message.mentions) > 0:
            randnum = randint(1,3)
            dstr = ctx.message.mentions[0].mention+DORIANTALK[randint(0, 7)]
            
            if randnum == 1:
                dstr += " - **=Pug, Bop & Slinger**"
                await self.bot.send_file(ctx.message.channel, 'img/bop_pug_slinger_2.gif',content= dstr)
            if randnum == 2:
                dstr += " - **Bop & Pug**"
                await self.bot.send_file(ctx.message.channel, 'img/pug_bop.gif',content= dstr)
            if randnum == 3:
                dstr += " - **Bop, Pug, & Slinger**"
                await self.bot.send_file(ctx.message.channel, 'img/bop_pug_slinger.gif',content= dstr)

    @commands.command(pass_context=True)
    async def underbelly(self, ctx, *args):
        
        if not onoff.check('underbelly',CLNSERVERS['Ex Aspera Ad Astra']):
            return
        
        if len(args) == 0:
            await self.bot.say(ctx.message.author.mention + ', Must include an argument')
            return
        
        # Command must be done in raid channel
        if ctx.message.channel.name != 'raid' and ctx.message.channel.name != 'team01' and ctx.message.channel.name != 'team02' and ctx.message.channel.name != 'team03':
            await self.bot.say(ctx.message.author.mention +\
                             ', This command must be ran in '+\
                             self.bot.get_channel(CHANNELS['RAIDCHNL']).mention)
            return
        #Supports map and code
        if args[0].lower() == 'map':
            await self.bot.say(ctx.message.author.mention + ', Here is a map of the underbelly!')
            await self.bot.send_file(ctx.message.channel, 'img/underbelly_leviathan.jpg')

        elif args[0].lower() == 'code':
            await self.bot.say(ctx.message.author.mention + ', The code is `153246`')

        else:
            await self.bot.say(ctx.message.author.mention + ', Invalid argument')


    # gets strategy image for given leviathan task
    # Currently supports dogs and gauntlet.
    @commands.command(pass_context=True)
    async def leviathan(self, ctx, *args):
        
        if not onoff.check('leviathan',CLNSERVERS['Ex Aspera Ad Astra']):
            return
        
        errors = ''
        memb = ctx.message.author
        rchnl = self.bot.get_channel(CHANNELS['RAIDCHNL'])
        
        # Command must be done in raid channel
        if ctx.message.channel.name != 'raid' and ctx.message.channel.name != 'team01' and ctx.message.channel.name != 'team02' and ctx.message.channel.name != 'team03':
            error = memb.mention + ', This command must be ran in ' + rchnl.mention
            await self.bot.say(error)
            return
   
        if len(args) == 0:
            error = memb.mention + ' You must include an argument.'
            await self.bot.say(error)
            return

        if args[0].lower() == 'pleasure' or args[0].lower() == 'dogs':
            await self.bot.say(ctx.message.author.mention + '\n**Bop\'s Strategy is below:**')
            await self.bot.send_file(ctx.message.channel, 'img/BopsPG.png')


        elif args[0].lower() == 'gauntlet':
            await self.bot.say(ctx.message.author.mention + '\n**Bop\'s Strategy is below:**')
            await self.bot.send_file(ctx.message.channel, 'img/BopsG.png')
        
        
        elif args[0].lower() == 'baths' or args[0].lower() == 'royal':
            await self.bot.say(ctx.message.author.mention + '\n**Bop\'s Strategy is below:**')
            await self.bot.send_file(ctx.message.channel, 'img/BopsB.png')
                
                
        elif args[0].lower() == 'baths' or args[0].lower() == 'calus':
            await self.bot.say(ctx.message.author.mention + '\n**Bop\'s Strategy is below:**')
            await self.bot.send_file(ctx.message.channel, 'img/BopsC.png')
        
        elif args[0].lower() == 'eow' or args[0].lower() == 'argos' or\
                                (args[0].lower() == 'raid' and args[0].lower() == 'lair'):
            await self.bot.say(ctx.message.author.mention + '\n**Bop\'s Strategy is below:**')
            await self.bot.send_file(ctx.message.channel, 'img/BopsEoW.png')
        else:
            error = memb.mention + ', invalid argument <' + args[0] + '>.'
            await self.bot.say(error)
            return


    @commands.command(pass_context=True)
    async def guides(self, ctx, *args):

        guide = ''
        memb = ctx.message.author

        if len(args) == 0:
            error = memb.mention + ' You must include an argument.'
            await self.bot.say(error)
            return

        if args[0].lower() == 'whisper' and args[1].lower() == 'of' and args[2].lower() == 'the' and args[3].lower() == 'worm':
            guide += "**WHISPER OF THE WORM: BOSS FIGHT STRATEGY\nProvided by Forward Theory\n_\n**"
            guide += 'The strategy for clearing the final boss room in Whisper mission is as follows...\n**Just a reminder:**\n```'
            guide += 'Adds spawn as bosses spawn and when bosses die. They will not keep spawning on their own. Also you can '
            guide += 'ignore the adds in the back left of the room. ' 
            guide += 'One player should always be damaging the boss while the other two target adds and the boss when no adds are alive.```\n'
            guide += '**1.** Save a super (Ideally arcstrider w/raiden flux) to clear the first adds in the room. If it was an arcstrider '
            guide += 'have him/her target the Taken captain boss. As that is happening you want the other two members of the fireteam '
            guide += 'destroying the two blights closest to where you drop down for the fight and then the second right side blight (this '
            guide += 'opens the room for line of sight).\n_\n'
            guide += '**2.** Once the boss Captain spawns, prioritize killing adds and the boss Captain with supers. The Captain denies '
            guide += 'line of sight for shooting so he is your first priority.\n_\n'
            guide += '**3.** Once you’ve cleared the Boss Captain and have made the other two bosses spawn by killing adds, your next '
            guide += 'target is the Knight who ends up on left side. He is area denial (with his fire) so clearing him is your second priority.\n'
            guide += '**4.** While step 2. and 3. are occurring make sure to clear the centurions (back right of the room) and the normal '
            guide += 'captains (front of the room) failure to do so makes the fight horrendous.\n_\n'
            guide += '**5.** Your final target should be the centurion boss who usually ends up in the back center of the room and by this '
            guide += 'point kill him with whatever you’ve got.\n_\n***If you wish to add to this guide, please @admin****\n'
            await self.bot.say(ctx.message.author.mention + ' Heres your guide!\n' + guide)
        else:
            error = memb.mention + ' No guide found for that'
            await self.bot.say(error)
            return




# The setup fucntion below is neccesarry. Remember we give
# bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(StandardCog(bot))














