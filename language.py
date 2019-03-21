from langdetect import detect

def removeLinks(text): #(unnecessary)
    t = text.split(" ")
    for i,word in enumerate(t):
        if word.startswith("http") or word.startswith("https"):
            t.pop(i)
    return " ".join(t)

f = open("NewObamacare.csv",'r',encoding="utf8") # input file
w1 = open("NewObamacareEn.csv",'w',encoding="utf8") # output for english
w2 = open("NewObamacareNotEn.csv",'w',encoding="utf8") # output for nonEnglish (optional)
notEng = 0 # (optional)
Total = -1 # -1 b/c first line doesn't count (optional)
for line in f.readlines():
    try:
        text = line.split(";")[4]
        d = detect(text)
        Total = Total + 1 # (optional)
        if d != "en":
            notEng = notEng + 1 # Number for statistics (optional)
            w2.write(line) # output for nonEnglish (optional)
        else:
            w1.write(line) #output for English
    except KeyboardInterrupt:
        break
    except:
        print("Error with "+line)
print("Not English: "+str(notEng)+" Total: "+str(Total)) # (optional)
