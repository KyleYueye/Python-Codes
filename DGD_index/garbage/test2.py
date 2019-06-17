file = open('txt2.txt',encoding='utf8')
lines = file.readlines()
if lines[2][0] != ' ':
    date,time = lines[2].split('\t')[0],lines[2].split('\t')[1].strip()
else:
    date,time = lines[2].strip()[-16:-6],lines[2].strip()[-5:]

print(date,time)

s = "  2018-11-11 23:24\n"
print(s[-17:-7],s[-6:-1])