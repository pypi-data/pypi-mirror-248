Build the website
=================

For build your website there are two way:

* Auto generation
* Self made

If you want do all by your self and make custom gallery and use many section, 
you need follow https://recitale.readthedocs.io/en/latest/configuration.html#gallery-settings-yaml

But if is just for make gallery with only picture you can generate it automatically.

You need 

1. Create a folder
2. Put all pics you want
3. Create settings.yaml file in the folder
4. Add title key in folder/settings.yaml. Optionally provide a cover and date key, otherwise they are inferred from the oldest file in the gallery.
5. Use `recitale autogen -d folder`


Generate
--------

**Note: You need to be in an activated virtualenv.**

In a folder containing the **root** settings.yaml file, simply do::

    recitale

A `build` folder will be created in the current directory, containing an
index.html, static files (css & js) and pictures.

Preview
-------

In a root folder launch this command::

  recitale preview

Then, you can check your website at http://localhost:9000

Deployment
----------

recitale can upload your website with rsync, to do so, run::

  recitale deploy

