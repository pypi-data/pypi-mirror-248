import requests
import json
import os
import base64
import xml.etree.ElementTree as ET
import pprint
from ..common import prettyllog
import tempfile
import git
import os


import base64


def getenv():
  myenv = {}
  myenv["MANISBLE_GIT_URL"] = os.getenv("MANISBLE_GIT_URL")
  myenv["MANISBLE_GIT_USER"] = os.getenv("MANISBLE_GIT_USER")
  myenv["MANISBLE_GIT_PASSWORD"] = os.getenv("MANISBLE_GIT_PASSWORD")
  myenv["MANISBLE_GIT_TYPE"] = os.getenv("MANISBLE_GIT_TYPE")
  username = os.getenv("MANISBLE_GIT_USER")
  password = os.getenv("MANISBLE_GIT_PASSWORD")
  myenv["verifyssl"] = os.getenv("MANISBLE_GIT_VERIFY_SSL", "False")

  credentials = f"{username}:{password}"
  base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
  myenv["base64_credentials"] = base64_credentials
  return myenv

def init():
  prettyllog("state", "Init", "git", "start", "000", "login initiated", severity="DEBUG")
  myenv = getenv()
  session = requests.Session()
  url = os.getenv("MANISBLE_GIT_URL") + "/api/v1/user"
  headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + myenv['base64_credentials']
    }
  resp = session.get(url,headers=headers)
  if resp.status_code == 200:
    prettyllog("state", "Init", "git", "ok", resp.status_code, "login successful", severity="INFO")
    return session
  else:
    prettyllog("state", "Init", "git", "error", resp.status_code, "login failed", severity="ERROR")
    return None

def clone_git_project(projectname):
    prettyllog("semaphore", "Init", "clone", projectname , "000", "clone project initiated", severity="DEBUG")
    # create a temporary dir and clone the project
    # return the config data
    tempfiledir = tempfile.mkdtemp()
    prettyllog("semaphore", "Init", "clone", projectname , "000", "cloning", severity="DEBUG")
    username = os.getenv("MANISBLE_GIT_USER")
    password = os.getenv("MANISBLE_GIT_PASSWORD")
    #split http(s):// from the url
    protocol = os.getenv("MANISBLE_GIT_URL").split("://")[0]
    endpoint = os.getenv("MANISBLE_GIT_URL").split("://")[1]
    remote = f"{protocol}://{username}:{password}@{endpoint}/gitea/{projectname}.git"
    remoteanonym = f"{protocol}://{endpoint}/gitea/{projectname}.git"
    pprint.pprint(remote)
    

    repo = git.Repo.clone_from(remote, tempfiledir)
    configdata = {}
    configdata['url'] = remoteanonym
    configdata['path'] = tempfiledir
    configdata['repo'] = repo

    prettyllog("semaphore", "Init", "clone", projectname , "000", "cloning done", severity="DEBUG")

    # check if the project has a manisble.json file in etc/manisble
    # if not create it
    prettyllog("semaphore", "Init", "clone", projectname , "000", "checking for manisble dir in repo", severity="DEBUG")
    if os.path.isdir(tempfiledir + "/etc/manisble"):
        prettyllog("semaphore", "Init", "clone", projectname , "000", "etc/manisble exists", severity="DEBUG")
    else:
        prettyllog("semaphore", "Init", "clone", projectname , "000", "etc/manisble missing", severity="DEBUG")
        os.mkdir(tempfiledir + "/etc")
        os.mkdir(tempfiledir + "/etc/manisble")
        prettyllog("semaphore", "Init", "clone", projectname , "000", "etc/manisble created", severity="DEBUG")

    if os.path.isfile(tempfiledir + "/etc/manisble/manisble.json"):
        prettyllog("semaphore", "Init", "clone", projectname , "000", "manisble.json exists", severity="DEBUG")
        f = open(tempfiledir + "/etc/manisble/manisble.json", "r")
        configdata['manisble'] = json.load(f)
        f.close()
    else:
        prettyllog("semaphore", "Init", "clone", projectname , "000", "manisble.json missing", severity="DEBUG")
        configdata['manisble'] = {}
        configdata['manisble']['project'] = {}
        configdata['manisble']['project']['name'] = projectname
        configdata['manisble']['project']['description'] = "manisble project"
        configdata['manisble']['project']['private'] = True
        configdata['manisble']['project']['auto_init'] = True
        configdata['manisble']['project']['inventory'] = {}
        configdata['manisble']['project']['inventory']['name'] = "inventory"
        configdata['manisble']['project']['inventory']['description'] = "manisble inventory"
        configdata['manisble']['project']['inventory']['private'] = True
        configdata['manisble']['project']['inventory']['auto_init'] = True
        configdata['manisble']['project']['inventory']['type'] = "static"
        configdata['manisble']['project']['inventory']['items'] = []
        configdata['manisble']['project']['inventory']['items'].append("localhost")
        #save the file

        f = open(tempfiledir + "/etc/manisble/manisble.json", "w")
        json.dump(configdata['manisble'], f)
        f.close()
        # add the file to git
        repo.git.add(A=True)
        repo.index.commit("manisble project created")
        origin = repo.remote(name='origin')
        origin.push()
    return configdata

  
def create_git_project(project):
  prettyllog("state", "Init", "git", "start", "000", "create project initiated", severity="DEBUG")
  myenv = getenv()
  session = init()
  url = myenv['MANISBLE_GIT_URL'] + "/api/v1/user/repos"
  headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + myenv['base64_credentials']
    }
  data = {
    "name": project['name'],
    "description": project['description'],
    "private": project['private'],
    "auto_init": project['auto_init']
    }
  resp = session.post(url,headers=headers, json=data)
  if resp.status_code == 201:
    prettyllog("state", "Init", "git", "ok", resp.status_code, "create project successful", severity="INFO")
    return resp.json()
  else:
    prettyllog("state", "Init", "git", "error", resp.status_code, "create project failed", severity="ERROR")
    return None
  
  
def get_git_projects():
  myenv = getenv() 
  session = init()
  url = myenv['MANISBLE_GIT_URL'] + "/api/v1/user/repos"
  headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + myenv['base64_credentials']
    }
  resp = session.get(url,headers=headers)
  if resp.status_code == 200:
    prettyllog("state", "Init", "git", "ok", resp.status_code, "get projects successful", severity="INFO")
    return resp.json()
  else:
    prettyllog("state", "Init", "git", "error", resp.status_code, "get projects failed", severity="ERROR")
    return None
  

  
def create_git_token():
  session = init()
  myenv = getenv()
  url = myenv['MANISBLE_GIT_URL'] + "/api/v1/users/" + myenv['MANISBLE_GIT_USER'] + "/tokens?sudo=" + myenv['MANISBLE_GIT_USER']
  headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + myenv['base64_credentials']
    }
  data = {
    "name": myenv['MANISBLE_GIT_USER']
    }
  resp = session.post(url,headers=headers, json=data)
  if (resp.status_code == 201):
    prettyllog("state", "Init", "git", "ok", resp.status_code, "create token successful", severity="INFO")
    return resp.json()
  else:
    prettyllog("state", "Init", "git", "error", resp.status_code, "create token failed", severity="INFO")
    return None



def refresh_git_token(git_token):
  create = True
  if (len (git_token) == 0):
    prettyllog("state", "Init", "git", "error", "000", "no tokens found", severity="INFO")
    create = Truesyst
    mytoken = create_git_token()
    pprint.pprint(mytoken)
  else:
    prettyllog("state", "Init", "git", "ok", "000", "tokens found", severity="INFO")
    mytoken = create_git_token()
    pprint.pprint(mytoken)
  if create == True:
    mytoken = create_git_token()



def delete_token():
  prettyllog("state", "Init", "git", "ok", "000", "token found", severity="INFO")
  session = init()
  myenv = getenv()
  url = myenv['MANISBLE_GIT_URL'] + "/api/v1/users/" + myenv['MANISBLE_GIT_USER'] + "/tokens/"
  headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + myenv['base64_credentials']
    }
  data = {
    "username": myenv['MANISBLE_GIT_USER']
    }
  resp = session.delete(url,headers=headers)
  if (resp.status_code == 204):
    prettyllog("state", "Init", "git", "ok", resp.status_code, "delete token successful", severity="INFO")
  else:
    prettyllog("state", "Init", "git", "error", resp.status_code, "delete token failed", severity="INFO")
  return None


def get_git_tokens():

  session = init()
  myenv = getenv()
  url = myenv['MANISBLE_GIT_URL'] + "/api/v1/users/" + myenv['MANISBLE_GIT_USER'] + "/tokens?sudo=" + myenv['MANISBLE_GIT_USER']
  headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + myenv['base64_credentials']
    }
  data = {
    "username": myenv['MANISBLE_GIT_USER']
    }
  resp = session.get(url,headers=headers, json=data)
  if (resp.status_code == 200):
    prettyllog("state", "Init", "git", "ok", resp.status_code, "get token successful", severity="INFO")
    return resp.json()
  else:
    prettyllog("state", "Init", "git", "error", resp.status_code, "get token failed", severity="INFO")
    return None
  


 
