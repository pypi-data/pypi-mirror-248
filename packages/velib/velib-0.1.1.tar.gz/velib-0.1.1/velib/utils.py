#
from datetime import datetime, timedelta
from decimal import Decimal, Context, ROUND_HALF_UP, ROUND_HALF_DOWN, ROUND_HALF_EVEN, ROUND_UP, ROUND_DOWN 

def password_check(passwd, ch_min=None, ch_max=None, special_symbol=None):
    errors = []
    ch_min = ch_min if ch_min else 6
    ch_max = ch_max if ch_max else 32
    
    if len(passwd) < ch_min:
        errors.append('length should be at least {min}'.format(min=ch_min))
    
    if len(passwd) > ch_max:
        errors.append('length should not be greater than {max}'.format(max=ch_max))
    
    if not any(char.isdigit() for char in passwd):
        errors.append('should have at least one numeral')
    
    if not any(char.isupper() for char in passwd):
        errors.append('should have at least one uppercase letter')
    
    if not any(char.islower() for char in passwd):
        errors.append('should have at least one lowercase letter')
    
    if special_symbol and not any(char in special_symbol for char in passwd):
        errors.append('should have at least one of the symbols {cs}'.format(cs=''.join(special_symbol)))

    if len(errors) > 0:
        return errors
    
def dict_to_inline(d):
    try:
        return ', '.join([str(x) + ': ' + str(d[x]) for x in d.keys()])
    except:
        return str(d)
    
def shift_dates(begin_date, end_date):
    begin = datetime.fromisoformat(begin_date)
    end = datetime.fromisoformat(end_date)        
    interval = end - begin        
    shifted_begin = begin - interval
    shifted_end = end - interval        
    return shifted_begin.strftime('%Y-%m-%d'), shifted_end.strftime('%Y-%m-%d')



def calculate_percentage(previous_value, current_value):
    if previous_value is None or current_value is None:
        return 0    
    decrease = previous_value - current_value
    increase = current_value - previous_value
    numerator = decrease if previous_value > current_value else increase
    denominator = previous_value if previous_value > current_value else current_value
    if denominator == 0:
        return 0
    percentage = (numerator / denominator) * 100
    percentage = round(percentage, 2)
    percentage = percentage if current_value > previous_value else percentage * -1
    return percentage

def to_decimal(value, is_string=True, precision=4, rounding=ROUND_HALF_EVEN):
    if value is None:
        return 0 if not is_string else '0'
    if isinstance(value, Decimal):
        return value if not is_string else str(value)
    if isinstance(value, (int, float)):
        val = Decimal(str(value), context=Context(prec=precision, rounding=rounding))
        return val if not is_string else str(val)
    if isinstance(value, str):
        if value.isdigit():
            val = Decimal(value, context=Context(prec=precision, rounding=rounding))
            return val if not is_string else str(val)
    return value

def to_decimal_collection(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = to_decimal(value)
    elif isinstance(data, list):
        for item in data:
            to_decimal_collection(item)
    return data
        

