import sys
import random
from time import sleep
from py4j.java_gateway import JavaGateway, GatewayParameters, CallbackServerParameters, get_field
from demoAI import demoAI
from IdleAI import IdleAI


def check_args(args):
	for i in range(argc):
		if args[i] == "-n" or args[i] == "--n" or args[i] == "--number":
			global GAME_NUM
			GAME_NUM = int(args[i+1])

def start_game():

	#Select AI action index
	index = 54

	#Read the file
	# Using readlines()
	with open("Inputs\\actions.txt") as fin:
		data = fin.read().splitlines(True)
		actionList = data[index]
		print(len(actionList))
		print(actionList[0:10])

	# writing to file
	file1 = open("Inputs\\demo.txt", 'w')
	file1.writelines(actionList)
	file1.close()

	manager.registerAI("demoAI", demoAI(gateway))
	manager.registerAI("IdleAI", IdleAI(gateway))
	print("Start game")

	game = manager.createGame("ZEN", "ZEN", "demoAI", "IdleAI", GAME_NUM)
	manager.runGame(game)
	
	print("After game")
	sys.stdout.flush()

def close_gateway():
	gateway.close_callback_server()
	gateway.close()

def main_process():
	check_args(args)
	start_game()
	close_gateway()



args = sys.argv
argc = len(args)
GAME_NUM = 1


gateway_port = 4242
gateway = JavaGateway(gateway_parameters=GatewayParameters(port=gateway_port), callback_server_parameters=CallbackServerParameters(port=0))
real_callback_port = gateway.get_callback_server().get_listening_port()
gateway.java_gateway_server.resetCallbackClient(gateway.java_gateway_server.getCallbackClient().getAddress(), real_callback_port)

manager = gateway.entry_point

main_process()

