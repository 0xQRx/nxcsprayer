# NXCSprayer

NXCSprayer is a Python script designed to perform password spraying attacks on SMB services, ensuring minimal risk of causing account lockouts by adhering to defined lockout policies.

## Features

- **Lockout Protection**: Automatically pauses the attack based on a predefined number of attempts to avoid triggering account lockouts.
- **Verbose and Debug Outputs**: Detailed outputs including timestamped log entries, success and failure notifications, and debugging information if enabled.
- **Local Authentication Support**: Option to use local authentication flags with the SMB service.

## Prerequisites

Before you start using NXCSprayer, make sure you have Python and NetExec installed along with the following Python packages:
- `argparse`
- `subprocess`
- `time`
- `math`
- `termcolor`

These can be installed using `pip` if not already available:

```bash
pip install termcolor
```

## Usage

```
python nxcsprayer.py --target-ip <target_ip> --username-file <username_file> --password-file <password_file> --lockout-count <lockout_count> --lockout-timeout <lockout_timeout> [--debug] [--verbose] [--timestamp] [--local-auth]
```

Arguments:

- `--target-ip`: Target IP address for SMB.
- `--username-file`: File path containing usernames, one per line.
- `--password-file`: File path containing passwords, one per line.
- `--lockout-count`: Number of password attempts before a lockout risk is considered.
- `--lockout-timeout`: Minutes to wait after reaching the lockout count to resume attempts.
- `--debug`: Enables detailed debug output.
- `--timestamp`: Prefixes each log entry with a timestamp.
- `--verbose`: Enables verbose output, including failed attempts.
- `--local-auth`: Uses local authentication method with `nxc`.

## Example

```
python nxcsprayer.py --target-ip 192.168.1.100 --username-file users.txt --password-file passwords.txt --lockout-count 3 --lockout-timeout 30 --verbose --timestamp
```

## TODO

- output valid creds into a file
- check for connectivity issues, abort if found any