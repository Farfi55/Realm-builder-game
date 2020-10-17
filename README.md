# Realm-builder
Turn based strategy game where you administer a castle and its territories


 
![welcome-screen](https://github.com/Farfi55/Realm-builder-game/blob/main/Immagine.png)

You can build many upgrades, each with different effects

Watch your castle grow from nothing to a flourishing stronghold

Make the right choises when the time will come or face the consequences (events)





# Tutorial

In this turn based game you are the king of a castle and its territories

Your objective is to get to 5000 Population


## Resources

Resources are **FOOD** (f), **GOLD** (g) and **MANPOWER** (m)
- *FOOD* is used to feed the people of your castle and sometimes for buildings
- *GOLD* is used to pay for stuff like upgrades or mercenaries, the population will pay taxes giving you gold
- *MANPOWER* is mostly used for warfare but also buildings 

there is also **population** which is the end-goal

population will grow using the food produced every round, they will pay taxes and make up your army

you can increase your resources production by building upgrades

Upgrades are buildings in your castle that improve something. For example the farm produces food to feed the people, the houses provide more capacity for the population.

## Upgrades
An upgrade(or building) has
- name (or category)
- level
- build cost
- upkeep cost
- production
- (sometimes) special effect
- turns for constructing

![houses-upgrade](https://github.com/Farfi55/Realm-builder-game/blob/main/Screenshot%202020-10-17%20231311.png)


You can build upgrades by entering the `build` command followed by the building name (es. farm, houses) that you want to upgrade/build

if you forget the names you can always see them by just entering `build` or heading over to `shop`


Once you're happy with what you've achieved this turn, you can **end the turn** with the `end` command (`e`, `next`, `n` also work)

After every turn you gain(or lose) a certain amount of resources and population, if any of your resources go lower than 0 you will LOSE THE GAME

Buildings wont comlete immidiately and you'll need to wait for how many turns the upgrade takes. You can always check what is in construction by using the `construction` command
Once finished an upgrade you'll be able to see all your castle buildings using the `upgrades` command

for additional help or if you forget commands use **`help`** or `?`
