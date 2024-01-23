def dest(s: str) -> str:
    c = ""
    for d in ["A", "D", "M"]:
        if d in s:
            c += "1"
        else:
            c += "0"
    return c
