## Intro

Libsaas extension for gitlab support.

See: https://github.com/ducksboard/libsaas.git

## Installation

~~~bash
sudo apt-get install python-pip
sudo pip install libsaas
~~~

## Install libsaas_gitlab

~~~bash
sudo python setup.py install
~~~

## Run tests

~~~bash
python setup.py test
~~~

## Usage

Provide url and token below. And some parts like IDs and so on need to be adjusted.

~~~python
import json
import libsaas_gitlab as gitlab

gitlabServer = "http//gitlab.com"
token        = "8adf3984joiajf"
service      = gitlab.Gitlab(gitlabServer, token)

print json.dumps(service.issues().get({'state':"opened", 'labels':'feature'}), indent=4, sort_keys=True)
print json.dumps(service.project(257579).issue(240301).get(), indent=4, sort_keys=True)
print json.dumps(service.users().get("b-sh"), indent=4, sort_keys=True)

projects = service.projects().get();
print json.dumps(projects, indent=4, sort_keys=True)

for project in projects:
  print "=======mr========"
  mrs = service.project(project['id']).merge_requests().get()
  if mrs:
    for mr in mrs:
      print "Getting comments"
      comments = service.project(project['id']).merge_request(mr['id']).comments().get()
      print "Print comments"
      print json.dumps(comments, indent=4, sort_keys=True)
~~~

## Client applications

* git-gitlab: git command line interface to gitlab https://gitlab.com/bor-sh/git-gitlab
