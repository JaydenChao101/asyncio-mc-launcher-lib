Install Fabric
==========================
This tutorial shows how to install forge using minecraft-launcher-lib.

-------------------------
Install Fabric
-------------------------
Installing Fabric is very easy. Let's say you want to install Fabric for 1.17:

.. code:: python

    launcher_corefabric.install_fabric("1.17", minecraft_directory)

:func:`~launcher_corefabric.install_fabric` supports the same callbacks as :func:`~launcher_coreinstall.install_minecraft_version`.

-------------------------
Launch Fabric
-------------------------
Use :func:`~launcher_coreutils.get_installed_versions` to get a list of all installed versions. Your new installed fabric version should be in the list.
You can launch it like any other Minecraft version.
