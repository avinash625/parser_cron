import threading
import time
import os

exitFlag = 0
fileNameExitMap = {}

class RunParsers(threading.Thread):
    def __init__(self, threadID, name, counter, parserFileName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.parserFileName = parserFileName

    def runparser(self, parserFileName):
        status = os.WEXITSTATUS(os.system("python3 " + "/Users/avi/Documents/ebcs_workspace/DarknetMarketParsers/"+ self.parserFileName))
        if status == 0:
            fileNameExitMap.update({self.parserFileName: True})
        else:
            fileNameExitMap.update({self.parserFileName: False})

    def run(self):
        print("starting thread : ", self.name)
        self.runparser(self.parserFileName)
        print("Exiting :" , self.name)

if __name__ == "__main__":
    filesList = ["product_descriptions_agartha.py", "product_descriptions_bitbazer.py", "vendor_profiles_bitbazar.py", "vendor_ratings_bitbazar.py", "vendor_ratings_whitehouse.py","vendor_profiles_whitehouse.py"]
    threadsList = []
    for files in filesList:
        newly_spaned_thread = RunParsers(1,files,1,files)
        newly_spaned_thread.start()
        threadsList.append(newly_spaned_thread)

    print(threadsList)


