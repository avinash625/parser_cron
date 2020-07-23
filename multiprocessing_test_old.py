import multiprocessing
import os
import subprocess
import platform
from sendEmail import sendEmail
import pprint

# fetch username from system service "whoami".
process = subprocess.Popen("whoami",stdout = subprocess.PIPE)
username, error = process.communicate()

#set some constants values.
baseFolderPathUbuntu = "/home/"+ (username.strip()).decode('utf-8') +"/workbench/DarknetMarketParsers/"
baseFolderPathMac = "/Users/"+(username.strip()).decode("utf-8")+"/Documents/ebcs_workspace/DarknetMarketParsers/"
parserFolderPath = ""
logfilePath = ""
listedMarkets = ["agartha","bitbazar","whitehouse","square","apollon","elite","icarus","cryptonia", "asean","amazin","darkode","darkfox","darkbay","darknet"]

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

def runProductDescriptions(result):
    print("*************************product descriptions******************************")
    productDescriptionsRelatedFiles = ["product_descriptions_apollon.py","product_descriptions_whitehouse.py",
                                       "product_descriptions_square.py","product_descriptions_agartha.py",
                                       "product_descriptions_bitbazar.py", "product_descriptions_elite.py",
                                       "product_descriptions_cryptonia.py", "product_descriptions_asean.py",
                                       "product_descriptions_amazin.py","product_descriptions_darkbay.py",
                                       "product_descriptions_darkfox.py","product_descriptions_darknet.py",
                                       "product_descriptions_darkode.py","product_descriptions_deeppaste"]
    pd = multiprocessing.Pool()
    processStatusList = pd.map(runParser, productDescriptionsRelatedFiles)
    for record in processStatusList:
        result[record[0].partition("ons_")[2][:-3]]["productDescriptions"] =  str(record[1])
    return result

def runProductRatings(result):
    print("*************************product ratings******************************")
    #WH market doesn't have product ratings as of now.
    productRatingsRelatedFiles = ["product_ratings_square.py", "product_ratings_bitbazar.py",
                                  "product_ratings_apollon.py", "product_ratings_elite.py",
                                  "product_ratings_cryptonia.py", "product_ratings_asean.py",
                                  "product_ratings_amazin.py","product_ratings_darkbay.py",
                                  "product_ratings_darkfox.py","product_ratings_darknet.py"]
    pr = multiprocessing.Pool()
    processStatusList = pr.map(runParser, productRatingsRelatedFiles)
    for record in processStatusList:
        result[record[0].partition("ngs_")[2][:-3]]["productRatings"] = str(record[1])
    return result

def runVendorProfiles(result):
    print("*************************vendor profiles******************************")
    vendorProfileRelatedFiles = ["vendor_profiles_square.py", "vendor_profiles_bitbazar.py",
                                 "vendor_profiles_whitehouse.py", "vendor_profiles_agartha.py",
                                 "vendor_profiles_apollon.py", "vendor_profiles_elite.py",
                                 "vendor_profiles_icarus.py", "vendor_profiles_cryptonia.py",
                                 "vendor_profiles_asean.py","vendor_profiles_dark0de.py",
                                 "vendor_profiles_darkbay.py","vendor_profiles_darkfox.py",
                                 "vendor_profiles_darknet.py"]
    vp = multiprocessing.Pool()
    processStatusList = vp.map(runParser, vendorProfileRelatedFiles)
    for record in processStatusList:
        result[record[0].partition("les_")[2][:-3]]["vendorProfiles"] = str(record[1])
    return result

def runVendorRatings(result):
    print("*************************vendor ratings******************************")
    vendorRatingRelatedFiles = ["vendor_ratings_bitbazar.py", "vendor_ratings_square.py",
                                "vendor_ratings_whitehouse.py","vendor_ratings_apollon.py",
                                "vendor_ratings_agartha.py", "vendor_ratings_elite.py",
                                "vendor_ratings_cryptonia.py", "vendor_ratings_asean.py",
                                "vendor_ratings_darkbay.py","vendor_ratings_darkfox.py",
                                "vendor_Ratings_darknet.py"]
    vr = multiprocessing.Pool()
    processStatusList = vr.map(runParser, vendorRatingRelatedFiles)
    for record in processStatusList:
        result[record[0].partition("ngs_")[2][:-3]]["vendorRatings"] = str(record[1])
    return result

def runParserUtility():
    result = getDefaultResultSet()
    result = runVendorProfiles(result)
    result = runProductDescriptions(result)
    result = runVendorRatings(result)
    result = runProductRatings(result)

    return result

def getDefaultResultSet():
    global listedMarkets
    result = {}
    for market in listedMarkets:
        result.update({market:{"productDescriptions": "NA", "productRatings":"NA", "vendorProfiles":"NA", "vendorRatings":"NA"}})
    return result

if __name__ == "__main__":
    parsersResult = runParserUtility()
    sendEmail(parsersResult)
    pprint.pprint(parsersResult,indent=4)