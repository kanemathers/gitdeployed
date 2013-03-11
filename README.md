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
    $ python setup.py install

Run it:

    $ gitdeployed -i [config.ini]

See ``pirateguide --help`` for more options.

Configuring
-----------

``repos.root_path`` - If set, repositories added without a path specified
will be saved into a new folder within the root path.

Dependencies
------------

You'll need the [less](http://lesscss.org/) binary in your ``$PATH``. That,
or the full path specified in the setting ``webassets.less_bin``.
