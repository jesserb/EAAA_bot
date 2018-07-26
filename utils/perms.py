import json  # for json parsing

# Open the json file with the role settings and pars it with JSON.
f = open("settings.json")
settings = json.load(f)
f.close()

# Save json properties into variables for better handling.
lvl1 = settings["perms"]["lvl1"]
lvl2 = settings["perms"]["lvl2"]
lvl3 = settings["perms"]["lvl3"]
lvl4 = settings["perms"]["lvl4"]
lvl5 = settings["perms"]["lvl5"]
lvl6 = settings["perms"]["lvl6"]

def Get_Role(memb):
    lvl = [0]
    # Tests if the role in roles is existent in one of the role name arrays
    for r in memb.roles:
        if r.name in lvl6:
            lvl.append(6)
        if r.name in lvl5:
            lvl.append(5)
        if r.name in lvl4:
            lvl.append(4)
        if r.name in lvl3:
            lvl.append(3)
        elif r.name in lvl2:
            lvl.append(2)
        elif r.name in lvl1:
            lvl.append(1)
    # Returns the maximum level
    return max(lvl)

# Checks in the max role level is bigger than the required level
def check(memb, lvl):
    return Get_Role(memb) >= lvl
