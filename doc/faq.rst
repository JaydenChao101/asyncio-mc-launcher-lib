FAQ
==================================================

Q: Which Minecraft versions are supported?
    A: minecraft-launcher-lib supports all Minecraft versions that the official Launcher from Mojang supports. It provides automatic installation for Vanilla, Forge and Fabric.
    Other versions can be launched after they got installed in other ways.

Q: Which Python versions are supported?
    A: minecraft-launcher-lib supports at the moment Python 3.8 and above. `PyPy <https://www.pypy.org>`_ is also official supported.

Q: Which Operating Systems are supported?
    A: minecraft-launcher-lib official supports Windows, macOS and Linux, which are the Operating Systems that also supported by Mojang. It might work on other OS, but there is no guaranty.

Q: Can I use minecraft-launcher-lib in my project?
    A: minecraft-launcher-lib is licensed under :repolink:`BSD 2-Clause <LICENSE>` what means it is OpenSource and it can be used in any of your projects.
    For more information check out the license.

Q: How can I make a cracked launcher?
    A: Just buy Minecraft. It's cheaper than a AAA title and brings years of fun.

Q: Is the API stable?
    A: All functions that are documented here are stable.

Q: Minecraft does not start
    A: Please visit :doc:`/troubleshooting`.

Q: Minecraft is creating a logs folder inside my project directory
    A: Minecraft is using the working directory for it's logs. You should run Minecraft with a other working directory.

Q: I get a :class:`~launcher_coreexceptions.AzureAppNotPermitted` Exception
    A: Please take a look at the :doc:`/tutorial/microsoft_login` tutorial

Q: Does minecraft-launcher-lib supports the Bedrock Edition?
    A:  Only the Java Edition is supported and there are no plans to support Bedrock
