#was at line 126
import discord
from discord.ext import commands
import sys, asyncio
import perms, onoff
from constants import TIMEZONES, CLANICONWHT, CLANLOGOBLK, DESTICON, CHANNELS, CLNSERVERS
import functions as f

sys.path.append('../utils')



'''
COMMANDS LIST:
- roster file
- roster add
- roster show
- roster update
- roster remove
- roster user
'''
class RosterCog:
    
    def __init__(self, bot):
        self.bot = bot
        self.lvl = 5 # some comands sensitive here
        self.next = '\N{BLACK RIGHTWARDS ARROW}'
        self.stop = '\N{WHITE SQUARE BUTTON}'
        self.prev = '\N{LEFTWARDS BLACK ARROW}'
        self.eaaa  = f.Member_Obj(self.bot.get_all_members(), 'EAAA')
        self.eaaat = f.Member_Obj(self.bot.get_all_members(), 'EAAA-tester')





    # All roster commands - see below
    @commands.command(pass_context=True)
    async def roster(self, ctx, *args):
        
        if not onoff.check('roster',CLNSERVERS['Ex Aspera Ad Astra']):
            return
        
        success = True
        badArg = user = desc = ''
        
        
        
        # all commands require arguments of some sort
        if len(args) == 0:
            await self.bot.say(':x: '+ ctx.message.author.mention+\
                              ' Command requires argument(s).')
            return



        # FILE ~~~~~~~
        # Send roster file to admin channel,
        # assumin permission criteria is met.
        elif args[0] == 'file':
            s = ctx.message.author.mention + 'here is the file you requested'
            if  perms.check(ctx.message.author, self.lvl):
                    await self.bot.send_file(self.bot.get_channel(CHANNELS['ADMINCHATCHNL']),
                                             'utils/roster.csv',content= s)
            else:
                await self.bot.say(':x: '+ ctx.message.author.mention+\
                        ' You do not have permission to execute this command!')



        # ADD ~~~~~~~
        # add member and/or addition info about member.
        # see Add_To_Roster in functions.py
        elif args[0] == 'add':
            if len(args) > 1 and args[1].lower() == 'gt':
                if len(args) > 2:
                    success = f.Add_Gamertag(ctx.message.author, args)
                    if not success:
                        await self.bot.say(':x: '+ ctx.message.author.mention+\
                             ' You have not added yourself to the roster yet.')
                        return
                else:
                    await self.bot.say(':x: '+ ctx.message.author.mention+\
                              ' Must include your Gamertag as final argument.')
                    return
        
        
            elif len(args) > 1 and args[1].lower() == 'note':
                if len(args) > 2:
                    success, issue = f.Add_Note(ctx.message.author, args)
                    if not success and issue == 'length':
                        await self.bot.say(':x: '+ ctx.message.author.mention+\
                          ' Note is too long. Must be less than 20 characters.')
                        return
            
                    success, issue = f.Add_Note(ctx.message.author, args)
                    if not success and issue == 'not found':
                        await self.bot.say(':x: '+ ctx.message.author.mention+\
                        ' You have not added yourself to the roster yet.')
                        return
                else:
                    await self.bot.say(':x: '+ ctx.message.author.mention+\
                                       ' Must include note as final argument.')
                    return
        
        
        
        
            else:
                success, badArg = f.Add_To_Roster(ctx.message.author, args)
        
        
        
        # SHOW ~~~~~~~
        # show clan roster, post results as paginated embed.
        # Can take query args. See Show_Roster in functions.py
        elif args[0] == 'show':
            memb = ctx.message.author
            r = [self.stop]
            i = 0

            # Gen roster shows only work for gamertag and tpref
            if len(args) == 2 and not\
                (args[1] == 'gamertag' or args[1] == 'tpref' or args[1] == 'birthday' or args[1] == 'status'):
                await self.bot.say(':x: '+ memb.mention+' Invalid Roster Query <'+args[1]+'>.')
                return

            # Get list + info for embed
            desc, pgs, num, type = f.Show_Roster(memb, args)

            # If function returns info, make an embed!
            if desc[0] != '':
                embed = discord.Embed(title='', description=desc[0], color=1234123)
                embed.set_author(name='Ex Aspera Ad Astra Roster: '+type, icon_url= CLANICONWHT)
                embed.set_footer(text='Total Members: '+num+' | page '+ '1'+'/'+pgs,icon_url=CLANICONWHT)
                msg = await self.bot.send_message(ctx.message.channel, embed=embed)
                
                # Add reactions
                await self.bot.add_reaction(msg,self.stop)
                if len(desc) > 1:
                    r.append(self.next)
                    await self.bot.add_reaction(msg,self.next)
                
                # get response
                res = await self.bot.wait_for_reaction(message=msg, timeout=60)
  

                # Begin pagination.
                # This while loop will handle viewing
                # of the roster show command until the end
                try:
                    while res.reaction.emoji != self.stop or res.user != memb:
                        
                        # NEXT page~~
                        if res.reaction.emoji == self.next and res.user == memb and f.available(self.next, r):
                            i += 1
                            r = []
                            txt = 'Total Members: '+num+' | page '+ str(i+1)+'/'+pgs
                            embed = discord.Embed(title='', description=desc[i], color=1234123)
                            embed.set_author(name='Ex Aspera Ad Astra Roster: '+type, icon_url= CLANICONWHT)
                            embed.set_footer(text=txt, icon_url=CLANICONWHT)
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
                            txt = 'Total Members: '+num+' | page '+ str(i+1)+'/'+pgs
                            embed = discord.Embed(title='', description=desc[i], color=1234123)
                            embed.set_author(name='Ex Aspera Ad Astra Roster: '+type, icon_url= CLANICONWHT)
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
                            desc[0] = '**:warning: SESSION TIMED OUT:warning: **\n'
                            desc[0] += 'Please try again, use "'+self.stop+'" when finished.'
                            break
                except:
                    desc[0] = '**:warning: SESSION TIMED OUT:warning: **\n'
                    desc[0] += 'Please try again, use "'+self.stop+'" when finished.'

                # wrap up pagination, clear all reactions to indicate end.
                # add end to footer and new desc/or first page
                await self.bot.clear_reactions(msg)
                embed = discord.Embed(title='', description=desc[0], color=1234123)
                embed.set_author(name='Ex Aspera Ad Astra Roster: '+type, icon_url= CLANICONWHT)
                embed.set_footer(text='Total Members: '+num+' | Session End',icon_url=CLANICONWHT)
                msg = await self.bot.edit_message(msg, embed=embed)
                return
            
            # handle invalid commands
            else:
                err = ' command contained invalid argument <'+type+'>. Please try again.'
                await self.bot.say(':x: '+ memb.mention+err)
                return



        # UPDATE ~~~~~~~
        # updates member status/role in roster. Works with
        # mention or string obj. See Update_Member in functions.py
        elif args[0] == 'update':
            if len(args) > 1:
                # permission level 3 "Admin" minimum requirement
                if  perms.check(ctx.message.author, self.lvl):
                    
                    if len(ctx.message.mentions) > 0:
                        success, badArg = f.Update_Member(ctx.message.mentions[0], args[1])
                    
                    elif args[1].lower() == 'all':
                        s = ctx.message.author.mention + 'heres a backup incase something goes wrong!'
                        await self.bot.send_file(self.bot.get_channel(CHANNELS['ADMINCHATCHNL']),
                                                 'utils/roster.csv',content= s)
                        success, badArg = f.Update_All(self.bot.get_all_members(), args[1])
                        if not success:
                            err = ':x: command was at least partially '
                            err += 'unsuccessful. **See list below:**\n'
                            for i in badArg:
                                err += i+', '
                            await self.bot.say(err)
                            return
                        
                    else:
                        memb = f.Member_Obj(self.bot.get_all_members(), f.Build_User(args[1::]))
                        success, badArg = f.Update_Member(memb,args[1])
                    
                    if not success:
                        await self.bot.say(':x: '+ ctx.message.author.mention+\
                        ' Cannot find user in roster.')
                        return
                else:
                    await self.bot.say(':x: '+ ctx.message.author.mention+\
                            ' You do not have permission to execute this command!')
                    return
            else:
                await self.bot.say(':x: '+ ctx.message.author.mention+\
                                   ' Command requires username or user object argument.')
                return



        # REMOVE ~~~~~~~
        # removes member from clan roster, requires username
        # string. See Remove_From_Roster in functions.py
        elif args[0] == 'remove':
            if len(args) > 1:
                # permission level 3 "Admin" minimum requirement
                if  perms.check(ctx.message.author, self.lvl):
                    if len(ctx.message.mentions) > 0:
                        success, badArg = f.Remove_From_Roster(ctx.message.mentions[0].name)
                    else:
                        if len(args) > 2:
                            success, badArg = f.Remove_From_Roster(f.Build_User(args[1::]))
                        else:
                            success, badArg = f.Remove_From_Roster(args[1])
                else:
                    await self.bot.say(':x: '+ ctx.message.author.mention+\
                            ' You do not have permission to execute this command!')
                    return
            else:
                await self.bot.say(':x: '+ ctx.message.author.mention+\
                          ' Command requires username or user object argument.')
                return



        # MEMBER LOOKUP ~~~~~~~
        # Get information about a specific user
        elif len(ctx.message.mentions) != 0\
                 or f.Member_Obj(self.bot.get_all_members(), args[0]) != None:
                     
            if len(args) != 1 or len(ctx.message.mentions) > 1:
                err = ctx.message.author.mention+', to look up a members information '
                err += ' you must input a single user mention as the argument.'
                await self.bot.say(err)
                return
            
            if len(ctx.message.mentions) > 0:
                user,desc = f.Roster_User_info(ctx.message.mentions[0])
            else:
                user,desc = f.Roster_User_info(f.Member_Obj(self.bot.get_all_members(),args[0]))

            if desc != '':
                embed = discord.Embed(title='', description=desc, color=0xD6D6D6)
                embed.set_author(name=user, icon_url= DESTICON)
                embed.set_image(url=CLANLOGOBLK)
                embed.set_footer(text='Ex Aspera Ad Astra',icon_url=CLANICONWHT)
                await self.bot.send_message(ctx.message.channel, embed=embed)
                return
            else:
                await self.bot.say(':x: '+ ctx.message.author.mention+\
                        'The user '+user.mention+\
                        ' is on the server but has not registered with me yet.')
                return

        # Get information about a specific user, with spaces in username
        elif len(args) > 1 and f.Member_Obj(self.bot.get_all_members(), f.Build_User(args)) != None:
            user,desc = f.Roster_User_info(f.Member_Obj(self.bot.get_all_members(),f.Build_User(args)))
            embed = discord.Embed(title='', description=desc, color=0xD6D6D6)
            embed.set_author(name=user, icon_url= DESTICON)
            embed.set_image(url=CLANLOGOBLK)
            embed.set_footer(text='Ex Aspera Ad Astra',icon_url=CLANICONWHT)
            await self.bot.send_message(ctx.message.channel, embed=embed)
            return




        # Unrecognized roster parameter
        else:
            await self.bot.say(':x: '+ ctx.message.author.mention+\
                               ' command contained invalid argument <'+\
                               args[0]+'>. Please try again.')
            return
        
        # If changes are successful or not
        if success:
            await self.bot.say(':white_check_mark: Successfully initiated '+\
                               ctx.message.author.mention)
        else:
            await self.bot.say(':x: '+ ctx.message.author.mention+\
                               ' command contained invalid argument <'+\
                               badArg+'>. Please try again.')




    # admin override to add emmber to roster.
    @commands.command(pass_context=True)
    async def rosteradmin(self, ctx, *args):
        
        if args[0].lower() == 'count':
            if  perms.check(ctx.message.author, self.lvl):
                await self.bot.say(ctx.message.author.mention+' '+f.Roster_Count())
                return
    
        if args[0].lower() == 'noserver':
            if  perms.check(ctx.message.author, self.lvl):
                if len(args) == 2:
                    msg = f.Admin_Add_To_Roster(args[1])
                    if msg == '':
                        await self.bot.say(':white_check_mark: Successfully initiated '+\
                                           ctx.message.author.mention)
                    else:
                        await self.bot.say(':x: '+ ctx.message.author.mention+msg)
                else:
                    await self.bot.say(':x: '+ ctx.message.author.mention+\
                                        ' command contained too many arguments'+\
                                        ' or too little arguments.')
            return
    
        if args[0] == 'add':
            if  perms.check(ctx.message.author, self.lvl):
                try:
                    user = ctx.message.mentions[0]
                except:
                    await self.bot.say(':x: must mention user to add')
                    return
                if len(args) > 2 and args[1].lower() == 'gt':

                    if len(args) > 3:
                        success = f.Add_Gamertag(user, args[3::], admin=True)
                        if not success:
                            await self.bot.say(':x: '+ ctx.message.author.mention+\
                                            ' You have not added yourself to the roster yet.')
                            return
                    else:
                        await self.bot.say(':x: '+ ctx.message.author.mention+\
                                           ' Must include your Gamertag as final argument.')
                        return
                else:
                    success, badArg = f.Add_To_Roster(user, args[1::], admin=True)

                # If changes are successful or not
                if success:
                    await self.bot.say(':white_check_mark: Successfully initiated '+\
                                        ctx.message.author.mention)
                else:
                    await self.bot.say(':x: '+ ctx.message.author.mention+\
                                  ' command contained invalid argument <'+\
                                    badArg+'>. Please try again.')

# END ROSTER CLASS



# The setup fucntion below is neccesarry. Remember we give
# bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(RosterCog(bot))











