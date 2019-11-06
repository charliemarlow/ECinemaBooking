from text import header, required_validation_1, required_validation_2, required_getter_template, optional_validation_1, optional_getter_1, body

attributes = [('num_seats', 'validate_num'),
              ('showroom_name', 'validate_name'),]

def create_validation_list():
    li = ''
    first = True
    for attr in attributes:
        if first:
            li = attr[1]
            first= False
        else:
            li = li + ", " + attr[1]

    return li

class_name = "showroom"
model_class=class_name.title()
model_plural_cap=model_class + "s"
validation_list = create_validation_list()
plural_name = class_name + "s"
id_name = class_name[0] + "id"


def create_kwargs():
    kw = ''
    first = True
    for attr in attributes:
        if first:
            kw = attr[0] + "=" + attr[0]
        else:
            kw = kw + ", " + attr[0] + "=" + attr[0]

    return kw

def create_required_validation():
    required_validation = ''
    first = True
    for attr in attributes:
        if first:
            required_validation = required_validation_1.format(attr=attr[0], func=attr[1])
            first = False
        else:
            required_validation = required_validation + required_validation_2.format(attr=attr[0], func=attr[1])
    return required_validation

def create_required_getter():
    required_getter = ''
    for attr in attributes:
        required_getter = required_getter + required_getter_template.format(attr=attr[0])

    return required_getter

def create_optional_validation():
    optional_validation = ''
    for attr in attributes:
        optional_validation = optional_validation + optional_validation_1.format(attr=attr[0], func=attr[1], class_name=class_name)


    return optional_validation

def create_optional_getter():
    optional_getter = ''
    for attr in attributes:
        optional_getter = optional_getter + optional_getter_1.format(attr=attr[0])


    return optional_getter


head = header.format(model_class=model_class,
                    model_plural_cap=model_plural_cap,
                     validation_list=validation_list)


bd = body.format(plural_name=plural_name,
                  lowercase_name=class_name,
                  model_class=model_class,
                  model_plural_cap=model_plural_cap,
                  id_name=id_name,
                  input_optional=create_optional_getter(),
                  optional_validation=create_optional_validation(),
                  required_validation=create_required_validation(),
                  required_getter=create_required_getter(),
                  kwargs=create_kwargs()
)

f = head + bd

print(f)
with open('Admin' + model_class + 'Controller.py', 'w') as fil:
    fil.write(f)

