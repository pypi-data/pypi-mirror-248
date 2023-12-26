import subprocess, configparser, os, importlib, shlex, time
import paramiko as mod_ssh

def run_command(command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Read and print output in real-time
        for line in iter(process.stdout.readline, ''):
            print(line, end='')
            
        for line in iter(process.stderr.readline, ''):
            print(line, end='')
        
        process.wait()
        
        # Check for errors
        if process.returncode != 0:
            print("Error executing command. Return code: {}".format(process.returncode))
            return False
        
        return True
    
    except Exception as e:
        print("Error: {}".format(e))
        return False

def create_config_file(config_data, file_path):
    config = configparser.ConfigParser()

    for section, settings in config_data.items():
        config[section] = settings

    try:
        with open(file_path, 'w') as config_file:
            config.write(config_file)
        print(f"Config file successfully created at {file_path}")
    except Exception as e:
        print(f"Error: {e}")

def is_repo_up_to_date(path):
    try:
        cwd = os.getcwd()
        os.chdir(path)
        # Check if the local repository is up to date
        subprocess.run(['git', 'fetch'], check=True)
        result = subprocess.run(['git', 'status', '-uno'], capture_output=True, text=True, check=True)

        # If the repository is not up to date, pull the changes
        if "Your branch is behind" in result.stdout:
            print("Local repository is not up to date. Pulling changes...")
            subprocess.run(['git', 'pull'], check=True)
            print("Changes pulled successfully.")
        else:
            print("Local repository is up to date.")
        os.chdir(cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def install_required_modules(requirements):
    with open(requirements) as f:
        required_modules = f.read().splitlines()

    for module in required_modules:
        name = module.split("==")[0]

        spec = importlib.util.find_spec(name)
        if spec is None:
            print(f"Module {name} not found. Installing...")
            subprocess.call(['pip', 'install', module])
        else:
            print(f"Module {name} is already installed.")

def check_command_exists(command):
    try:
        subprocess.run(shlex.split(command), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def create_ssh_connection(hostname, username, keyfile, max_retries=10, retry_interval=5, port=22):
    retries = 0
    while retries < max_retries:
        try:
            # Create an SSH client
            ssh = mod_ssh.SSHClient()
            # Automatically add the server's host key (this is insecure, see comments below)
            ssh.set_missing_host_key_policy(mod_ssh.AutoAddPolicy())

            # Connect to the server with the specified keyfile
            ssh.connect(hostname, username=username, key_filename=keyfile,port=port)

            return ssh

        except Exception as e:
            print(f"Error creating SSH connection: {e}")
            retries += 1
            if retries < max_retries:
                print(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)

    raise RuntimeError(f"Failed to create SSH connection after {max_retries} attempts.")

def execute_ssh_command(ssh, command):
    try:
        channel = ssh.get_transport().open_session()
        channel.get_pty()
        channel.exec_command(command)

        # Print each line of the command output in real-time
        while True:
            if channel.recv_ready():
                line = channel.recv(1024).decode()
                if not line:
                    break
                print(line.strip())

            if channel.exit_status_ready():
                break

        # Print any errors
        error_output = channel.recv_stderr(1024).decode()
        if error_output:
            print(f"Error: {error_output}")
        return channel.recv_exit_status()
    
    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the SSH connection
        ssh.close()

def parse_tuple(input):
    return tuple(k.strip() for k in input[1:-1].split(','))
