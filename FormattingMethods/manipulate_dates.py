from datetime import datetime


def rebase_year(base_date, rebase_list):
    """
    Instead of working from jan-dec work from another month - month within a year.

    Lets say you have dates of birth based on january to december but actually want them to be based on september to
    august to model a disease session. By providing a list of datetime's that have the years of interest and then the
    month set to september you can rebase those born in the year after to the form to insure season are consistent.

    Example
    ---------
    For example lets say you have two individuals born in March and October 1944. If you are modeling a disease with
    non-gregorian calender seasonality of september to august then you want to ensure that individuals year fixed
    effects are consistent with seasons of disease rather than just the year they where born in. This method would put
    the individual born in March to now be born in the 1943 season of this disease, whilst the individual in October
    would remain in 1944.

    :param base_date: The original datetime date you want to rebase to another year
    :type base_date: datetime

    :param rebase_list: A list of datetime that you want to check that a date is between
    :type rebase_list: list[datetime]

    :return: The year of the year in the rebase list
    :rtype: int
    """
    for i, y in enumerate(rebase_list):
        if (i > 0) and (rebase_list[i - 1] <= base_date < y):
            return rebase_list[i - 1].year


def check_date(date, date_to_check):
    """
    Check to see if the date of birth is before or after the date to check
    """
    if date < date_to_check:
        return 0
    else:
        return 1


def within_date(date_min, date_max, current_date):
    """
    Test if a provided date is greater than or equal to a min date or less than max date
    """
    if date_min <= current_date < date_max:
        return True
    else:
        return False

