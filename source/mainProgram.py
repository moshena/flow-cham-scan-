import sys
import objects
import filter
import classifier
import flowChart
import convertor
import HEADER


def printError(str):
    print("[Error] " + str)
    return -1

def checkHEADER(HEADER):
    #if(HEADER.status<100):# under debug
    if True:
        return 1
    else:
        return printError("Image path should be pass")




def main():
    # parse command line options
    data = objects.mainData(len(sys.argv), sys.argv)

    if (data.PARAMSlength < 2):
        printError("Image path should be pass")

    data.setImage()

    # init objects

    filterObj = filter.filter("some params")
    classifierObj = classifier.classifier("some params")
    flowChartObj = flowChart.flowChart("some params")
    convertorObj =  convertor.convertor("some params")

    #start process


    HEADER =filterObj.startFiler()
    if(checkHEADER(HEADER) ==-1):
        printError("UnkmownError")

    HEADER =classifierObj.startProcess()
    if(checkHEADER(HEADER) ==-1):
        printError("UnkmownError")

    HEADER =flowChartObj.startProcess()
    if(checkHEADER(HEADER) ==-1):
        printError("UnkmownError")

    HEADER =convertorObj.startProcess()
    if(checkHEADER(HEADER) ==-1):
        printError("UnkmownError")

    print("Complete")










if __name__ == "__main__":
    main()










