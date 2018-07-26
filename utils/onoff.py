import json  # for json parsing



# check settings for command,
# returns an integer represented
# as a bool 0 or 1
def check(command, id):
    f = open("settings.json")
    settings = json.load(f)
    f.close()
    return settings[id]["commands"][command]



# Set the command settings, admin only
# command is a valid command category,
# vall is either on or off. returns bool
# to signify success or not.
def set(command, val):
    
    valid = False
    # TURN given COMMAND OFF
    if val.lower() == 'off':
        with open("settings.json", 'r') as f:
            settings = json.load(f)
            for k,v in settings["379449337119506433"]['commands'].items():
                if k == command.lower():
                    valid = True
                    settings["379449337119506433"]['commands'][command] = 0
                    break
        
        with open("settings.json", 'w') as f:
            f.write(json.dumps(settings, sort_keys=True, indent=4, separators=(',', ': ')))
        if valid:
            return True, ''
        else:
            return False, command

    # TURN given COMMAND ON
    if val.lower() == 'on':
        with open("settings.json", 'r') as f:
            settings = json.load(f)
            for k,v in settings["379449337119506433"]['commands'].items():
                if k == command.lower():
                    valid = True
                    settings["379449337119506433"]['commands'][command] = 1
                    break
        
        with open("settings.json", 'w') as f:
            f.write(json.dumps(settings, sort_keys=True, indent=4, separators=(',', ': ')))
        if valid:
            return True, ''
        else:
            return False, command
    return False, val



# Set the command settings, admin only
# command is a valid command category,
# vall is either on or off. returns bool
# to signify success or not.
def setAll(val):
    
    # Turn all commands OFF
    if val.lower() == 'off':
        with open("settings.json", 'r') as f:
            settings = json.load(f)
            for k,v in settings["379449337119506433"]['commands'].items():
                settings["379449337119506433"]['commands'][k] = 0
    
        with open("settings.json", 'w') as f:
            f.write(json.dumps(settings, sort_keys=True, indent=4, separators=(',', ': ')))
        return True
    
    # Turn all cmmands ON
    if val.lower() == 'on':
        with open("settings.json", 'r') as f:
            settings = json.load(f)
            for k,v in settings["379449337119506433"]['commands'].items():
                settings["379449337119506433"]['commands'][k] = 1
        
        with open("settings.json", 'w') as f:
            f.write(json.dumps(settings, sort_keys=True, indent=4, separators=(',', ': ')))
        return True

    return False



# accesses the command settings
# and returs a discriptive list
# of all current settings
def Get_Command_Settings():
    f = open("settings.json")
    settings = json.load(f)
    f.close()
    msg = ''
    for k,v in settings["379449337119506433"]['commands'].items():
        if v == 0:
            msg += '**×** `' +  str(k).ljust(20) + 'OFF`\n'
        else:
            msg += '**×** `' +  str(k).ljust(20) + 'ON`\n'
    return msg
