# keep manisble and manage your vspere

from . import serve
import argparse

def main():
    parser = argparse.ArgumentParser(description="Manageable Ansible", usage="manisble_semaphore <action> \n\n \
\
version : 0.0.2 (semaphore)\n\
actions:\n\
serve      keep manisble and serve vspere\n\
\n\
")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkins')
    args = parser.parse_args()
    ready = False

    if args.action[0] == "serve":
        serve.main()
        return 0
    