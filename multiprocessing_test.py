import multiprocessing
import os
import subprocess
import platform

# fetch username from system service "whoami".
process = subprocess.Popen("whoami",stdout = subprocess.PIPE)
username, error = process.communicate()

#set some constants values.
baseFolderPathUbuntu = "/home/"+ (username.strip()).decode('utf-8') +"/WB/DarknetMarketParsers/"
baseFolderPathMac = "/Users/"+(username.strip()).decode("utf-8")+"/Documents/ebcs_workspace/DarknetMarketParsers/"
parserFolderPath = ""
logfilePath = ""


if platform.system() == "Darwin":
    parserFolderPath = baseFolderPathMac
    logfilePath = "/Users/"+(username.strip()).decode("utf-8")+"/Desktop/test.txt"
elif platform.system() == "Linux":
    parserFolderPath = baseFolderPathUbuntu
    logfilePath = "/home/"+(username.strip()).decode("utf-8") + "/Desktop/test.txt"


def writelog(message):
    file = open(logfilePath, mode="w+")
    file.write(message)
    file.write("\n")

def runParser(fileName):
    # print('worker ID for filename: ' + fileName + ' is ', os.getpid())
    status = os.WEXITSTATUS(os.system("python3 " + parserFolderPath +fileName))
    # print("worker ID for "+ fileName +"  exited with status ", status)
    return (fileName, status)

def runProductDescriptions():
    print("*************************product descriptions******************************")
    productDescriptionsRelatedFiles = ["product_descriptions_apollon.py","product_descriptions_whitehouse.py",
                                       "product_descriptions_square.py","product_descriptions_agartha.py",
                                       "product_descriptions_bitbazer.py", "product_descriptions_elite.py"]
    pd = multiprocessing.Pool()
    result = pd.map(runParser, productDescriptionsRelatedFiles)
    for record in result:
        print(record[0] + "\t" + str(record[1]))
    return result

def runProductRatings():
    print("*************************product ratings******************************")
    #WH market doesn't have product ratings as of now.
    productRatingsRelatedFiles = ["product_ratings_square.py", "product_ratings_bitbazar.py",
                                  "product_ratings_apollon.py"]
    pr = multiprocessing.Pool()
    result = pr.map(runParser, productRatingsRelatedFiles)
    for record in result:
        print(record[0] + "\t" + str(record[1]))
    return result

def runVendorProfiles():
    print("*************************vendor profiles******************************")
    vendorProfileRelatedFiles = ["vendor_profiles_square.py", "vendor_profiles_bitbazar.py",
                                 "vendor_profiles_whitehouse.py", "vendor_profiles_agartha.py",
                                 "vendor_profiles_apollon.py", "vendor_profiles_elite.py"]
    vp = multiprocessing.Pool()
    result = vp.map(runParser, vendorProfileRelatedFiles)
    for record in result:
        print(record[0] + "\t" + str(record[1]))
    return result

def runVendorRatings():
    print("*************************vendor ratings******************************")
    vendorRatingRelatedFiles = ["vendor_ratings_bitbazar.py", "vendor_ratings_square.py",
                                "vendor_ratings_whitehouse.py","vendor_ratings_apollon.py",
                                "vendor_ratings_agartha.py", "vendor_ratings_elite.py"]
    vr = multiprocessing.Pool()
    result = vr.map(runParser, vendorRatingRelatedFiles)
    for record in result:
        print(record[0] + "\t" + str(record[1]))
    return result

def runParserUtility():
    vendorProfiles = runVendorProfiles()
    productDescriptions = runProductDescriptions()
    vendorRatings = runVendorRatings()
    productRatings = runProductRatings()

    return [productDescriptions, productRatings, vendorProfiles, vendorRatings]

def sendEmail(combinedValues):
    print("combined values are ")
    print(combinedValues)

if __name__ == "__main__":
    combinedValues = runParserUtility()
    sendEmail(combinedValues)