# borgctl - wrapper around borgbackup

## Overview
[borgbackup](https://www.borgbackup.org/) is cool and easy to use. But in the end, we all have to write our own bash script arround borg. borgctl helps you by having

## Features
- One or more configuration files used by borgctl to invoke borg. You can backup different directories to different repositories.
- Run multiple borg commands using `--cron` (commands can be specified in the config file)
- Write a state file (text file with current timestamp in) after sucessfully executing borg commands (can be used for monitoring)
- Add logging

## Quickstart
- ascinema

## Installation
- pip install borgctl
- yay borgctl
- debian Paket?

## Default location for config files and logging

borgctl uses config files. If you run `borgctl`, it expects a default.yml in the config directory. You can specify one or more config files with `-c`/`--config`. If the config file contains a /, the path is interpreted as relative/absolute path. There is also a logging configuration (logging.conf) stored, which is used by borgctl and borg itself.

- Default config location for root user: /etc/borgctl

- Default config location for non-root users: `$XDG_CONFIG_HOME/borgctl` or `~/.config/borgctl`

The output of borg and borgctl will be written to borg.log. The file gets logrotated automatically.

- Default log directory for root user: /var/log/borgctl/
- Default log directory for non-root users: `$XDG_STATE_HOME/borgctl` or `~/.local/state/borgctl`

bortctl also writes status files, if a borg command runs successfully. It contains the current date. You can use it for monitoring. The state files are written to the log directory. The state file has the format `borg_state__$config_file_prefix_$borg_command.txt` (e. g. borg_state_default_create.txt). In the config file you can specify a list of commands for which a state file should be created (state_commands).

#### How borgctl behaves

borgctl needs a configuration file. If you run it without specifying one, a default.yml in the default config location is expected to exist.



























