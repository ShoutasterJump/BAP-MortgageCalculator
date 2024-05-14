import pytest
from mortgage import Mortgage


class TestStrings:
    Mortgage = Mortgage(1, "Test Mortgage", "16-04-2024", 0.05,
                        30, 100000, 0, 20000, 1)

    def test_mortgage_principal_setter(self):
        self.mortgage = Mortgage(1, "Test Mortgage", "16-04-2024",
                                 0.05, 30, 100000, 0, 20000, 1)
        assert self.mortgage.initialPrincipal == 100000

    def test_mortgage_principal_setter_with_string(self):
        mortgage = Mortgage(1, "Test Mortgage", "16-04-2024",
                            0.05, 30, 100000, 0, 20000, 1)
        with pytest.raises(ValueError):
            mortgage.principal = "test"
