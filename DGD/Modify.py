import os

def modify_repeat():
    f = open("index.txt", 'r')
    g = open("new.txt",'w')

    repeat = []
    for line in f.readlines():
        alt, src = line.split('\t')
        # print alt,src
        if os.path.exists("newscontent1\\"+alt) and alt not in repeat:
            repeat.append(alt)
            g.write(alt+'\t'+src)

    f.close()
    g.close()


def modify_notitle():
    root = "newscontent1"
    folder = "newstxt1"
    count = 1
    for root,dirnames,filenames in os.walk(root):
        for filename in filenames:
            print count,filename
            count += 1
            path = os.path.join(root,filename)
            if not os.path.exists(os.path.join(folder,filename)):
                os.remove(path)

    picroot = "thepaper1"
    for root,dirnames,filenames in os.walk(picroot):
        for filename in filenames:
            path = os.path.join(picroot,filename)
            if not os.path.exists(os.path.join(folder,filename)[:-4]+'.txt'):
                os.remove(path)


if __name__ == '__main__':
    modify_repeat()
