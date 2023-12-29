from . import pitv
import argparse
from ..common import prettyllog




def main():
    parser = argparse.ArgumentParser(description="Manageable Ansible", usage="manisble_pitv <action> \n\n \
               \
               version : 0.1.2 pitv  \n                                              \
               actions:\n                                                      \
               status        status pitv \n  \
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkins')
    args = parser.parse_args()
    ready = False
    print("check if we are ready to go")


    if args.action[0] == "evacuate":
        pitv.evacuate()

    if args.action[0] == "status":
        print("status pitv")
        pitv.status()


    if args.action[0] == "list_datasets":
        print("list_datasets pitv")
        pitv.list_datasets()
    
    if args.action[0] == "delete_all_datasets":
        print("delete_all_datasets pitv")
        pitv.delete_all_datasets()
        

    if args.action[0] == "delete_all_dags":
        print("delete_all_dags pitv")
        pitv.delete_all_dags()


    if args.action[0] == "set":
        print("set pitv")
        pitv.set()

    if args.action[0] == "list_dags":
        print("list_dags pitv")
        pitv.list_dags()



