
def hello(msg : str) -> str:
    print("Hello" + msg)
    return msg

hello("test")

mylist = [5, 6, 7]

for num in mylist:
    print(mylist)

for i in range(0, 30):
    print("test")

class Mine:
    def ___init___(self):
        print("init")
        self.myFunc()

    def myFunc(self):
        print("my func")

my_dict = {'test' : 1,
           'tom' : 12}
print(my_dict['tom'])
'''
multiline comment
'''
#single line comments

if i < 5:
    print("i < 5")
elif i > 5:
    print("i > 5")

my_tuples = ("test", "pair")
