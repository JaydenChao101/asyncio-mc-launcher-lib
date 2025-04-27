#!/usr/bin/env python3
# This example shows how to install fabric using minecraft-launcher-lib
import launcher_core
import sys


def main():
    vanilla_version = input("Select the Minecraft version for which you want to install fabric:")
    if not launcher_core.fabric.is_minecraft_version_supported(vanilla_version):
        print("This version is not supported by fabric")
        sys.exit(0)
    minecraft_directory = launcher_core.utils.get_minecraft_directory()
    callback = {
        "setStatus": lambda text: print(text)
    }
    launcher_core.fabric.install_fabric(vanilla_version, minecraft_directory, callback=callback)


if __name__ == "__main__":
    main()
