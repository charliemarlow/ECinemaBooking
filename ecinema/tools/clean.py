

def clean_phone(phone: str) -> str:
    num = ""
    for c in phone:
        if not (c == ' ' or c == '-' or
            c =='(' or c == ')' or c == '+'):
            num = num + c

    return num
