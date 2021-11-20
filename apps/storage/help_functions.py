import re
import random, string


def get_random_string(n=50) -> str:
    random_string = lambda n: ''.join([random.choice(string.ascii_letters) for i in range(n)])
    return random_string(n)


def get_period_and_number_duration(duration: str) -> (int, int):
    """
    Возвращает единицу измерения периода аренды и 
    их количество периодов аренды из элементов списка
    OrderUnit:DURATION_CHOICES
    """
    # находим единицу измерения периода, week или month
    period_id = 3 if 'week' in duration else 4

    # находим количество периодов, т.е. срок аренды
    # ВНИМАНИЕ, ИЗВРАТ! Слабонервным не смотреть.
    number_of_periods = int(re.match(r'\d{1,2}', duration).group(0))
    
    return period_id, number_of_periods