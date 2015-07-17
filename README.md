A collection of scripts useful for working with Digital Ocean instances.

- tugboat
- dsync
- setup
- lighter

### tugboat

Provides a useful CLI to the Digital Ocean API.

Install with:

    pip install tugboat

Requires an API v1 key. (Digital Ocean control panel >> API >> View API v1).

### dsync

Creates `$HOME/.do_ssh_config` from your current set of droplet.

Requires `tugboat`. After running `dsync`, ssh or scp to a droplet with:

    ssh -F ~/.do_ssh_config {droplet-name} ...
    scp -F ~/.do_ssh_config {droplet-name} ...

Setting up the following aliases can make this more convenient:

    alias dssh="ssh -F ~/.do_ssh_config"
    alias dscp="scp -F ~/.do_ssh_config"

### setup

A bash script which contains several useful scripts to initialize
a new instance.

    setup                  -- displays available commands
    setup debian-init      -- sets up swap, creates a user account
                              performs apt-get update

### lighter

A Python script to create and control lighttpd instances.

Commands:

    lighter create -p PORT -d DOC-ROOT   -- create a new lighttpd instance
    lighter start PORT                   -- start an instance
    lighter stop PORT                    -- stop an instance
    lighter show                         -- show configured instances

Requires `lighttpd`.

