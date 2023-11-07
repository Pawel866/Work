import json
import subprocess
import sys
import importlib.util

# get json file
json_file = open('apps.json', encoding='utf-8')

# create dict out of json file
all_apps_dict = json.load(json_file)

# create separate empty dict to track app installation status
install_status_dict = {}

# apps installation states
installed = 'installed'
not_installed = 'not installed'


def install_packages_without_dependencies():
    # iterate on every app object in file
    for each_app_name in all_apps_dict.keys():

        # add initial value state for every app as 'not installed'
        install_status_dict.update({each_app_name: not_installed})

        # for each app check if there are no dependencies on other apps
        if not all_apps_dict[each_app_name]["Requires"]:

            # if no dependencies on other apps install this app
            name = all_apps_dict[each_app_name]["Name"]
            subprocess.check_call([sys.executable, "-m", "pip", "install", name])

            # check if app is successfully installed, if yes change the status of the app to installed
            if importlib.util.resolve_name(name, None) is not None:
                install_status_dict.update({each_app_name: installed})


def install_packages_with_dependencies():

    # iterate all apps
    for install_status_app_name in install_status_dict.keys():

        # check which app is not installed yet
        if install_status_dict[install_status_app_name] == not_installed:
            not_installed_app_name = install_status_app_name

            # check if not installed app have dependencies
            dependencies = all_apps_dict[install_status_app_name]["Requires"]
            for dependency in dependencies:

                # check in install_status_dict if app dependencies are not installed also add new dependencies
                if install_status_dict[dependency] == not_installed or not install_status_dict[dependency]:

                    # install this dependencies
                    subprocess.check_call([sys.executable, "-m", "pip", "install", dependency])

                    # check if installation success and update app status to installed
                    if importlib.util.resolve_name(dependency, None) is not None:
                        install_status_dict.update({dependency: installed})

                # install app after its dependency installation
                subprocess.check_call([sys.executable, "-m", "pip", "install", not_installed_app_name])

                # check if installed app was installed
                if importlib.util.resolve_name(not_installed_app_name, None) is not None:
                    install_status_dict.update({install_status_app_name: installed})


def check_dependency_installation():
    # print all project dependencies installation status
    for app in install_status_dict:
        print(f"{app} was {install_status_dict[app]}")

        # raise value error if dependency not installed
        if install_status_dict[app] == not_installed:
            raise ValueError(app, "installation failed")

    # print when all dependencies installed with success
    print("Installation finished with success")


install_packages_without_dependencies()
install_packages_with_dependencies()
check_dependency_installation()
