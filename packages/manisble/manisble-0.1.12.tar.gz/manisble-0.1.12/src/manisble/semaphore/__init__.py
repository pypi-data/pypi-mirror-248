# keep manisble and con5entrate on your semaphores

from . import serve
import argparse

def main():
    parser = argparse.ArgumentParser(description="Manageable Ansible", usage="manisble_semaphore <action> \n\n \
\
version : 0.0.2 (semaphore)\n\
actions:\n\
serve      keep manisble and serve semaphore\n\
init       keep manisble and init semaphore systemd service\n\
start      keep manisble and start semaphore systemd service\n\
stop       keep manisble and stop semaphore systemd service\n\
restart    keep manisble and restart semaphore systemd service\n\
setup      keep manisble and setup semaphore\n\
test       keep manisble and test semaphore\n\
audit      keep manisble and audit semaphore\n\
")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup jenkins')
    args = parser.parse_args()
    ready = False

    if args.action[0] == "serve":
        serve.main()
        return 0
    

