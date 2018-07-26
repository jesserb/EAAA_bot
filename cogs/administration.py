import discord
from discord.ext import commands
import sys, asyncio
import perms, onoff
sys.path.append('../utils')
from constants import CHANNELS, ACTIVECHANNELS, CLANICONWHT, VERSION, CLNSERVERS
import functions as f
import datetime, re

'''
COMMANDS LIST:
- clear
- channelid
'''
class AdministrationCog:
    
    def __init__(self, bot):
        self.bot = bot
        self.lvl = 5 # some comands sensitive here
        self.next = '\N{BLACK RIGHTWARDS ARROW}'
        self.stop = '\N{WHITE SQUARE BUTTON}'
        self.prev = '\N{LEFTWARDS BLACK ARROW}'
        self.eaaa  = f.Member_Obj(self.bot.get_all_members(), 'EAAA')
        self.eaaat = f.Member_Obj(self.bot.get_all_members(), 'EAAA-tester')


    # change the settings of the various commands
    # from EAAA. Current options are simply ON/OFF
    @commands.command(pass_context=True)
    async def EAAA(self, ctx, cmd='', switch=''):
        
        # chnl variable for better handeling
        chnl = ctx.message.channel.name
        
        #ERROR CHECKING: correct channel list
        if chnl != 'admin-chat' and chnl != 'admin-testing':
            await self.bot.delete_message(ctx.message)
            await self.bot.say(ctx.message.author.mention+', command not allowed here.')
            return
        
        #ERROR CHECKING: command specified
        if cmd == '':
            await self.bot.say('Must supply command as 1st argument')
            return
    
        # return list of settings to admin
        if cmd.lower() == 'settings' and switch == '':
            msg = onoff.Get_Command_Settings()
            embed = discord.Embed(title="**Command Settings**", description=msg, color=0x000000)
            embed.set_author(name='EAAA | Version '+VERSION, icon_url=CLANICONWHT)
            embed.set_thumbnail(url = CLANICONWHT)
            embed.set_footer(text='Ex Aspera Ad Astra Bot Commands',icon_url=CLANICONWHT)
            await self.bot.send_message(ctx.message.channel, embed=embed)
            return
                
        #ERROR CHECKING: switch is not empty
        if switch == '':
            err = ':x: If your setting a command, additional argument '
            err += 'of `on` or `off` is required.'
            await self.bot.say(err)
            return
        
        # Turn all commands on or off
        if cmd.lower() == 'all':
            if switch.lower() == 'on' or switch.lower() == 'off':
                
                action = onoff.setAll(switch)
                if not action:
                    await self.bot.say('Command group not found.')
                    return
                
                await self.bot.say(':white_check_mark: `ALL` commands turned `'+switch.upper()+'`.')
        
            # bot recieved input that was neither on nor off.
            else:
                await self.bot.say('`'+switch+'` is not a valid option.')
            return

        # turn a single command category on or off
        if switch.lower() == 'on' or switch.lower() == 'off':
            
            action, issue = onoff.set(cmd,switch)
            if not action:
                await self.bot.say(':x: Invalid argument <'+issue+'>.')
                return
            
            await self.bot.say(':white_check_mark: .'+cmd+' commands turned `'+switch.upper()+'`.')

        # bot recieved input that was neither on nor off.
        else:
            await self.bot.say('`'+switch+'` is not a valid option.')
    
    
                               
    # Function deletes the last 'n' amount of messages
    # in same channel as the command was given in.
    @commands.command(pass_context=True)
    async def clear(self, ctx, number):
        if not perms.check(ctx.message.author, self.lvl):
            err = ctx.message.author.mention + 'You do not have permission to use this command.'
            await self.bot.say(err)
            return
        number = int(number) + 1
        counter = 0
        count = 0
        async for x in self.bot.logs_from(ctx.message.channel, limit = number):
            count += 1
            if counter < number:
                await self.bot.delete_message(x)
                counter += 1



    # command returns the discord channel id for
    # the current channel of command user
    @commands.command(pass_context=True)
    async def channelid(self, ctx):
        await self.bot.say(ctx.message.channel.name+': `'+ctx.message.channel.id+'`')



    # command sets the ascended role to given member
    # in argument 1. This is a multi step process,
    # requiring admin approval
    @commands.command(pass_context=True)
    async def ascended(self, ctx, *args):
        
        # check for ovveride in arguments
        override = False
        for a in args:
            if a.lower() == 'override' and ctx.message.author.name == 'Bop':
                args = args[:-1]
                override = True
        
        #BUILD USERNAME
        arg1 = ''
        for i in range(len(args)):
            if i == len(args) - 1:
                arg1 += args[i]
            else:
                arg1 += args[i] + ' '

        #PERMS CHECK
        if not perms.check(ctx.message.author, self.lvl):
            err = ctx.message.author.mention + ' You do not have permission to use this command.'
            await self.bot.say(err)
            return
        
        #ERROR CHECKING
        if len(args) == 0:
            err = ':x: '+ctx.message.author.mention + ' Command requires user as argument.'
            await self.bot.say(err)
            return
        if f.Member_Obj(self.bot.get_all_members(), arg1) is None:
            err = ':x: '+ctx.message.author.mention + ', '+arg1+' is not a valid username.'
            await self.bot.say(err)
            return
        
        # variables
        roles = ctx.message.server.roles
        ascendedRole = f.Role_Obj(roles, 'Ascended')
        ascendedMemb = f.Member_Obj(self.bot.get_all_members(), arg1)
        cont = False
        await self.bot.say(ctx.message.author.mention+', I sent you a pm.')

        # PERFORM AUTOCHECKS
        msg = f.Ascended_Check(1,arg1, '')
        botmsg = await self.bot.send_message(ctx.message.author,msg)
        await asyncio.sleep(5.0)
        grO, grS = f.Get_Guided_Roles(ascendedMemb)
        if len(grO) > 0:
            cont = True
            msg = f.Ascended_Check(2,arg1,':white_check_mark:')
            botmsg = await self.bot.edit_message(botmsg,msg)
        else:
            msg = f.Ascended_Check(2,arg1, ':x:')
            botmsg = await self.bot.edit_message(botmsg,msg)
            err = '\nUser does not have any **guidedroles**, and therefore does '
            err += 'not qualify for the role of **Ascended**.\n'
            err += ':x: **Submission Denied**'
            await self.bot.send_message(ctx.message.author,err)
            return

        if cont:
            await asyncio.sleep(5.0)
            cont = False
            if f.User_Joined_By(ascendedMemb, 28) or override:
                cont = True
                msg = f.Ascended_Check(3,arg1,':white_check_mark:')
                botmsg = await self.bot.edit_message(botmsg,msg)
            else:
                msg = f.Ascended_Check(3,arg1,':x:')
                botmsg = await self.bot.edit_message(botmsg,msg)
                err = '\nUser has not been in the clan for a minimum time '
                err += 'of **1 month**, and therefore does '
                err += 'not qualify for the role of **Ascended**.\n'
                err += ':x: **Submission Denied**'
                await self.bot.send_message(ctx.message.author,err)
                return

        if cont:
            cont = False
            break_flag = False
            target = datetime.datetime.today() - datetime.timedelta(days=7)
            for k in ACTIVECHANNELS:
                chnl = self.bot.get_channel(ACTIVECHANNELS[k])
                async for message in self.bot.logs_from(chnl, after=target, limit=2000):
                    if message.author == ascendedMemb:
                        break_flag = True
                        cont = True
                        break
                if break_flag:
                    break

        if cont:
            msg = f.Ascended_Check(4,arg1,':white_check_mark:')
            await asyncio.sleep(3.0)
            botmsg = await self.bot.edit_message(botmsg,msg)
            await asyncio.sleep(3.0)
        else:
            msg = f.Ascended_Check(4,arg1,':x:')
            botmsg = await self.bot.edit_message(botmsg,msg)
            err = '\nUser has not been **active** enough on **discord**, '
            err += 'and therefore does not qualify for the role of **Ascended**.\n'
            err += ':x: **Submission Denied**'
            await self.bot.send_message(ctx.message.author,err)
            return

        # CHECKS SUCCESSFULL, SEND REST OF MESSAGE
        msg = '\n:white_check_mark: Checks **sucessful**, the rest must be '
        msg += 'confirmed by you manually..\n'
        msgtemp = '**Just a moment... ... ...**'
        botmsg = await self.bot.send_message(ctx.message.author,msg+msgtemp)
        await asyncio.sleep(5.0)
        msg = '\nThe bold statements above are required. If '+arg1+' qualifies for '
        msg += 'at least **6/7** of the above criteria, then they are qualified '
        msg += 'for the ascended role.\nYou can respond with **confirm** or **cancel**.'
        await self.bot.edit_message(botmsg,msg)
        resp = await self.bot.wait_for_message(timeout=120.0, author=ctx.message.author)

        if resp is None:
            err = '**:x: Command timedout. Please try again.**'
            await self.bot.send_message(ctx.message.author,err)
            return

        # Confirm nomination, begin process of nomination
        if resp.content.lower() == 'confirm':

            chnl = self.bot.get_channel(CHANNELS['ADMINCHATCHNL'])
            responder = f.Member_Obj(self.bot.get_all_members(), resp.author.name)
            
            # non-Founders must have a second confirm nomination
            if not f.Member_Is_Role(responder, 'Founder'):
                msg = 'Thank you,\nTo continue, another Admin must confirm the nomination. '
                msg += 'We have sent a message to Admin-Chat stating this.'
                await self.bot.send_message(ctx.message.author,msg)
                admsg = f.Role_Obj(roles, 'Admin').mention+',\n\n'
                admsg += ctx.message.author.mention + ' has nomiminated **' + arg1
                admsg += '** for the role of '+f.Role_Obj(roles, 'Ascended').mention
                admsg += '.\nWe require **one additional **'+ f.Role_Obj(roles, 'Admin').mention
                admsg += ' to confirm this nomination to continue.\n\nPlease send the '
                admsg += 'message ***"confirm '+arg1+'"*** to validate this nomination.'
                await self.bot.send_message(chnl,admsg)
                
                # Check admin-chat for second admin confirmation
                while True:
                    resp = await self.bot.wait_for_message(timeout=300.0, channel=chnl)
                    if resp.content.lower() == 'confirm '+arg1.lower():
                        if f.Member_Is_Role(resp.author, 'Admin'):
                            if resp.author != ctx.message.author or resp.author.name == 'Bop':
                                msg = f.Ascended_Message(ascendedMemb)
                                await self.bot.send_file(ascendedMemb, 'img/ascended.png')
                                await self.bot.send_message(ascendedMemb,msg)
                                conf = f.Role_Obj(roles, 'Admin').mention + ' **"'+arg1+'"** '
                                conf += 'has been sent a message informing them of their '
                                conf += 'nomination for '+ascendedRole.mention+'.'
                                await self.bot.send_message(chnl,conf)
                                return
                    # timeout
                    if resp is None:
                        tout = ctx.message.author.mention + ', there was no response '
                        tout += 'from another admin. Please try again later.'
                        await self.bot.send_message(chnl,tout)
                        return

            # Founder responsible for nomination
            else:
                msg = 'As the clan **Founder**, a *second* confirmation from another Admin '
                msg += 'is not required...\nJust a moment please...'
                await asyncio.sleep(3.0)
                await self.bot.send_message(ctx.message.author,msg)
                await self.bot.send_file(ascendedMemb, 'img/ascended.png')
                await self.bot.send_message(ascendedMemb,f.Ascended_Message(ascendedMemb))
                msg = '**There!!** Member `'+arg1+'` has been sent a message about their '
                msg += 'nomination for the role **Ascended**. a message will be sent to '
                msg += '**admin-chat** to inform the Admins.'
                await self.bot.send_message(ctx.message.author,msg)
                await asyncio.sleep(3.0)
                admsg = f.Role_Obj(roles, 'Admin').mention+',\n\n'
                admsg += ctx.message.author.mention + ' has nomiminated **' + arg1
                admsg += '** for the role of '+f.Role_Obj(roles, 'Ascended').mention
                admsg += '.\nas the clan '+ f.Role_Obj(roles, 'Founder').mention
                admsg += ', this nomination has been **automatically accepted**, and the '
                admsg += 'invite has been sent to '+arg1+'.'
                await self.bot.send_message(chnl,admsg)
        else:
            await self.bot.send_message(ctx.message.author,' The process has been cancelled.')
    


    # Command that checks user activity in the last however
    # many weeks on the server, as specified by the callee.
    # callee.
    @commands.command(pass_context=True)
    async def activity(self, ctx, arg1='', arg2=''):
        
        memb = ctx.message.author
        
        # PERMS CHECK
        if not perms.check(memb, self.lvl):
            err = memb.mention + 'You do not have permission to use this command.'
            await self.bot.say(err)
            return
        
        #ERROR CHECKING
        try:
            if arg1.lower() != 'full':
                int(arg1)
            if arg2.lower() != 'week' and arg2.lower() != 'weeks':
                err = ':x: '+memb.mention+', arg2 must be week or weeks.'
                await self.bot.say(err)
                return
        except:
            err = ':x: '+memb.mention+', arg1 must be integer in this form.'
            await self.bot.say(err)
            return

        #variables
        mcount = 0
        num_msgs = 0
        desc = []
        membersList = []
        target = datetime.datetime.today() - datetime.timedelta(days=7*float(arg1))
        members = set(self.bot.get_all_members())
        
        # let user know you got message, and begin loading
        tempmsg = await self.bot.say(memb.mention+', give me a moment....')
        insert = str(mcount)+'/'+str(len(members)-6)
        msg = await self.bot.send_message(ctx.message.channel,'Checking member `<'+insert+'>`')

        # MEMBER LOOP: Find all members messages after given
        #              target date in each channel.
        break_flag    = False
        user_inactive = True
        for m in members:
            num_msgs = 0
            if not f.Is_Bot(m) and m != self.eaaat:
                mcount += 1
                insert = '`<'+str(mcount)+'/'+str(len(members)-6)+'>`'
                await self.bot.edit_message(msg,'Checking member '+insert+'... ...')
                break_flag = False
                user_inactive = True
                for k in ACTIVECHANNELS:
                    chnl = self.bot.get_channel(ACTIVECHANNELS[k])
                    async for message in self.bot.logs_from(chnl, after=target, limit=3000):
                        if message.author == m:
                            num_msgs += 1
                            if num_msgs > 1:
                                break_flag = True
                                user_inactive = False
                                break
                    if break_flag:
                        break
                if user_inactive:
                    membersList.append(m.name)

        # PREPARE RESULTS
        i = 0
        count = 0
        membersList.sort(key=str.lower)
        if len(membersList) > 0:
            desc.append('')
            for m in membersList:
                count += 1
                desc[i] += '**×** '+m+'\n'
                if count == 15:
                    desc.append('')
                    i += 1
                    count == 0

        #PAGINATION VARIABLES
        pgs = str(i + 1)
        r = [self.stop]
        i = 0
        
        # Prepare first page of activity report
        await self.bot.delete_message(tempmsg)
        await self.bot.delete_message(msg)
        await self.bot.say(memb.mention+', Activity is now ready to view below.')
        embed = discord.Embed(title='', description=desc[0], color=1234123)
        embed.set_author(name='Ex Aspera Ad Astra Activity Report', icon_url= CLANICONWHT)
        embed.set_thumbnail(url = CLANICONWHT)
        txt = 'Activity Report | Option: '+arg1+' '+arg2+' | page 1'+'/'+pgs
        embed.set_footer(text=txt,icon_url=CLANICONWHT)
        msg = await self.bot.send_message(ctx.message.channel, embed=embed)

        # Add reactions
        await self.bot.add_reaction(msg,self.stop)
        if len(desc) > 1:
            r.append(self.next)
            await self.bot.add_reaction(msg,self.next)
                
        # get response
        res = await self.bot.wait_for_reaction(message=msg, timeout=60)

        # BEGIN PAGINATION: This while loop will handle viewing
        #                   of the roster show command until the end
        try:
            while res.reaction.emoji != self.stop or res.user != memb:
                
                # NEXT page~~
                if res.reaction.emoji == self.next and res.user == memb and f.available(self.next, r):
                    i += 1
                    r = []
                    txt = 'Activity Report | Option: '+arg1+' '+arg2+' | page '+str(i+1)+'/'+pgs
                    embed = discord.Embed(title='', description=desc[i], color=1234123)
                    embed.set_author(name='Ex Aspera Ad Astra Activity Report', icon_url= CLANICONWHT)
                    embed.set_thumbnail(url = CLANICONWHT)
                    embed.set_footer(text=txt,icon_url=CLANICONWHT)
                    msg = await self.bot.edit_message(msg, embed=embed)
                    await self.bot.clear_reactions(msg)
                    
                    # Add reactions
                    await self.bot.add_reaction(msg,self.prev)
                    await self.bot.add_reaction(msg,self.stop)
                    if len(desc) > i + 1:
                        r.append(self.next)
                        await self.bot.add_reaction(msg,self.next)
                    r.append(self.prev)
                    
                # PREV page~~
                elif res.reaction.emoji == self.prev and res.user == memb and f.available(self.prev, r):
                    i -= 1
                    r = []
                    txt = 'Activity Report | Option: '+arg1+' '+arg2+' | page '+str(i+1)+'/'+pgs
                    embed = discord.Embed(title='', description=desc[i], color=1234123)
                    embed.set_author(name='Ex Aspera Ad Astra Activity Report', icon_url= CLANICONWHT)
                    embed.set_thumbnail(url = CLANICONWHT)
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
            
                elif i == len(desc) - 1:
                    res = await self.bot.wait_for_reaction(message=msg, timeout=60)
                    
                else:
                    res = await self.bot.wait_for_reaction(message=msg, timeout=60)
            
                # Timeout
                if res is None:
                    break
        except:
            do_nothing = ''

        # End session on first page
        await self.bot.clear_reactions(msg)
        embed = discord.Embed(title='', description=desc[0], color=1234123)
        embed.set_author(name='Ex Aspera Ad Astra Activity Report', icon_url= CLANICONWHT)
        embed.set_thumbnail(url = CLANICONWHT)
        txt = text='Activity Report | Option: '+arg1+' '+arg2+' | Session Ended'
        embed.set_footer(text=txt,icon_url=CLANICONWHT)
        msg = await self.bot.edit_message(msg, embed=embed)
        return


                    
    # Delete user messages from #upcoming-events channel for now.
    # Only leave messages left by spirit that are embeds.
    # Notify admin if user inputs command other than !event command
    async def on_message(self, message):

        if not onoff.check('u-events-mngr',CLNSERVERS['Ex Aspera Ad Astra']):
            return
        
        # UPCOMING-EVENTS MESSAGES
        if message.channel.name == 'upcoming-events':
            if message.author.name != 'Spirit':
                await asyncio.sleep(2.0)
                await self.bot.delete_message(message)
                if message.content != '!event':
                    msg = ':warning: \n' + f.Role_Obj(message.server.roles, 'Admin').mention + ', '
                    msg += message.author.name + ' has entered an illegal message in '
                    msg += self.bot.get_channel(CHANNELS['UPCOMINGEVENTSCHNL']).mention
                    await self.bot.send_message(self.bot.get_channel(CHANNELS['ADMINCHATCHNL']), msg)
            else:
                if message.content != '':
                   await self.bot.delete_message(message)
            
            await self.bot.process_commands(message)
                
        # PRIVATE CHANNEL MESSAGES
        if message.channel.is_private:
            memb = f.Member_Obj(self.bot.get_all_members(), message.author.name)
            try:
                args = message.content.split()
                if args[0].lower() == 'i' and args[1].lower() == 'accept':
                    code = f.Get_Ascended_Code(message.author)
                    if str(code) == str(args[2]):
                        # variables
                        gchat = self.bot.get_channel(CHANNELS['GAMECHATCHNL'])
                        achat = self.bot.get_channel(CHANNELS['ASCENDEDCHATCHNL'])
                        ascendedRole = f.Role_Obj(gchat.server.roles, 'Ascended')
                        
                        # check that member doesnt already have role
                        if f.Member_Is_Role(memb, ascendedRole.name):
                            err = 'You have already Ascended '+memb.name+'?'
                            await self.bot.send_message(memb, err)
                            self.bot.process_commands(message)
                            return
                        
                        # make changes
                        await self.bot.add_roles(memb, ascendedRole)
                        msg = '**Thank you, The changes have been made.**'
                        await self.bot.send_message(memb, msg)
                        
                        # confirm to user, and announce
                        gmsg = message.author.mention + ' **has** '+ascendedRole.mention+'!'
                        amsg = message.author.mention + ' **welcome to the **'+ascendedRole.mention+'!'
                        await self.bot.send_message(gchat, gmsg)
                        await self.bot.send_message(achat, amsg)
                    else:
                        err = ':x: That code is invalid. Try again.'
                        await self.bot.send_message(memb, err)

            except:
                err = 'Sorry2? I didnt understand that. speak with Admin if theres an issue.'
                await self.bot.send_message(memb, err)
            await self.bot.process_commands(message)


        i = 0
        msgList = message.content.split(' ')
        while i < len(msgList):
            if msgList[i].lower() == 'get':
                if (i+1) < len(msgList) and msgList[i+1].lower() == 'it':
                    if (i+2) < len(msgList):
                        s = re.sub('[^a-zA-Z]+', '', msgList[i+2])
                        if s.lower() == 'done':
                            dstr = '*Your minds must be one!*'
                            await self.bot.send_file(message.channel, 'img/bop_church.gif',content= dstr)
                            await self.bot.process_commands(message)
                            break
            i += 1
                





def setup(bot):
    bot.add_cog(AdministrationCog(bot))











