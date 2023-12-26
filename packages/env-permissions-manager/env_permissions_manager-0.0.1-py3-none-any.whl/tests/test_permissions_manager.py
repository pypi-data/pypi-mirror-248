import os
import pytest
from permissions_manager.permissions_manager import PermissionsManager

@pytest.fixture
def temp_directory(tmp_path):
    return tmp_path

def test_check_permissions(temp_directory):
    permissions_manager = PermissionsManager()
    package_names = ['requests', 'numpy']
    permissions = permissions_manager.check_permissions(package_names)
    for package_name in package_names:
        assert permissions[package_name] == True

def test_change_permissions(temp_directory):
    permissions_manager = PermissionsManager()
    package_names = ['requests', 'numpy']
    new_permissions = 0o755
    permissions_manager.change_permissions(package_names, new_permissions)
    checked_permissions = permissions_manager.check_permissions(package_names)
    for package_name in package_names:
        assert checked_permissions[package_name] == True

def test_report_non_standard_permissions(temp_directory):
    permissions_manager = PermissionsManager()
    package_names = ['requests', 'numpy']
    standard_permissions = True
    non_standard_packages = permissions_manager.report_non_standard_permissions(package_names, standard_permissions)
    assert len(non_standard_packages) == 0
