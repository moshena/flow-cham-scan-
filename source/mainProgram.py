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
        print(HEADER.headerString)
        return 1
    else:
        return printError("Image path should be pass")




def main():
    # parse command line options
    data = objects.mainData(len(sys.argv), sys.argv)

    if (data.PARAMSlength < 2):
        printError("Image path should be pass")
        exit(-1)

    data.setImage()

    # init objects

    filterObj = filter.filter(data)
    classifierObj = classifier.classifier()
    flowChartObj = flowChart.flowChart("some params")
    convertorObj =  convertor.convertor("some params")

    #start process


    head =filterObj.startFiler(data)
    if(checkHEADER(head) ==-1):
        printError("UnknownError")

    head =classifierObj.startProcess(data)
    if(checkHEADER(head) ==-1):
        printError("UnknownError")

    head =flowChartObj.startProcess()
    if(checkHEADER(head) ==-1):
        printError("UnknownError")

    head =convertorObj.startProcess()
    if(checkHEADER(head) ==-1):
        printError("UnknownError")

    print("Complete")










if __name__ == "__main__":
    main()










