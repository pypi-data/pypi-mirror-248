import pytest
from my_functions_beatzaplenty import check_outgoing_ports
#     ###################### LOAD TESTING MODULE  ###########################
# from importlib.machinery import SourceFileLoader
# from os import getenv
# test = SourceFileLoader("check_outgoing_ports", f"{getenv('HOME')}/common/src/my_functions_beatzaplenty/check_outgoing_ports.py").load_module()
  #############################################################################
@pytest.mark.parametrize("hostname, ports, expected_results", [
    ("smtp.gmail.com", [25, 465, 587], {25: "Closed", 465: "Open", 587: "Open"}),  # Replace with actual expected results
    # Add more test cases as needed
])
def test_check_outgoing_ports(hostname, ports ,expected_results):
    actual_results = check_outgoing_ports(hostname, ports)
    assert actual_results == expected_results, f"Expected: {expected_results}, Actual: {actual_results}"

# Run the test using: pytest -v your_test_module.py
# You can add more tests based on the specific scenarios you want to cover.
if __name__ == '__main__':
    pytest.main()
