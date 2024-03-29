from django.core.exceptions import ValidationError


def validate_meli_code(value: str) -> bool:
    """
    To see how the algorithem works, see http://www.aliarash.com/article/codemeli/codemeli.htm

    """
    if not len(value) == 10:
        # raise ValueError("کد ملی باید ۱۰ رقم باشد.")
        return False

    res = 0
    for i, num in enumerate(value[:-1]):
        res = res + (int(num) * (10 - i))

    remain = res % 11
    if remain < 2:
        if not remain == int(value[-1]):
            # raise ValueError("کد ملی درست نیست")
            return False
    else:
        if not (11 - remain) == int(value[-1]):
            # raise ValueError("کد ملی درست نیست")
            return False

    return True


# function for validations of Iranian national code
def national_code_validator(value):
    if not validate_meli_code(value):
        raise ValidationError(f'{str(value)}+ is not valid')
