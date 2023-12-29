from . import ssh
import argparse
from ..common import prettyllog


def main():
    parser = argparse.ArgumentParser(description="Manageable Ansible", usage="manisble_ssh <action> \n\n \
               \
               version : 0.0.1 manisble_ssh  \n\
               actions:                  \n\
               signssh                   \n\
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkins')
    args = parser.parse_args()
    ready = False

    if args.action[0] == "signssh":
        ssh.signssh()