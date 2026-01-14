import os
import subprocess



def getExtensionName(text:str):
    return text[text.rfind('.'):]
def removeExtensionName(text:str):
    return text[:text.rfind('.')]

class exam:
    code = ""
    time = ""
    paper = 0
    variation = 0

    qppath=""
    xopppath=""
    mspath=""
    def __init__(self, filename):
        sanitized = removeExtensionName(filename)
        splitted = sanitized.split('_')
        self.code = splitted[0]
        self.time = splitted[1]
        self.paper = splitted[3][0]
        self.variation = splitted[3][1]
        self.checkFiles()
    def info(self):
        return [self.code, self.time, self.paper + self.variation, str(os.path.exists(self.qppath)), str(os.path.exists(self.xopppath)), str(os.path.exists(self.mspath))]
    def checkFiles(self):
        qppath="_".join([self.code,self.time,"qp",self.paper + self.variation]) + ".pdf"
        xopppath=qppath.replace(".pdf", ".xopp")
        mspath="_".join([self.code,self.time,"ms",self.paper + self.variation]) + ".pdf"
        if os.path.exists(qppath):
            self.qppath = qppath
        if os.path.exists(xopppath):
            self.xopppath = xopppath
        if os.path.exists(mspath):
            self.mspath = mspath
    def __eq__(self, other):
        # Check if 'other' is also an exam object
        if not isinstance(other, exam):
            return False
            
        # Return True if the important data matches
        return (self.code == other.code and 
                self.time == other.time and 
                self.paper == other.paper and
                self.variation == other.variation
                )
    
def clear():
    os.system( 'clear' )
    os.system( 'cls' )
def printtable(printlist, buffersize):
    for i in printlist:
        print(i, end=" "*(buffersize-len(i)))
    print('')

columnbuffer = 10
while True:
    rawpath = __file__
    index = rawpath.rfind("/")
    execpath = rawpath[:index]
    filelist = os.listdir(str(execpath))
    listofqp = []
    examlist = []
    for file in filelist:
        if getExtensionName(file) == ".pdf":
            
            ex = exam(file)
            if(not ex in examlist):
                examlist.append(ex)
    clear()
    printtable(['Index', 'CODE', 'TIME', 'PAP', 'HAS_QP', 'HAS_XOPP', 'HAS_MS'], columnbuffer)
    for i in range(len(examlist)):
        printtable([str(i)] + examlist[i].info(), columnbuffer)

    examindex = int(input("Enter index of exam:\n"))
    print("Enter the operation you would like to perform:")
    print("(1) Edit question paper")
    print("(2) Open mark scheme")
    print("(q) Quit")
    usrinput = input()
    selectedexam = examlist[examindex]
    if usrinput == "1":
        if selectedexam.xopppath:
            # Popen starts the process and immediately continues with the Python script
            subprocess.Popen(
                ["xournalpp", selectedexam.xopppath],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("Opening Xournal++...")
        else:
            subprocess.Popen(
                ["xournalpp", selectedexam.qppath],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("Opening Xournal++...")
    elif usrinput == "2":
        if selectedexam.mspath:
            subprocess.Popen(
                ["open", selectedexam.mspath],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("Opening Xournal++...")
    else:
        exit(1)