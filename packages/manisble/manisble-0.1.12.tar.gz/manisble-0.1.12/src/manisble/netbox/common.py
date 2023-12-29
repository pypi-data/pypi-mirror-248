import os
import json


def usage():
  # export the environment variables
  print("export MANISBLE_NETBOX_URL=\"\"")
  print("export MANISBLE_NETBOX_TOKEN=\"\"")
  print("export MANISBLE_NETBOX_SSL=\"\"")


def  get_env():
  myenv = {}
  myenv['subproject'] = {}
  try:
    myenv['MANISBLE_NETBOX_URL'] = os.getenv("MANISBLE_NETBOX_URL")
    myenv['MANISBLE_NETBOX_TOKEN'] = os.getenv("MANISBLE_NETBOX_TOKEN")
    myenv['MANISBLE_NETBOX_SSL'] = os.getenv("MANISBLE_NETBOX_SSL", "false")
    myenv['MANISBLE_WORKDIR'] = os.getenv("MANISBLE_WORKDIR", "/tmp/manisble")
  except KeyError as key_error:
    print(key_error)
    usage()
    raise SystemExit("Unable to get environment variables.")
  if myenv['MANISBLE_NETBOX_URL'] == None:
    usage()
    raise SystemExit("Unable to get environment variables.")
  if myenv['MANISBLE_NETBOX_TOKEN'] == None:
    usage()
    raise SystemExit("Unable to get environment variables.")
  
  if myenv['MANISBLE_NETBOX_SSL'] == "false" or myenv['MANISBLE_NETBOX_SSL'] == "False" or myenv['MANISBLE_NETBOX_SSL'] == "FALSE" or myenv['MANISBLE_NETBOX_SSL'] == "no" or myenv['MANISBLE_NETBOX_SSL'] == "NO" or myenv['MANISBLE_NETBOX_SSL'] == "No":
    myenv['MANISBLE_NETBOX_SSL'] = False
  else:
    myenv['MANISBLE_NETBOX_SSL'] = True
  if myenv['MANISBLE_NETBOX_URL'][-1] == "/":
    myenv['MANISBLE_NETBOX_URL'] = myenv['MANISBLE_NETBOX_URL'][:-1]

  

  # list all files in /etc 
  if os.path.exists(myenv['MANISBLE_WORKDIR']) == False:
    os.mkdir(myenv['MANISBLE_WORKDIR'])
  files = os.listdir(myenv['MANISBLE_WORKDIR'] + "/etc/manisble")
  print(files)

  if os.path.exists(myenv['MANISBLE_WORKDIR'] + "/etc/manisble/manisble.json") == False:
    raise SystemExit("Unable to find " + myenv['MANISBLE_WORKDIR'] +"/etc/manisble/manisble.json")
  

  f = open(myenv['MANISBLE_WORKDIR'] + "/etc/manisble/manisble.json", "r")
  manisbleconfig = json.loads(f.read())
  f.close()
  for key in manisbleconfig:
    myenv[key] = manisbleconfig[key]

  mysubprojects = []
  for subproject in myenv['subprojects']:
    filename = myenv['MANISBLE_WORKDIR'] + "/etc/manisble/conf.d/" + subproject['name'] + ".json"
    try: 
      ff =  open(filename, "r")
      ff.close()
    except:
      errorstring = "unable to open " + filename
      print(errorstring)
# create file
#{
#  "subproject": {
#    "description": "The zabbix agent installation and configuration"
#  },
#  "inventory": {
#    "globalvars": {
#      "zabbix_server": "zabbix.it.rm.dk"
#    }
#  },
#  "hosts": [
#    "exrhel001.it.rm.dk",
#    "exrhel002.it.rm.dk"
#  ]
#}
      description = "The %s project" % subproject['name']
      data = {
    "subproject": {
        "description": description
    },
    "inventory": {
        "globalvars": {
        }
    },
    "hosts": [
    ]
}
      with open(filename, "w") as file:
        json.dump(data, file, indent=2)

    ff =  open(filename, "r")
    subprojectconfig = json.loads(ff.read())
    print(subprojectconfig)
    myenv['subproject'][subproject['name']] = subprojectconfig
    ff.close()







  return myenv
