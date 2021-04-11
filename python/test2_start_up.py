import sys
import random
from time import sleep
from py4j.java_gateway import JavaGateway, GatewayParameters, CallbackServerParameters, get_field
from testAI2 import testAI2
from IdleAI import IdleAI



def check_args(args):
    for i in range(argc):
        if args[i] == "-n" or args[i] == "--n" or args[i] == "--number":
            global GAME_NUM
            GAME_NUM = int(args[i + 1])


def start_game():
    print("Start game")

    manager.registerAI("testAI2", testAI2(gateway))
    manager.registerAI("IdleAI", IdleAI(gateway))

    game = manager.createGame("ZEN", "ZEN", "testAI2", "IdleAI", GAME_NUM)
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
gateway = JavaGateway(gateway_parameters=GatewayParameters(port=gateway_port),
                      callback_server_parameters=CallbackServerParameters(port=0))
real_callback_port = gateway.get_callback_server().get_listening_port()
gateway.java_gateway_server.resetCallbackClient(gateway.java_gateway_server.getCallbackClient().getAddress(),
                                                real_callback_port)

manager = gateway.entry_point

main_process()

