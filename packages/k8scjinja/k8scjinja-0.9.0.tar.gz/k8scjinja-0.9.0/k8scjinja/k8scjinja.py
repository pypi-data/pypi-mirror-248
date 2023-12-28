import jinja2
import argparse
import sys
import os
import yaml


class Environment:
    def __init__(self, envs=None):
        if envs is None:
            envs = []
        self.envs = envs
    
    def __str__(self):
        for env in reversed(self.envs):
            return str(env)
        return ''
    
    def __getattr__(self, name):
        new_envs = []
        for env in reversed(self.envs):
            if name in env:
                if not (isinstance(env[name], list) or isinstance(env[name], dict)) and not new_envs:
                    return env[name]
                new_envs.append(env[name])
        new_envs.reverse()
        return Environment(new_envs)
    
    def add_environment(self, environment):
        self.envs.append(environment)


def run():
    parser = argparse.ArgumentParser(prog='ProgramName', description='What the program does', epilog='Text at the bottom of help')
    parser.add_argument('-t', '--template_filename', required=True)
    parser.add_argument('-d', '--destination_filename', required=False)
    parser.add_argument('-e', '--environment_filename', required=False)
    parser.add_argument('-i', '--input', action='store_true')
    args = parser.parse_args()

    if not os.path.isfile(args.template_filename):
        print(f'File <{args.template_filename}> not found. Please, check that you provided the path relatively to $PWD variable.')
        return 1
    if args.destination_filename and not os.path.isfile(args.destination_filename):
        print(f'File <{args.destination_filename}> not found. Please, check that you provided the path relatively to $PWD variable.')
        return 2

    if args.input:
        print('Waiting for environment in stdin...', end=' ')
        str_env = sys.stdin.read()
        print('received')
    else:
        environment_filename = args.environment_filename
        if environment_filename is None:
            environment_filename = os.path.expanduser('~/.k8scjinja.env.yaml')
        if not os.path.isfile(environment_filename):
            print(f'Environment file <{environment_filename}> not found. Please, specify correct environment file with -e option')
            return 3
        with open(environment_filename, 'r') as fp:
            str_env = fp.read()

    envs = str_env.split('---')
    env = Environment()
    for env_part in envs:
        template = jinja2.Environment(loader=jinja2.BaseLoader).from_string(env_part)
        env_rendered = template.render(env=env)
        yaml_env = yaml.load(env_rendered, yaml.FullLoader)
        env.add_environment(yaml_env)
    
    print(f'Rendering <{args.template_filename}>...', end=' ')
    with open(args.template_filename, 'r') as fp:
        rtemplate = jinja2.Environment(loader=jinja2.BaseLoader).from_string(fp.read())
    data = rtemplate.render(env=env)
    print('done')

    destination_filename = args.destination_filename
    if destination_filename is None:
        splitted = args.template_filename.split('.')
        if len(splitted) > 1:
            del splitted[-1]
            destination_filename = '.'.join(splitted)
        else:
            destination_filename = f'{args.template_filename}.rendered'
    
    print(f'Writing result to <{destination_filename}>...', end=' ')
    with open(destination_filename, 'w') as fp:
        fp.write(data)
    print('done')
    return 0


if __name__ == '__main__':
    sys.exit(run())