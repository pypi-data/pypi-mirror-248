# File: permissions_manager.py
import os
import importlib.metadata

class PermissionsManager:
    def __init__(self):
        pass

    def check_permissions(self, package_names):
        """
        Check the permissions of multiple Python packages.
        """
        permissions = {}
        for package_name in package_names:
            package_path = importlib.metadata.distribution(package_name).locate_file('')
            permissions[package_name] = os.access(package_path, os.R_OK | os.W_OK)
        return permissions

    def change_permissions(self, package_names, permissions):
        """
        Change the permissions of multiple Python packages.
        """
        for package_name in package_names:
            package_path = importlib.metadata.distribution(package_name).locate_file('')
            os.chmod(package_path, permissions)

    def report_non_standard_permissions(self, package_names, standard_permissions):
        """
        Provide a report of multiple Python packages with non-standard permissions.
        """
        non_standard_packages = []
        for package_name in package_names:
            package_path = importlib.metadata.distribution(package_name).locate_file('')
            permissions = os.access(package_path, os.R_OK | os.W_OK)
            if permissions != standard_permissions:
                non_standard_packages.append((package_name, permissions))
        return non_standard_packages
