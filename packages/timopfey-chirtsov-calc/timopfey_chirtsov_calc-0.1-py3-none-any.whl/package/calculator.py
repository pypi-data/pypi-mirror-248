from typing import Union

__all__ = ['calculate']


def calculate(op1: Union[float, int], op2: Union[float, int],
              act: str) -> Union[float, int]:
    # TODO: написать документацию для каждой функции, которая у вас в калькуляторе
    """
    op1 - первое число
    op3 - второе число
    act - действие:
     "+"" --- Сложение
     "-"" --- вычетание
     "*"" --- умножение
     "/"" --- деление 
     "**"" --- возведние в степень
     "%"" --- остаток от деления

    """
    if act == "+":
        r = op1 + op2
    elif act == "-":
        r = op1 - op2
    elif act == "*":
        r = op1 * op2
    elif act == "/":
        if op2 != 0:
            r = op1 / op2
        else:
            r = "деление на ноль невозможно"
    elif act == "**":
        r = op1**op2
    elif act == "%":
    
        if op2 != 0:
            r = op1 % op2
        else:
            r = "деление на ноль невозможно"
    else:
        r = "операция не распознана"

    return r


