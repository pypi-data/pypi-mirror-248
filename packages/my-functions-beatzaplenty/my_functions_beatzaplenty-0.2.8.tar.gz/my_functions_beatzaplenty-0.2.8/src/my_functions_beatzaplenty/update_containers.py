#!/usr/bin/env python3

import general_purpose as general_purpose

def usage():
    print("Usage: {} [-p project name. default is app] and [-q quiet mode optional list compose services to recreate]".format(__file__))
    exit(1)

def main(services):
    for service in services:
        try:
            path = f"/docker/{service}/docker-compose.yml"
            pull_command = ["docker-compose", "--file", path, "pull"]
            up_command = ["docker-compose", "--file", path, "up", "-d"]
            if not general_purpose.run_command(pull_command):
                continue
            
            if not general_purpose.run_command(up_command):
                continue
                
        except Exception as e:
            print("Error: {}".format(e))

if __name__ == "__main__":
    # Pass the list of services to the main function
    main(["service1", "service2"])  # Replace with your list of services