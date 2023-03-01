import time
'''
This overwrites anything that was in the file previously
'''
file = open("text.txt", "w")


for i in range(15, 30):
    file.write("testing|line|" + str(i) + '\n')

time = time.time()
file = open("text.txt", "r")
lines = file.readlines()[1:] # skip first line

for line in lines:
    line = line.strip('\n') # Remove new line char from end of line
    vars = line.split("|") # Split each element of the line into a var split up by | character
    print(len(line.split("|")))
    print(vars)

file.close()