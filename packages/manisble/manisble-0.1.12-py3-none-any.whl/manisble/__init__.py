from manisble import manisble

import os
import sys
import redis
import time
import subprocess
import json
import argparse
import requests

class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in 
    Python, i.e. will suppress all print, even if the print originates in a 
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).      

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0],1)
        os.dup2(self.null_fds[1],2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            os.close(fd)



def runme(command):
  commandlist = command.split(" ")
  result = subprocess.run(commandlist, capture_output=True)
  payload = {"returncode": result.returncode, "stdout": result.stdout.decode(), "stderr": result.stderr }
  return payload

def setupmanisble(force):
    if not force:
        print("We need to setup manisble - Do you with to continue (y/N)? ")
        answer = input()
        if answer == "Y" or answer == "y" or answer == "Yes" or answer == "yes":
            force = True
    if force:
        print("Initializing")
        runme("sudo mkdir /etc/manisble >/dev/null 2>&1")

def checktoken(host, token):
      headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(token)}
      url = host + "/api/v2/ping/"
      resp = requests.get(url,headers=headers)
      if resp.status_code == 200:
        return True
      else:
        return False

def connectiontest():
    checks=[]
    errors=[]
    TOWERCLI = { 
        "installed": False, 
        "version": "unknown",
        "status": "unknown", 
        "env_password": os.getenv("TOWER_PASSWORD"), 
        "env_host": os.getenv("TOWER_HOST"),
        "env_username": os.getenv("TOWER_USERNAME") 
        }

    ANSIBLE_TOKEN = { "set": False, "value": "", "status": "unknown"} 
    if os.getenv("ANSIBLE_TOKEN") != None:
        ANSIBLE_TOKEN = { "set": True, "value": os.getenv("ANSIBLE_TOKEN")   , "status": "unknown"} 

    NETBOX_TOKEN = { "set": False, "value": "", "status": "unknown"} 
    if os.getenv("NETBOX_TOKEN") != None:
        NETBOX_TOKEN = { "set": True, "value": os.getenv("NETBOX_TOKEN")   , "status": "unknown"} 

    # We need to check if the config is there and a  valid  json    
    MANISBLE_CONFIG = { "set": False, "value": "", "status": "unknown"} 
    if os.getenv("MANISBLE_CONFIG") != None:
        MANISBLE_CONFIG = { "set": True, "value": os.getenv("MANISBLE_CONFIG")  , "status": "unknown"} 
    else:
        # fall back to default if not set
        MANISBLE_CONFIG = { "set": False, "value": "/etc/manisble/manisble.json"  , "status": "unknown"} 

    MANISBLE_SECRET = { "set": False, "value": "", "status": "unknown"} 
    if os.getenv("MANISBLE_SECRET") != None:
        MANISBLE_SECRET = { "set": True, "value": os.getenv("MANISBLE_SECRET")  , "status": "unknown"} 
    else:
        # fall back to default if not set
        MANISBLE_SECRET = { "set": False, "value": "/etc/manisble/secret.json"  , "status": "unknown"} 



    if os.path.isfile(MANISBLE_CONFIG['value']):
      with open(MANISBLE_CONFIG['value']) as user_file:
        try:
          parsed_json = json.load(user_file)
        except:
          errors.append("003: error in json format")
          print("003: error in json file")
          # BAIL OUT WHEN config is not json
          return False
    else:
        errors.append("004: File not found")
        # BAIL OUT WHEN config is not existing
        return False

    if os.path.isfile(MANISBLE_SECRET['value']):
      with open(MANISBLE_SECRET['value']) as user_file:
        try:
          parsed_json = json.load(user_file)
        except:
          errors.append("003: error in json format")
          print("003: error in json file")
          # BAIL OUT WHEN config is not json
          return False
    else:
        errors.append("004: File not found")
        # BAIL OUT WHEN config is not existing
        return False

    result = runme("/usr/local/bin/awx --version")
    if result['returncode'] == 0:
        checks.append("004: awx is installed")
        TOWERCLI["installed"] =True
        TOWERCLI["version"] =  result['stdout']

    result = runme("/usr/local/bin/awx me | jq .results[].is_superuser |grep true")
    if result['returncode'] == 0:
        checks.append("006: we are superuser on awx")
        TOWERCLI["status"] =  "ready"
    else:
        errors.append("006: we need admin access")
        return False
    
    # We neek to know if the api is accesable with our TOKEN and/or we can or shall create a new TOKEN
    if TOWERCLI["env_host"] == None:
       #We need to know where to go
        errors.append("100: We have no target defined in TOWER_HOST environment")
        return False
       
    if ANSIBLE_TOKEN['set']:
      headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(ANSIBLE_TOKEN['value'])}
      url = TOWERCLI['env_host'] + "/api/v2/ping/"
      resp = requests.get(url,headers=headers)
      if resp.status_code == 200:
        ANSIBLE_TOKEN['status']  = "ready"
      else:
        ANSIBLE_TOKEN['status']  = "failed"
        return False

    if ANSIBLE_TOKEN["status"] != "ready" and  TOWERCLI["status"] == "ready":
        result = runme("/usr/local/bin/awx --conf.color False tokens create |jq '{'id': .id, 'token': .token }")
        parsed_json = json.loads(result["stdout"])
        newtoken = parsed_json['token']
        if result['returncode'] == 0:
          checks.append("004: awx token created")
          headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(newtoken)}
          url = TOWERCLI['env_host'] + "/api/v2/ping/"
          resp = requests.get(url,headers=headers)
          if resp.status_code == 200:
            ANSIBLE_TOKEN['status']  = "ready"
            os.environ["ANSIBLE_TOKEN"] = newtoken
            ANSIBLE_TOKEN = { "set": True, "value": os.getenv("ANSIBLE_TOKEN")   , "status": "ready"} 
          else:
            ANSIBLE_TOKEN['status']  = "failed"
            return False

    if len(errors) > 0:
        return False
    else:
        return True


def main():
    parser = argparse.ArgumentParser(description="Manageable Ansible", usage="manisble <action> \n\n \
               \
               version : 1.0.0\n\
               actions:\n\
               core           Run manisble using the core/initial process to ensure the core environment is intact (/etc/manisble/manisble.json)\n  \
               seeder         Run manisble using the config files in (/etc/manisble.d)\n  \
               seed           Run manisble using the config specific configuration\n  \
               check          check access to core services defined\n  \
               setup          setup access to core services defined\n  \
               netbox         Run manisble to update netbox configured in /etc/manisble/netbox.json \n  \
               service        Run manisble from systemd service \n  \
               initservice    setup manisble systemd service \n  \
               stopservice    disable and cleanup manisble systemd service \n  \
               startservice   setup and enable manisble systemd service \n  \
               deploy         deploy an ansible tower, awx, awxrpm \n  \
               version        show the installed version\n  \
               upgrade        upgrade manisble to the latest version\n  \
               ")
    parser.add_argument('action', metavar='<action>', type=str, nargs='+', help='setup netbox')
    args = parser.parse_args()
    ready = False
    print("check if we are ready to go")
    ready  = connectiontest()

    if args.action[0] == "netbox":
        print("netbox")
        if ready:
            print("We have the access we need")
            exit(0)
        else:
            exit(1)

    if args.action[0] == "check":
        if ready:
            print("We have the access we need")
            exit(0)
        else:
            exit(1)

    if args.action[0] == "setup":
        force = False
        try: 
            arg1 = args.action[1]
            if arg1 == "-y":
                force = True
            else: 
                force = False
        except:
            force = False
        setupmanisble(force)

    if args.action[0] == "version":
      os.system("pip show manisble |grep Version")

    if args.action[0] == "upgrade":
      os.system("pip show manisble |grep Version")
      os.system("pip install --upgrade pip >/tmp/deleteme 2>&1")
      os.system("pip show manisble |grep Version | tee /tmp/manisble.version > /tmp/deleteme 2>&1")
      os.system("pip install --upgrade manisble > /tmp/deleteme 2>&1")
      os.system("pip install --upgrade manisble > /tmp/deleteme 2>&1")
      os.system("pip show manisble |grep Version | tee /tmp/manisble.version.new > /tmp/deleteme 2>&1")
      os.system("diff /tmp/manisble.version /tmp/manisble.version.new |tee  /tmp/manisble.version.diff > /tmp/deleteme 2>&1 ")
      os.system("cat /tmp/manisble.version.diff " )
      os.system("rm /tmp/manisble.version.difF >  /tmp/deleteme 2>&1")
      os.system("rm /tmp/manisble.version > /tmp/deleteme 2>&1")
      os.system("rm /tmp/manisble.version.new > /tmp/deleteme 2>&1")
      os.system("rm /tmp/deleteme")
      os.system("pip show manisble |grep Version")



    if args.action[0] == "service":
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = os.getenv("REDIS_PORT", "6379")
        redis_db = os.getenv("REDIS_DB", "0")
        redis_password = os.getenv("REDIS_PASSWORD", "")
        r = redis.Redis( host=redis_host, port=redis_port, db=redis_db, password=redis_password)
        r.flushdb()
        servicefile = open("/etc/manisble/manisble.service.token", mode="r")
        cfgfile="/etc/manisble/manisble.json"
        f = open(cfgfile)
        config = json.loads(f.read())
        f.close
        token = servicefile.read()
        token = token.replace("\n", "")
        while True:
            print("Daemon running")
            print("main loop")
            for org in (config['organization']):
              manisble.manisble(token, r, org['project'], "main")
              for subproject in org['subprojects']:
                manisble.manisble(token, r, "subproject", subproject['name'])
            print("Daemon sleeping")
            time.sleep(60)
            

            


    if ready and args.action[0] == "initservice":
        r = redis.Redis()
        r.flushdb()
        result = runme("/usr/local/bin/awx --conf.color False tokens create |jq '{'id': .id, 'token': .token }")
        parsed_json = json.loads(result["stdout"])
        runme("sudo touch /etc/manisble/manisble.service.token")
        runme("sudo touch /etc/systemd/system/manisble.service")
        runme("sudo chown knowit:knowit /etc/manisble/manisble.service.token")
        runme("sudo chown knowit:knowit /etc/systemd/system/manisble.service")
        mycofig = open("/etc/manisble/manisble.service.token", "w")
        myservice = open("/etc/systemd/system/manisble.service", "w")
        try:
          newtoken = parsed_json['token']
          mycofig.write(newtoken)
        except:
          print("Service not ready")
        myservice.write("[Unit]\n")
        myservice.write("Description=Ansible Automation on Ansible Automation\n")
        myservice.write("After=network.target\n")
        myservice.write("[Service]\n")
        myservice.write("Environment=\"TOWER_FORMAT=json\n\"")
        myservice.write("Environment=\"TOWER_PASSWORD=%s\"\n" % os.getenv("TOWER_PASSWORD"))
        myservice.write("Environment=\"TOWER_HOST=%s\"\n" % os.getenv("TOWER_HOST"))
        myservice.write("ExecStart=/usr/local/bin/manisble service\n")
        myservice.write("User=knowit\n")
        myservice.write("Restart=always\n")
        myservice.write("[Install]\n")
        myservice.write("WantedBy=default.target\n")
        myservice.write("RequiredBy=network.target\n")
        myservice.close
        runme("sudo systemctl daemon-reload")
        ready  = False

    if ready and ( args.action[0] == "reset" or args.action[0] == "stopservice"):
        runme("sudo systemctl daemon-reload")
        runme("sudo systemctl enable manisble.service")
        runme("sudo systemctl start manisble.service")
        ready  = False

    if ready and ( args.action[0] == "reset" or args.action[0] == "startservice"):
        runme("sudo systemctl daemon-reload")
        runme("sudo systemctl enable manisble.service")
        runme("sudo systemctl start manisble.service")
        ready  = False

    if ready and ( args.action[0] == "reset" or args.action[0] == "init"):
        r = redis.Redis()
        r.flushdb()
        ansibletoken = os.getenv("ANSIBLE_TOKEN")
        manisble.manisble(ansibletoken, r)

    





