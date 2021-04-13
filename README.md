# ComboFighter
This is an python AI for FightingICE.

run arguments:
--py4j --mute -f 1014 -r 20 --fastmode --disable-window

--py4j: run the FightingICE in python mode

--mute: play the game without sound

-f [number]: set the frame for each round. The first move starts in the 14th frame. ex: If there are 1000 actions, you need 1014 frame to perform all actions.

-r [number]: set the round number. The genetic algorithm have size of population X. If we want Y iterations, we need set the number to X*Y

--fastmode: make the game run above 60fps.

--disable-window: play the game without window.


Setup guide:
1. Download all the files in the python folder. Move all the files to the "FTG4.50 --> python folder".
2. Open Eclipse and set the run arguments in "Run As --> Run Configuration"
3. Run the game.
4. Open a cmd and find the location of the python folder.
5. use command: python generator.py    ##this line generate the initial values for the actions
6. use command: python genetic_start_up.py

Customize:
Population size: If you want to change the population size of the genetic algorithm. Change the self.popSize and popSize parameters in GeneticAI, IdleAI, and generator.py. You also need to set the run arguments -r to the new X

Action Length: To change the number of actions, change the seqLen = F to the value you want. And set the run arguments -f to F + 14
