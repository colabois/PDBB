Introduction
============

A PDB module is a simple python package, ie. a folder which contains a ``__init__.py`` file. A valid module must have a
file named ``infos.toml`` which contains some informations about the module, and ``__init__.py__`` must have one thing:
a variable named ``__main_class__``, which point to a class, and this class must have a method named ``__dispatch__``.

Lets look a simple example:

.. code-block::

    └─── modules
      └─── my_module
        ├── infos.toml
        └── __init__.py

Now examine ``infos.toml`` file:

.. code-block:: toml
    :linenos:

    version = "0.1.0"
    bot_version = "~=0.2.0"

This file is minimal, but necessary to describe your module, and fields are very clear:

- ``version`` is version of module
- ``bot_version`` is the required version of bot (the ``~=`` is to say version ``0.2.0`` or compatible)

You can refer to ``version`` section for more informations about ``version`` and ``bot_version`` fields, and
``infos file`` section for other fields of this file.

Now look at ``__init__.py``

.. code-block:: python
    :linenos:

    class MyModule:
        def __dispatch__(self, event_name, *args, **kwargs):
            pass

    __main_class__ = MyModule


As you can see a module is very simple.

``__dispatch__`` method will be called for each event, these events are listed in section ``events``. As you can see,
there is a lot of event types, and handle them manually will be very long, so there is a module, who parse them, and
call ``on_{event}`` method, and an other one who parse message to handle commands. In next part we learn to use them.