Basic module
============

In last part we learn how to create a module from scratch, but as it is very long and difficult, we will use other
modules to create our first module. Theses modules are called metamodules, as they don't provide ``__main_class__`` or
``__dispatch__`` method, but only useful things for module developpers.

Let's use ``mod_base``!

First we need to install ``mod_base``, so follow instruction on PDMI. Then we need to add this module as dependency
to our module:

.. code-block:: toml
    :linesnos:

    version = "0.1.0"
    bot_version = "~=0.2.0"

    [dependencies]
    bot_base = "~=1.2.0"

Now, mod_base is available, so we can use it in our module:

.. code-block:: python
    :linenos:

    import mod_base as m_b

    class MyModule:
        def __dispatch__(self, event_name, *args, **kwargs):
            pass

    __main_class__ = MyModule

