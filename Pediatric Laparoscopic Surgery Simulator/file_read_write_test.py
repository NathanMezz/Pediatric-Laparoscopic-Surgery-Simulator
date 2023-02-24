
'''
This overwrites anything that was in the file previously
'''
file = open("text.txt", "w")


for i in range(15, 30):
    file.write("testing|line|" + str(i) + '\n')

file = open("text.txt", "r")
lines = file.readlines()

for line in lines:
    line = line.strip('\n') # Remove new line char from end of line
    vars = line.split("|") # Split each element of the line into a var split up by | character
    print(vars)

file.close()