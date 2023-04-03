Installation
============
.. _installation:
    Package_installation

--------------------

The pycopo module is execectubale in docker container because of it specific environment. 
    + First clone the project throught this gitlab link: 

    .. code-block:: console
        
        $ git clone https://gitlab.com/symmehub/pycopo.git

    + Then pull the docker image using these commands line in a terminal:

    .. code-block:: console

        $ docker pull matisboualam/mon_image:0.0
    
    + Finally build and run the docker compose:

    .. code-block:: console
        
        $ docker compose build main_container

        $ docker compose run -rm -i main_container

.. note::
    *You can also open the git in a devcontainer using vscode.*


.. testcode::
    
    2+2

.. testoutput::

    5
