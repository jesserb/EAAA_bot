import discord
from discord.ext import commands
import sys, asyncio, onoff
sys.path.append('../utils')
from constants import GUIDED_ROLES, GROLES, DESTICON, CHANNELS, CLANICONWHT, CLNSERVERS
import functions as f




'''
COMMANDS LIST:
- guidedroles add
- guidedroles role
'''
class GuidedrolesCog:
    
    def __init__(self, bot):
        self.bot = bot


    # SOLSTICE OF HEROES: TEMP ROLES FOR CURRENT EVENT
    # @commands.command(pass_context=True)
    # async def solsticeofheroes(self, ctx, *args):

    #     chnl = self.bot.get_channel('474920435839139855')
    #     roles = ctx.message.server.roles

    #     # check if more than 1 arg given
    #     if len(args) > 2:
    #         await self.bot.say('{} command takes but at most 2 arguments, either **"shattered"**, **"rekindled"**, or **"resplendent"**, or **"remove"** plus a valid role'
    #                            .format(ctx.message.author.mention))
    #         return

    #     # check if 0 args are given
    #     if len(args) < 1:
    #         await self.bot.say('{} must include an argument, either **"remove"** then a valid role, or **"shattered"**, **"rekindled"**, or **"resplendent"**'
    #                            .format(ctx.message.author.mention))
    #         return

    #     # Check that guided role is valid
    #     if args[0].lower() != 'remove' and f.Role_Obj(roles, (args[0].lower()).title()) == None:
    #         await self.bot.say(':x: {} <{}> is not a valid argument for this command. argument must be **"shattered"**, **"rekindled"**, or **"resplendent"**'
    #                            .format(ctx.message.author.mention,args[0].lower().title()) )
    #         return

    #     # check if shattered, then add
    #     if args[0].lower() == 'shattered':
    #             role = f.Role_Obj(roles, 'Shattered')
    #             await self.bot.add_roles(ctx.message.author, role)
    #             msg = '\n**{} has taken on the role of {}!**'.format(ctx.message.author.mention, role)
    #             # await self.bot.send_message(chnl, msg)
    #             await self.bot.say(msg)
    #             return

    #     # check if rekindled or resplendent, then add
    #     if args[0].lower() == 'rekindled' or args[0].lower() == 'resplendent':
    #             role = f.Role_Obj(roles, (args[0].lower()).title())
    #             await self.bot.add_roles(ctx.message.author, role)
    #             msg = '\n**{} has upgraded their armor to {},\nand as such, taken on the role of {}!**'.format(ctx.message.author.mention, role.name, role)
    #             # await self.bot.send_message(chnl, msg)
    #             await self.bot.say(msg)
    #             return

    #     # handle role removal option
    #     role = f.Role_Obj(roles, args[1].title())
    #     if args[0].lower() == 'remove' and len(args) == 2:

    #             if args[1].lower() == 'shattered':
    #                 if f.Member_Is_Role(ctx.message.author, 'Rekindled'):
    #                     await self.bot.remove_roles(ctx.message.author, role)
    #                     await self.bot.say('\n{}, you have successfully removed the role of {}.'.format(ctx.message.author.mention, role.name))
    #                 else:
    #                     await self.bot.say('\n{}, you cannot remove all Solstice of Heroes roles.'.format(ctx.message.author.mention))

    #             elif args[1].lower() == 'rekindled':
    #                 if f.Member_Is_Role(ctx.message.author, 'Shattered'):
    #                     await self.bot.remove_roles(ctx.message.author, role)
    #                     await self.bot.say('\n{}, you have successfully removed the role of {}.'.format(ctx.message.author.mention, role.name))
    #                 else:
    #                     await self.bot.say('\n{}, you cannot remove all Solstice of Heroes roles.'.format(ctx.message.author.mention))
    #             else:
    #                 await self.bot.say('\n{}, <{}> is not a valid role. You can remove only **"Shattered** or **"rekindled"**.'.format(ctx.message.author.mention, args[1]))
    #             return
    #     else:
    #         await self.bot.say('{} must include a second argument of either **"rekindled"** or **"resplendent"**.'.format(ctx.message.author.mention))



    # GUIDED ROLES COMMANDS~~~
    @commands.command(pass_context=True)
    async def guidedroles(self, ctx, arg1='', arg2='', arg3=''):
        
        if not onoff.check('guidedroles',CLNSERVERS['Ex Aspera Ad Astra']):
            return

        # make some variables for large class calls
        gchat = self.bot.get_channel(CHANNELS['GAMECHATCHNL'])
        ichat = self.bot.get_channel(CHANNELS['INFORMATIONCHNL'])
        roles = ctx.message.server.roles
        
        # arg1 cannot be empty
        if arg1 == '':
            await self.bot.say('Must include a valid Guided Role')
            return
        
        
        # ADD GUIDED ROLE~~~~~
        if arg1.lower() == 'add':

            gr = '' # <--- placeholder for guided role
            # Command must be ran in GAME-CHAT
            if ctx.message.channel.name != 'game-chat':
                await self.bot.delete_message(ctx.message)
                await self.bot.say(ctx.message.author.mention +\
                            ', That command must be ran in '+gchat.mention)
                return
            
            # arg2 cannot be empty
            if arg2 == '':
                await self.bot.delete_message(ctx.message)
                await self.bot.say('Must include a valid Guided Role to add!')
                return
            
            # assign guided role string
            if arg2[1] == '@':
                try:
                    gr = f.Role_Obj(roles,arg2).name
                except: # mention was not a role
                    await self.bot.delete_message(ctx.message)
                    await self.bot.say(':x: ' + ctx.message.author.mention +\
                         ', That was not a valid Guided Role')
                    return
            else:
                gr = arg2
                # role = arg2 + arg3
                if arg3 != '':
                    gr = arg2 + ' ' + arg3
                
            # Check that guided role is valid
            if f.Role_Obj(roles, gr) == None:
                await self.bot.delete_message(ctx.message)
                await self.bot.say(':x: ' + ctx.message.author.mention + ' <' +\
                                   gr + '> is not a valid Guided Role.' )
                return
            
            # send user a private message
            gchatmsg1 = ctx.message
            msg = f.Add_Guided_Role(ctx.message.author, ichat, gr)
            await self.bot.send_message(ctx.message.author, msg)
            gchatmsg2 = await self.bot.say(ctx.message.author.mention+', I sent you a private message.')
            
            # wait for user to type cancel or acknowledged
            while True:
                
                ans = await self.bot.wait_for_message(timeout=300, author=ctx.message.author)
                await self.bot.delete_message(gchatmsg2)
                if ans.content.lower() == 'cancel':
                    await self.bot.delete_message(gchatmsg1)
                    await self.bot.send_message(ctx.message.author, 'Application cancelled.')
                    return
                
                if ans.content.lower() == 'acknowledged':
                    await self.bot.add_roles(ctx.message.author, f.Role_Obj(roles, gr))
                    msg = f.Guided_Roles_Msg(ctx.message.author, roles, gr)
                    await self.bot.send_message(gchat, msg)
                    break

                else:
                    err = ':x: Your response was not recognized.\nYou must type the word '
                    err += '**acknowledged** to accept the role, and **cancel** to cancel '
                    err += 'the promotion.\n**Please try again**, and check your spelling!:'
                    await self.bot.send_message(ctx.message.author, err)

        # LOOK UP MEMBERS WITH GROLE~~~~~
        else:
            # for mentions
            if arg1[1] == '@':
                try:
                    arg1 = f.Role_Obj(roles,arg1).name
                except: # mention was not a guided role
                        await self.bot.say('Invalid Guided Role <@'+\
                        str(ctx.message.author.id)+'>')
                        return

            # for roles with spaces
            if arg2 != '':
                arg1 = arg1+' '+arg2

            valid = False
            members = set(self.bot.get_all_members())
            for g in GUIDED_ROLES:
                
                if arg1 == g:
                    valid = True
                    list, grole = f.Get_Role_Members(members, arg1)
                    memlist = '\n───────\n'
                    for l in list:
                        memlist += '× '+l+'\n'

                    embed = discord.Embed(title="**Guides**", description=memlist, color=0x000000)
                    embed.set_thumbnail(url = CLANICONWHT)
                    embed.set_image(url=GROLES[arg1])
                    await self.bot.send_message(ctx.message.channel, embed=embed)

            # handle invalid guided role
            if not valid:
                await self.bot.say( ':x: Invalid Guided Role ' + ctx.message.author.mention)






# The setup fucntion below is neccesarry. Remember we give
# bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(GuidedrolesCog(bot))














