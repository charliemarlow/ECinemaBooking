from data_text import body

table = "review"
capital_name=table.title()
table_id ="review_id"

attributes = ['customer_id', 'movie_id', 'rating', 'subject', 'review']

def create_attribute_values():

    attr_list = ''
    values = ''
    first = True
    for attr in attributes:
        if first:
            attr_list = attr
            values = '?'
            first = False
        else:
            attr_list = attr_list + ", " + attr
            values = values + ', ?'

    return attr_list, values

def create_update():
    update = ''
    first = True

    for attr in attributes:
        if first:
            update = attr + " = ?"
            first = False
        else:
            update = update + ", " + attr + " = ?"

    return update

attr, values = create_attribute_values()

f = body.format(table=table,
                capital_name=capital_name,
                table_id=table_id,
                attr=attr,
                values=values,
                update=create_update()
)

print(f)
with open(table.title() + 'Data.py', 'w') as fil:
    fil.write(f)
