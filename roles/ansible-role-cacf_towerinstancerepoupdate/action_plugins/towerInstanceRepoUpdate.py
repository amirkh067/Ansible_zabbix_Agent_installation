#!/usr/bin/python3 -u


# Copyright: (c) 2020, Prabir Sengupta <psengupt@in.ibm.com>
# IBM internal usage


from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError
import json
import os
import requests
import re


class ActionModule(ActionBase):
    
  def run(self, tmp=None, task_vars=None):
    globalOrg = self._task.args.pop('globalOrg', None)
    instanceOrg = self._task.args.pop('instanceOrg', None)
    role_name = self._task.args.pop('roleName', None)
    version_name = self._task.args.pop('versionName', "NA")
    for param_val in [globalOrg, instanceOrg, role_name]:
      if param_val is None:
        raise AnsibleError(param_val+'is None')

    if version_name!='NA':
      git_token=os.environ['EVNTINTE_GIT_TOKEN']
      gitHeader={ "Content-Type": "application/json", "Authorization": "token "+git_token.strip(), "Accept": "application/vnd.github.mercy-preview+json" }
      instance_search_uri="https://github.kyndryl.net/api/v3/repos/{}/{}".format(instanceOrg, role_name)
      instance_search_release_uri="https://github.kyndryl.net/api/v3/search/repositories?q=v{}Updated+in:description+repo:{}/{}".format(version_name, instanceOrg, role_name)
      if re.match('^\d{1,3}\.\d{1,3}\.?\d*$', version_name):
        global_search_uri="https://github.kyndryl.net/api/v3/repos/{}/{}/git/refs/tags/{}".format(globalOrg, role_name, version_name)
      else:
        global_search_uri="https://github.kyndryl.net/api/v3/repos/{}/{}/branches/{}".format(globalOrg, role_name, version_name)
      instance_repo_create_uri="https://github.kyndryl.net/api/v3/orgs/{}/repos".format(instanceOrg)
      updateInstance_repo_topic_uri="https://github.kyndryl.net/api/v3/repos/{}/{}/topics".format(instanceOrg, role_name)
      instance_repo_delete_uri="https://github.kyndryl.net/api/v3/repos/{}/{}".format(instanceOrg, role_name)
      create_payload={ \
                            "name": role_name,\
                            "description": "v"+version_name+"Updated",\
                            "homepage": "https://github.kyndryl.net/"+instanceOrg,\
                            "public": "true",\
                            "has_issues": "true",\
                            "has_projects": "true"\
        }
      repotopic={ \
        "names": [\
        "globaldev",\
        "eventintegration",\
              ]\
        }
      try:
        search_req=requests.get(instance_search_uri, headers=gitHeader, verify=False)
        gitcmd="(mkdir git_repo && cd git_repo && git clone https://{}@github.kyndryl.net/{}/{}.git -b {} && cd {} && git remote add origin1 https://{}@github.kyndryl.net/{}/{}.git && git checkout -b master && git push origin1 master && cd ../.. && rm -rf git_repo/)>/dev/null 2>&1".format(git_token, globalOrg, role_name, version_name, role_name, git_token, instanceOrg, role_name)
        print("Validating https://github.kyndryl.net/"+instanceOrg+"/"+role_name)
        if search_req.status_code != 200:
          search_req=requests.get(global_search_uri, headers=gitHeader, verify=False)
          if search_req.status_code == 200:
            print("Creating "+role_name+" in "+instanceOrg)
            create_req=requests.post(instance_repo_create_uri, headers=gitHeader, data=json.dumps(create_payload), verify=False)
            if create_req.status_code == 201:
              topic_update=requests.put(updateInstance_repo_topic_uri, headers=gitHeader, data=json.dumps(repotopic), verify=False)
              #if topic_update.status_code == 200:
              os.system(gitcmd)
              print("#############################################################################################################")
              print(role_name+":"+version_name+" has been created in https://github.kyndryl.net/"+instanceOrg)
              print("#############################################################################################################")
            else:
              print("#############################################################################################################")
              print("Create status code: "+create_req.status_code)
              print("Unable to create "+role_name+":"+version_name+" in https://github.kyndryl.net/"+instanceOrg)
              print("Please validate github credential on https://github.kyndryl.net/"+instanceOrg)
              print("#############################################################################################################")
          else:
            print("#############################################################################################################")
            print(role_name+":"+version_name+" does not exist in https://github.kyndryl.net/"+globalOrg)
            print("#############################################################################################################")
        else:
          search_instance_version_req=requests.get(instance_search_release_uri, headers=gitHeader, verify=False)
          print("Validating version: "+version_name+" in https://github.kyndryl.net/"+instanceOrg+"/"+role_name)
          search_opt=json.loads(search_instance_version_req.text)
          if search_opt["total_count"]==0:
            print("#############################################################################################################")
            print(role_name+":"+version_name+" does not exist in https://github.kyndryl.net/"+instanceOrg+",  Updating https://github.kyndryl.net/"+instanceOrg+"/"+role_name)
            print("#############################################################################################################")
            search_req=requests.get(global_search_uri, headers=gitHeader, verify=False)
            if search_req.status_code == 200:
              delete_req=requests.delete(instance_repo_delete_uri, headers=gitHeader, verify=False)
              if delete_req.status_code == 204:
                create_req=requests.post(instance_repo_create_uri, headers=gitHeader, data=json.dumps(create_payload), verify=False)
                if create_req.status_code == 201:
                  os.system(gitcmd)
                  print("https://github.kyndryl.net/"+instanceOrg+"/"+role_name+" has been created")
              elif delete_req.status_code == 403:
                print("Delete permission issue in https://github.kyndryl.net/"+instanceOrg)
            else:
              print("version: "+version_name+" does not esist in https://github.kyndryl.net/"+globalOrg)
          else:
            print("#############################################################################################################")
            print("version: "+version_name+" already exist in https://github.kyndryl.net/"+instanceOrg)
            print("#############################################################################################################")
      except Exception as e:
        print(e.args)
    return {role_name: "Completed"}
