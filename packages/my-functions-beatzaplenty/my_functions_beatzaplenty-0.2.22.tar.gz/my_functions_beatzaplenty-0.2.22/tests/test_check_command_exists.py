import pytest
from my_functions_beatzaplenty import check_command_exists
# #     ###################### LOAD TESTING MODULE  ###########################
# from importlib.machinery import SourceFileLoader
# from os import getenv
# test = SourceFileLoader("check_command_exists", f"{getenv('HOME')}/common/src/my_functions_beatzaplenty/general_purpose.py").load_module()
#   #############################################################################
def test_check_command_exists():
    # Test for an existing command (you can replace 'ls' with any valid command on your system)
    assert check_command_exists('ls') is True

    # Test for a non-existing command
    assert check_command_exists('nonexistentcommand123') is False

    # Test for a command that raises FileNotFoundError
    assert check_command_exists('this_command_does_not_exist') is False

    # Test for a command that raises subprocess.CalledProcessError
    assert check_command_exists('ls /nonexistentdirectory') is False

    # You can add more test cases as needed

if __name__ == '__main__':
    pytest.main()
