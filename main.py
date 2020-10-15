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


# UPGRADES:
# farm (1 - 5)     keep (1 - 3)       workshop (1 - 3)   stable (1)
# houses (1 - 5)   market (1 - 3)     port (1 - 2)       hospital (1)
class Upgrade:

    def __init__(self, name:str, level:int, baseCost:Resources, production:Resources, constructionTime:int):
        self.name = name
        self.level = level
        self.baseCost = baseCost
        self.production = production
        self.constructionTime = constructionTime

    def Print(self):
        print(self.name, "\tlvl:", self.level, "\tcost:", self.baseCost.Show(), "\tprod:", self.production.Show(),
              "\tturns:", self.constructionTime)


class Farm(Upgrade):
    def __init__(self, level, baseCost, production, constructionTime):
        super().__init__("farm", level, baseCost, production, constructionTime)

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
    def __init__(self, level, baseCost, production, constructionTime):
        super().__init__("houses", level, baseCost, production, constructionTime)

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
    AllUpgrades = {
        "farm": [Farm(1, Resources(0, 100, 350), Resources(30, -5, 0), 1),
                 Farm(2, Resources(0, 150, 400), Resources(45, -10, 0), 2),
                 Farm(3, Resources(0, 230, 500), Resources(60, -17, 0), 3),
                 Farm(4, Resources(0, 300, 620), Resources(80, -25, 0), 4),
                 Farm(5, Resources(0, 400, 780), Resources(100, -38, 0), 6), ],

        "houses": [Houses(1, Resources(100, 50, 0), Resources(-10, 20, 50), 2),
                   Houses(2, Resources(150, 100, 0), Resources(-20, 35, 75), 3),
                   Houses(3, Resources(220, 150, 0), Resources(-30, 50, 100), 4),
                   Houses(4, Resources(300, 200, 0), Resources(-40, 65, 125), 5),
                   Houses(5, Resources(400, 300, 0), Resources(-50, 90, 150), 6), ],

    }

    Categories = AllUpgrades.keys()

    @staticmethod
    def ShowPossibleUpgrades(builtUpgrades):
        for category in Shop.Categories:

            currentUpgradeLevel = builtUpgrades[category]
            if currentUpgradeLevel >= len(Shop.AllUpgrades[category]):
                print("All " + category + " upgrades have been built")
                continue

            upgrade = Shop.AllUpgrades[category][builtUpgrades[category]]
            upgrade.Print()

    @staticmethod
    def ShowAllUpgrades(self):
        for category in Shop.Categories:
            print(category, end=":\n")
            for upgrade in Shop.AllUpgrades[category]:
                upgrade.Print()


class Castle:

    def __init__(self, name:str, baseResources:Resources, production:Resources):
        self.name = name

        self.resources = baseResources
        self.baseProduction = production

        self.builtUpgrades = dict.fromkeys(Shop.Categories, 0)
        self.upgradesInConstruction = dict.fromkeys(Shop.Categories, 0)

    def BuyUpgrade(self, category:str):
        if (category not in Shop.Categories):
            print("Invalid category")
            return

        if (self.upgradesInConstruction[category] > 0):
            print(f"Already building an Upgrade for this category ({category})")
            return

        currentLVL = self.builtUpgrades[category]
        upgrade = Shop.AllUpgrades[category][currentLVL]

        if (self.resources >= upgrade.baseCost):
            print(f"Started construction for {category} lvl: {currentLVL + 1}")

            self.resources -= upgrade.baseCost

            self.ShowResources()
            self.upgradesInConstruction[category] = upgrade.constructionTime
            print(f"it will take {upgrade.constructionTime} turns to finish")
        else:
            print(f"{self.name} doesn't have enough resources ({category})")

    def GetProduction(self):
        totalProduction = self.baseProduction

        for category in Shop.Categories:
            upgradeLevel = self.builtUpgrades[category]
            if upgradeLevel == 0:
                continue

            totalProduction += Shop.AllUpgrades[category][upgradeLevel - 1].production
        return totalProduction

    def Construct(self):
        for category in Shop.Categories:
            turnsToFinish = self.upgradesInConstruction[category]
            if turnsToFinish > 0:
                self.upgradesInConstruction[category] -= 1
                if self.upgradesInConstruction[category] == 0:
                    self.builtUpgrades[category] += 1
                    lvl = self.builtUpgrades[category]
                    print(f"!! {category} lvl: {lvl} has finished construction after {Shop.AllUpgrades[category][lvl-1].constructionTime} !!")
                    Shop.AllUpgrades[category][lvl-1].ShowArt()


    def ShowResources(self):
        print(f"reserves:   [ {self.resources.Show()}]")
        print(f"production: [ {self.GetProduction().Show()}] per turn")

    def ShowUpgrades(self):
        for category in Shop.Categories:
            upgradeLevel = self.builtUpgrades[category]
            if upgradeLevel != 0:
                upgrade = Shop.AllUpgrades[category][upgradeLevel - 1]
                upgrade.Print()

    def ShowConstruction(self):
        for category in Shop.Categories:
            turnsToFinish = self.upgradesInConstruction[category]
            if turnsToFinish > 0:
                upgrade = Shop.AllUpgrades[category][self.builtUpgrades[category]]

                print(f"[{turnsToFinish}/{upgrade.constructionTime}] turns left. ", end="")

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


class Options:
    askForSaveName = True
    showHelpText = False
    autoLoadLastSaveOnStartup = True
    savesDir = "saves/"

class Utils:
    def FormatSaveName(savename:str) -> str:
        return savename[len(Options.savesDir):len(savename)-4] # len(".txt") : 4





class Game:
    commandsHelp = {
        "help": "shows you all the commands and how to use them\nyou can also use '?'",
        "?": "same as 'help'",
        "tutorial":"shows you a brief guide on how to play",
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
        "options": "to change how the game works",
        "save": "saves the game\nquick form: 'save SAVE_NAME'",
        "load": "loads the save file\nquick form: 'load SAVE_NAME'",
        "menu": "brings you back to the menu"
    }
    commands = commandsHelp.keys()


    tutorialPages = [
        #TODO come up with a name
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
        self.gameState = "normal"
        self.turn = 0
        #self.hasLoan = False
        self.isQuitting = False
        self.castle = Castle("missing name", Resources(100, 500, 1000), Resources(5, 30, 50))

    def Start(self):
        print("welcome back to")
        print(r"""
   ___  ___   __  ______ __     ____      ___   ___  ___  ___  ____
  //   // \\ (( \ | || | ||    ||        // \\ // \\ ||\\//|| ||   
 ((    ||=||  \\    ||   ||    ||==     (( ___ ||=|| || \/ || ||== 
  \\__ || || \_))   ||   ||__| ||___     \\_|| || || ||    || ||___                                                                   
  """)
        # print("How shall we name this castle?\n>", end="")
        # castleName = input()

        self.castle.ShowArt()
        if Options.showHelpText: print("(?) if you are unsure on what to do, enter 'help' or '?'")

    def GameLoop(self):
        while self.gameState not in ["won", "over"] or self.isQuitting:

            self.turn += 1
            print(f"<[ TURN {self.turn} IN {self.castle.name.upper()} ]>\n")

            self.castle.Construct()

            self.castle.ShowResources()


            #TODO: Autosave

            while True:
                fullCommand = self.GetCommand()
                command = fullCommand[0]

                if command == "help" or command=="?":
                    self.Help()

                elif command == "tutorial":
                    self.Tutorial()

                elif command in ["end","next","e","n"]:
                    self.EndTurn()
                    break

                elif command == "quit":
                    cmd = input("do you want to save before quitting? [yes | no | cancel]\n>").lower()
                    if (cmd in ["yes", "save"]):
                        self.Save()
                        self.isQuitting = True
                        return
                    elif (cmd == "cancel"):
                        print("happy to hear that you're not leaving ")
                    else:
                        self.isQuitting = True
                        return

                elif command == "shop":
                    Shop.ShowPossibleUpgrades(self.castle.builtUpgrades)
                    self.castle.ShowResources()
                    if Options.showHelpText: print("(?) to construct an upgrade use the 'build' command")

                elif command == "build":
                    if len(fullCommand) > 1:
                        self.Build(fullCommand[1])
                    else:
                        self.Build()

                elif command == "resources":
                    self.castle.ShowResources()

                elif command == "upgrades":
                    self.castle.ShowUpgrades()

                elif command == "construction":
                    self.castle.ShowConstruction()

                elif command == "options":
                    pass
                    #self.Options()

                elif command == "save":
                    if len(fullCommand) > 1:
                        self.Save(fullCommand[1])
                    else:
                        self.Save()

                elif command == "load":
                    if len(fullCommand) > 1:
                        self.Load(fullCommand[1])
                    else:
                        self.Load()

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
            fullCommand = input(">").lower().split()

            if (len(fullCommand) > 0 and fullCommand[0] in Game.commands):
                return fullCommand
            else:
                print("Invalid Command, enter help if you don't know what to do")

    @classmethod
    def Help(cls):
        for command in cls.commands:
            print("[",command,"]")
            for line in cls.commandsHelp[command].split("\n"):
                print("\t| " + line)
            print()


    def EndTurn(self):
        self.castle.resources += self.castle.GetProduction()


        self.UpdateGameState()



    def Save(self, saveName:str = ""):
        if (saveName != "" and saveName != None):
            if(len(saveName) > 0):
                fullSaveName = Options.savesDir + saveName + ".txt"
                import os
                if not os.path.exists(Options.savesDir):
                    os.mkdir(Options.savesDir)

                saveFile = open(fullSaveName,"w")

                saveFile.write(f"turn {self.turn}\n")
                saveFile.write(f"name {self.castle.name}\n")
                saveFile.write(f"gameState {self.gameState}\n")

                for upgrade in self.castle.builtUpgrades:
                    saveFile.write(f"upgrades {upgrade} {self.castle.builtUpgrades[upgrade]} {self.castle.upgradesInConstruction[upgrade]}\n")

                saveFile.write(f"reserves {self.castle.resources.food} {self.castle.resources.gold} {self.castle.resources.manpower}\n")
                saveFile.write(f"production {self.castle.baseProduction.food} {self.castle.baseProduction.gold} {self.castle.baseProduction.manpower}\n")

                saveFile.close()

                print("game saved...")

            else: print("save names can't be this short")

        else:
            if Options.askForSaveName == True:
                self.Save(input("What should the save be called?\n>"))
            else:
                self.Save(f"{self.castle.name}_{self.turn}")


    @classmethod
    def Load(cls, saveName:str = ""):
        if (saveName != "" and saveName != None):
            if (len(saveName) > 0):
                if(saveName == "last"):
                    saveFiles = glob.glob(Options.savesDir + "*.txt")
                    if (len(saveFiles) > 0):
                        fullSaveName = Options.savesDir + max(saveFiles, key=os.path.getctime)
                    else:
                        fullSaveName = Options.savesDir + saveName + ".txt"
                else:
                    fullSaveName = Options.savesDir + saveName + ".txt"
                if os.path.exists(fullSaveName):

                    saveFile = open(fullSaveName, "r")
                    game = Game()

                    for line in saveFile.readlines():
                        information = line.split()
                        if(not len(information) > 1):
                            continue
                        key = information[0]
                        value = information[1]

                        if key == "turn":
                            game.turn = int(value)
                        elif key == "name" and len(line) > 5:
                            game.castle.name = line[4:].replace('\n','')
                        elif key == "gameState" and len(line) > 11:
                            game.gameState = line[9:].replace('\n','')
                        elif key == "upgrades":
                            game.castle.builtUpgrades[value] = int(information[2]) # upgrade lvl
                            game.castle.upgradesInConstruction[value] = int(information[3]) # turns until it's finished
                        elif key == "reserves":
                            key, food, gold, manpower = information
                            game.castle.resources = Resources(int(food),int(gold),int(manpower))
                        elif key == "production":
                            key, food, gold, manpower = information
                            game.castle.baseProduction = Resources(int(food), int(gold), int(manpower))


                    saveFile.close()

                    print("loading completed...")
                    return game

                else: print("no such file: '"+saveName+"'")
        else:
            saveFiles = glob.glob(Options.savesDir + "*.txt")
            if(len(saveFiles) > 0):
                print("What save should be loaded?")
                for save in saveFiles: print(Utils.FormatSaveName(save), end=", ")
                latest_file = max(saveFiles, key=os.path.getctime)
                print("\nlast save:", Utils.FormatSaveName(latest_file))
                Game.Load(input("\n>"))
            else: print("there are no save files")



    def Over(self):
        self.gameState = "over"

        if self.castle.resources.food:
            print(
                f"After this year harvest it was clear that {self.castle.name} didn't have enough food for everyone.\n"
                f"So while the wealthy of {self.castle.name} eat until exploding, the plebs were starving to death.\n"
                f"This lead many to take arms with what they could find and start a rebellion.\n"
                f"After all the bloodshed, there was hardly something left of {self.castle.name}")

        if self.castle.resources.gold:
            print(
                f"Having nothing left in the treasury, {self.castle.name}'s soldiers organized a military coup and overthrow your rule.\n"
                f"Under this other ruler, plebes would get taxed to death and executed for frivolous reasons.\n"
                f"So the great majority of people fled away from {self.castle.name}, who soon turned into an abbandoned castle occupied by thiefs and looters")

        if self.castle.resources.manpower:
            print(
                f"The manpower reserves in {self.castle.name} got so thin that it was no longer able to maintain order.\n"
                f"This caused {self.castle.name} to get sacked and burned to the ground by some looters.\n"
                f"Leaving death and smoke of what was once a Great castle")

        print(f"{self.castle.name} has survived for {self.turn} turns.\nBut in the end it all got destroyed")



    def Build(self, category:str = None):
        if category != None:
            if category in Shop.Categories:
                self.castle.BuyUpgrade(category)
            else: print("invalid category!")
        else:
            for category in Shop.Categories: print(category, end=", ")
            self.Build(input("\nenter the upgrade's category\n>"))





    def UpdateGameState(self):
        if not self.castle.resources > Resources(0, 0, 0):
            self.Over()

    def Tutorial(self):
        print("press enter to continue")
        print("or enter 'skip' to skip the tutorial\n")
        for page in Game.tutorialPages:
            print(page)
            print()
            if(input().lower() == "skip"):
                return


if __name__ == '__main__':

    import glob
    import os

    if not os.path.exists(Options.savesDir):
        os.mkdir(Options.savesDir)

    game = None
    saveFiles = glob.glob(Options.savesDir + "*.txt")
    if len(saveFiles) > 0:
        latest_file = max(saveFiles, key=os.path.getctime)
        if Options.autoLoadLastSaveOnStartup == True:
            game = Game.Load(Utils.FormatSaveName(latest_file))
        else:
            print("Do you want to load last save? [yes/no]")
            if input(">").lower() == "yes":
                game = Game.Load(Utils.FormatSaveName(latest_file))


    while True:
        while game == None:
            print("[resume], [new], [load]")
            cmd = ""
            while cmd not in ["new","resume","load"]:
                cmd = input(">")


            if cmd == "new":
                game = Game()
                game.castle.name = input("How shall your castle be called?\n>")

            else:
                if len(saveFiles) > 0:
                    if cmd == "resume":
                        latest_file = max(saveFiles, key=os.path.getctime)
                        game = Game.Load(Utils.FormatSaveName(latest_file))
                    else:
                        game = Game.Load()
                else: print("There are no saves\nstart a new game by entering 'new'")

        game.Start()
        game.GameLoop()

        if game.isQuitting == True:
            break
        game = None
