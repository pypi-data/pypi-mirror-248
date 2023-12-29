# Manisble - Manageable Ansible


### Install and update Manisble

pip install --upgrade manisble


### Basic configuration
```
mansible setup
```

creates a basic manisble configuration

/etc/manisble/manisble.yaml and /etc/manisble/secrets.yaml

```
---
organization:
- name: manisble
  meta:
    description: Manageable Ansible
    max_hosts: 100
    default_environment: Ansible Engine 2.9 execution environment
    secrets: files
  projects:
  - name: main
    description: Manageable Ansible
    scm_type: git
    scm_url: git@github.com:JakobHolstDK/openknowit_ansibleautomation_main.git
    scm_branch: main
    credential: github
    master: 'True'
  inventories:
  - name: 000_masterinventory
    description: Inventorycontaining all servers under automation control
    variables:
      serviceaccount:
        name: knowit
        gecos: Ansible automation manager
    type: static
  - name: 001_netboxinventory
    description: Inventory containing all servers in netbox
    variables:
      serviceaccount:
        name: knowit
        gecos: Ansible automation manager
    type: netbox
  hosts:
  - name: prodmanisble001.openknowit.com
    description: Server cabable for running selfmaintainance
    inventories:
    - 000_masterinventory
  templates:
  - name: 000_ansibleautomationmanager_checkup
    description: Master job for self healing ansible automation as code
    job_type: run
    inventory: 000_masterinventory
    project: main
    EE: Automation Hub Default execution environment
    credentials: manisbleserver
    playbook: checkup.yml
  - name: 000_ansibleautomationmanager_update
    description: Maintain ansible manager and prereqs
    job_type: run
    inventory: 000_masterinventory
    project: main
    EE: Automation Hub Default execution environment
    credentials: manisbleserver
    playbook: ansiblemanager.yml
  schedules:
  - name: 000_jobschedule_ansibleautomationmanager_checkup
    type: job
    template: 000_ansibleautomationmanager_checkup
    description: Master job for ensuring connectivity
    local_time_zone: CET
    run_every_minute: '5'
    start: now
    end: never
  - name: 000_jobschedule_ansibleautomationmanager_update
    type: job
    template: 000_ansibleautomationmanager_update
    description: Master job updating automation manager
    local_time_zone: CET
    run_every_minute: '5'
    start: now
    end: never
  - name: 000_projectschedule_ansibleautomationmanager
    type: project
    project: main
    description: Master job for syncing project main
    local_time_zone: CET
    run_every_minute: '10'
    start: now
    end: never
  users:
    user_vault_path: project/openknowit/users
    description: AD integration is mandatory
  labels:
  - name: static
  - name: production
  - name: test


```
and the secret.yaml
```
---
manisble:
  vault:
  - name: myvault
    description: Credentials to access a hashicorp vault
    vault_id: https://vault.example.com
    vault_token: "/etc/manisble/vault.token"
  ssh:
  - name: manisbleserver
    username: manisble
    password: "/etc/manisble/manisbleserver.password"
    description: Credentials to login to manisble server and setup manisble service
    ssh_private_key: "/opt/manisble/manisbleserver_rsa"
    privilege_escalation_method: sudo
    privilege_escalation_username: root
    privilege_escalation_password: "/etc/manisble/manisbleserver.password"
  - name: productionserver
    username: root
    password: "/etc/manisble/productionserver.password"
    description: Credentials to login to productionservers
    ssh_private_key: "/opt/manisble/prodservers_rsa"
    privilege_escalation_method: sudo
    privilege_escalation_username: root
    privilege_escalation_password: xxx
  scm:
  - name: github
    username: Githubuser
    password: ''
    description: Credential to connect to git
    type: Source Control
    ssh_private_key: "/opt/manisble/github"
    kind: scm

```



![Python Logo](https://www.python.org/static/community_logos/python-logo.png "Sample inline image")

This is the README file for Mansible
you need this to access your ansible server

export TOWER_PASSWORD="<ADMIN PASSWORD>"
export TOWER_HOST="https://<ANSIBLE HOST>"
export TOWER_USERNAME="<ADMIN USER>"

```
---
manisble:
  vault:
    vault_addr: https://demo.vault.com
    vault_token: xcvcvbdsfgsdsdfsdfsdf
  ssh:
    name: manisbleserver
    username: manisble
    password: xxx
    descriptions: Credentials to login to manisble server and setup manisble service
    ssh_private_key: "/opt/manisble/id_rsa"
    privilege_escalation_method: xxx
scm: {}


```

### Thanks

Thanks to Jakob Holst for creating the original project, Kalm
