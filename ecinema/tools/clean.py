from datetime import datetime
from ecinema.tools.validation import validate_year
from ecinema.models.Price import Price

def clean_phone(phone: str) -> str:
    num = ""
    for c in phone:
        if not (c == ' ' or c == '-' or
            c =='(' or c == ')' or c == '+'):
            num = num + c

    return num

def clean_expiration(month: str, year: str):
    exp_date = datetime.now()
    error = None
    if validate_year(year):
        exp_date = datetime(int(year),
                             int(month[0:2]),
                             1, 1, 1)
    else:
        error = "Invalid year"

    return exp_date, error

def create_datetime_from_sql(stime):
    print("stime!!")
    print(stime)
    year = int(stime[0:4])
    month = int(stime[5:7])
    day = int(stime[8: 10])

    hour = int(stime[11:13])
    minute = int(stime[14:16])

    return datetime(year, month, day, hour, minute, 0)

def clean_tickets(a_tickets):
    tickets = []
    ticket = {}
    subtotal = 0
    tid = 0
    for t in a_tickets:
        ticket['tid'] = tid
        tid = tid + 1
        ticket['seat'] = t[0]
        ticket['type'] = t[1]

        # fetch a price object for that type
        # use get price to get the actual price
        price = Price()
        price.fetch(ticket['type'])
        price_amt = price.get_price()
        ticket['price'] = "${0:.2f} USD".format(price_amt)
        ticket['num_price'] = price_amt
        subtotal = subtotal + price_amt

        tickets.append(dict(ticket))
    return tickets, subtotal

def format_price(string) -> str:
    return "${0:.2f} USD".format(string)
