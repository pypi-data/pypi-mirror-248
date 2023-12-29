from . import bump
import argparse
from ..common import prettyllog




def main():
    parser = argparse.ArgumentParser(description="Keep manisble and bump", usage="manisble_bump <action> \n\n \
               \
               version : 1.0.0 bump  \n                                              \
               actions:\n                                                      \
               major        major bump \n  \
               minor        minor bump \n  \
               patch        patch bump \n  \
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkins')
    args = parser.parse_args()
    ready = False
    print("check if we are ready to go")


    if args.action[0] == "major":
        bump.major()
        ready = True
    if args.action[0] == "minor":
        bump.minor()
        ready = True
    if args.action[0] == "patch":
        bump.patch()
        ready = True

    