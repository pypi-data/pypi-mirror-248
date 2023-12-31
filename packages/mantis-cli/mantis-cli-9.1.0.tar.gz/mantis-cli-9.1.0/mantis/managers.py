import json
import os
import datetime
import requests
from distutils.util import strtobool
from os import path
from os.path import dirname, normpath
from time import sleep

from mantis.crypto import Crypto
from mantis.environment import Environment
from mantis.helpers import CLI, Colors, load_config


class DefaultManager(object):
    environment_id = None

    def __init__(self, config=None, environment_id=None, mode='remote'):
        self.environment_id = environment_id
        self.mode = mode

        # init config
        self.init_config(config)

        # init environment
        self.init_environment()

        self.KEY = self.read_key()
        self.encrypt_deterministically = self.config.get('encrypt_deterministically', False)

    @property
    def host(self):
        return self.connection_details['host']

    @property
    def user(self):
        return self.connection_details['user']

    @property
    def port(self):
        return self.connection_details['port']

    def parse_ssh_connection(self, connection):
        return {
            'host': connection.split("@")[1].split(':')[0],
            'user': connection.split("@")[0].split('://')[1],
            'port': connection.split(":")[-1]
        }

    @property
    def connection_details(self):
        property_name = '_connection_details'
        details = {
            'host': None,
            'user': None,
            'port': None
        }

        if hasattr(self, property_name):
            return getattr(self, property_name)

        if 'local' in self.env.id:
            details = {
                'host': 'localhost',
                'user': None,
                'port': None
            }
        elif self.connection:
            if self.connection.startswith('ssh://'):
                details = self.parse_ssh_connection(self.connection)

            elif self.connection.startswith('context://'):
                context_name = self.connection.replace('context://', '')

                # TODO: move to own method
                context_details = json.loads(os.popen(f'docker context inspect {context_name}').read())

                try:
                    ssh_host = context_details[0]["Endpoints"]["docker"]["Host"]
                    details = self.parse_ssh_connection(ssh_host)
                except IndexError:
                    pass
            else:
                raise CLI.error(f'Invalid connection protocol {self.connection}')

        # set to singleton
        setattr(self, property_name, details)

        # set project path
        self.project_path = self.config.get('project_path', f'/home/{self.user}/public_html/web')

        return details

    @property
    def docker_connection(self):
        if 'local' in self.env.id:
            return ''

        if self.mode == 'remote':
            if self.connection.startswith('ssh://'):
                return f'DOCKER_HOST="{self.connection}"'
            elif self.connection.startswith('context://'):
                context_name = self.connection.replace('context://', '')
                return f'DOCKER_CONTEXT={context_name}'

        return ''

    def init_config(self, config):
        self.config_file = os.environ.get('MANTIS_CONFIG', 'configs/mantis.json')
        self.config = config or load_config(self.config_file)

        configs_folder_path = self.config.get('configs_folder_path', '')
        configs_folder_name = self.config.get('configs_folder_name', 'configs')
        self.configs_path = f'{configs_folder_path}{configs_folder_name}'
        self.configs_compose_folder = self.config.get('configs_compose_folder', 'compose')
        self.key_file = path.join(f'{dirname(self.config_file)}', 'mantis.key')

        # Get environment settings
        self.PROJECT_NAME = self.config['project_name']

    def init_environment(self):
        self.env = Environment(
            environment_id=self.environment_id,
            folder=self.config.get('environment_folder', 'environments'),
            file_prefix=self.config.get('environment_file_prefix', '')
        )

        # connection
        self.connection = self.config.get('connections', {}).get(self.env.id, None)

        # containers
        # self.CONTAINER_PREFIX = self.config['containers']['prefix']
        self.CONTAINER_PREFIX = self.PROJECT_NAME
        self.IMAGE_PREFIX = self.PROJECT_NAME

        if 'containers' in self.config:
            # TODO: refactor
            self.CONTAINER_WEBSERVER = f"{self.CONTAINER_PREFIX}{self.get_container_suffix('webserver')}"

            self.compose_name = self.config['compose']['name']
            self.COMPOSE_PREFIX = 'docker-compose' if self.compose_name == '' else f'docker-compose.{self.compose_name}'
            self.compose_config = f'{self.configs_path}/{self.configs_compose_folder}/{self.COMPOSE_PREFIX}.{self.env.id}.yml',

        # TODO: refactor
        self.DATABASE = self.config.get('db', 'postgres')
        self.CACHE = self.config.get('cache', 'redis')
        self.WEBSERVER = self.config.get('webserver', 'nginx')

        self.database_config = f'{self.configs_path}/{self.DATABASE}/{self.env.file_prefix}{self.env.id}.conf'
        self.cache_config = f'{self.configs_path}/{self.CACHE}/{self.env.file_prefix}{self.env.id}.conf'
        self.webserver_html = f'{self.configs_path}/{self.WEBSERVER}/html/'
        self.webserver_config_proxy = f'{self.configs_path}/{self.WEBSERVER}/proxy_directives.conf'
        self.webserver_config_default = f'{self.configs_path}/{self.WEBSERVER}/default.conf'
        self.webserver_config_site = f'{self.configs_path}/{self.WEBSERVER}/sites/{self.env.file_prefix}{self.env.id}.conf'
        self.htpasswd = f'{self.configs_path}/{self.WEBSERVER}/secrets/.htpasswd'

    def check_environment_encryption(self, env_file):
        decrypted_environment = self.decrypt_env(env_file=env_file, return_value=True)        # .env.encrypted
        loaded_environment = self.env.load(env_file)                                          # .env

        if decrypted_environment is None:
            env_file_encrypted = f'{env_file}.encrypted'
            CLI.error(f'Encrypted environment {env_file_encrypted} is empty!')

        if loaded_environment is None:
            CLI.error(f'Loaded environment {env_file} is empty!')

        if loaded_environment != decrypted_environment:
            CLI.danger('Encrypted and decrypted environment files do NOT match!')

            if loaded_environment is None:
                CLI.danger('Decrypted env from file is empty !')
            elif decrypted_environment is None:
                CLI.danger('Decrypted env is empty !')
            else:
                set1 = set(loaded_environment.items())
                set2 = set(decrypted_environment.items())
                difference = set1 ^ set2

                for var in dict(difference).keys():
                    CLI.info(var, end=': ')

                    encrypted_value = loaded_environment.get(var, '')

                    if encrypted_value == '':
                        CLI.bold('-- empty --', end=' ')
                    else:
                        CLI.warning(encrypted_value, end=' ')

                    print(f'[{env_file}]', end=' / ')

                    decrypted_value = decrypted_environment.get(var, '')

                    if decrypted_value == '':
                        CLI.bold('-- empty --', end=' ')
                    else:
                        CLI.danger(decrypted_value, end=' ')

                    print(f'[{env_file}.encrypted]', end='\n')

        else:
            CLI.success(f'Encrypted and decrypted environments DO match [{env_file}]...')

    def read_key(self):
        if not os.path.exists(self.key_file):
            return None

        with open(self.key_file, "r") as f:
            return f.read()

    def generate_key(self):
        CLI.info(f'Deterministic encryption: ', end='')
        CLI.warning(self.encrypt_deterministically)

        key = Crypto.generate_key(self.encrypt_deterministically)
        CLI.bold('Generated cryptography key: ', end='')
        CLI.pink(key)
        CLI.danger(f'Save it to {self.key_file} and keep safe !!!')

    def encrypt_env(self, params='', env_file=None, return_value=False):
        if env_file is None:
            CLI.info(f'Environment file not specified. Walking all environment files...')

            values = {}

            for env_file in self.env.files:
                value = self.encrypt_env(params=params, env_file=env_file, return_value=return_value)
                if return_value:
                    values.update(value)

            return values if return_value else None

        CLI.info(f'Encrypting environment file {env_file}...')
        env_file_encrypted = f'{env_file}.encrypted'

        if not self.KEY:
            CLI.error('Missing mantis key! (%s)' % self.key_file)

        decrypted_lines = self.env.read(env_file)

        if not decrypted_lines:
            return None

        encrypted_lines = []
        encrypted_env = {}

        for line in decrypted_lines:
            if Environment.is_valid_line(line):
                var, decrypted_value = Environment.parse_line(line)
                encrypted_value = Crypto.encrypt(decrypted_value, self.KEY, self.encrypt_deterministically)
                encrypted_lines.append(f'{var}={encrypted_value}')
                encrypted_env[var] = encrypted_value
            else:
                encrypted_lines.append(line)

            if not return_value and 'force' not in params:
                print(encrypted_lines[-1])

        if return_value:
            return encrypted_env

        if 'force' in params:
            Environment.save(env_file_encrypted, encrypted_lines)
            CLI.success(f'Saved to file {env_file_encrypted}')
        else:
            # save to file?
            CLI.warning(f'Save to file {env_file_encrypted}?')

            save_to_file = input("(Y)es or (N)o: ")

            if save_to_file.lower() == 'y':
                Environment.save(env_file_encrypted, encrypted_lines)
                CLI.success(f'Saved to file {env_file_encrypted}')
            else:
                CLI.warning(f'Save it to {env_file_encrypted} manually.')

    def decrypt_env(self, params='', env_file=None, return_value=False):
        if env_file is None:
            CLI.info(f'Environment file not specified. Walking all environment files...')

            values = {}

            for encrypted_env_file in self.env.encrypted_files:
                env_file = encrypted_env_file.rstrip('.encrypted')
                value = self.decrypt_env(params=params, env_file=env_file, return_value=return_value)
                if return_value:
                    values.update(value)

            return values if return_value else None

        env_file_encrypted = f'{env_file}.encrypted'

        if not return_value:
            CLI.info(f'Decrypting environment file {env_file_encrypted}...')

        if not self.KEY:
            CLI.error('Missing mantis key!')

        encrypted_lines = self.env.read(env_file_encrypted)

        if encrypted_lines is None:
            return None

        if not encrypted_lines:
            return {}

        decrypted_lines = []
        decrypted_env = {}

        for line in encrypted_lines:
            if Environment.is_valid_line(line):
                var, encrypted_value = Environment.parse_line(line)
                decrypted_value = Crypto.decrypt(encrypted_value, self.KEY, self.encrypt_deterministically)
                decrypted_lines.append(f'{var}={decrypted_value}')
                decrypted_env[var] = decrypted_value
            else:
                decrypted_lines.append(line)

            if not return_value and 'force' not in params:
                print(decrypted_lines[-1])

        if return_value:
            return decrypted_env

        if 'force' in params:
            Environment.save(env_file, decrypted_lines)
            CLI.success(f'Saved to file {env_file}')
        else:
            # save to file?
            CLI.warning(f'Save to file {env_file}?')

            save_to_file = input("(Y)es or (N)o: ")

            if save_to_file.lower() == 'y':
                Environment.save(env_file, decrypted_lines)
                CLI.success(f'Saved to file {env_file}')
            else:
                CLI.warning(f'Save it to {env_file} manually.')

    def check_env(self):
        # check if pair file exists
        for encrypted_env_file in self.env.encrypted_files:
            env_file = encrypted_env_file.rstrip('.encrypted')
            if not os.path.exists(env_file):
                CLI.warning(f'Environment file {env_file} does not exist')

        for env_file in self.env.files:
            env_file_encrypted = f'{env_file}.encrypted'

            # check if pair file exists
            if not os.path.exists(env_file_encrypted):
                CLI.warning(f'Environment file {env_file_encrypted} does not exist')
                continue

            # check encryption values
            self.check_environment_encryption(env_file)

    def cmd(self, command):
        command = command.strip()

        error_message = "Error during running command '%s'" % command

        try:
            if os.system(command) != 0:
                CLI.error(error_message)
                # raise Exception(error_message)
        except:
            CLI.error(error_message)
            # raise Exception(error_message)

    def contexts(self):
        self.cmd('docker context ls')

    def create_context(self):
        CLI.info('Creating docker context')
        protocol = input("Protocol: (U)nix or (S)sh: ")

        if protocol.lower() == 'u':
            protocol = 'unix'
            socket = input("Socket: ")
            host = f'{protocol}://{socket}'
        elif protocol.lower() == 's':
            protocol = 'ssh'
            host_address = input("Host address: ")
            username = input("Username: ")
            port = input("Port: ")
            host = f'{protocol}://{username}@{host_address}:{port}'
        else:
            CLI.error('Invalid protocol')
            exit()

        endpoint = f'host={host}'

        # CLI.warning(f'Endpoint: {endpoint}')

        description = input("Description: ")
        name = input("Name: ")

        command = f'docker context create \\\n'\
                  f'    --docker {endpoint} \\\n'\
                  f'    --description="{description}" \\\n'\
                  f'    {name}'

        CLI.warning(command)

        if input("Confirm? (Y)es/(N)o: ").lower() != 'y':
            CLI.error('Canceled')
            exit()

        # create context
        self.cmd(command)
        self.contexts()

    def get_container_suffix(self, service):
        delimiter = '-'
        return self.config.get('containers', {}).get('suffixes', {}).get(service, f'{delimiter}{service}')

    def get_container_name(self, service):
        suffix = self.get_container_suffix(service)
        return f'{self.CONTAINER_PREFIX}{suffix}'.replace('_', '-')

    def get_image_suffix(self, service):
        delimiter = '_'
        return self.config.get('containers', {}).get('suffixes', {}).get(service, f'{delimiter}{service}')

    def get_image_name(self, service):
        suffix = self.get_image_suffix(service)
        return f'{self.IMAGE_PREFIX}{suffix}'.replace('-', '_')

    def healthcheck(self, retries=5, service=None, break_if_successful=False):
        if service:
            container = self.get_container_name(service)
            target = container
            method = 'gunicorn'  # TODO: method per service
            success_responses = [200]
        else:
            target = f'http://{self.host}'
            method = 'curl'
            success_responses = [200, 401]

        CLI.info(f'Health-checking {Colors.YELLOW}{target}{Colors.ENDC} ({method})...')
        retries = int(retries)
        last_status = False
        status_code = None

        for retry in range(retries):
            if service is None:
                response = requests.get(target)
                status_code = response.status_code
                success = status_code in success_responses
                result = status_code
            else:
                # command = 'curl -s -o /dev/null -w "%%{http_code}" -L -H "Host: %s" %s' % (self.host, url)
                command = "pgrep -x gunicorn -d ' '"
                pids = self.docker(f'container exec -it {container} {command}', return_output=True)
                pids = pids.strip()
                pids = [] if pids == '' else pids.split(' ')
                success = len(pids) > 0
                result = ', '.join(pids)

            if success:
                print(f'#{retry}: {Colors.GREEN}Success{Colors.ENDC}. Result: {result}')
                last_status = True

                if break_if_successful:
                    return last_status
            else:
                print(f'#{retry}: {Colors.RED}Fail{Colors.ENDC}. Result: {result}')
                last_status = False

            if retries > 1:
                sleep(1)

        return last_status

    def build(self, params=''):
        CLI.info(f'Building...')
        CLI.info(f'Params = {params}')

        for service, image in self.config['services'].items():
            self.build_image(service, params)

    def build_image(self, service, params=''):
        service_build = self.config['services'][service]
        image = service_build.get('image', self.get_image_name(service))
        dockerfile = f"{self.config['build'].get('context', '.')}{service_build['dockerfile']}"
        CLI.info(f'Building image {image} from {dockerfile}...')

        if not os.path.exists(dockerfile):
            CLI.error(f'Dockerfile {dockerfile} not found')

        DOCKER_REPOSITORY = service_build['repository']
        DOCKER_TAG = self.config['build']['tag']
        DOCKER_REPOSITORY_AND_TAG = f'{DOCKER_REPOSITORY}:{DOCKER_TAG}'

        CLI.warning(f'Building Docker image [{DOCKER_REPOSITORY_AND_TAG}]...')

        build_args = self.config['build']['args']
        build_args = ','.join(map('='.join, build_args.items()))
        build_kit = self.config['build']['kit']
        build_kit = 'DOCKER_BUILDKIT=1' if build_kit else ''
        time = 'time ' if build_kit == '' else ''

        if build_args != '':
            build_args = build_args.split(',')
            build_args = [f'--build-arg {arg}' for arg in build_args]
            build_args = ' '.join(build_args)

        CLI.info(f'Kit = {build_kit}')
        CLI.info(f'Args = {build_args}')

        self.cmd(f'{time}{build_kit} docker build . {build_args} -t {image} -f {dockerfile} {params}')

    def push(self, params=''):
        CLI.info(f'Pushing...')
        CLI.info(f'Params = {params}')

        for service, image in self.config['services'].items():
            self.push_image(service, params)

    def push_image(self, service, params):
        service_build = self.config['services'][service]
        image = service_build.get('image', self.get_image_name(service))
        CLI.info(f'Pushing image {image}...')

        DOCKER_REPOSITORY = service_build['repository']
        DOCKER_TAG = self.config['build']['tag']
        DOCKER_REPOSITORY_AND_TAG = f'{DOCKER_REPOSITORY}:{DOCKER_TAG}'

        steps = 2

        CLI.step(1, steps, f'Tagging Docker image [{DOCKER_REPOSITORY_AND_TAG}]...')
        self.cmd(f'docker tag {image} {DOCKER_REPOSITORY_AND_TAG}')
        CLI.success(f'Successfully tagged {DOCKER_REPOSITORY_AND_TAG}')

        CLI.step(2, steps, f'Pushing Docker image [{DOCKER_REPOSITORY_AND_TAG}]...')
        self.cmd(f'docker push {DOCKER_REPOSITORY_AND_TAG}')
        CLI.success(f'Successfully pushed {DOCKER_REPOSITORY_AND_TAG}')

    def pull(self):
        CLI.info('Pulling docker image...')
        self.docker_compose('pull')

    def upload(self, context='services'):
        if not self.connection:
            return CLI.warning('Connection not defined. Skipping uploading files')

        mapping = {
            'services': {
                self.database_config: f'{self.project_path}/{self.configs_path}/{self.DATABASE}/',
                self.cache_config: f'{self.project_path}/configs/{self.CACHE}/',
                self.webserver_html: f'{self.project_path}/configs/{self.WEBSERVER}/html/',
                self.webserver_config_default: f'{self.project_path}/configs/{self.WEBSERVER}/',
                self.webserver_config_proxy: f'{self.project_path}/configs/{self.WEBSERVER}/',
                self.webserver_config_site: f'{self.project_path}/configs/{self.WEBSERVER}/sites/',
                self.htpasswd: f'{self.project_path}/configs/{self.WEBSERVER}/secrets/'
            }

            # TODO: other contexts
        }

        if context == 'all':
            self.upload('services')
            self.upload('compose')
            self.upload('mantis')
        elif context == 'services':
            CLI.warning('Uploading configs for context "services" [webserver, database, cache, htpasswd]')
        elif context == 'compose':
            CLI.warning('Uploading configs for context "compose" [docker compose configs and environment]')
        elif context == 'mantis':
            CLI.warning('Uploading configs for mantis [mantis.json]')
        else:
            CLI.error(f'Unknown context "{context}". Available: services, compose, mantis or all')

        if self.env.id == 'local':
            print('Skipping for local...')
        elif self.mode == 'host':
            CLI.warning('Not uploading due to host mode! Be sure your configs on host are up to date!')
        else:
            CLI.info('Uploading...')

            # TODO: refactor
            if context == 'services':
                for local_path, remote_path in mapping['services'].items():
                    if os.path.exists(local_path):
                        self.cmd(f'rsync -arvz -e \'ssh -p {self.port}\' -rvzh --progress {local_path} {self.user}@{self.host}:{remote_path}')
                    else:
                        CLI.info(f'{local_path} does not exists. Skipping...')
            elif context == 'mantis':
                if os.path.exists(self.config_file):
                    self.cmd(f'rsync -arvz -e \'ssh -p {self.port}\' -rvzh --progress {self.config_file} {self.user}@{self.host}:{self.project_path}/configs/')
                else:
                    CLI.info(f'{self.config_file} does not exists. Skipping...')

            elif context == 'compose':
                for env_file in self.env.files:
                    if os.path.exists(env_file):
                        self.cmd(f'rsync -arvz -e \'ssh -p {self.port}\' -rvzh --progress {env_file} {self.user}@{self.host}:{self.project_path}/configs/environments/')  # TODO: paths
                    else:
                        CLI.info(f'{env_file} does not exists. Skipping...')

                if os.path.exists(self.compose_config):
                    self.cmd(f'rsync -arvz -e \'ssh -p {self.port}\' -rvzh --progress {self.compose_config} {self.user}@{self.host}:{self.project_path}/configs/{self.configs_compose_folder}/')
                else:
                    CLI.info(f'{self.compose_config} does not exists. Skipping...')

    def restart(self):
        CLI.info('Restarting...')
        steps = 4

        # run down project containers
        CLI.step(1, steps, 'Running down project containers...')
        self.down()

        # stop and remove all other containers
        CLI.step(2, steps, 'Stopping and removing remaining containers...')

        containers = self.get_containers()

        for container in containers:
            self.docker(f'container stop {container}', return_output=True)
            self.docker(f'container rm {container}')

        # recreate project
        CLI.step(3, steps, 'Recreating project containers...')
        self.up()

        # clean
        CLI.step(4, steps, 'Prune Docker images and volumes')
        self.clean()

    def deploy(self):
        CLI.info('Deploying...')
        self.clean()
        self.upload()
        self.pull()
        self.reload()

    def reload(self):
        CLI.info('Reloading containers...')
        zero_downtime_services = self.config['containers']['deploy']['zero_downtime']
        restart_services = self.config['containers']['deploy']['restart']

        steps = 4

        step = 1
        CLI.step(step, steps, f'Zero downtime services: {zero_downtime_services}')

        for service in zero_downtime_services:
            container = self.get_container_name(service)

            # run new container
            self.docker_compose(f'run -d --service-ports --name={container}-new {service}')

            # healthcheck
            # TODO: configurable retries number
            num_retries = 30
            # num_retries = 20

            self.healthcheck(retries=num_retries, service=f'{service}-new', break_if_successful=True)

            # rename old container
            CLI.info(f'Renaming old container [{container}-old]...')

            if container in self.get_containers():
                self.docker(f'container rename {container} {container}-old')
            else:
                CLI.info(f'{container}-old was not running')

            # rename new container
            CLI.info(f'Renaming new container [{container}]...')
            self.docker(f'container rename {container}-new {container}')

        step += 1
        # TODO: hook into this step from extension
        CLI.step(step, steps, 'Reloading webserver...')
        self.docker(f'exec -it {self.CONTAINER_WEBSERVER} {self.WEBSERVER} -s reload')

        step += 1
        CLI.step(step, steps, f'Stopping old zero downtime services: {zero_downtime_services}')

        for service in zero_downtime_services:
            container = self.get_container_name(service)

            if container in self.get_containers():
                CLI.info(f'Stopping old container [{container}-old]...')
                self.docker(f'container stop {container}-old')

                CLI.info(f'Removing old container [{container}-old]...')
                self.docker(f'container rm {container}-old')
            else:
                CLI.info(f'{container}-old was not running')

        step += 1
        CLI.step(step, steps, f'Restart services: {restart_services}')

        for service in restart_services:
            container = self.get_container_name(service)

            CLI.underline(f'Recreating {service} container ({container})...')

            if container in self.get_containers():
                CLI.info(f'Stopping container [{container}]...')
                self.docker(f'container stop {container}')

                CLI.info(f'Removing container [{container}]...')
                self.docker(f'container rm {container}')
            else:
                CLI.info(f'{container} was not running')

            CLI.info(f'Creating new container [{container}]...')
            self.docker_compose(f'run -d --service-ports --name={container} {service}')

    def stop(self, params=None):
        CLI.info('Stopping containers...')

        containers = self.get_containers() if not params else params.split(' ')

        steps = len(containers)

        for index, container in enumerate(containers):
            CLI.step(index + 1, steps, f'Stopping {container}')
            self.docker(f'container stop {container}')

    def start(self, params=''):
        CLI.info('Starting containers...')

        containers = self.get_containers() if not params else params.split(' ')

        steps = len(containers)

        for index, container in enumerate(containers):
            CLI.step(index + 1, steps, f'Starting {container}')
            self.docker(f'container start {container}')

    def run(self, params):
        CLI.info(f'Running {params}...')
        self.docker_compose(f'run {params}')

    def up(self, params=''):
        CLI.info(f'Starting up {params}...')
        self.docker_compose(f'up {params} -d')

    def down(self, params=''):
        CLI.info(f'Running down {params}...')
        self.docker_compose(f'down {params}')

    def remove(self, params=''):
        CLI.info('Removing containers...')

        containers = self.get_containers() if params == '' else params.split(' ')

        steps = len(containers)

        for index, container in enumerate(containers):
            CLI.step(index + 1, steps, f'Removing {container}')
            self.docker(f'container rm {container}')

    def clean(self):  # todo clean on all nodes
        CLI.info('Cleaning...')
        # self.docker(f'builder prune')
        self.docker(f'system prune --volumes --force')
        # self.docker(f'container prune')
        # self.docker(f'container prune --force')

    def reload_webserver(self):
        CLI.info('Reloading webserver...')
        self.docker(f'exec -it {self.CONTAINER_WEBSERVER} {self.WEBSERVER} -s reload')

    def status(self):
        CLI.info('Getting status...')
        steps = 2

        CLI.step(1, steps, 'List of Docker images')
        self.docker(f'image ls')

        CLI.step(2, steps, 'Docker containers')
        self.docker(f'container ls -a --size')

    def networks(self):
        CLI.info('Getting networks...')
        CLI.warning('List of Docker networks')

        networks = self.docker('network ls', return_output=True)
        networks = networks.strip().split('\n')

        for index, network in enumerate(networks):
            network_data = list(filter(lambda x: x != '', network.split(' ')))
            network_name = network_data[1]

            if index == 0:
                print(f'{network}\tCONTAINERS')
            else:
                containers = self.docker(f'network inspect -f \'{{{{ range $key, $value := .Containers }}}}{{{{ .Name }}}} {{{{ end }}}}\' {network_name}', return_output=True)
                containers = ', '.join(containers.split())
                print(f'{network}\t{containers}'.strip())

    def logs(self, params=None):
        CLI.info('Reading logs...')

        containers = params.split(' ') if params else self.get_containers()
        lines = '--tail 1000 -f' if params else '--tail 10'
        steps = len(containers)

        for index, container in enumerate(containers):
            CLI.step(index + 1, steps, f'{container} logs')
            self.docker(f'logs {container} {lines}')

    def bash(self, params):
        CLI.info('Running bash...')
        self.docker(f'exec -it --user root {params} /bin/bash')
        # self.docker_compose(f'run --entrypoint /bin/bash {container}')

    def sh(self, params):
        CLI.info('Logging to container...')
        self.docker(f'exec -it --user root {params} /bin/sh')

    def exec(self, params):
        container, command = params.split(' ', maxsplit=1)
        CLI.info(f'Executing command "{command}" in container {container}...')
        self.docker(f'exec -it {container} {command}')

    def get_containers(self):
        containers = self.docker(f'container ls -a --format \'{{{{.Names}}}}\'', return_output=True)\
            .strip('\n').strip().split('\n')

        # Remove empty strings
        containers = list(filter(None, containers))

        print(containers)
        return containers

    def get_containers_starting_with(self, start_with):
        return [i for i in self.get_containers() if i.startswith(start_with)]

    def docker(self, command, return_output=False):
        if return_output:
            return os.popen(f'{self.docker_connection} docker {command}').read()

        self.cmd(f'{self.docker_connection} docker {command}')

    def docker_compose(self, command):
        self.cmd(f'{self.docker_connection} docker compose -f {self.compose_config} --project-name={self.PROJECT_NAME} {command}')
