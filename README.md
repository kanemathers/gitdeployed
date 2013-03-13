gitdeployed
===========

gitdeployed allows you to easily setup the end points for all your POST
service hooks.

Screenshot
----------

![screenshot](/docs/screenshot.png)

About
-----

Add a new repository to gitdeployed and a URL will be generated for you.
This URL can then be added to your GitHub/BitBucket POST service hook.

When the repository is updated at the upstream (GitHub/BitBucket/etc), it
will be automatically synced locally.

Getting Started
---------------

Install gitdeployed:

    $ git clone git://github.com/kanemathers/gitdeployed.git
    $ cd gitdeployed
    $ git submodule init
    $ git submodule update
    $ python setup.py install

Create a user account and start the service:

    $ gitdeployed -i -e "my@emailaddress.com" [config.ini]

See ``pirateguide --help`` for more options.

Configuring
-----------

``repos.root_path`` - If set, repositories added without a path specified
will be saved into a new folder within the root path.
