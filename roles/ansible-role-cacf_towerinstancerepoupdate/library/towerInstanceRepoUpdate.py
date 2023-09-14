#!/usr/bin/python3 -u

# Copyright: (c) 2020, Prabir Sengupta <psengupt@in.ibm.com>
# IBM internal usage

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
Module name: towerInstanceRepoUpdate
Description: Module is used migrate event integration roles from global Organisation ( default: Continuous-Engineering ) into instance specific Org
Arguments:
  globalOrg:
    required: false
    description: This contain global Org name from where we want to migrate role ( default: Continuous-Engineering ).
  instanceOrg:
    required: true
    description: This contain instance Org name where we want migrate role into.
  roleName:
    required: true
    description: This contain role name which we want to migrate.
  versionName:
    required: true
    description: This contain role version which we want to migrate.
Author: Prabir Sengupta
'''

EXAMPLES = r'''
- name: Migrating role from global org into instace org
  towerInstanceRepoUpdate:
    globalOrg: <Global Org name>
    instanceOrg: <Instance Org name>
    roleName: <role name>
    version: <role version name>
    
'''
