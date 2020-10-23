import json
import os
import collections

def read_config(config_path):
  f = open(config_path, 'r')
  config = json.load(f)
  f.close()
  return config

def update_config(config, config_path):
  with open(config_path, 'w', newline='') as f:
    json.dump(config, f, indent=4)

def set_config(workspace, config_path, args):
  # initialize
  if not os.path.exists(config_path):
    new_config = collections.OrderedDict()
    new_config['site'] = 'atcoder'
    new_config['contest'] = None
    new_config['problem'] = None
    update_config(new_config, config_path)

  config = read_config(config_path)

  # set contest
  if args.contest != None:
    config['contest'] = args.contest

  # set problem
  if args.problem != None:
    config['problem'] = args.problem
  update_config(config, config_path)

  return config

def set_problem_id(workspace, config, config_path):
  contest_path = os.path.join(workspace, config['contest'])
  mtime = -float('inf')
  for d in os.listdir(contest_path):
    prob_path = os.path.join(contest_path, d, 'main.cpp')
    t = os.path.getmtime(prob_path)
    if mtime < t:
      mtime = t
      problem_id = d
  assert problem_id != None
  config['problem'] = problem_id
  config = update_config(config, config_path)
