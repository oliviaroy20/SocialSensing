from langdetect import detect

def removeLinks(text):
    t = text.split(" ")
    for i,word in enumerate(t):
        if word.startswith("http") or word.startswith("https"):
            t.pop(i)
    return " ".join(t)

f = open("NewObamacare.csv",'r',encoding="utf8")
w1 = open("NewObamacareEn.csv",'w',encoding="utf8")
w2 = open("NewObamacareNotEn.csv",'w',encoding="utf8")
notEng = 0
Total = -1 # b/c first line doesn't count
for line in f.readlines():
    try:
        #if Total > 1000:
        #    break
        text = line.split(";")[4]
        d = detect(text)
        Total = Total + 1
        if d != "en":
            d = detect(text)
            notEng = notEng + 1
            w2.write(line)       
        else:
            w1.write(line)
    except KeyboardInterrupt:
        break
    except:
        print("Error with "+line)
print("Not English: "+str(notEng)+" Total: "+str(Total))
