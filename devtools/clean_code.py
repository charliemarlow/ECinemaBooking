import os

autopep_args = "autopep8 --in-place --aggressive {}"
files = ["ecinema/*.py",
         "ecinema/models/*.py",
         "ecinema/controllers/*.py",
         "ecinema/tools/*.py",
         "ecinema/data/*.py",]

for i in range(0, 5):
    for f in files:
        os.system(autopep_args.format(f))



arg = "pycodestyle {}"
for f in files:
    print("")
    print("For files: {}".format(f))
    os.system(arg.format(f))

