Introduction
============

Creating a module is relatively simple: just create a python package (a folder that contains a ``__init__.py`` file) in
the modules folder, insert a ``version.json`` file (which will allow you to add dependencies and general information for
your module) and have a MainClass class in the ``__init__.py`` file.

So the next step is to create the :py:class:`MainClass`, which inherits from :py:class:`BaseClassPython`, here is a minimal example:

.. code-block:: python
    :linenos:

    class MainClass:
        name = "MyFirstModule"
        help = {
            "description": "My first module",
            "commands": {
            }
        }

As you can see it's very simple, from now on you can start the bot and load the module.

Currently it does nothing, so let's add a ``say`` command:

.. code-block:: python
    :linenos:
    :emphasize-lines: 6,10,11

    class MainClass:
        name = "MyFirstModule"
        help = {
            "description": "My first module",
            "commands": {
                "{prefix}{command} say <message>": "Bot send message <message>",
            }
        }

        async def com_say(self, message, args, kwargs):
            await message.channel.send(args[0])

You can now reload the module and test the command ``!myfirstmodule say "Hello world"``.

You can see that without the quotation marks the returned message contains only the first word. Indeed each message is
processed to extract the module (here ``module``), the command (here ``say``) and the arguments. This is how the
arguments are processed:


``!mymodule say "Hello world" "Goodbye world"`` - ``args = ["Hello world", "Goodbye world"] kwargs=[]``

``!mymodule say --long-option -an -s "s value"`` - ``args = [] kwargs = [("long-option", None), ("a", None), ("n", None), ("s", "s value")]``

``!mymodule say -s "s value" "value"`` - ``args = ["value"] kwargs = [("s", "s value")]``

So let's add an ``-m`` option that adds the mention of the author to the message:


.. code-block:: python
    :linenos:
    :lineno-start: 10
    :emphasize-lines: 2,3,4

        async def com_say(self, message, args, kwargs):
            if 'm' in [k for k, v in kwargs]:
                await message.channel.send(message.author.mention + args[0])
                return
            await message.channel.send(args[0])

