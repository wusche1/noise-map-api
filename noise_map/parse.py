import re


def parse_db(value: str) -> str:
    m = re.search(r"(\d{2})(\d{2})", value.replace("Lden", "").replace("Lnight", ""))
    if m:
        return f"{m.group(1)}-{m.group(2)} dB(A)"
    if "75" in value:
        return ">75 dB(A)"
    return value
