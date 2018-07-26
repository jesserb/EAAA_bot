#WAS AT LINE 756


from constants import *
import pandas as pd
import sys, re, datetime, pendulum
import perms
from random import randint

'''
MEMBER FUNCTIONS~~~~~~
available:
    TAKES: obj(emoji), list(obj(reaction emojis))
    Returns: True or False
    
Valid_Date:
    TAKES:   str(date)
    RETURNS: bool

Date_Transform:
    TAKES: str(date with no year e.g. mm/dd)
    RETURNS: True or False
    
get:
    TAKES: str(member)
    RETURNS: char-only-string(member)

Get_Role_Members:
    TAKES:   obj(list(members)), str(role)
    RETURNS: str(list(members w/ role)), str(grole)
   
Get_Member_Role:
    TAKES:   obj(member)
    RETURNS: str(status/role)
   
Get_Member_Obj:
    TAKES:   str(member)
    RETURNS: obj(member)

Get_Guided_Roles:
    TAKES:   obj(members)
    RETURNS: obj(list(guided roles)), obj(list(guided roles))
'''

# Given a timezone t, looks up UTC equivalent
# and returns UTC and offset value
def split_zone(t):
    if len(t.split('+')) > 1:
        return t.split('+')[0], float(t.split('+')[1])
    
    if len(t.split('-')) > 1:
        return t.split('-')[0], float(t.split('-')[1]) * -1
    
    if t in UTCOFFSETS:
        return 'UTC',UTCOFFSETS[t]
    
    if t == 'ACT':
        month = int(datetime.datetime.now().strftime("%m"))
        if (month > 3 and month < 11):
            return 'UTC',9.5
        else:
            return 'UTC', 10.5
    return t,0



# Function returns the time right now
# in the given timezone using UTC and offset.
def User_Time(tzone):
    t, off = split_zone(tzone)
    utc0 = datetime.datetime.utcnow()
    delta = datetime.timedelta(hours=off)
    return '{:%I:%M %p}'.format(utc0 + delta)



# Function returns the difference in hours
# between 2 given timezones
def Tzone_Diff(home, away, on=None):
    if on is None:
        on = pendulum.today()
        home, offset1 = split_zone(home)
        away, offset2 = split_zone(away)
        if offset1 == 0:
            diff = (on.timezone_(home) - on.timezone_(away)).total_hours() + offset2
        elif offset2 == 0:
            diff = (on.timezone_(home) - on.timezone_(away)).total_hours() - offset1
        elif offset1 < offset2 and offset2 < 0:
            diff = abs(offset1) - abs(offset2)
        elif offset1 > 0 and offset2 < 0:
            diff = offset2 - offset1
        
        elif offset2 > 0 and offset1 < 0:
            diff = offset1 - offset2
        
        elif offset1 > offset2:
            diff = abs(offset1) - abs(offset2)
        
        elif offset2 == offset1:
            diff = 0
        
        if abs(diff) > 12.0:
            if diff < 0.0:
                diff += 24.0
            else:
                diff -= 24.0
    return diff



# Function formats the timezone time difference
# as an easy to read sentence for user
def Tzone_Diff_Format(t1, t2):
    val =Tzone_Diff(t1, t2, on=None)
    if val < 0:
        return (t2+' is '+str(abs(val))+' hour(s) behind '+t1)
    else:
        return (t2+' is '+str(abs(val))+' hour(s) ahead of '+t1)



# check function to decide if page emoji
# is valid based on page number
def available(emoj, reactAvail):
    for k in reactAvail:
        if k == emoj:
            return True
    return False




# takes in a yearless date in the format of
# mm/dd andChecks if user date input is a valid
# date. Valid dates are in format mm/dd.
def Valid_Date(date):
    isValidDate = True
    try :
        month,day = date.split('/')
        datetime.datetime(2018,int(month),int(day))
    except ValueError :
        isValidDate = False
    return isValidDate



# converts date string to mm/dd format
def Date_Transform(date):
    month,day = date.split('/')
    month = int(month)
    day = int(day)
    if day < 10:
        day = '0' + str(day)
    if month < 10:
        month = '0' + str(month)
    return str(month) +'/'+str(day)



# Function removes emojis and other crap
# from usernames before checking/editing roster
def get(m):
    return re.sub(r'([^\s\w]|_)+', '', m)



def Prepare_String(username):
    if len(username) > 16:
        return username[0:13] + '...'
    else:
        return username



# Creates username from list of strings due to
# spacing in arguments for said usernae
def Build_User(args):
    user = ''
    for i in range(len(args)):
        if i == len(args) - 1:
            user += args[i]
        else:
            user += args[i] + ' '
    return user



# Returns list of member names with given role
# members are objects, role is string
def Get_Role_Members(members, role):
    list = []
    grole = ''

    for m in members:
        roles = m.roles
        for r in roles:
            if r.name == role:
                grole = r
                list.append(get(m.name))
    return list, grole


# Returns true if given member object
# has given role string.
def Member_Is_Role(memb, role):
    roles = memb.roles
    for r in roles:
        if r.name.lower() == role.lower():
            return True
    return False



# Given a member object, returns the main
# status/role of a member in string format
def Get_Member_Role(memb):
    roles = memb.roles
    rlist = {7: 'Founder',
             6: 'Owner',
             5: 'Admin',
             4: 'Ascended',
             3: 'member',
             2: 'beginner',
             1: 'unregistered'}
    
    rolenum = perms.Get_Role(memb)
    return rlist[rolenum]



# Given a member object, returns the true
# if member is a bot, false otherwise
def Is_Bot(memb):
    for r in memb.roles:
        if r.name == 'bot':
            return True
    return False



# Takes username string value and returns
# the member object. If member cannot be found,
# returns empty string.
def Member_Obj(members, memb):
    for m in members:
        if memb == m.name or memb == get(m.name):
            return m
    return None



# Given a member object, returns list of
# members guided roles, both str and obj
def Get_Guided_Roles(memb):
    list1 = [] #objects
    list2 = [] #strings
    roles = memb.roles


    for r in roles:
        for g in GUIDED_ROLES:
            if r.name == g:
                list1.append(r)
                list2.append(r.name)

    return list1, list2



# Given all server roles and a string role,
# returns role object
def Role_Obj(roles, role):
    
    #convert mention
    if role[0] == '<' and role[-1] == '>':
        role = role[3:-1]
        for r in roles:
            if str(r.id) == role:
                return r
    # convert string
    else:
        for r in roles:
            if (r.name).lower() == role.lower():
                return r
    return None



'''
GUARDIAN COMMAND FUNCTIONS~~~~~~
Guardian_Profile:
    TAKES:   str(profile), str(helmet), str(gauntlets), str(chest), str(legs),
             str(classItem), str(shaders), str(groles), str(author)
    RETURNS: str(description), str(message)
'''


# Returns description and message content
# for the gurdian command.
def Guardian_Profile(profile, helmet, gauntlets, chest,
                     legs, classItem, shaders, groles, author):

    shaders = shaders.split(',')
    gclass = profile.split(',')[0]
    species = profile.split(',')[1]
    power = profile.split(',')[2]
    roles = {
                'PvEers':'384818716233433089', 'PvPers':'384818397541826570',
                'Veteran':'384819452757409802', '335': '384819268568481793',
                'Leviathan':'382037554892898316','Flawless': '384818859984683019',
                'Lore Specialist':'384820104354856971','EoW': '409027837937451018',
                'Class Specialist':'384819627911544833',
                'Weapons Specialist': '384820009270116352'
            }

    message = '__**EX ASPERA AD ASTRA MEMBER PROFILE**__\n\n'
    message += "**GUIDED ROLES: ** "+author+" \n"

    temp = ''
    for i in range(len(groles)):
        if i == (len(groles) - 1):
            temp += '<@&'+roles[groles[i]]+'>\n\n'
        else:
            temp += '<@&'+roles[groles[i]]+'> | '

        if len(temp) > 30 and i != (len(groles)-1):
            message += temp + '\n'
            temp = ''
        if i == (len(groles)-1):
            message += temp
            
    strDesc = "**:beginner: "+gclass + " | "+species\
              +"\t\t\t:small_blue_diamond:"+power+"**\n───────────────\n"
    if len("× **Helmet:** "+helmet) > 37:
        strDesc += "× **Helmet:**\n\t\t"+helmet+"\n"
    else:
        strDesc += "× **Helmet:** "+helmet+"\n"

    if len("× **Gauntlets:** "+gauntlets) > 37:
        strDesc += "× **Gauntlets:**\n\t\t"+gauntlets+"\n"
    else:
        strDesc += "× **Gauntlets:** "+gauntlets+"\n"

    if len("× **Chest:** "+chest) > 37:
        strDesc += "× **Chest:**\n\t\t"+chest+"\n"
    else:
        strDesc += "× **Chest:** "+chest+"\n"

    if len("× **Legs:** "+legs) > 37:
        strDesc += "× **Legs:**\n\t\t"+legs+"\n"
    else:
        strDesc += "× **Legs:** "+legs+"\n"

    if len("× **Class Item:** "+classItem) > 37:
        strDesc += "× **Class Item:**\n\t\t"+classItem+"\n"
    else:
        strDesc += "× **Class Item:** "+classItem+"\n"

    strDesc += "× **Shaders:** "+shaders[0]+"\n"
    for i in range(1,len(shaders)):
        strDesc += "\t\t\t\t\t "+shaders[i]+"\n"

    strDesc += "───────────────\n"

    return strDesc, message




'''
CHANGE ROSTER FUNCTIONS~~~~~~
sortRoster
    TAKES: dataFrame
    RETURNS: sorted dataFrame
    
Check_Roster:
    TAKES:   str(member), str(list(usernames))
    RETURNS: True, False

Add Functions ~~
    Add_To_Roster:
        TAKES:   obj(member), str(list(arguments))
        RETURNS: True, 'success' or False, str(bad arg)
        
    Add_Gamertag:
        TAKES:   obj(memb), str(gamertag)
        RETURNS: None
        
    Add_Class:
        TAKES:   obj(memb), str(class)
        RETURNS: None
        
    Add_Timezone:
        TAKES:   obj(memb), str(timezone)
        RETURNS: None
        
    Add_Time+Pref:
        TAKES:   obj(memb), str(time preference)
        RETURNS: None
        
Remove_From_Roster:
    TAKES:   str(memb)
    RETURNS: True, 'success' or False, str(member)
    
Update_Member:
    TAKES:   obj(memb)
    RETURNS: True, 'success' or False, str(member)
'''



# Sorts a csv file by member status
def sortRoster(df):
    df['status_cat'] = pd.Categorical(df['status'],
                                      categories=['Founder','Owner',
                                                  'Admin','Ascended','member',
                                                  'beginner','unregistered'],
                                      ordered=True)
    df = df.sort_values(by='status_cat')
    df = df.drop('status_cat', 1)
    return df



# Function checks if x is in y, aka if member
# 'x' is already in the roster.csv username list 'y'
def Check_Roster(x,y):
    for i in y:
        if str(i) == str(x):
            return True
    return False



# Add member to the roster.csv file. Some information
# is collected automatically, other information added if
# user provides said information.
def Add_To_Roster(memb, args, admin=False):

    # load roster
    roster = pd.read_csv('./utils/roster.csv', dtype=object)
    
    # only add user if user not in roster already
    if not Check_Roster(memb.id, roster['id']):
        # Information to append when new
        roster = roster.append({
                               'username': get(memb.name),
                               'date': datetime.date.today(),
                               'id': memb.id,
                               'on_server': 'Y',
                               'status':Get_Member_Role(memb),
                               'nickname':memb.nick
                               },ignore_index=True)
        roster = sortRoster(roster)
        roster.to_csv('./utils/roster.csv', index=False) # save changes
    
    # process additional args, use valid to check user input
    valid = False
    for arg in args:
        # ADD CLASSES
        if arg.lower() == 'hunter' or arg.lower() == 'warlock' or arg.lower() == 'titan':
            valid = True
            Add_Class(memb, arg.lower())
        # ADD TIME PREFERENCE
        if arg.lower() == 'day' or arg.lower() == 'morning' or arg.lower() == 'night':
            valid = True
            Add_Time_Pref(memb, arg.lower())
        # ADD BIRTHDAY
        if Valid_Date(arg):
            valid = True
            Add_Birthday(memb, arg)
        # ADD TIMEZONE
        for t in TIMEZONES:
            if arg == t:
                valid = True
                Add_Timezone(memb, arg)

        if arg != 'add' and not valid and not admin:
            return False, arg
        valid = False  # reset arg validity for next round
    return True, 'success' # additions successfull



# Add member to the roster.csv file. Some information
# is collected automatically, other information added if
# user provides said information.
def Admin_Add_To_Roster(memb):
    msg = ''
    # load roster
    roster = pd.read_csv('./utils/roster.csv', dtype=object)
    
    # only add user if user not in roster already
    if not Check_Roster(memb.id, roster['id']):
        # Information to append when new
        roster = roster.append({
                               'gamertag': memb,
                               'date': datetime.date.today(),
                               'on_server': 'N',
                               'status':'beginner',
                               },ignore_index=True)
        roster = sortRoster(roster)
        roster.to_csv('./utils/roster.csv', index=False) # save changes
    else:
        msg = 'User already in roster.'
    return msg



# Function gets a count of how many rows
# are in .csv file
def Roster_Count():
    f = open('./utils/roster.csv')
    count = len(f.readlines())
    f.close()
    return 'There are `'+str(count-1)+'` members in the roster database.'



# Function adds the users gamertag to the
# roster .csv file, and supports gametags
# with spaces. This command is seperate
# from the standard roster add command
def Add_Gamertag(memb, args, admin=False):
    try:
        roster = pd.read_csv('./utils/roster.csv', dtype=object)
        idx = roster[roster['id'] == memb.id].index.item()
        gt = ''
        start = 2
        if admin:
            start = 0
        for i in range(start,len(args)):
            if i == (len(args) - 1):
                gt += args[i]
            else:
                gt += args[i] + ' '
        roster.at[idx,'gamertag'] = gt
        roster = sortRoster(roster)
        roster.to_csv('./utils/roster.csv', index=False)
        return True
    except:
        return False


# Function adds a note to the users info in
# roster.csv file. This command is seperate
# from the standard roster add command
def Add_Note(memb, args):
    try:
        roster = pd.read_csv('./utils/roster.csv', dtype=object)
        idx = roster[roster['id'] == memb.id].index.item()
        note = ''
        for i in range(2,len(args)):
            if i == (len(args) - 1):
                note += args[i]
            else:
                note += args[i] + ' '
        if len(note) < 35:
            roster.at[idx,'note'] = note
            roster = sortRoster(roster)
            roster.to_csv('./utils/roster.csv', index=False)
            return True, ''
        else:
            return False, 'length'
    except:
        return False, 'not found'




# Function adds members class(es)
# and is a helper to Add_To_Roster
def Add_Class(memb, clss):
    roster = pd.read_csv('./utils/roster.csv', dtype=object)
    idx = roster[roster['id'] == memb.id].index.item()
    roster.at[idx,clss] = 'Y'
    roster = sortRoster(roster)
    roster.to_csv('./utils/roster.csv', index=False)


# Function adds members timezone
# and is a helper to Add_To_Roster
def Add_Timezone(memb, tzone):
    roster = pd.read_csv('./utils/roster.csv', dtype=object)
    idx = roster[roster['id'] == memb.id].index.item()
    roster.at[idx,'timezone'] = tzone
    roster = sortRoster(roster)
    roster.to_csv('./utils/roster.csv', index=False)



# Function adds members time preference
# and is a helper to Add_To_Roster
def Add_Time_Pref(memb, tpref):
    roster = pd.read_csv('./utils/roster.csv', dtype=object)
    idx = roster[roster['id'] == memb.id].index.item()
    roster.at[idx,'tpref'] = tpref
    roster = sortRoster(roster)
    roster.to_csv('./utils/roster.csv', index=False)



# Function adds members time preference
# and is a helper to Add_To_Roster
def Add_Birthday(memb, bday):
    roster = pd.read_csv('./utils/roster.csv', dtype=object)
    idx = roster[roster['id'] == memb.id].index.item()
    roster.at[idx,'birthday'] = Date_Transform(bday)
    roster = sortRoster(roster)
    roster.to_csv('./utils/roster.csv', index=False)




# Functions removes member data from
# the roster.csv file.
def Remove_From_Roster(memb):
    roster = pd.read_csv('./utils/roster.csv', dtype=object)
    if Check_Roster(get(memb), roster['username']):
        roster = roster[roster.username != get(memb)]
        roster = sortRoster(roster)
        roster.to_csv('./utils/roster.csv', index=False)
        return True, 'success'
    if Check_Roster(get(memb), roster['gamertag']):
        roster = roster[roster.gamertag != get(memb)]
        roster = sortRoster(roster)
        roster.to_csv('./utils/roster.csv', index=False)
        return True, 'success'
    return False, memb



# Updates member status in roster.csv
# memb is member object.
def Update_Member(memb, arg):
    if memb is not None:
        roster = pd.read_csv('./utils/roster.csv', dtype=object)
        if Check_Roster(memb.id, roster['id']):
            idx = roster[roster['id'] == memb.id].index.item()
            roles = memb.roles
            rlist = {7: 'Founder',
                     6: 'Owner',
                     5: 'Admin',
                     4: 'Ascended',
                     3: 'member',
                     2: 'beginner',
                     1: 'unregistered'}
            rolenum = perms.Get_Role(memb)
            roster.at[idx,'status'] = rlist[rolenum]
            roster.at[idx,'username'] = get(memb.name)
            roster.at[idx,'nickname'] = memb.nick
            roster = sortRoster(roster)
            roster.to_csv('./utils/roster.csv', index=False)
            return True, 'success'
    return False, arg



def Update_All(members, arg):
    members = set(members)
    success = True
    issue = []
    for memb in members:
        try:
            roster = pd.read_csv('./utils/roster.csv', dtype=object)
            if Check_Roster(memb.id, roster['id']):
                idx = roster[roster['id'] == memb.id].index.item()
                roles = memb.roles
                rlist = {7: 'Founder',
                         6: 'Owner',
                         5: 'Admin',
                         4: 'Ascended',
                         3: 'member',
                         2: 'beginner',
                         1: 'unregistered'}
                rolenum = perms.Get_Role(memb)
                roster.at[idx,'status'] = rlist[rolenum]
                roster.at[idx,'username'] = get(memb.name)
                roster.at[idx,'nickname'] = memb.nick
                roster = sortRoster(roster)
                roster.to_csv('./utils/roster.csv', index=False)
        except:
            success = False
            issue.append(memb.name)

    return success, issue



'''
    SHOW ROSTER FUNCTIONS ~~~~~~
Show_Roster_Gamertag:
    TAKE:    str(description), dataFrame(row)
    RETURNS: True, str(description)

Show_Roster_Tpref:
    TAKE:    str(description), dataFrame(row)
    RETURNS: True, str(description)

Show_Roster_Birthday:
    TAKE:    str(description), dataFrame(row)
    RETURNS: True, str(description)

Show_Roster_Wrapup:
    TAKES:   str(col), str(desc), dataFrame(sub), bool(gt), bool(tp)
    RETURNS: str(description)

Show_Roster:
    TAKES: str(list(arguments)
    RETURNS: Show_Roster_Wrapup
Roster_User_info:
    TAKES: obj(memb)
    returns str(memb) str(description)
    RETURNS:
'''


# Helper function to Roster_Show()
# completes description given gamertag query
# desc is a string, row is a dataFrame
def Show_Roster_Gamertag(desc, row):
    # print None or value
    if pd.isnull(row['gamertag']):
        desc += 'None\n'
    else:
        desc += str(row['gamertag'])+'\n'
    return True, desc



# Helper function to Roster_Show()
# completes description given birthday query
# desc is a string, row is a dataFrame
def Show_Roster_Birthday(desc, row):
    # print None or value
    if pd.isnull(row['birthday']):
        desc += 'None\n'
    else:
        desc += str(row['birthday'])+'\n'
    return True, desc



# Helper function to Roster_Show()
# completes description given tpref query
# desc is a string, row is a dataFrame
def Show_Roster_Tpref(desc,row):
    # print None or value
    if pd.isnull(row['tpref']):
        desc += str(row['timezone'])+' | no preference\n'
    else:
        desc += str(row['timezone'])+' | '+str(row['tpref'])+'\n'
    return True, desc



# Helper function to Roster_Show()
# completes description given status query
# desc is a string, row is a dataFrame
def Show_Roster_Status(desc,row):
    # print None or value
    if pd.isnull(row['status']):
        desc += 'None\n'
    else:
        desc += str(row['status'])+'\n'
    return True, desc



# Helper function to Roster_Show()
# finalizes roster description given boolean values
# desc & col are strings, sub is a dataFrame, gt & tp are booleans
def Show_Roster_Wrapup(col, desc, pgs, total, sub, gt, tp, bd, st):
    if gt:
        for i in range(0,len(desc)):
            desc[i] = col + ' | gamertag**\n'+desc[i]
        return desc, str(pgs), str(total), 'Gamertag'

    elif tp:
        for i in range(0,len(desc)):
            desc[i] = col + ' | timezone | tpref**\n'+desc[i]
        return desc, str(pgs), str(total), 'time-of-day'

    if bd:
        for i in range(0,len(desc)):
            desc[i] = col + '\t\t\t\t\t\t\tbirthday**\n```' + desc[i] + '```'
        return desc, str(pgs), str(total), 'Birthday'
    if st:
        for i in range(0,len(desc)):
            desc[i] = col + '\t\t\t\t\t\t\tstatus**\n```' + desc[i] + '```'
        return desc, str(pgs), str(total), 'Status'
    
    else:
        for i in range(0,len(desc)):
            desc[i] = col + '\t\t\t\t\t\t\ttimezone**\n```' + desc[i] + '```'
        return desc, str(pgs), str(total), 'General'



# Function prepares the output for the roster show tpref
# command. tpref is day, night, or morning.
def Roster_Subshow_Tpref(sub, col, desc,pgs, tpref):
    if tpref.lower() != 'day' and tpref.lower() != 'morning'\
                       and tpref.lower() != 'night' and tpref.lower() != 'none':
        return desc, pgs, '-1', tpref
    count = i = total = 0
    for index, row in sub.iterrows():
        if count > 19:
            desc.append('')
            i += 1
            count = 0
        # Dont include members not on discord!
        if not pd.isnull(row['username']):
            if str(row['tpref']) == tpref.lower():
                count += 1
                total += 1
                desc[i] += Prepare_String(str(row['username'])).ljust(16)
                desc[i] += str(row['timezone'])+'\n'
            if 'none' == tpref.lower() and pd.isnull(row['tpref']):
                count += 1
                total += 1
                desc[i] += Prepare_String(str(row['username'])).ljust(16)
                desc[i] += str(row['timezone'])+'\n'

    pgs = len(desc)
    for i in range(0,len(desc)):
        desc[i] = col + '\t\t\t\t\t\t\tzone/'+tpref+'**\n```' + desc[i] + '```'
    return desc, str(pgs), str(total), '\ntime-of-day = '+tpref



# Function prepares the output for the roster show tpref
# command. tpref is day, night, or morning.
def Roster_Subshow_Status(sub, col, desc,pgs, sts):
    if sts.lower() != 'beginner' and sts.lower() != 'member' and sts.lower() != 'ascended':
        return desc, pgs, '-1', sts
    count = i = total = 0
    for index, row in sub.iterrows():
        if count > 19:
            desc.append('')
            i += 1
            count = 0
        # Dont include members not on discord!
        if not pd.isnull(row['username']):
            if str(row['status']).lower() == sts.lower():
                count += 1
                total += 1
                desc[i] += Prepare_String(str(row['username'])).ljust(16)
                desc[i] += str(row['status'])+'\n'

    pgs = len(desc)
    for i in range(0,len(desc)):
        desc[i] = col + '\t\t\t\t\t\t\tstatus**\n```' + desc[i] + '```'
    return desc, str(pgs), str(total), '\nstatus = '+sts




# Function prepares the output for the roster show tpref
# command. tpref is day, night, or morning.
def Roster_Subshow_Timezone(memb, sub, col, desc,pgs, tzone):
    valid = False
    for t in TIMEZONES:
        if tzone == t:
            valid = True
    
    if not valid:
        return desc, pgs, '-1', tzone

    idx = sub[sub['username'] == get(memb.name)].index.item()
    mtzone = str(sub.at[idx,'timezone'])
    count = i = total = 0
    for index, row in sub.iterrows():
        if count > 19:
            desc.append('')
            i += 1
            count = 0
        # Dont include members not on discord!
        if not pd.isnull(row['username']):
            if str(row['timezone']) == tzone:
                count += 1
                total += 1
                desc[i] += Prepare_String(str(row['username'])).ljust(16)
                desc[i] += str(row['timezone'])+'\n'

    pgs = len(desc)
    for i in range(0,len(desc)):
        temp =  memb.name + '\n'
        temp += '**Your time: **'+User_Time(mtzone)+' | ** '+tzone+' time: **'+User_Time(tzone)+'\n'
        temp += '*'+Tzone_Diff_Format(mtzone, tzone)+'*\n\n'
        desc[i] = temp + col + '\t\t\t\t\t\t\ttimezone**\n```' + desc[i] + '```'
    return desc, str(pgs), str(total), '\ntimezone = '+tzone



# Function prepares the output for the roster show class
# command. class is either Titan, Warlock, or Hunter
def Roster_Subshow_Class(sub, col, desc, pgs, clss):
    if clss.lower() != 'titan' and clss.lower() != 'hunter' and clss.lower() != 'warlock':
        return desc, pgs, '-1', clss
    count = i = total = 0
    i = 0
    for index, row in sub.iterrows():
        if count > 19:
            desc.append('')
            i += 1
            count = 0
        # Dont include members not on discord!
        if not pd.isnull(row['username']):
            if str(row[clss.lower()]) == 'Y':
                count += 1
                total += 1
                desc[i] += Prepare_String(str(row['username'])).ljust(16)
                desc[i] += clss.title()+'\n'

    pgs = len(desc)
    for i in range(0,len(desc)):
        desc[i] = col + '\t\t\t\t\t\t\t'+clss+'**\n```' + desc[i] + '```'
    return desc, str(pgs), str(total), '\nClass = '+clss.title()



# Function prepares the output for the roster show birthday
# command. month is a string word representing one of the
# 12 months
def Roster_Subshow_Birthday(sub, col, desc, pgs, month):
    months = {'january':'01', 'february':'02','march':'03',
            'april':'04','may':'05','june':'06','july':'07',
            'august':'08','september':'09','october':'10',
            'november':'11','december':'12'}

    try:
        Valid_Date(months[month.lower()]+'/1')
    except:
        return desc, pgs, '-1', month

    count = i = total = 0
    i = 0
    for index, row in sub.iterrows():
        if count > 19:
            desc.append('')
            i += 1
            count = 0
        
        # Dont include members not on discord!
        if not pd.isnull(row['username']):
            if not pd.isnull(row['birthday']):
                if str((row['birthday'])).split('/')[0] == months[month.lower()]:
                    count += 1
                    total += 1
                    desc[i] += Prepare_String(str(row['username'])).ljust(16)
                    desc[i] += str(row['birthday'])+'\n'
    pgs = len(desc)
    for i in range(0,len(desc)):
        desc[i] = col + '\t\t\t\t\t\t\tbirthday**\n```' + desc[i] + '```'
    return desc, str(pgs), str(total), '\nBirthday = '+month.title()



# Function prepares the output for the roster show
# command. args s a list of strings/queries, which modifies
# the output.
def Show_Roster(memb, args):
    roster = pd.read_csv('./utils/roster.csv', dtype=object)
    gt = tp = bd = st = False
    col = '**username'
    desc = ['']
    pgs = 1

    if len(args) > 2:
        if args[1].lower() == 'tpref':
            return Roster_Subshow_Tpref(roster, col, desc, pgs, args[2])
        if args[1].lower() == 'class':
            return Roster_Subshow_Class(roster, col, desc, pgs, args[2])
        if args[1].lower() == 'birthday':
            return Roster_Subshow_Birthday(roster, col, desc, pgs, args[2])
        if args[1].lower() == 'status':
            return Roster_Subshow_Status(roster, col, desc, pgs, args[2])
        if args[1].lower() == 'timezone':
            return Roster_Subshow_Timezone(memb, roster, col, desc, pgs, args[2])
        else:
            return desc,'-1','-1',args[1]
    else:
        sub = roster[['username','id','status','gamertag','birthday','timezone', 'tpref']]
        count = i = total = 0
        # GENERAL ROSTER SHOWS: GAMETAG, TIME PREF, & TIME ZONE
        for index, row in sub.iterrows():
            if count > 19:
                desc.append('')
                i += 1
                count = 0

            # Dont include members not on discord!
            if not pd.isnull(row['username']):
                count += 1
                total += 1
                # different format for gamertag roster show
                if len(args) > 1 and (args[1].lower() == 'gamertag' or args[1].lower() == 'tpref'):
                    desc[i] += '× ' + Prepare_String(str(row['username'])) + ' | '
                else:
                    desc[i] += Prepare_String(str(row['username'])).ljust(16)

                # for specific outputs
                if len(args) > 1:
                    if args[1].lower() == 'gamertag':
                        gt, desc[i] = Show_Roster_Gamertag(desc[i], row)
                    if args[1].lower() == 'birthday':
                        bd, desc[i] = Show_Roster_Birthday(desc[i], row)
                    if args[1].lower() == 'tpref':
                        tp, desc[i] = Show_Roster_Tpref(desc[i], row)
                    if args[1].lower() == 'status':
                        st, desc[i] = Show_Roster_Status(desc[i], row)
                # no args
                else:
                    # print None or value
                    if pd.isnull(row['timezone']):
                        desc[i] += 'None\n'

                    else:
                        desc[i] += str(row['timezone'])+'\n'

            pgs = i + 1
        return Show_Roster_Wrapup(col, desc, pgs, total, sub, gt, tp, bd, st)



# Function creates description of user from
# roster. memb is member object.
def Roster_User_info(memb):
    roster = pd.read_csv('./utils/roster.csv', dtype=object)
    
    try:
        idx = roster[roster['id'] == memb.id].index.item()
    except:
        return memb, ''
    scrap, groles = Get_Guided_Roles(memb)
    desc = ''
    desc += '**× Status**: '+str(roster.at[idx,'status']) + '\n'
    desc += '**× Gamertag**: '+str(roster.at[idx,'gamertag']) + '\n'
    if not pd.isnull(roster.at[idx,'nickname']):
        desc += '**× nickname**: '+str(roster.at[idx,'nickname']) + '\n'
    desc += '**× Join Date**: '+str(roster.at[idx,'date']) + '\n'
    desc += '**× Birthday**: '+str(roster.at[idx,'birthday']) + '\n'
    desc += '**× Timezone**: '+str(roster.at[idx,'timezone'])+'\n'
    if pd.isnull(roster.at[idx,'tpref']):
        desc += '**× Time Preference**: no preference\n'
    else:
        desc += '**× Time Preference**: '+str(roster.at[idx,'tpref']) +'\n'
    desc += '**× Classes**: '
    clsscount = 0
    if roster.at[idx,'hunter'] == 'Y':
        clsscount += 1
        desc += 'Hunter'
    if roster.at[idx,'titan'] == 'Y':
        clsscount += 1
        if clsscount > 1:
            desc += ', Titan'
        else:
            desc += 'Titan '
    if roster.at[idx,'warlock'] == 'Y':
        clsscount += 1
        if clsscount > 1:
            desc += ', Warlock '
        else:
            desc += 'Warlock '
    if clsscount == 0:
        desc+= 'unknown'
    desc += '\n'
    if not pd.isnull(roster.at[idx,'note']):
        desc += '**× Note**: '+str(roster.at[idx,'note']) +'\n'
    desc += '**× Guided Roles**: '
    if len(groles) > 0:
        for i in range(len(groles)):
            if i == len(groles) -1 :
                desc += groles[i]
            else:
                desc += groles[i] + ', '
    else:
        desc += 'none'
    desc +=  '\n'

    return memb.name, desc


'''
REGISTRATION FUNCTIONS ~~~~~~
Registration_Begin:
    TAKES: obj(member)
    RETURNS: str(message), str(message), str(message)
    
Registration_Check_One:
    TAKES: obj(member)
    RETURNS: str(message), list(str(missing parameters)), bool
Registration_Final:
    TAKES: obj(member), obj(founders chnl), obj(info chnl), bool
    RETURNS: str(message)
'''

# Function returns messages based on which
# step member "m" is on in the registration
# process.
def Registration_Begin(m, step):
    missing_params = []
    msg = msg1 = msg2 = ''
    if step == 1:
        msg += 'Hello '+m.mention + '. **PLEASE READ this entire message before trying '
        msg += 'any of the commands below.**\nTo begin, we need to add you to the clan '
        msg += 'roster. To do so, we will use the following command:\n'
        msg += '```css\n.roster add <timezone> <time pref> '
        msg += '<class>```\n I will let you know if the command worked. Next, use the following '
        msg += 'command to add your gamertag:\n```css\n.roster add gt <gamertag>```\n'
        msg1 += m.mention + '\nIn the above commands, text in "<>" brackets are optional and specific '
        msg1 += 'to you:\n\n**+** The ***timezone*** parameter should be capatilized (ex. **EST**),'
        msg1 += '\n**+** The ***time preference*** should be **morning**. **day**, or **night**,'
        msg1 += '\n**+** You should include any ***character classes*** you have,'
        msg1 += '\n**+** Finally, the ***gamertag*** should be entered exactly as is on XBOX Live, '
        msg1 += 'spaces and all.\n\n__**NOTE:**__ *the angled brackets "<>" should NOT be included, '
        msg1 += 'and a space should be made between each parameter.*\n\n'
        msg2 += m.mention + '\nAn example of valid commands are below:\n'
        msg2 += '```css\n.roster add EST morning Hunter Warlock```'
        msg2 += '```css\n.roster add gt EAAA Bot```\n where the gamertag is *"EAAA Bot"*. '
        msg2 += 'Once you have completed the above step, please send the message\n'
        msg2 += '```css\ncontinue```\nand we will move to step 2!.'
    
    elif step == 2:
        msg += m.mention + '\nThe last step is to register yourself with our '
        msg += 'designated Destiny 2 Bot, **Charlemagne**. This bot is extremely '
        msg += 'useful, and can return to you almost any information related to your '
        msg += 'Destiny 2 account, stats, and/or progress. To register with '
        msg += 'Charlemagne, type the following command as a message and send it:'
        msg += '```css\n!register```\n This will prompt Charlemagne to send you '
        msg += 'a private message with a link to authorize the bot to access your '
        msg += 'Destiny 2 information with Bungie.net.\nFollow the link, complete '
        msg += 'the form, and return here and input the following command to test '
        msg += 'if you successfully registered with Charlemagne:```css\n!loadout'
        msg += '```\n, If successful, we will upgrade your clan status and lift all '
        msg += 'current restrictions.'
    else:
        return 'Something Went Wrong'
    return msg, msg1, msg2



# Function checks that member successfully
# added their username, timezone, gamertagm
# and at least 1 class to the clan Roster.csv
# file. Returns a message, a list of missing
# requirements (if applicable), and a boolean
# indicating if the check was successful.
def Registration_Check_One(memb):
    
    msg = ''
    missing_params = []
    dict = {'username':False, 'Class':False, 'Timezone':False, 'Gamertag':False}
    roster = pd.read_csv('./utils/roster.csv', dtype=object)
    
    # try to get idx, if fails, user not in roster
    try:
        idx = roster[roster['username'] == get(memb.name)].index.item()
        dict['username'] = True
        msg += '**Username Added: :white_check_mark: |** '

        # check that requirements are finished
        if pd.isnull(roster.loc[idx,'timezone']):
            msg += '**Timezone Added: :x: |** '
        else:
            dict['Timezone'] = True
            msg += '**Timezone Added: :white_check_mark: |** '

        if pd.isnull(roster.loc[idx,'gamertag']):
            msg += '**Gamertag Added: :x: |** '
        else:
            dict['Gamertag']  = True
            msg += '**Gamertag Added: :white_check_mark: |** '

        if pd.isnull(roster.loc[idx,'hunter']) and\
            pd.isnull(roster.loc[idx,'titan']) and\
                    pd.isnull(roster.loc[idx,'warlock']):
            msg += '**Class Added: :x:** '
        else:
            dict['Class']  = True
            msg += '**Class Added: :white_check_mark:** '

    except:
        msg += '**Username Added: :x:** '

    # Check for missing requirements, add to list
    for key in dict:
        if dict[key] == False and key != 'username':
            missing_params.append(key)

    # If list is not empty, return list and False, else return true
    if len(missing_params) > 0:
        return msg, missing_params, False
    return msg, missing_params, True



# Function prepares a message to the user
# which is dependent on whether they successfully
# registered with Charlemagne
def Registration_Final(m, founders, information, success):
    if success:
        msg = m.mention + '\n **you have successfully completed '
        msg += 'registration**.\nYour status has been upgraded to **Beginner**. Make '
        msg += 'sure you read through '+founders.mention+' when you have time to '
        msg += 'learn all about the clan. Additionally, **please** take the time '
        msg += 'to read through the '+information.mention+' channel to learn about '
        msg += 'our Discord server, the different channels available to you, and how '
        msg += 'our bots and various commands work!\n **WELCOME TO THE CLAN!!**'
    else:
        msg = m.mention + '\n**You did not register with Charlemagne.**\n'
        msg += 'Please try the following command again: ```css\n!register```'
        msg += '**remember**, this command does not register you!!\nIt simply '
        msg += 'instructs Charlemagne to send you a **private message** with a '
        msg += 'link that you must tap/click on to register!! Please try again, '
        msg += 'and repeat the command `!loadout` to continue... ...'
    return msg




'''
GUIDED ROLES FUNCTIONS ~~~~~~
Add_Guided_Role:
    TAKES: obj(member), obj(info channel), str(guided roles)
    RETURNS: str(message)
    
Guided_Roles_Msg
    TAKES: obj(member), obj(server roles), str(guided roles)
    RETURNS: str(guided role message)
'''

# function creates the message to be sent to a member in
# a private message. Here, memb is a member object, info is
# the information channel object.
def Add_Guided_Role(memb, info, gr):
    msg = '**GUIDED ROLE PROTOCOL INITIATED~~~**\n\n'
    msg += '__User has applied for Guided Role: *'+gr+'*__\n'
    msg += memb.mention + ', thank you for your **Guided Role** application.\n'
    msg += 'Before giving you the role, we want to make absalutely sure that you '
    msg += 'have read the requirements for the role in ' + info.mention
    msg +=  ' **Section VI**. We (The Admins) would **hate to have to take the role away from you** at a '
    msg += 'later time due to you not meeting the minimum requirements for said role.\n\n'
    msg += 'If you have already checked the requirements and have confirmed you are '
    msg += 'qualified, type and reply to this message with **"acknowledged"** to continue. '
    msg += 'If you wish to cancel your application, simply type and send **"cancel"**.'
    return msg


# returns a unique message for the given
# guided role gr. r is all roless object,
# m is a member objecy.
def Guided_Roles_Msg(m, r, gr):
    GROLESMSG = {
    'pveers': '**Well looky here looky here!! '+m.mention+' has just added a new Guided Role:** '\
              +Role_Obj(r, gr).mention+'. Looks like you just hate those non-human-looking-sp'\
              +'ecies? Well done...... Well done indeed...',
    'pvpers': '**Awwww Shittttttt! '+m.mention+' has just added a new Guided Role:** '\
              +Role_Obj(r, gr).mention+'. Looks like you\'ve been kicking ass in the'\
              +' crucible? Well done...... Well done indeed...',
    'veteran':'**Damn, your old!! '+m.mention+' has just added a new Guided Role:** '\
              +Role_Obj(r, gr).mention+'. Looks like you knew the Speaker pretty '\
              +'well... How was the funeral? Did you at least send flowers? Well done'\
              +'...... Well done indeed...',
    '335': '**Well you should stand up right now, and scream "Celebrate Me!!". '+m.mention\
              +' has just added a new Guided Role:** '+Role_Obj(r, gr).mention\
              +'. I need kinetic mods..... You got kinetic mods? Well done...... Well done indeed...',
    'leviathan': '**Well fill my golden chalice up, cause I\'ve got a toast to make!! '\
              +m.mention+' has just added a new Guided Role:** '+Role_Obj(r, gr).mention\
              +'. So how many times have you killed that big-ass robot guy now? Well '\
              +'done...... Well done indeed...',
    'flawless': '**Holy shit, your light is literally blinding!! '+m.mention+' has just'\
              +' added a new Guided Role:** '+Role_Obj(r, gr).mention+'. So..... '\
              +'seven-in-a-row ay? How did you do it?!..... seriously..... how did '\
              +'you do it dude/dudett.....',
    'lore specialist': '** Well look what we have here, our very own valedictorian!! '\
              +m.mention+' has just added a new Guided Role:** '+Role_Obj(r, gr).mention\
              +'., So whats your research paper called? I\'m listed as an author...... '\
              +'right?  Well done...... Well done indeed...',
    'class specialist': '**Holy shit you\'ve been busy!! '+m.mention+' has just added '\
              +'a new Guided Role:** '+Role_Obj(r, gr).mention+'. So..... What do I '\
              +'call you now? And be honest, whose your favorite child? Well done......'\
              +' Well done indeed...',
    'weapons specialist': '** Three volleys to you my friend!! '+m.mention+' has just '\
              +'added a new Guided Role:** '+Role_Obj(r, gr).mention+'. Im happy for '\
              +'you, but can you point that thing somewhere else? Well done...... Well done indeed...',
    'eow': '** you puzzle-jumpin, robot-killin maniac!! '+m.mention+' has just '\
              +'added a new Guided Role:** '+Role_Obj(r, gr).mention+'. That\'s cool and '\
              +'all, but shrunken vex heads is kind of creepy... hey, everyon has their "thang".'
    }
    return GROLESMSG[gr.lower()]



'''
HELP FUNCTIONS ~~~~~~
Help_Gen:
    TAKES: None
    RETURNS: strings(descriptions)
Help_Roster:
    TAKES: None
    RETURNS: strings(descriptions)
Help_Guidedroles:
    TAKES: None
    RETURNS: strings(descriptions)
Help_Destiny:
    TAKES: None
    RETURNS: strings(descriptions)
Help_Other:
    TAKES: None
    RETURNS: strings(descriptions)
Help_Admin:
    TAKES: None
    RETURNS: strings(descriptions)
'''


def Help_Gen():
    desc = '**Note:** Angled brackets "<>" represent command arguments and '
    desc += 'should not be included. The text within angled brackets describe '
    desc += 'the argument, but is not the argument itself. Addintionaly,\n\n'
    desc += '**×** ***italicised*** arguments are optional.\n'
    desc += '**×** __**underlined**__ arguments are required.\n'
    desc += '**×**  use **.help <*category*>** for additonal info. '
    roster = '**.roster add <*tzone*> <*tpref*> <*class*> <*birthday*>**\n'
    roster += '**.roster add gt <__users gamertag__>**\n'
    roster += '**.roster add note <__note contents__>**\n'
    roster += '**.roster show <*query1*> <*query2*>**\n'
    roster += '**.roster <__user/@user__>**\n'
    gr = '**.guidedroles add @<__valid guided role__>**\n'
    gr += '**.guidedroles @<__valid guided role__>**\n'
    D2 = '**.guardian**\n'
    D2 += '**.underbelly <*map*> <*code*>**\n'
    D2 += '**.leviathan <__dogs/bathes/gauntlet/calus__>**\n'
    other = '**.congrats @<__user__>**\n'
    other += '**.poll "<__question__>" "<__option1__>" "<__option2__>" "<*options*>"**\n'
    other += '**.tally <__poll ID__>**\n'
    return desc, roster, gr, D2, other



def Help_Roster():
    desc = 'Basic guide to Roster commands.\n'
    
    r1 = '**Adds user (if not already added) to the clan roster, plus '
    r1 += 'additional information about said user given by arguments.**'
    r1 += '\n─────────────\n'
    r1 += '**Args: ** <*tzone*> <*tpref*> <*class*> <*birthday*>\n'
    r1 += '*Arguments add additional information about a user to the clan roster.*\n'
    r1 += '**×** *"tzone"* A valid timezone.\n'
    r1 += '**×** *"tpref"* is your time preference:\n\tmorning/day/night\n'
    r1 += '**×** *"class"* is a valid Destiny 2 class:\n\tHunter/Titan/Warlock.\n'
    r1 += '**×** *"birthday"* format is <month/day>. Include "/" in your command.\n'
    r1 += '\t Can add 1, 2, or all 3 classes.'
    r1 += '\n─────────────\n'
    r1 += '**EXAMPLE COMMAND:**\n.roster add EST 4/28 morning warlock hunter titan.\n\n\n'
    
    r2 = '**Adds users gamertag to the clan roster.**'
    r2 += '\n─────────────\n'
    r2 += '**Args: ** <__gamertag__>\n'
    r2 += '*Argument is the users gamertag, exactly as is on **XBOX LIVE**.*'
    r2 += '\n─────────────\n'
    r2 += '**EXAMPLE COMMAND:**\n.roster add gt EAaA BoT\n\n\n'
    
    r3 = '**Adds a user note to the clan roster.**'
    r3 += '\n─────────────\n'
    r3 += '**Args: ** <__note contents__>\n'
    r3 += '*Argument is a message or note, less than 25 characters.**.*'
    r3 += '\n─────────────\n'
    r3 += '**EXAMPLE COMMAND:**\n.roster add note has 2 hunter classes\n\n\n'
    
    
    r4 = '**Shows the clan roster. Defaults to username and timezone,  '
    r4 += 'but arguments can be used to specify show options.**'
    r4 += '\n─────────────\n'
    r4 += '**Args: ** class/tpref/birthday/status/timezone <*class/tpref/month/role/tzone*>\n'
    r4 += '*Using one of the 1st arguments alone specifies what information to '
    r4 += 'show in the second column of the output. Adding the corresponding 2nd '
    r4 += 'argument queries the roster to show only those users who fit that '
    r4 += 'criteria.*\n'
    r4 += '**×** *"tpref"* is a time preference:\n\tmorning/day/night/none.\n'
    r4 += '**×** *"class"* is a valid Destiny 2 class:\n\tHunter/Titan/Warlock.\n'
    r4 += '**×** *"month"* is a valid month name. eg.. February.\n'
    r4 += '**×** *"role"* is a valid general role. eg.. member.\n'
    r4 += '**×** *"tzone"* is a valid timezone acronym. eg.. member.\n'
    r4 += '\n─────────────\n'
    r4 += '**EXAMPLE COMMANDS:**\n'
    r4 += '.roster show gamertag.\n'
    r4 += '.roster show class hunter.\n'
    r4 += '.roster show tpref night.\n'
    r4 += '.roster show birthday June.\n'
    r4 += '.roster show status beginner.\n'
    r4 += '.roster show timezone UTC.\n'
    
    r5 = '**Shows roster information for given user.**'
    r5 += '\n─────────────\n'
    r5 += '**Args: ** <__user/@user__>\n'
    r5 += '*Argument is a username, exactly as is on discord.*'
    r5 += '\n─────────────\n'
    r5 += '**EXAMPLE COMMAND:**\n.roster @EAAA'
    
    return desc,r1,r2, r3, r4, r5

def Help_Guidedroles():
    desc = 'Basic guide to Guided Roles commands.\n'
    
    gr1 = '**Assigns given Guided Role to user. Command sends user a private '
    gr1 += 'message, with directions on how to obtain said role. If successful '
    gr1 += 'approval of said role is announced in game-chat.**'
    gr1 += '\n─────────────\n'
    gr1 += '**Args: ** @<__Guided Role__>\n'
    gr1 += '*Argument is a valid Guided Role. See information channel, Section VI.*'
    gr1 += '\n─────────────\n'
    gr1 += '**EXAMPLE COMMAND:**\n.guidedroles add @Lore Specialist.\n\n\n'
    gr2 = '**Shows list of all members with given guided roles.**'
    gr2 += '\n─────────────\n'
    gr2 += '**Args: ** @<__Guided Role__>\n'
    gr2 += '*Argument is a valid Guided Role. See information channel, Section VI.*'
    gr2 += '\n─────────────\n'
    gr2 += '**EXAMPLE COMMAND:**\n.guidedroles @Class Specialist.\n\n\n'
    return desc, gr1, gr2


def Help_Destiny():
    desc = 'Basic guide to Destiny 2 commands.\n'
    
    d1 = '**Allows user to display their guardian image and profile. The command '
    d1 += 'sends a private message to user, who must enter/answer multiple questions '
    d1 += 'about their  guardian image.**'
    d1 += '\n─────────────\n'
    d1 += '**Args:** None\n'
    d1 += '*It is recommended that you collect the following info before '
    d1 += 'using the command to make the process easier: *\n'
    d1 += '**×** Image URL of your guardian in the start menu,\n'
    d1 += '**×** The names of your equiped helmet, arms,\n\tchest, legs, class item, '
    d1 += '& shaders.\n'
    d1 += 'You can use [OneDrive](https://onedrive.live.com/about/en-us/) to get your '
    d1 += 'screenshots URL - just sign in, go to files -> xbox screenshots, '
    d1 += 'select image, select share in top left of screen, input given url into '
    d1 += 'your browser, select image. Finally, copy the link in your browser '
    d1 += 'and **use that!!**. If you have an alternative method, thats fine, '
    d1 += 'this is just **ONE** way to do it.*\n'
    d1 += '**× Note** your profile will not be posted unless\n\tyou confirm at the end.'
    d1 += '\n─────────────\n'
    d1 += '**EXAMPLE COMMAND:**\n.guardian\n\n\n'

    d2 = '**Given argument, shows underbelly map or pipes code..**'
    d2 += '\n─────────────\n'
    d2 += '**Args: ** __map/code__\n'
    d2 += '*Argument is either map or code.*'
    d2 += '\n─────────────\n'
    d2 += '**EXAMPLE COMMAND:**\n.underbelly map\n\n\n'
    
    d3 = '**Given argument, shows Bop\'s strategy for completing the task..**'
    d3 += '\n─────────────\n'
    d3 += '**Args: ** __dogs/gauntlet/baths/calus__\n'
    d3 += '*Argument is either dogs, bathes, gauntlet or calus.*'
    d3 += '\n─────────────\n'
    d3 += '**EXAMPLE COMMAND:**\n.leviathan gauntlet\n\n\n'

    d4 = '** Given argument, shows a guide/tips for the task'
    d4 += '\n─────────────\n'
    d4 += '**Args: ** __currently suported arguments below:__\n'
    d4 += '*Whisper of the Worm\n'
    d4 += '\n─────────────\n'
    d4 += '**EXAMPLE COMMAND:**\n.guides whisper of the worm\n\n\n'
    return desc, d1, d2, d3, d4


def Help_Other():
    desc = 'Basic guide to Other commands.\n'
    
    o1 = '**Given user argument, sends a gif of our Founder\'s (AeonsVerita) '
    o1 += 'dancing Titan along with a random message, congratulating the user.**'
    o1 += '\n─────────────\n'
    o1 += '**Args: ** @<__user__>\n'
    o1 += '*Argument is a mention of a user. As long as user is second item in '
    o1 += ' message, command can say anything!*'
    o1 += '\n─────────────\n'
    o1 += '**EXAMPLE COMMAND:**\n.congrats @Bop for creating me, the Bot!!!\n\n\n'
    
    o2 = '**Command creates a poll given a question and the corresponding options. '
    o2 += 'Each poll includes a "poll id" to be used with .tally to get results.**'
    o2 += '\n─────────────\n'
    o2 += '**Args: ** "<__question__>" "<__option1__>" "<__option2__>" "<*options*>"\n'
    o2 += '*All arguments (question and options) must be in quotations and space. '
    o2 += 'seperated. Additionally, a minimum of **2** options must be included, with a '
    o2 += 'max of **10**.*'
    o2 += '\n─────────────\n'
    o2 += '**EXAMPLE COMMAND:**\n.poll "Do you like the EAAA bot?" "yes" "no" "maybe so"\n\n\n'
    
    
    o3 = '**Command tally\'s up the poll results from the .poll command,  and '
    o3 += 'presents them to the user.**'
    o3 += '\n─────────────\n'
    o3 += '**Args: ** "<__poll ID__>\n'
    o3 += '* poll ID is a valid identification number associated with a poll given '
    o3 += 'by the **.poll** command described above.*'
    o3 += '\n─────────────\n'
    o3 += '**EXAMPLE COMMAND:**\n.tally 407192647313391617'
    return desc, o1, o2, o3



def Help_Admin():
    desc = '**Note:** These commands require **level 4 permissions or higher**, '
    desc += 'meaning user must be an Admin of this server.'

    roster = '**.roster __file__**\n'
    roster += '*Send the current roster file to admin-chat*\n'
    roster += '**.roster remove <__user__>**\n'
    roster += '*Command removes all information for given user from the roster.*\n'
    roster += '**.roster update <__user__>/all**\n'
    roster += '*Command updates given user\'s status in the roster if username '
    roster += 'is given, or updates all users if "all" is given*.\n'
    
    radmin = '**.rosteradmin add @<__user__> <*tz*> <*tpref*> <*class*> <*bday*>**\n'
    radmin += '*Command adds given user and info to roster.*\n'
    radmin += '**.rosteradmin gt @<__user__> <__gamertag__>**\n'
    radmin += '*Command adds given users gamertag to roster.*\n'
    radmin += '**.rosteradmin count**\n'
    radmin += '*Returns clan count, including those not on discord.*\n'
    
    announce = '**.reset**\n'
    announce += '*Command prompts the bot to send you a private message, where '
    announce += 'you must input/answer a number of questions for setting up the '
    announce += 'weekly-reset embed.*\n'
    announce += '**.clanreward <__reward type__>**\n'
    announce += '*Sends an announcement to all members that the given reward type '
    announce += '(crucible, raid, trials, or nightfall) is now available.*\n'
    announce += '**.announce**\n'
    announce += '*Command sends the weekly announcement image to the announcements '
    announce += 'channel. Remember to do this every Tuesday!*\n'
    
    reg = '**.registration begin**\n'
    reg += '*Guides a new user through the registration process, checking that '
    reg += 'all required information is inputted/added before upgrading new members '
    reg += 'role to beginner.*'
    
    other = '**.clear <__number__>**\n'
    other += '*Delete specified number of mesages from a channel.*\n'
    other += '**.ascended __<username>__**\n'
    other += '*Begins the process of Ascended role nomination. A pm will be '
    other += 'sent to Admin callee with directions upon command call.*\n'
    other += '**.activity __<n>__ weeks**\n'
    other += '*returns a list of user inactive in the last n weeks.*\n'
    other += '**.channelid**\n'
    other += '*returns the current channels id.*\n'
    other += '**.EAAA settings**\n'
    other += '*returns a display of the bots command settings.*\n'
    other += '**.EAAA <__cmd category__>/__all__  __on__/__off__**\n'
    other += '*if category given, turns that command on or off. If all given, '
    other += 'turns all commands on or off.*\n'
    return desc, roster, radmin, announce, reg, other




'''
ASCENDED FUNCTIONS ~~~~~~
'''


def Ascended_Check(phase, arg1, emoj):
    msg = ''
    if phase == 1:
        msg += 'Hello,\n You have nominated ' + arg1 + ' for the role of **Ascended**.\n'
        msg += 'The role has certain requirements, some of which we can confirm.'
        msg += 'We will first perform a check on said requirements, but for the rest '
        msg +=  'we will need **you** to confirm. '
        msg += 'Please confirm that the user has fullfilled all the following '
        msg += 'requirements for said role:\n\n'
        msg += '**- The user has participated in at least 1 Guided Role.** <`waiting...`>\n'
        msg += '**- User has been with the clan a minimum of 1 month.** <`waiting...`>\n'
        msg += '**- The user is very active on discord weekly.** <`waiting...`>\n'
        msg += '**- The user plays weekly on average with clan members.** \n'
        msg += '**-** User frequently goes out of there way to help other clan members.\n'
        msg += '**-** User is responsible for members first completions.\n'
        msg += '**-** User is calm and collected during drawn out activities.\n'

    if phase == 2:
        msg += 'Hello,\n You have nominated ' + arg1 + ' for the role of **Ascended**.\n'
        msg += 'The role has certain requirements, some of which we can confirm.'
        msg += 'We will first perform a check on said requirements, but for the rest '
        msg +=  'we will need **you** to confirm. '
        msg += 'Please confirm that the user has fullfilled all the following '
        msg += 'requirements for said role:\n\n'
        msg += '**- The user has participated in at least 1 Guided Role.** <'+emoj+'>\n'
        msg += '**- User has been with the clan a minimum of 1 month.** <`waiting...`>\n'
        msg += '**- The user is very active on discord weekly.** <`waiting...`>\n'
        msg += '**- The user plays weekly on average with clan members.** \n'
        msg += '**-** User frequently goes out of there way to help other clan members.\n'
        msg += '**-** User is responsible for members first completions.\n'
        msg += '**-** User is calm and collected during drawn out activities.\n'

    if phase == 3:
        msg += 'Hello,\n You have nominated ' + arg1 + ' for the role of **Ascended**.\n'
        msg += 'The role has certain requirements, some of which we can confirm.'
        msg += 'We will first perform a check on said requirements, but for the rest '
        msg +=  'we will need **you** to confirm. '
        msg += 'Please confirm that the user has fullfilled all the following '
        msg += 'requirements for said role:\n\n'
        msg += '**- The user has participated in at least 1 Guided Role.** <:white_check_mark:>\n'
        msg += '**- User has been with the clan a minimum of 1 month.** <'+emoj+'>\n'
        msg += '**- The user is very active on discord weekly.** <`waiting...`>\n'
        msg += '**- The user plays weekly on average with clan members.** \n'
        msg += '**-** User frequently goes out of there way to help other clan members.\n'
        msg += '**-** User is responsible for members first completions.\n'
        msg += '**-** User is calm and collected during drawn out activities.\n'
        
        
    if phase == 4:
        msg += 'Hello,\n You have nominated ' + arg1 + ' for the role of **Ascended**.\n'
        msg += 'The role has certain requirements, some of which we can confirm.'
        msg += 'We will first perform a check on said requirements, but for the rest '
        msg +=  'we will need **you** to confirm. '
        msg += 'Please confirm that the user has fullfilled all the following '
        msg += 'requirements for said role:\n\n'
        msg += '**- The user has participated in at least 1 Guided Role.** <:white_check_mark:>\n'
        msg += '**- User has been with the clan a minimum of 1 month.** <:white_check_mark:>\n'
        msg += '**- The user is very active on discord weekly.** <'+emoj+'>\n'
        msg += '**- The user plays weekly on average with clan members.** \n'
        msg += '**-** User frequently goes out of there way to help other clan members.\n'
        msg += '**-** User is responsible for members first completions.\n'
        msg += '**-** User is calm and collected during drawn out activities.\n\n'
    
    
    
    
    
    return msg






# Function checks if user joined by
# the given number of days since today.
def User_Joined_By(memb, numdays):
    target = datetime.datetime.today() - datetime.timedelta(days=numdays)
    roster = pd.read_csv('./utils/roster.csv', dtype=object)
    try:
        idx = roster[roster['username'] == get(memb.name)].index.item()
    except:
        return False

    join = str(roster.at[idx,'date']) + '\n'
    if str(join) == 'Season 1\n':
        return True

    isValidDate = True
    joinDate = datetime.datetime(2018,1,1)
    try :
        month,day,year = str(join).split('/')
        joinDate = datetime.datetime(int(year),int(month),int(day))
    except ValueError:
        try:
            year,month,day = str(join).split('-')
            joinDate = datetime.datetime(int(year),int(month),int(day))
        except ValueError:
            isValidDate = False

    if joinDate <= target:
        return True

    return False




def Unique_Identifier():
    s = ''
    i = 0;
    while i < 10:
        if i == 0:
            s += str(randint(1, 9))
        else:
            s += str(randint(0, 9))
        i += 1
    return s



# Function adds members class(es)
# and is a helper to Add_To_Roster
def Add_Ascended_Code(memb):
    roster = pd.read_csv('./utils/roster.csv', dtype=object)
    idx = roster[roster['username'] == get(memb.name)].index.item()
    roster.at[idx,'ascended'] = Unique_Identifier()
    roster = sortRoster(roster)
    roster.to_csv('./utils/roster.csv', index=False)



# Function adds members class(es)
# and is a helper to Add_To_Roster
def Get_Ascended_Code(memb):
    roster = pd.read_csv('./utils/roster.csv', dtype=object)
    idx = roster[roster['username'] == get(memb.name)].index.item()
    return roster.at[idx,'ascended']


def Ascended_Message(memb):
    Add_Ascended_Code(memb)
    msg = '\n**Congratulations '+memb.name+'**\n\n'
    msg += 'The Ex Aspera Ad Astra Founder and Admins have nominated you for '
    msg += 'the role of **Ascended**. Ascended is the highest obtainable role '
    msg += 'in the clan for members, and as such is given out to those members '
    msg += 'who meet specific criteria above and beyond the average clan member.\n\n'
    msg += 'As a nominee, your actions in the clan have shown you to have leadership '
    msg += 'capabilities and dedication to being apart of this clan, as show through your '
    msg += 'actions both in-game and on this discord server.\n\n'
    msg += 'Before you accept this nomination, you should be aware of a few things:\n\n'
    msg += '**-** Ascended recieve an additional channel visible to them and admins only. '
    msg += 'This is a place to speak with other Ascended, and share ideas you might have '
    msg += 'with the Admins about how to improve our clan overall. As an Ascended, '
    msg += 'the Admins promise to take your recommendations and ideas seriously.\n\n'
    msg += '**-** The role is meant to be one of leadership, and therefore some '
    msg += 'responsibility on helping our members both new and old. Admins will look'
    msg += 'to you to be an example and representative of the clan.'
    msg += '**-** Unlike the member role, this role can be taken away if criteria '
    msg += 'is no longer met. This is nothing personal, but you earned this nomination '
    msg += 'based on fitting specific criteria - that criteria must be maintained by '
    msg += 'you to keep the role.'
    msg += '\n\n**To accept** this nomination, simply reply to this message at your '
    msg += 'convenience with: \n***I accept '+str(Get_Ascended_Code(memb))+'***.\n\n'
    msg += '**Again, Congratulations!**\n\nEx Aspera Ad Astra Admin,\n'
    return msg


# function retrieves the main EAAA server role for the given
# member and awards that to that member on one of the EAAA
# sub-servers.
def Get_EAAA_Role(memb):
    roster = pd.read_csv('./utils/roster.csv', dtype=object)

    idx = roster[roster['id'] == memb.id].index.item()
    return roster.at[idx,'status']
#return 'error'









