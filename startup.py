import discord
from discord.ext import commands
import sys, traceback, platform
sys.path.append('./utils')
import onoff
from constants import CHANNELS, CLNSERVERS
from functions import Role_Obj, Get_EAAA_Role

# COGS
initial_extensions = ['cogs.standard',
                      'cogs.announcements',
                      'cogs.roster',
                      'cogs.registration',
                      'cogs.administration',
                      'cogs.guidedroles',
                      'cogs.champions',
                      'cogs.help',
                      'cogs.poll']


# determine which bot to load up
botType = ''
# error checking
if len(sys.argv) > 2:
    print('**ERROR: Too many arguments. program takes at most one.\nexiting... ... ...')
    sys.exit()
# hadnle argument
if len(sys.argv) > 1:
    botType = sys.argv[1]
else:
    botType = 'EAAA'

# Load configs
configFile = open('config')
configs = configFile.readlines()
config = {
    'EAAA': {
        'token': (configs[1].split()[1]).split('\n')[0],
        'prefix': (configs[2].split()[1]).split('\n')[0],
    }, 
    'EAAA_tester': {
        'token': (configs[5].split()[1]).split('\n')[0],
        'prefix': (configs[6].split()[1]).split('\n')[0],
    }
}


bot = commands.Bot(command_prefix = config[botType]['prefix'])
bot.remove_command('help')

@bot.event
async def on_ready():
    print('\n\n\nLogged in as '+bot.user.name+' (ID:'+bot.user.id+') | Connected to '+\
          str(len(bot.servers))+' servers | Connected to '+str(len(set(bot.get_all_members())))+' users')
    print('-------'*18)
    print('Discord.py Version: {} | Python Version: {}'.format(discord.__version__, platform.python_version()))
    print('-------'*18)
    print('Use this link to invite {}:'.format(bot.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
    print('-------'*18)
    print('Support Discord Server: https://discord.gg/FNNNgqb')
    print('-------'*18)

    if __name__ == '__main__':
        for extension in initial_extensions:
            try:
                bot.load_extension(extension)
                print('{} loaded'.format(extension))
            except Exception as e:
                print('issue with',extension)
                traceback.print_exc()
        print('Successfully logged in and booted...! Use prefix: "'+config[botType]['prefix']+'".\n\n')



#Welcome message to all incoming users.
@bot.event
async def on_member_join(member):

    if str(member.server.id) == CLNSERVERS['Ex Aspera Ad Astra: Other Games']:
    
        if not onoff.check('arrival',CLNSERVERS['Ex Aspera Ad Astra: Other Games']):
            return
        
        eaaa_role = Get_EAAA_Role(member)
        if eaaa_role == 'error':
            err = member.mention + ', Something went wrong with retrieving your role'
            await bot.send_message(bot.get_channel('407211886984298506'), err)
        else:
            await bot.replace_roles(member, Role_Obj(member.server.roles, eaaa_role))
            msg = member.mention + ', **you have been given your role as it stands '
            msg += 'on the main Ex Aspera Ad Astra Discord Server.\n\n WELCOME!!**'
            await bot.send_message(bot.get_channel('407211886984298506'), msg)
        return

    if not onoff.check('arrival',CLNSERVERS['Ex Aspera Ad Astra']):
        return
    
    
    await bot.replace_roles(member, Role_Obj(member.server.roles, 'unregistered'))
    rmsg = "**Welcome "+member.mention+" to the Ex Aspera Ad Astra Clan Discord!**\n"
    rmsg += "I am EAAA, and I am the main **bot** deployed to the "
    rmsg += "clan server. If you don't know what a 'bot' is, don't worry, "
    rmsg += "we will get there...\n\n"
    
    rmsg += "As a new member, your currently listed as **unregistered** on "
    rmsg += "this server, so we need to take care of that immediately, "
    rmsg += "as right now your access to the server is **GREATLY** reduced "
    rmsg += "and restricted.\n\n"
    
    rmsg1 = "To begin, type the following command in the message prompt, "
    rmsg1 += "then press enter: ```.registration begin```"
    rmsg1 += "im waiting... ... ... ...**\n.\n**Ex Aspera Ad Astra Admins**\n."
    
    msg = member.mention+ ", Welcome to the **Ex Aspera Ad Astra Clan**!\n\n"
    msg += "**There is an important message waiting for you in the "
    msg += bot.get_channel(CHANNELS['REGISTERCHNL']).mention+" channel**!\n\nIf you are new to discord, "
    msg += "**channels** are *\"chat rooms\"*. Simply tap/click the blue text or tap/click"
    msg += " on the Ex Aspera Ad Astra server icon in the left pane of"
    msg += " your screen, scroll to the top of the menu that pops up, and tap/click"
    msg += " on "+bot.get_channel(CHANNELS['REGISTERCHNL']).mention+" to navigate there."
    
    await bot.send_message(bot.get_channel(CHANNELS['GAMECHATCHNL']), msg)
    await bot.send_message(bot.get_channel(CHANNELS['REGISTERCHNL']),rmsg)
    await bot.send_message(bot.get_channel(CHANNELS['REGISTERCHNL']),rmsg1)


#departure message when someone leaves the clan.
@bot.event
async def on_member_remove(member):
    
    if str(member.server.id) != CLNSERVERS['Ex Aspera Ad Astra: Other Games']:
        if not onoff.check('goodbye',CLNSERVERS['Ex Aspera Ad Astra']):
            return
        
        ascendedmsg = (Role_Obj(member.server.roles, 'Ascended')).mention + " :warning: \n**"+member.name
        ascendedmsg += "** has left the clan."
        adminmsg = (Role_Obj(member.server.roles, 'Admin')).mention + " :warning: \n"+member.name
        adminmsg += " has left the clan.\nYou can remove this member from the roster "
        adminmsg += "with the command:\n** .roster remove "+member.name+"**."
        await bot.send_message(bot.get_channel(CHANNELS['ASCENDEDCHATCHNL']), ascendedmsg)
        await bot.send_message(bot.get_channel(CHANNELS['ADMINCHATCHNL']), adminmsg)



# Start your engines~~
bot.run(config[botType]['token'], bot=True, reconnect=True)






