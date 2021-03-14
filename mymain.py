# file purely used for testing code by running this file in the terminal
from src.DTMC.spatialModel.Hub.HubSIS import HubSIS

def main():
    test = HubSIS(1000, .17, 4, 2, 25, 999, 1, 31, .3)
    test.run()
    test.plot()
    #print(test.toDataFrame())

if  __name__ == '__main__':
    main()

