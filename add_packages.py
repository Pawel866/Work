import json
import subprocess
import sys
import importlib.util


# create dict out of json file
def map_json_to_dict(input_json_file):
    json_file = open(input_json_file, encoding='utf-8')
    return json.load(json_file)


packages_dict = map_json_to_dict("packages.json")

# create separate empty dict to track app installation status
packages_install_status_dict = {}

# apps installation states
package_installed = 'installed'
package_not_installed = 'not installed'


def install_all_packages_without_dependencies():
    # iterate on every package name in file
    package_names = packages_dict.keys()
    for package_name in package_names:

        # add initial value state for every package as 'not installed'
        packages_install_status_dict.update({package_name: package_not_installed})

        # for each package check if there are no dependencies on other packages
        package_dependencies = packages_dict[package_name]["Requires"]
        if not package_dependencies:
            # if no dependencies on other packages install this package
            install_package(package_name)

            # check if package is successfully installed, if yes change the status to installed
            change_states_when_package_installed(package_name)


def install_packages_with_dependencies():
    # iterate on all packages in install status dict
    packages_with_status = packages_install_status_dict.keys()
    for packages_with_status in packages_with_status:

        # check which package is not installed yet
        if packages_install_status_dict[packages_with_status] == package_not_installed:
            not_installed_package_name = packages_with_status

            # check if not installed package have dependencies
            package_dependencies = packages_dict[packages_with_status]["Requires"]
            for package_dependency in package_dependencies:

                # check in install_status_dict if package dependencies are not installed
                # if any new dependency occurs add it
                if packages_install_status_dict[package_dependency] == package_not_installed \
                        or not packages_install_status_dict[package_dependency]:
                    # install this dependency
                    install_package(package_dependency)

                    # check if installation success and update app status to installed
                    change_states_when_package_installed(package_dependency)

                # install package after its dependency packages installation
                install_package(not_installed_package_name)

                # check if package with dependencies was installed
                change_states_when_package_installed(not_installed_package_name)


def install_package(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    except Exception:
        print(f"{package_name} not installed")


def change_states_when_package_installed(package_name):
    if importlib.util.resolve_name(package_name, None) is not None:
        packages_install_status_dict.update({package_name: package_installed})


def check_packages_installation_status():
    # print information about packages installation status
    for app in packages_install_status_dict:
        print(f"{app} was {packages_install_status_dict[app]}")

        # raise error if package not installed
        if packages_install_status_dict[app] == package_not_installed:
            raise ValueError(app, "installation failed")

    # print when all packages installed with success
    print("Installation finished with success")


def import_project_packages():
    install_all_packages_without_dependencies()
    install_packages_with_dependencies()
    check_packages_installation_status()


import_project_packages()
