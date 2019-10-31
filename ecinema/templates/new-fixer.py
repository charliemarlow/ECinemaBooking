import sys
import os

print(len(sys.argv) - 1)

for name in sys.argv:
    if(name != sys.argv[0]):
        with open(name, "rt") as fin:
            with open("TEMP.txt", "wt") as fout:
                for line in fin:
                    if(line.replace("{{ url_for('static', filename='https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js') }}", '') != line):
                        print(line)
                        line = line.replace("{{ url_for('static', filename='https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js') }}","https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js")
                        print(line)
                    if( line.replace("{{ url_for('static', filename='https://maps.googleapis", '') != line):
                        line = line.replace("{{ url_for('static', filename='https://maps.googleapis.com/maps/api/js?key=AIzaSyCjCGmQ0Uq4exrzdcL6rvxywDDOvfAu6eE') }}","https://maps.googleapis.com/maps/api/js?key=AIzaSyCjCGmQ0Uq4exrzdcL6rvxywDDOvfAu6eE")

                    fout.write(line)

        os.system("DEL " + name)

        with open("TEMP.txt", "rt") as f1in:
            with open(name, "wt") as f1out:
                for line in f1in:
                    f1out.write(line)
