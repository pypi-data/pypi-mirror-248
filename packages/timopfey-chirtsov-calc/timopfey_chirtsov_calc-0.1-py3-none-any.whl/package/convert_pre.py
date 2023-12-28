
__all__ = ['convert_precision']

def convert_precision(precision='0.00001'):
    # Хак, чтобы приветси к правильному виду
    if (isinstance(precision, float)):
        precision = str(precision + 8)
        precision = precision.replace("8", "0")

    for i in range(len(str(precision))):
        if float(precision) * 10**i >= 1:
            return i
