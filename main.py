from game import *
import sys
from optparse import OptionParser


def take_command(argv):
    parser = OptionParser()
    usage = ""
    parser.add_option("-m", "--game_mode", dest="game_mode", type="int", action="store", default=1)
    parser.add_option("-o", "--opening", dest="opening", type="int", action="store", default=0)
    parser.add_option("-i", "--moveInfo", dest="show_move", action="store_true", default=True)
    parser.add_option("-I", "--searchInfo", dest="show_search", action="store_true", default=True)
    parser.add_option("-d", "--depth", dest="depth", type="int", action="store", default=2)
    parser.add_option("-p", "--pos_eva", dest="use_pos", action="store_true", default=False)
    parser.add_option("-s", "--save", dest="save_data", action="store_true", default=True)
    parser.add_option("-l", "--load", dest="load_data", action="store_true", default=False)

    options, temp = parser.parse_args(argv)

    print(options.game_mode)

    if len(temp) != 0:
        raise Exception("Invalid Input: " + str(temp))
    arguments = dict()

    arguments["game_mode"] = options.game_mode
    arguments["opening"] = options.opening
    arguments["depth"] = options.depth

    if options.show_move:
        arguments["show_move"] = True
    else:
        arguments["show_move"] = False
    if not options.show_search:
        arguments["show_search"] = False
    else:
        arguments["show_search"] = True

    arguments["show_gui"] = True

    if options.use_pos:
        arguments["use_pos"] = True
    else:
        arguments["use_pos"] = False
    if options.save_data:
        arguments["save_data"] = True
    else:
        arguments["save_data"] = False
    if options.load_data:
        arguments["load_data"] = True
    else:
        arguments["load_data"] = False
    return arguments


if __name__ == '__main__':

    # Get game components based on input
    args = sys.argv[1:]
    args=take_command(args)
    valid_response=False
    val = input("Select Game Mode:\nEnter 1 for Human vs AI Mode \nEnter 2 for Human vs Human Mode \nEnter 3 To load Previous Game\n")
    while valid_response==False:
        if val=='1':
            args["game_mode"]=1
            valid_response = True
        elif val=='2':
            args["game_mode"] = 0
            valid_response = True
        elif val=='3':
            args["load_data"]=True
            valid_response = True
        else:
            print("Enter a valid Response")
    game = Game()
    game.set_stage(args["game_mode"], args["opening"], args["show_move"], args["show_search"], args["show_gui"],
                   args["save_data"], use_pos=args["use_pos"], depth=args["depth"], load_data=args["load_data"])
    game.start()
