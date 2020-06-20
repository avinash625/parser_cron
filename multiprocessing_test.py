import multiprocessing
import os

def runParser(fileName):
    print('worker ID for filename: ' + fileName + ' is ', os.getpid())
    status = os.WEXITSTATUS(os.system("python3" + " /Users/avi/Documents/ebcs_workspace/DarknetMarketParsers/"+fileName))
    print("worker ID for "+ fileName +"  exited with status ", status)
    return (fileName, status)

if __name__ == "__main__":
    mylist = ["product_descriptions_agartha.py", "product_descriptions_bitbazer.py", "vendor_profiles_bitbazar.py", "vendor_ratings_bitbazar.py", "vendor_ratings_whitehouse.py","vendor_profiles_whitehouse.py"]
    p = multiprocessing.Pool()
    result = p.map(runParser, mylist)
    print("*******************************************************")
    for record in result:
        print(record[0] + "\t" + record[1])
