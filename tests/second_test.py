import pytest
from app.calculator import Calculator

class TestCalc:
    def setup(self):
        self.calc = Calculator
    def test_division_calculate_correctly(self):
        assert self.calc.division(self, 6, 2) == 3
    def test_division_calculate_failed(self):
        assert self.calc.division(self, 6, 2) == 4
    def test_subtraction_calculate_correctly(self):
        assert self.calc.subtraction(self, 6, 5) == 1
    def test_subtraction_calculate_failed(self):
        assert self.calc.subtraction(self, 5, 6) == 1
    def test_adding_calculate_correctly(self):
            assert self.calc.adding(self, 6, 5) == 11
    def test_adding_calculate_failed(self):
            assert self.calc.adding(self, 5, 6) == 13