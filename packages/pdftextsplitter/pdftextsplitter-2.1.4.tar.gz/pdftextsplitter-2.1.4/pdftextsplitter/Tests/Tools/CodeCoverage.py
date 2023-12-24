import sys
import os
# caution: path[0] is reserved for script path (or '' in REPL)

class myreport:
    """
    Used to store the information from the report of coverage in an easily-accesible format.
    """
    
    def __init__(self):
        self.filename = ""
        self.nlines = 0
        self.nmissed = 0
        self.coverage = 0.0
        self.missedlines = ""
        
    def printreport(self):
        """
        Function to print the content of the class.
        """
        print("Filename = <" + str(self.filename) + "> | nLines=" + str(self.nlines) + " | #Missed=" + str(self.nmissed) + " | %Coverage= " + str(self.coverage) + " | MissedLines = " + str(self.missedlines))
        
    def printclean(self):
        """
        Function to print the content of the class in a nice overview:
        """
        print(str(self.filename) + "                    " + str(self.coverage) + "%                    " + str(self.missedlines))

def CodeCoverage(Coverage_Threshold: float):
    """
    This function processes the report from the coverage-package and processes it a little
    further to make a more easily-readable format.
    
    # parameters: 
    Coverage_Threshold (float): on 0-100, the threshold below which we report a certain file.
    # Return: None: printed on the terminal.
    """
    
    # ---------------------------------------------------------------
    
    # Begin by reading the report
    report = open("../Reports/TheReport.txt", 'r',encoding='utf-8',errors='ignore')
    textarray = []
    arrayindex = -1
    lineindex = -1
    
    # Loop over the textfile:
    for textline in report:
        
        # Update index:
        lineindex = lineindex + 1
        
        # Skip lines that we cannot use:
        if (not("Name" in textline))and(not("TOTAL" in textline))and(not("------" in textline)):
            
            # Only open new textlines for new files:
            if (".py" in textline):
                textarray.append(textline)
                arrayindex = arrayindex + 1
            else:
                if (arrayindex>=0):
                    textarray[arrayindex] = textarray[arrayindex] + " " + textline
    
    # That is enough to read the proper file. Now, put it in the proper format:
    TheData = []
    for textline in textarray:
        
        # Split the textlines, so we can put them in the class:
        textparts = textline.split()
        length = len(textparts)
        
        # Create a new class and attempt to fill it:
        thisreport = myreport()
        if (length>0): thisreport.filename = str(textparts[0])
        if (length>1): thisreport.nlines = int(textparts[1])
        if (length>2): thisreport.nmissed = int(textparts[2])
        if (length>3): thisreport.coverage = float(textparts[3].replace("%",""))
        if (length>4): 
            for n in range(4,length):
                thisreport.missedlines = thisreport.missedlines + " " + str(textparts[n])
        
        # Clean up the filenames:
        if ("/" in thisreport.filename):
            splittedname = thisreport.filename.split("/")
            for namepart in splittedname:
                if (".py" in namepart):
                    thisreport.filename = namepart
        
        # Append it to the array:
        TheData.append(thisreport)
    
    # Next, Identify the files in the core product directory:
    print("==================================================================================\n")
    CoreNames = os.listdir('../../TextPart/')
    nr_problems = 0
                
    # Then, identify those files in TheData:
    print(" [OUTCOMES]: Files in TextPart-folder with code coverage below " + str(Coverage_Threshold) + "%\n")
    for myname in CoreNames:
        isfound = False
        for mydata in TheData:
            if (myname==mydata.filename):
                isfound = True
                if (mydata.coverage<Coverage_Threshold):
                    mydata.printclean()
                    nr_problems = nr_problems + 1
        if not isfound:
            if (".py" in myname)and(not("BatchExecution" in myname))and(not("SingleRun" in myname)):
                print(myname + "                    " + "[NOT TESTED!!!]")
                nr_problems = nr_problems + 1
                
    if (nr_problems==0):
        print("\n ==> CONGRATULATIONS!!!")
        print(" All files in this folder meet the required threshold for code coverage!\n")
        
    print("==================================================================================\n")
    
    # Next, Identify the files in the core product directory:
    CoreNames = os.listdir('../Tools/')
    nr_problems = 0
                
    # Then, identify those files in TheData:
    print(" [OUTCOMES]: Files in Tests/Tools/-folder with code coverage below " + str(Coverage_Threshold) + "%\n")
    for myname in CoreNames:
        isfound = False
        for mydata in TheData:
            if (myname==mydata.filename):
                isfound = True
                if (mydata.coverage<Coverage_Threshold):
                    mydata.printclean()
                    nr_problems = nr_problems + 1
        if not isfound:
            if (".py" in myname):
                print(myname + "                    " + "[Currently not used in the product or tests...]")
                
    if (nr_problems==0):
        print("\n ==> CONGRATULATIONS!!!")
        print(" All files in this folder meet the required threshold for code coverage!\n")
        
    print("==================================================================================\n")
    
    # Next, Identify the files in the core product directory:
    CoreNames = os.listdir('../../Source/')
    nr_problems = 0
                
    # Then, identify those files in TheData:
    print(" [OUTCOMES]: Files in Source-folder with code coverage below " + str(Coverage_Threshold) + "%\n")
    for myname in CoreNames:
        isfound = False
        for mydata in TheData:
            if (myname==mydata.filename):
                isfound = True
                if (mydata.coverage<Coverage_Threshold):
                    mydata.printclean()
                    nr_problems = nr_problems + 1
        if not isfound:
            if (".py" in myname)and(not("Execution" in myname)):
                print(myname + "                    " + "[NOT TESTED!!!]")
                nr_problems = nr_problems + 1
    
    if (nr_problems==0):
        print("\n ==> CONGRATULATIONS!!!")
        print(" All files in this folder meet the required threshold for code coverage!\n")
        
    print("==================================================================================\n")
                    
            
    # Done.
    
if __name__ == '__main__':
        
    # Identify parameters:
    Coverage_Threshold = 90.0
    if (len(sys.argv)>1):
        try:
            Coverage_Threshold = float(sys.argv[1])
        except:
            print("\n\n===> Cannot convert " + str(sys.argv[1]) + " to float-object!\n\n")
    
    # Execute:
    CodeCoverage(Coverage_Threshold)
