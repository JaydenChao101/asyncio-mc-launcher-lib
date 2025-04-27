#!/usr/bin/env python3
# This example shows how to write a basic launcher with Tkinter.
from tkinter import Tk, Label, Entry, Button, mainloop
from tkinter.ttk import Combobox
import launcher_core
import subprocess
import sys


def main():
    def launch():
        window.withdraw()

        launcher_core.install.install_minecraft_version(version_select.get(), minecraft_directory)

        login_data = launcher_core.account.login_user(username_input.get(), password_input.get())

        options = {
            "username": login_data["selectedProfile"]["name"],
            "uuid": login_data["selectedProfile"]["id"],
            "token": login_data["accessToken"]
        }
        minecraft_command = launcher_core.command.get_minecraft_command(version_select.get(), minecraft_directory, options)

        subprocess.run(minecraft_command)

        sys.exit(0)

    window = Tk()
    window.title("Minecraft Launcher")

    Label(window, text="Username:").grid(row=0, column=0)
    username_input = Entry(window)
    username_input.grid(row=0, column=1)
    Label(window, text="Password:").grid(row=1, column=0)
    password_input = Entry(window)
    password_input.grid(row=1, column=1)

    minecraft_directory = launcher_core.utils.get_minecraft_directory()
    versions = launcher_core.utils.get_available_versions(minecraft_directory)
    version_list = []

    for i in versions:
        version_list.append(i["id"])

    Label(window, text="Version:").grid(row=2, column=0)
    version_select = Combobox(window, values=version_list)
    version_select.grid(row=2, column=1)
    version_select.current(0)

    Button(window, text="Launch", command=launch).grid(row=4, column=1)

    mainloop()


if __name__ == "__main__":
    main()
