def calculate_risk(age, salary, expenses, savings):
    """
    Calculate the financial risk profile of a user.
    """
    disposable = salary - expenses
    ratio = disposable / salary

    if age < 28 and ratio >= 0.35:
        return "aggressive"
    elif age < 45 and ratio >= 0.20:
        return "moderate"
    else:
        return "conservative"
