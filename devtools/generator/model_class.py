from class_text import setup_id_template, set_all_8, set_all_12, tup_template, get_set_template, body


attributes = ['showtime_id', 'booking_id', 'age', 'seat_number']
class_name="ticket"
capital_name=class_name.title()

def create_setup_id():
    setup_id = ''
    for attr in attributes:
        setup_id = setup_id + setup_id_template.format(attr=attr)

    return setup_id

def create_set_all(template):
    setall = ''
    for attr in attributes:
        setall = setall + template.format(class_name=class_name, attr=attr)
    return setall

def create_get_set():
    ters = ''
    for attr in attributes:
        ters = ters + get_set_template.format(attr=attr)

    return ters

def create_member_tup(is_save=False):
    first = True
    tup = ''

    for attr in attributes:
        if first:
            tup = tup_template.format(attr=attr)
            first= False
        else:
            tup = tup + ", " + tup_template.format(attr=attr)

    if is_save:
        tup = tup + ", " + tup_template.format(attr="id")

    return tup


f = body.format(capital_name=capital_name,
                class_name=class_name,
                setup_id=create_setup_id(),
                set_all_indent_12=create_set_all(set_all_12),
                set_all_indent_8=create_set_all(set_all_8),
                getter_set=create_get_set(),
                create_tup=create_member_tup(False),
                save_tup=create_member_tup(True),
                dicti="{}")

print(f)

with open(capital_name + ".py", 'w') as fil:
    fil.write(f)
    print("Writing")
print("wrote")
