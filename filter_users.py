import json
import re
from typing import List, Dict, Callable


def load_users(path: str = "users.json") -> List[Dict]:
    with open(path, "r") as file:
        return json.load(file)


def print_users(users: List[Dict]) -> None:
    if not users:
        print("No matching users.")
        return
    for user in users:
        print(user)


def filter_users_by_name(name: str, users: List[Dict]) -> List[Dict]:
    name_l = name.strip().lower()
    return [user for user in users if str(user.get("name", "")).lower() == name_l]


def parse_age_filter(expr: str) -> Callable[[Dict], bool]:
    """
    Unterstützte Formate:
      - "30"     (genau 30)
      - ">30", "<=25", ">=21", "<22"
      - "21-29"  (inklusive Bereich)
    """
    s = expr.strip().replace(" ", "")

    # Bereich a-b (inklusive)
    m = re.fullmatch(r"(\d+)-(\d+)", s)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        lo, hi = min(a, b), max(a, b)
        return lambda u: isinstance(u.get("age"), int) and lo <= u["age"] <= hi

    # Einzelner Vergleich
    m = re.fullmatch(r"(>=|<=|>|<|==)?(\d+)", s)
    if m:
        op = m.group(1) or "=="
        val = int(m.group(2))
        if op == "==":
            return lambda u: u.get("age") == val
        if op == ">":
            return lambda u: isinstance(u.get("age"), int) and u["age"] > val
        if op == "<":
            return lambda u: isinstance(u.get("age"), int) and u["age"] < val
        if op == ">=":
            return lambda u: isinstance(u.get("age"), int) and u["age"] >= val
        if op == "<=":
            return lambda u: isinstance(u.get("age"), int) and u["age"] <= val

    raise ValueError("Invalid age filter. Use '30', '>30', '<=25', or '21-29'.")


def filter_users_by_age(expr: str, users: List[Dict]) -> List[Dict]:
    predicate = parse_age_filter(expr)
    return [user for user in users if predicate(user)]


if __name__ == "__main__":
    users = load_users()

    filter_option = input("What would you like to filter by? ('name' or 'age'): ").strip().lower()

    if filter_option == "name":
        name_to_search = input("Enter a name to filter users: ").strip()
        result = filter_users_by_name(name_to_search, users)
        print_users(result)

    elif filter_option == "age":
        expr = input("Enter an age filter (e.g., '30', '>30', '<=25', '21-29'): ").strip()
        try:
            result = filter_users_by_age(expr, users)
            print_users(result)
        except ValueError as e:
            print(e)

    else:
        print("Filtering by that option is not supported. Use 'name' or 'age'.")