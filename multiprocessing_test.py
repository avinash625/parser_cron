import multiprocessing
import os
import subprocess
import platform

process = subprocess.Popen("whoami",stdout = subprocess.PIPE)
username, error = process.communicate()
baseFolderPathUbuntu = "/home/"+ (username.strip()).decode('utf-8') +"/WB/DarknetMarketParsers/"
baseFolderPathMac = "/Users/"+(username.strip()).decode("utf-8")+"/Documents/DarknetMarketParsers/"
parserFolderPath = ""
logfilePath = ""
def writelog(message):
    file = open(logfilePath, mode="w")
    file.write(message)
    file.write("\n")


if platform.system() == "Darwin":
    parserFolderPath = baseFolderPathMac
    logfilePath = "/Users/avi/Desktop/test.txt"
elif platform.system() == "Linux":
    parserFolderPath = baseFolderPathUbuntu
    logfilePath = "/home/"+(username.strip()).decode("utf-8") + "/Desktop/test.txt"



def runParser(fileName):
    print('worker ID for filename: ' + fileName + ' is ', os.getpid())
    status = os.WEXITSTATUS(os.system("python3 " + parserFolderPath +fileName))
    print("worker ID for "+ fileName +"  exited with status ", status)
    return (fileName, status)

if __name__ == "__main__":
    ## Do not change the following order. First we need to parse vendor profile, product desc, product rating and then
    ## vendor ratings. This is because vendor ID is required for PD, PR and VR.

    ## for vendor profiles
    vendorProfileRelatedFiles = ["vendor_profiles_bitbazar.py", "vendor_profiles_whitehouse.py", "vendor_profiles_agartha.py"]
    vp = multiprocessing.Pool()
    result = vp.map(runParser, vendorProfileRelatedFiles)
    print("*************************vendor profiles******************************")
    for record in result:
        print(record[0] + "\t" + str(record[1]))

    ## for product descriptions
    productDescriptionsRelatedFiles = ["product_descriptions_agartha.py", "product_descriptions_bitbazer.py"]
    pd = multiprocessing.Pool()
    result = pd.map(runParser, productDescriptionsRelatedFiles)
    print("*************************product descriptions******************************")
    for record in result:
        print(record[0] + "\t" + str(record[1]))

    ## for product ratings
    productRatingsRelatedFiles = []
    pr = multiprocessing.Pool()
    result = pr.map(runParser, productDescriptionsRelatedFiles)
    print("*************************product descriptions******************************")
    for record in result:
        print(record[0] + "\t" + str(record[1]))

    ## for vendor ratings
    vendorRatingRelatedFiles = ["vendor_ratings_bitbazar.py",
                                   "vendor_ratings_whitehouse.py", "vendor_ratings_apollon.py"]
    vr = multiprocessing.Pool()
    result = vr.map(runParser, vendorProfileRelatedFiles)
    print("*************************vendor profiles******************************")
    for record in result:
        print(record[0] + "\t" + str(record[1]))

