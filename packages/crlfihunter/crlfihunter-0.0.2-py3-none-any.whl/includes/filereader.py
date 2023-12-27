from includes import crlfi

def reader(input,output):

    with open(input, 'r') as file:
        for line in file:
            crlfi.scan(line.strip(),output)  
