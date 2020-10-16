# OBJECTIVE:
# make a turn based game where you have manage a castle
# every turn you get some resources (gold,food,manpower)
# you get decision that influence the game
# you can shop some stuff like mercenary and start building projects
# you win by getting the castle to a certain pop
# you can save the game and load a save


class Resources:

    def __init__(self, food, gold, manpower):
        self.food = food
        self.gold = gold
        self.manpower = manpower

    def Show(self):
        finalString = ""
        if self.food != 0: finalString += f"{self.food}f "
        if self.gold != 0: finalString += f"{self.gold}g "
        if self.manpower != 0: finalString += f"{self.manpower}m "
        return finalString

    def __gt__(self, other):
        return self.food > other.food and \
               self.gold > other.gold and \
               self.manpower > other.manpower

    def __ge__(self, other):
        return self.food >= other.food and \
               self.gold >= other.gold and \
               self.manpower >= other.manpower

    def __lt__(self, other):
        return self.food < other.food and \
               self.gold < other.gold and \
               self.manpower < other.manpower

    def __le__(self, other):
        return self.food <= other.food and \
               self.gold <= other.gold and \
               self.manpower <= other.manpower

    def __eq__(self, other):
        return self.food == other.food and \
               self.gold == other.gold and \
               self.manpower == other.manpower

    def __neg__(self):
        food = -self.food
        gold = -self.gold
        manpower = -self.manpower
        return Resources(food, gold, manpower)

    def __add__(self, other):
        food = self.food + other.food
        gold = self.gold + other.gold
        manpower = self.manpower + other.manpower
        return Resources(food, gold, manpower)

    def __sub__(self, other):
        food = self.food - other.food
        gold = self.gold - other.gold
        manpower = self.manpower - other.manpower
        return Resources(food, gold, manpower)


# pop = 100
# pop += prd.food * 0.6 * (aspettativa_di_vita) * min((capacita / pop),2)


# UPGRADES:
# farm (1 - 5)     keep (1 - 3)       workshop (1 - 3)   stable (1)
# houses (1 - 5)   market (1 - 3)     port (1 - 2)       hospital (1)

# limited number of upgrades, can be increased through acquiring new territories

class Upgrade:

    def __init__(self, name: str, level: int, base_cost: Resources, production: Resources, construction_time: int):
        self.name = name
        self.level = level
        self.base_cost = base_cost
        self.production = production
        self.construction_time = construction_time

    def Print(self):
        print(self.name, "\tlvl:", self.level, "\tcost:", self.base_cost.Show(), "\tprod:", self.production.Show(),
              "\tturns:", self.construction_time)

    def OnEnable(self, castle):
        pass

    def OnDisable(self, castle):
        pass


class Farm(Upgrade):
    def __init__(self, level, base_cost, production, construction_time):
        super().__init__("farm", level, base_cost, production, construction_time)

    def ShowArt(self):
        print(f"\t\t\t[ {self.name} ]")
        print(r"""
                                        __
                 ,-_                  (`  ).
                 |-_'-,              (     ).
                 |-_'-'           _(        '`.
        _        |-_'/        .=(`(      .     )
       /;-,_     |-_'        (     (.__.:-`-_.'
      /-.-;,-,___|'          `(       ) )
     /;-;-;-;_;_/|\_ _ _ _ _   ` __.:'   )
        x_( __`|_P_|`-;-;-;,|        `--'
        |\ \    _||   `-;-;-'
        | \`   -_|.      '-'
        | /   /-_| `
        |/   ,'-_|  \
        /____|'-_|___\
 _..,____]__|_\-_'|_[___,.._
'                          ``'--,..,.             
        """)


class Houses(Upgrade):
    def __init__(self, level, base_cost, production, construction_time, added_capacity):
        super().__init__("houses", level, base_cost, production, construction_time)
        self.added_capacity = added_capacity

    def OnEnable(self, castle):
        print(castle.capacity, end=" ")
        castle.capacity += self.added_capacity
        print(f" + {self.added_capacity} = {castle.capacity} (capacity)")

    def OnDisable(self, castle):
        castle.capacity -= self.added_capacity

    def ShowArt(self):
        print(f"\t\t\t[ {self.name} ]")
        print(r"""
        ~         ~~          __
       _T      .,,.    ~--~ ^^
 ^^   // \                    ~
      ][O]    ^^      ,-~ ~
   /''-I_I         _II____
__/_  /   \ ______/ ''   /'\_,__
  | II--'''' \,--:--..,_/,.-{ },
; '/__\,.--';|   |[] .-.| O{ _ }
:' |  | []  -|   ''--:.;[,.'\,/
'  |[]|,.--'' '',   ''-,.    |
  ..    ..-''    ;       ''. '            
        """)


class Shop:
    all_upgrades = {
        "farm": [Farm(1, Resources(0, 100, 350), Resources(30, -5, 0), 1),
                 Farm(2, Resources(0, 150, 400), Resources(45, -10, 0), 2),
                 Farm(3, Resources(0, 230, 500), Resources(60, -17, 0), 3),
                 Farm(4, Resources(0, 300, 620), Resources(80, -25, 0), 4),
                 Farm(5, Resources(0, 400, 780), Resources(100, -38, 0), 6)],

        "houses": [Houses(1, Resources(100, 50, 0), Resources(0, 0, 50), 2, 250),
                   Houses(2, Resources(150, 100, 0), Resources(0, 0, 75), 3, 500),
                   Houses(3, Resources(220, 150, 0), Resources(0, 0, 100), 4, 800),
                   Houses(4, Resources(300, 200, 0), Resources(0, 0, 125), 5, 1250),
                   Houses(5, Resources(400, 300, 0), Resources(0, 0, 150), 6, 1750)],

    }

    categories = all_upgrades.keys()

    @classmethod
    def ShowPossibleUpgrades(cls, builtUpgrades):
        for category in Shop.categories:

            currentUpgradeLevel = builtUpgrades[category]
            if currentUpgradeLevel >= len(cls.all_upgrades[category]):
                print("All " + category + " upgrades have been built")
                continue

            upgrade = cls.all_upgrades[category][builtUpgrades[category]]
            upgrade.Print()

    @classmethod
    def ShowAllUpgrades(cls):
        for category in cls.categories:
            print(category, end=":\n")
            for upgrade in cls.all_upgrades[category]:
                upgrade.Print()


class Castle:

    def __init__(self, name: str, base_resources: Resources, production: Resources, base_population: int,
                 base_capacity: int, base_growth_rate: float):

        self.name = name

        self.resources = base_resources
        self.base_production = production
        self.population = base_population
        self.capacity = base_capacity
        self.pop_growth_rate = base_growth_rate

        self.built_upgrades = dict.fromkeys(Shop.categories, 0)
        self.upgrades_in_construction = dict.fromkeys(Shop.categories, 0)

    def BuyUpgrade(self, category: str):
        if (category not in Shop.categories):
            print("Invalid category")
            return

        if (self.upgrades_in_construction[category] > 0):
            print(f"Already building an Upgrade, in category: {category}")
            return

        currentLVL = self.built_upgrades[category]
        if len(Shop.all_upgrades[category]) <= currentLVL:
            print(f"Already built to the max level, in category: {category}")
            return
        upgrade = Shop.all_upgrades[category][currentLVL]

        if (self.resources >= upgrade.base_cost):
            print(f"Started construction for {category} lvl: {currentLVL + 1}")

            self.resources -= upgrade.base_cost

            self.ShowResources2()
            self.upgrades_in_construction[category] = upgrade.construction_time
            print(f"it will take {upgrade.construction_time} turns to finish")
        else:
            print(f"{self.name} doesn't have enough resources ({category})")

    def GetProduction(self):
        bp = self.base_production
        totalProduction = Resources(bp.food, bp.gold, bp.manpower)

        for category in Shop.categories:
            upgradeLevel = self.built_upgrades[category]
            if upgradeLevel == 0:
                continue

            totalProduction += Shop.all_upgrades[category][upgradeLevel - 1].production

        totalProduction.food -= self.population // 20  # persone sfamate con 1 food
        totalProduction.gold += self.population // 40  # persone che in totale pagano 1g di tasse
        return totalProduction

    def GetPopulationGrowth(self):
        food_prod = self.GetProduction().food
        growth = self.pop_growth_rate + food_prod * (1.0 if food_prod > 0 else -2.0)
        growth *= self.population / 100


        if growth + self.population > self.capacity:
            growth -= ((growth + self.population) - self.capacity) * 0.666

        return int(growth)

    def Construct(self):
        for category in Shop.categories:
            turnsToFinish = self.upgrades_in_construction[category]
            if turnsToFinish > 0:
                self.upgrades_in_construction[category] -= 1
                if self.upgrades_in_construction[category] == 0:
                    self.built_upgrades[category] += 1
                    lvl = self.built_upgrades[category]

                    if lvl > 1: Shop.all_upgrades[category][lvl - 2].OnDisable(self)
                    Shop.all_upgrades[category][lvl - 1].OnEnable(self)
                    print(
                        f"!! {category} lvl: {lvl} has finished construction after {Shop.all_upgrades[category][lvl - 1].construction_time} !!")
                    Shop.all_upgrades[category][lvl - 1].ShowArt()

    def ShowResources(self):
        print(f"reserves:   [ {self.resources.Show()}]")
        print(f"production: [ {self.GetProduction().Show()}] per turn")

    def ShowPop(self):
        growth = self.GetPopulationGrowth()
        print(f"[population: {self.population} \t({'+' if growth > 0 else ''}{growth}) \t]")

    def ShowResources2(self):
        prod = self.GetProduction()
        print(f"[      food: {self.resources.food} \t({'+' if prod.food > 0 else ''}{prod.food}) \t]")
        print(f"[      gold: {self.resources.gold} \t({'+' if prod.gold > 0 else ''}{prod.gold}) \t]")
        print(f"[  manpower: {self.resources.manpower} \t({'+' if prod.manpower > 0 else ''}{prod.manpower}) \t]")

    def ShowUpgrades(self):
        for category in Shop.categories:
            upgradeLevel = self.built_upgrades[category]
            if upgradeLevel != 0:
                upgrade = Shop.all_upgrades[category][upgradeLevel - 1]
                upgrade.Print()

    def ShowConstruction(self):
        for category in Shop.categories:
            turnsToFinish = self.upgrades_in_construction[category]
            if turnsToFinish > 0:
                upgrade = Shop.all_upgrades[category][self.built_upgrades[category]]

                print(f"[{turnsToFinish}/{upgrade.construction_time}] turns left. ", end="")

                upgrade.Print()

    def ShowArt(self):
        print(f"\t\t\t[ {self.name} ]")
        print(r"""
                                  |>>>
                                  |
                    |>>>      _  _|_  _         |>>>
                    |        |;| |;| |;|        |
                _  _|_  _    \\.    .  /    _  _|_  _
               |;|_|;|_|;|    \\:. ,  /    |;|_|;|_|;|
               \\..      /    ||;   . |    \\.    .  /
                \\.  ,  /     ||:  .  |     \\:  .  /
                 ||:   |_   _ ||_ . _ | _   _||:   |
                 ||:  .|||_|;|_|;|_|;|_|;|_|;||:.  |
                 ||:   ||.    .     .      . ||:  .|
                 ||: . || .     . .   .  ,   ||:   |       \,/
                 ||:   ||:  ,  _______   .   ||: , |            /`\
                 ||:   || .   /+++++++\    . ||:   |
                 ||:   ||.    |+++++++| .    ||: . |
              __ ||: . ||: ,  |+++++++|.  . _||_   |
     ____--`~    '--~~__|.    |+++++__|----~    ~`---,              ___
-~--~                   ~---__|,--~'                  ~~----_____-~'   `~----~~""")


class Settings:
    create_save_on_new_game = False
    auto_save_every = 3  # 0 means no autosaves,
    ask_for_save_name = False
    show_help_text = True
    auto_load_last_save_on_startup = False
    saves_dir = "saves/"
    commands_per_page = 9
    has_shown_tutorial = False

    # difficulty settings
    starting_resources = Resources(400, 400, 250)
    starting_production = Resources(50, 30, 25)
    starting_population = 100
    starting_capacity = 500
    starting_growth_rate = 0.45

    @classmethod
    def Save(cls):
        with open("settings.txt", "w") as saveFile:
            saveFile.write(
                f"\n# when the game start do you want to save? (True or False)\n"
                f"create_save_on_new_game {cls.create_save_on_new_game}\n"
                f"\n# how many turns in between saves? (0 = no autosaves) (number) \n"
                f"auto_save_every {cls.auto_save_every}\n"
                f"\n# do you want to specify the save name? (True or False)\n"
                f"ask_for_save_name {cls.ask_for_save_name}\n"
                f"\n# show helping text (recommended) (True or False)\n"
                f"show_help_text {cls.show_help_text}\n"
                f"\n# when starting the game do you want to \n"
                f"# resume where you left off automatically (True or False)\n"
                f"auto_load_last_save_on_startup {cls.auto_load_last_save_on_startup}\n"
                f"\n# the folder where the saves will be stored ( dirName/ )\n"
                f"saves_dir {cls.saves_dir}\n"
                f"\n# number of commands shown per page when using 'help' or '?' (number)\n"
                f"commands_per_page {cls.commands_per_page}\n"
                f"\n# False = show tutorial next time you open the game\n"
                f"# True = don't show the tutorial\n"
                f"has_shown_tutorial {cls.has_shown_tutorial}\n"
                f"\n# resources when starting a new game (number x3)\n"
                f"starting_resources {cls.starting_resources.food} {cls.starting_resources.gold} {cls.starting_resources.manpower}\n"
                f"\n# production when starting a new game (number x3)\n"
                f"starting_production {cls.starting_production.food} {cls.starting_production.gold} {cls.starting_production.manpower}\n"
                f"\n# population when starting a new game (number)\n"
                f"starting_population {cls.starting_population}\n"
                f"\n# soft population limit when starting a new game (number)\n"
                f"starting_capacity {cls.starting_capacity}\n"
                f"\n# modifier in the growth of population when starting a new game\n"
                f"(small number es: 0.2 )\n"
                f"starting_growth_rate {cls.starting_growth_rate}\n"
            )

    @classmethod
    def Load(cls):
        full_save_name = "settings.txt"
        if os.path.exists(full_save_name):
            with open(full_save_name, "r") as saveFile:
                for line in saveFile.readlines():
                    information = line.split()
                    if len(information) < 2:
                        continue
                    key = information[0]
                    value = information[1]

                    from distutils.util import strtobool

                    if key in ["#", "//"]:  # to make comments
                        pass
                    if key == "create_save_on_new_game":
                        cls.create_save_on_new_game = bool(strtobool(value))
                    elif key == "auto_save_every":
                        cls.auto_save_every = int(value)
                    elif key == "ask_for_save_name":
                        cls.ask_for_save_name = bool(strtobool(value))
                    elif key == "show_help_text":
                        cls.show_help_text = bool(strtobool(value))
                    elif key == "auto_load_last_save_on_startup":
                        cls.auto_load_last_save_on_startup = bool(strtobool(value))
                    elif key == "saves_dir":
                        cls.saves_dir = str(value)
                    elif key == "commands_per_page":
                        cls.commands_per_page = int(value)
                    elif key == "has_shown_tutorial":
                        cls.has_shown_tutorial = bool(strtobool(value))
                    elif key == "starting_resources":
                        key, f, g, m = information
                        cls.starting_resources = Resources(int(f), int(g), int(m))
                    elif key == "starting_production":
                        key, f, g, m = information
                        cls.starting_production = Resources(int(f), int(g), int(m))
                    elif key == "starting_population":
                        cls.starting_population = int(value)
                    elif key == "starting_capacity":
                        cls.starting_capacity = int(value)
                    elif key == "starting_growth_rate":
                        cls.starting_growth_rate = float(value)


class Utils:
    def FormatSaveName(savename: str) -> str:
        return savename[len(Settings.saves_dir):len(savename) - 4].replace(' ', '_')  # len(".txt") : 4


class Game:
    is_quitting = False
    commands_help = {
        "help": "shows you all the commands and how to use them\nyou can also use '?'",
        "?": "same as 'help'",
        "tutorial": "shows you a brief guide on how to play",
        "end": "ends turn\nsame as: 'e', 'next', 'n'",
        "next": "ends turn\nsame as: 'end', 'e', 'n'",
        "e": "ends turn\nsame as: 'end', 'next', 'n'",
        "n": "ends turn\nsame as: 'end', 'e', 'next'",
        "quit": "exits the game, asks you if you want to save",
        "shop": "opens the shop where you can get upgrades",
        "build": "allows you start constructing an upgrade\nquick form: 'build UPGRADE_NAME'",
        "resources": "shows current resources and production",
        "upgrades": "shows built upgrades and their effects",
        "construction": "shows all upgrades in construction and how many turns are left",
        "settings": "'settings load' to load from settings.txt file\n"
                    "'settings save' to write the changes into settings.txt\n"
                    "you can change settings inside the file 'settings.txt', in the same folder as this game",
        "save": "saves the game\nquick form: 'save SAVE_NAME'",
        "load": "loads the save file\nquick form: 'load SAVE_NAME'",
        "menu": "brings you back to the menu"
    }
    commands = commands_help.keys()

    tutorial_pages = [
        # TODO come up with a name
        "[1/7]\nWelcome to GAME_NAME"
        "\nIn this turn based game you are the king of a castle and its territories"
        "\nYour objective is to manage this castle so that your resources never run out",
        "[2/7]\nTo do so you'll have to keep building and improving your structures"
        "\nyou can do this by entering the build command and then the Structure category that you want to upgrade/build",
        "[3/7]\nOnce you're happy with what you've done this turn, you can end the turn with the 'end' command (there are many)"
        "\nAfter every turn you gain(or lose) a certain amount of resources",
        "[4/7]\nWhat are resources?"
        "\nThey are FOOD (f), GOLD (g) and MANPOWER (m)"
        "\nFOOD is used to feed people and building"
        "\nGOLD is used to pay for upgrades, mercenaries, and such"
        "\nMANPOWER is used for warfare",
        "[5/7]\nBuildings are very useful!"
        "\nThey have a one time cost and a Turn based production, you can always see buildings stats"
        "\nAt the start you won't have any buildings, but if you go into the shop you'll see all the possible buildings"
        "\nOnce started building something it will take some turns to finish (check out 'construction')"
        "\nOnce finished you'll be able to see all your castle buildings using 'upgrades' command",
        "[6/7]\nEvents",
        "[7/7]\nfor additional help use 'help' or '?'"
    ]

    def __init__(self):

        self.turns_to_autosave = (0 if Settings.create_save_on_new_game else Settings.auto_save_every)
        self.game_state = "normal"
        self.turn = 1
        # self.hasLoan = False
        Settings.starting_production.Show()
        Settings.starting_production.Show()
        self.castle = Castle("missing name", Settings.starting_resources, Settings.starting_production,
                             Settings.starting_population, Settings.starting_capacity, Settings.starting_growth_rate)

    def Start(self):
        print(r"""welcome back to...
  ____            _             ____        _ _     _           
 |  _ \ ___  __ _| |_ __ ___   | __ ) _   _(_) | __| | ___ _ __ 
 | |_) / _ \/ _` | | '_ ` _ \  |  _ \| | | | | |/ _` |/ _ \ '__|
 |  _ <  __/ (_| | | | | | | | | |_) | |_| | | | (_| |  __/ |   
 |_| \_\___|\__,_|_|_| |_| |_| |____/ \__,_|_|_|\__,_|\___|_|   
 """)

        self.castle.ShowArt()

        if Settings.has_shown_tutorial == False:
            self.Tutorial()
            Settings.has_shown_tutorial = True
            Settings.Save()

        if Settings.show_help_text: print("(?) if you are unsure on what to do, enter 'help' or '?'")

    def GameLoop(self):
        while self.game_state not in ["won", "over"] or Game.is_quitting:

            print(f"<[ TURN {self.turn} IN {self.castle.name.upper()} ]>\n")

            self.castle.ShowPop()
            self.castle.ShowResources2()

            if Settings.auto_save_every > 0:
                if self.turns_to_autosave <= 0:
                    self.turns_to_autosave = Settings.auto_save_every
                    self.Save(f"{self.castle.name.replace(' ', '_')}_{self.turn}_auto")

            while True:
                full_command = self.GetCommand()
                command = full_command[0]

                if command == "help" or command == "?":
                    self.Help()

                elif command == "tutorial":
                    self.Tutorial()

                elif command in ["end", "next", "e", "n"]:
                    self.EndTurn()
                    break

                elif command == "quit":
                    cmd = input("do you want to save before quitting? [yes | no | cancel]\n>").lower()
                    if (cmd in ["yes", "save"]):
                        self.Save()
                        Game.is_quitting = True
                        return
                    elif (cmd == "cancel"):
                        print("happy to hear that you're not leaving ")
                    else:
                        Game.is_quitting = True
                        return

                elif command == "shop":
                    Shop.ShowPossibleUpgrades(self.castle.built_upgrades)
                    self.castle.ShowResources2()
                    if Settings.show_help_text: print("(?) to construct an upgrade use the 'build' command")

                elif command == "build":
                    if len(full_command) > 1:
                        self.Build(full_command[1])
                    else:
                        self.Build()

                elif command == "resources":
                    self.castle.ShowResources2()

                elif command == "upgrades":
                    self.castle.ShowUpgrades()

                elif command == "construction":
                    self.castle.ShowConstruction()

                elif command == "settings":
                    if full_command[1] == "save":
                        Settings.Save()
                        print("settings have been saved")
                    elif full_command[1] == "load":
                        Settings.Load()
                        print("settings have been loaded")
                    else:
                        print("no command associated")

                elif command == "save":

                    if len(full_command) > 1:
                        self.Save("_".join(full_command[1:]))
                    else:
                        self.Save()

                elif command == "load":
                    if len(full_command) > 1:
                        self.Load(full_command[1])
                    else:
                        self.Load()
                    break

                elif command == "menu":
                    cmd = input("do you want to save before going to the menu? [yes | no | cancel]\n>").lower()
                    if (cmd in ["yes", "save"]):
                        self.Save()
                        return
                    elif (cmd == "cancel"):
                        print("got it!")
                    else:
                        return

                else:
                    print("you shouldn't see this message, if you do something went wrong")

    def GetCommand(self):
        while True:
            full_command = input(">").lower().split()

            if (len(full_command) > 0 and full_command[0] in Game.commands):
                return full_command
            else:
                print("Invalid Command, enter help if you don't know what to do")

    @classmethod
    def Help(cls):

        from math import ceil
        pages = ceil(len(cls.commands) / Settings.commands_per_page)

        i = 0
        for command in cls.commands:
            if i % Settings.commands_per_page == 0:
                print(f"[page {i // Settings.commands_per_page + 1}/{pages}]")

            print("[", command, "]")
            for line in cls.commands_help[command].split("\n"):
                print("\t| " + line)
            print()

            i += 1
            if i % Settings.commands_per_page == 0:
                input("waiting for input ...")

    def EndTurn(self):
        self.turn += 1
        self.castle.resources += self.castle.GetProduction()
        self.castle.population += self.castle.GetPopulationGrowth()

        self.castle.Construct()

        self.UpdateGameState()

        if Settings.auto_save_every > 0:
            self.turns_to_autosave -= 1

    def Save(self, save_name: str = ""):
        if (save_name != "" and save_name != None):
            if (len(save_name) > 0):
                if Settings.saves_dir in save_name and ".txt" in save_name:
                    full_save_name = save_name
                else:
                    full_save_name = Settings.saves_dir + save_name + ".txt"

                import os
                if not os.path.exists(Settings.saves_dir):
                    os.mkdir(Settings.saves_dir)

                save_file = open(full_save_name, "w")

                from datetime import datetime
                # datetime object containing current date and time

                # dd/mm/YY H:M:S
                date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                save_file.write(f"# MODIFYING VALUES IN THIS FILE IS CONSIDERED CHEATING\n"
                                f"# saved on {date_time}\n"
                                f"turn {self.turn}\n"
                                f"name {self.castle.name}\n"
                                f"game_state {self.game_state}\n"
                                f"turns_to_autosave {self.turns_to_autosave}\n")
                for upgrade in self.castle.built_upgrades:
                    save_file.write(
                        f"upgrades {upgrade} {self.castle.built_upgrades[upgrade]} {self.castle.upgrades_in_construction[upgrade]}\n")

                save_file.write(
                    f"reserves {self.castle.resources.food} {self.castle.resources.gold} {self.castle.resources.manpower}\n"
                    f"production {self.castle.base_production.food} {self.castle.base_production.gold} {self.castle.base_production.manpower}\n"
                    f"population {self.castle.population}\n"
                    f"capacity {self.castle.capacity}\n"
                    f"pop_growth_rate {self.castle.pop_growth_rate}\n"
                )

                save_file.close()

                print("game saved...")

            else:
                print("save names can't be this short")

        else:
            if Settings.ask_for_save_name == True:
                self.Save(input("What should the save be called?\n>"))
            else:
                self.Save(f"{self.castle.name}_{self.turn}")

    def Load(self, save_name: str = ""):
        if (save_name != "" and save_name != None and len(save_name) > 0):
            if (save_name == "last"):
                save_files = glob.glob(Settings.saves_dir + "*.txt")
                if (len(save_files) > 0):
                    fullSaveName = max(save_files, key=os.path.getctime)
                else:
                    if Settings.saves_dir in save_name and ".txt" in save_name:
                        fullSaveName = save_name
                    else:
                        fullSaveName = Settings.saves_dir + save_name + ".txt"
            else:
                fullSaveName = Settings.saves_dir + save_name + ".txt"
            if os.path.exists(fullSaveName):

                saveFile = open(fullSaveName, "r")

                for line in saveFile.readlines():
                    information = line.split()
                    if (not len(information) > 1):
                        continue
                    key = information[0]
                    value = information[1]

                    if key == "turn":
                        self.turn = int(value)
                    elif key == "name" and len(line) > 5:
                        self.castle.name = line[5:].replace('\n', '')
                    elif key == "game_state" and len(line) > 11:
                        self.game_state = line[10:].replace('\n', '')
                    elif key == "turns_to_autosave":
                        self.turns_to_autosave = int(value)
                    elif key == "upgrades":
                        self.castle.built_upgrades[value] = int(information[2])  # upgrade lvl
                        self.castle.upgrades_in_construction[value] = int(information[3])  # turns until it's finished
                    elif key == "reserves":
                        key, food, gold, manpower = information
                        self.castle.resources = Resources(int(food), int(gold), int(manpower))
                    elif key == "production":
                        key, food, gold, manpower = information
                        self.castle.base_production = Resources(int(food), int(gold), int(manpower))
                    elif key == "population":
                        self.castle.population = int(value)
                    elif key == "capacity":
                        self.castle.capacity = int(value)
                    elif key == "pop_growth_rate":
                        self.castle.pop_growth_rate = float(value)

                saveFile.close()

                print("loading completed...")
                return self

            else:
                print("no such file: '" + Utils.FormatSaveName(fullSaveName) + "'")
        else:
            save_files = glob.glob(Settings.saves_dir + "*.txt")
            if (len(save_files) > 0):
                print("What save should be loaded?")
                for save in save_files: print(Utils.FormatSaveName(save), end=", ")
                latest_file = max(save_files, key=os.path.getctime)
                print("\nlast save:", Utils.FormatSaveName(latest_file))
                self.Load(input("\n>"))
            else:
                print("there are no save files")

    def Over(self):
        self.game_state = "over"

        print("""        
  ▄▀  ██   █▀▄▀█ ▄███▄       ████▄     ▄   ▄███▄   █▄▄▄▄ 
▄▀    █ █  █ █ █ █▀   ▀      █   █      █  █▀   ▀  █  ▄▀ 
█ ▀▄  █▄▄█ █ ▄ █ ██▄▄        █   █ █     █ ██▄▄    █▀▀▌  
█   █ █  █ █   █ █▄   ▄▀     ▀████  █    █ █▄   ▄▀ █  █  
 ███     █    █  ▀███▀               █  █  ▀███▀     █   
        █    ▀                        █▐            ▀    
       ▀                              ▐                  
""")

        if self.castle.population <= 0:
            print(f"Everyone in {self.castle.name} has died leaving nothing of the castle")  # todo make this more engaging

        if self.castle.resources.food < 0:
            print(
                f"After this year harvest it was clear that {self.castle.name} didn't have enough food for everyone.\n"
                f"So while the wealthy of {self.castle.name} eat until exploding, the plebs were starving to death.\n"
                f"This lead many to take arms with what they could find and start a rebellion.\n"
                f"After all the bloodshed, there was hardly something left of {self.castle.name}")

        if self.castle.resources.gold < 0:
            print(
                f"Having nothing left in the treasury, {self.castle.name}'s soldiers organized a military coup and overthrow your rule.\n"
                f"Under this other ruler, plebes would get taxed to death and executed for frivolous reasons.\n"
                f"So the great majority of people fled away from {self.castle.name}, who soon turned into an abandoned castle occupied by thief and looters")

        if self.castle.resources.manpower < 0:
            print(
                f"The manpower reserves in {self.castle.name} got so thin that it was no longer able to maintain order.\n"
                f"This caused {self.castle.name} to get sacked and burned to the ground by some looters.\n"
                f"Leaving death and smoke of what was once a Great castle")

        print(f"{self.castle.name} has survived for {self.turn} turns.\nBut in the end it all got destroyed")

        input("waiting for input... ")

    def Build(self, category: str = None):
        if category != None:
            if category in Shop.categories:
                self.castle.BuyUpgrade(category)
            else:
                print("invalid category!")
        else:
            for category in Shop.categories: print(category, end=", ")
            self.Build(input("\nenter the upgrade's category\n>"))

    def UpdateGameState(self):
        if not self.castle.resources > Resources(0, 0, 0) or self.castle.population <= 0:
            self.Over()

    def Tutorial(self):
        print("press enter to continue")
        print("or enter 'skip' to skip the tutorial\n")
        for page in Game.tutorial_pages:
            print(page)
            print()
            if input().lower() == "skip":
                return


if __name__ == '__main__':

    import glob
    import os

    if not os.path.exists(Settings.saves_dir):
        os.mkdir(Settings.saves_dir)
    if not os.path.isfile('settings.txt'):
        Settings.Save()

    Settings.Load()

    game = Game()
    use_menu = True
    is_startup = True

    while True:

        while use_menu == True:
            print(f"Settings.auto_load_last_save_on_startup = {Settings.auto_load_last_save_on_startup}")
            if (Settings.auto_load_last_save_on_startup and is_startup):
                is_startup = False
                cmd = "resume"
            else:
                print("MENU:")
                print("[resume]\n[new]\n[load]\n[quit]")
                cmd = ""
                while cmd not in ["new", "resume", "load", "quit"]:
                    cmd = input(">").lower()

            if cmd == "new":
                game = Game()
                game.castle.name = input("How shall your castle be called?\n>")
                use_menu = False

            elif cmd == "quit":
                Game.is_quitting = True
                use_menu = False

            else:
                saveFiles = glob.glob(Settings.saves_dir + "*.txt")
                if len(saveFiles) > 0:
                    if cmd == "resume":
                        latest_file = max(saveFiles, key=os.path.getctime)
                        game.Load(Utils.FormatSaveName(latest_file))
                    else:
                        game.Load()
                    if game.castle.name != "missing name":
                        use_menu = False

                else:
                    print("There are no saves\nstart a new game by entering 'new'")

        if Game.is_quitting == True:
            break

        game.Start()
        game.GameLoop()

        if Game.is_quitting == True:
            break
        use_menu = True
