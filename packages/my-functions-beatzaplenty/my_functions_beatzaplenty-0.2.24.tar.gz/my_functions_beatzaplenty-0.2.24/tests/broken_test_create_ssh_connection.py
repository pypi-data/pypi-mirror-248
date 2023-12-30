import os
from unittest.mock import Mock, patch
import pytest
import my_functions_beatzaplenty.general_purpose as general_purpose


mykeyfile=f'{os.getenv("HOME")}/.ssh/id_rsa'

# Mocking the 'paramiko.SSHClient' class to avoid actual SSH connections during testing
mod_ssh_mock = Mock()
with patch('paramiko.SSHClient', mod_ssh_mock):
    @pytest.mark.parametrize("retries, expected_calls", [(0, 1), (5, 6), (10, 11)])
    def test_create_ssh_connection(retries, expected_calls):
        # Start the SSH server in a separate thread
            # Mocking time.sleep to avoid actual sleep during testing
            with patch('time.sleep'):
                with pytest.raises(RuntimeError) as excinfo:
                    # Add this inside the test, just before the function call
                    print("Mock calls:", mod_ssh_mock.return_value.connect.mock_calls)
                    # Call the function with mocked parameters
                    general_purpose.create_ssh_connection('localhost', 'wayne', mykeyfile, max_retries=retries, retry_interval=1, port=22)

                # Debugging: Print the call count and expected calls
                print(f"Call count: {mod_ssh_mock.return_value.connect.call_count}, Expected calls: {expected_calls}")

                # Check if the exception message is as expected
                assert str(excinfo.value) == f"Failed to create SSH connection after {retries} attempts."

            # Check if SSH client is created the expected number of times
            assert mod_ssh_mock.return_value.connect.call_count == expected_calls

# Run the tests with pytest
if __name__ == '__main__':
    pytest.main()
