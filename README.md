A collection of scripts useful for working with Digital Ocean instances.

### tugboat

Provides a useful CLI to the Digital Ocean API.

Install with:

    pip install tugboat

Requires an API v2 key.

### do-sync

Adds Digital Ocean droplet hosts to your `.ssh/config` file.

Typical usage:

    $ do-sync

### do-init

Usage:

    $ do-init hostname

(First perform a `do-ssh sync`)

### setup

A bash script which contains several useful scripts to initialize
a new instance.

    setup                  -- displays available commands
    setup debian-init      -- sets up swap, creates a user account
                              performs apt-get update

