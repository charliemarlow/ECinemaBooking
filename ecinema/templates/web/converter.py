import sys
import os

print(len(sys.argv) - 1)

for name in sys.argv:
    if(name != sys.argv[0]):
        with open(name, "rt") as fin:
            with open("TEMP.txt", "wt") as fout:
                for line in fin:
                    if((line.replace('src', '') != line) and (line.replace('url_for', '') == line)):
                        convert = "{{ url_for('static', filename='" + (((line[line.find('src'):]).split('"'))[1]) + "') }}"
                        line = line.replace((((line[line.find('src'):]).split('"'))[1]), convert)

                    if(( line.replace('rel=\"stylesheet\"', '') != line) and (line.replace('url_for', '') == line)):
                        convert = "{{ url_for('static', filename='" + (((line[line.find('href'):]).split('"'))[1]) + "') }}"
                        line = line.replace((((line[line.find('href'):]).split('"'))[1]), convert)


                    fout.write(line)

        os.system("DEL " + name)

        with open("TEMP.txt", "rt") as f1in:
            with open(name, "wt") as f1out:
                for line in f1in:
                    f1out.write(line)
