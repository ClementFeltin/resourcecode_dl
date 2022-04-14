import copy

def line_prepender(filename, line):
# https://stackoverflow.com/questions/5914627/prepend-line-to-beginning-of-a-file
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def csv_add_header(header,
                   dataframe,
                   filename):

    dataframe.to_csv(filename, sep="\t")
    
    for line in reversed(header):
        line_prepender(filename, line)
