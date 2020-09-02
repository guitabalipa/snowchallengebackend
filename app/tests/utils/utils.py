import random
import string


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_category_name() -> str:
    return f"Category {random_lower_string()}"


def random_site_name() -> str:
    return f"Site {random_lower_string()}"


def random_picture_name() -> str:
    return f"{random_lower_string()}.png"
