
__all__ = ['run_test']

from unittest import TestCase, main


from .calculator import calculate
from .convert_pre import convert_precision



class TestPrecision(TestCase):
    def test_cp_with_1(self):
        self.assertEqual(
            convert_precision('0.1'), 1, "Должна быть 1"
        )


    def test_cp_with_2(self):
        self.assertEqual(
            convert_precision('0.01'), 2, "Должно быть 2"
        )


    def test_cp_with_5(self):
        self.assertEqual(
            convert_precision('0.00001'), 5, "Должно быть 5"
        )


    def test_cp_with_5_as_float(self):
        self.assertEqual(
            convert_precision(0.00001), 5, "Должно быть 5"
        )
      
class TestCalculater(TestCase):

  def test_sum(self):
    self.assertTrue(calculate(12, 17, "+") == 29)

  def test_minus(self):
    self.assertTrue(calculate(17, 12, "-") == 5)


  def test_multiplication(self):
    self.assertTrue(calculate(17, 12,"*") == 204)


  def test_divide(self):
    self.assertTrue(calculate(25, 5, '/') == 5)


  def test_divide_to_zero(self):
    self.assertTrue(calculate(30, 0, '/') == 'деление на ноль невозможно'),

  def test_exponentiation(self):
    self.assertTrue(calculate(5, 6, "**") == 15625) 

def run_test():
  test_pre = TestPrecision()
  test_pre.test_cp_with_1()
  test_pre.test_cp_with_2()
  test_pre.test_cp_with_5()
  test_pre.test_cp_with_5_as_float()

  test_calc = TestCalculater()
  test_calc.test_sum()
  test_calc.test_minus()
  test_calc.test_multiplication()
  test_calc.test_divide()
  test_calc.test_divide_to_zero()
  test_calc.test_exponentiation()
  

if __name__ == '__main__':
    main()