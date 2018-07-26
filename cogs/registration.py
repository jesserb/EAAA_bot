import discord
from discord.ext import commands
import sys, asyncio, perms, onoff
sys.path.append('../utils')
from constants import CHANNELS, CLNSERVERS
import functions as f



# Check if user is allowed to use command
def allowed(memb, lvls):
    lvl = perms.Get_Role(memb)
    for l in lvls:
        if l == lvl:
            return True
    return False


'''
COMMANDS LIST
- registration
'''
class RegistrationCog:
    
    def __init__(self, bot):
        self.bot = bot
        self.lvls = [1, 5, 6, 7] # allowed permissions for these commands



    # REGISTRATION COMMAND~~~
    @commands.command(pass_context=True)
    async def registration(self, ctx, arg=''):
        
        if not onoff.check('registration',CLNSERVERS['Ex Aspera Ad Astra']):
            return
        
        #ERROR CHECKS ~~~~~
        if not allowed(ctx.message.author, self.lvls):
            await self.bot.say(ctx.message.author.mention + ', you are already registered.')

        if arg == '':
            await self.bot.say(ctx.message.author.mention + ' An argument is required.')

        if ctx.message.channel.name != 'register':
            await self.bot.say(ctx.message.author.mention +\
            ' This command must be ran in '+ self.bot.get_channel(CHANNELS['REGISTERCHNL']).mention)


        # REGISTRATION BEGIN~~~~~~
        if arg.lower() == 'begin':
            m = f.Member_Obj(self.bot.get_all_members(), 'Charlemagne')
            msg, msg1, msg2 = f.Registration_Begin(ctx.message.author, 1)
            await self.bot.say(msg)
            await self.bot.say(msg1)
            await self.bot.say(msg2)
            
            # Bot will check roster for requirements,
            #and aid user with missing info
            success = False
            while not success:
                
                ans = await self.bot.wait_for_message(timeout=600, author=ctx.message.author)
                
                # a respons was never recieved by user
                if ans is None:
                    warn = ctx.message.author.mention+',\n**Your registration '
                    warn += 'has timed out**.\n You must restart the registration '
                    warn += 'procedure again with command:\n ```.registration begin```'
                    warn += '\n**NOTE**: Until you complete registration, your '
                    warn += 'access on this server is **GREATLY RESTRICTED**!!'
                    await self.bot.say(warn)
                    return
                
                # command cancel to exit registration command
                if ans.content.lower() == 'cancel':
                    await self.bot.say('Registration cancelled...')
                    return
                
                # Continue to next step, checking previous step.
                if ans.content.lower() == 'continue':
                    msg, params, success = f.Registration_Check_One(ctx.message.author)
                    await self.bot.say(msg)
                    
                    # followup message when roster requirements not met
                    if not success and len(params) != 0:
                        
                        msg = ctx.message.author.mention + '\n**You are missing '
                        msg += 'required parameters: **'
                        for p in params:
                            if p == 'Gamertag':
                                msg += 'GT:<'+p+'> '
                            else:
                                msg+= '<'+p+'> '
                        
                        prfx = ctx.message.author.mention + '\nUse the command: '
                        msg1 = '```css\n.roster add '
                        msg2 = ''
                        
                        # get missing parameters for each required add command
                        for p in params:
                            if p == 'Gamertag':
                                msg2 += '```css\n.roster add gt <'+p+'> '
                            else:
                                msg1 += '<'+p+'> '
                
                        # build message based on above results
                        if msg1 == '```css\n.roster add ':
                            msg1 = ''
                        else:
                            msg1 += '```'
                        
                        if msg2 != '':
                            msg1 = prfx + msg1 + ' and '+msg2+'```'
                        
                        msg1 += 'To add the above missing parameters in regards '
                        msg1 += 'to you individually.\nSee the first message we sent you '
                        msg1 += 'above right after you typed in the command **.registration '
                        msg1 += 'begin** for an example of valid commands.\n'
                        msg1 += 'Type and send the message **continue** when finished...'
                        await self.bot.say(msg)
                        await self.bot.say(msg1)
                        # wait for user to correct roster input, then check again
                        ans = await self.bot.wait_for_message(timeout=600, author=ctx.message.author)

            # Step 1 complete, confirm to user, move on
            confirm = ctx.message.author.mention +\
                ':white_check_mark: **Successfully added to the roster** --- continuing... ... ...\n'
            await self.bot.say(confirm)
            msg, msg1, msg2 = f.Registration_Begin(ctx.message.author, 2)
            await self.bot.say(msg)

            # dont advance until registration with Charlemagne finished
            while True:
                
                # dont advance until ans is equal to >loadout
                while True:
                    ans = await self.bot.wait_for_message(timeout=600, author=ctx.message.author)
                    # a respons was never recieved by user
                    if ans is None:
                        warn = ctx.message.author.mention+',\n**Your registration '
                        warn += 'has timed out**.\n You must restart the registration '
                        warn += 'procedure again with command:\n ```.registration begin```'
                        warn += '\n**NOTE**: Until you complete registration, your '
                        warn += 'access on this server is **GREATLY RESTRICTED**!!'
                        await self.bot.say(warn)
                        return
                    
                    if ans.content.lower() == 'cancel':
                        await self.bot.say('Registration cancelled...')
                        return
                    
                    if ans.content == '!loadout':
                        break

                # collect Charlemagne response to interpret
                charResp = await self.bot.wait_for_message(timeout=600, author=m)

                # If successful:
                if charResp.content == '' or ctx.message.author.name == 'test8787':
                    await self.bot.replace_roles(ctx.message.author,f.Role_Obj(ctx.message.server.roles, 'beginner'))
                    # update member status
                    f.Update_Member(ctx.message.author, ctx.message.author.name)
                    # send success message and end
                    msg = f.Registration_Final(ctx.message.author,
                                    self.bot.get_channel(CHANNELS['FOUNDERSCHNL']),
                                    self.bot.get_channel(CHANNELS['INFORMATIONCHNL']),
                                    True)
                    await self.bot.send_message(self.bot.get_channel(CHANNELS['GAMECHATCHNL']),msg)
                    break
                # If user failed to properly register with Charlemagne
                else:
                    msg = f.Registration_Final(ctx.message.author,
                                    self.bot.get_channel(CHANNELS['FOUNDERSCHNL']),
                                    self.bot.get_channel(CHANNELS['INFORMATIONCHNL']),
                                    False)
                    await self.bot.say(msg)
# REGISTRATION CLASS END

# set the cog up
def setup(bot):
    bot.add_cog(RegistrationCog(bot))







