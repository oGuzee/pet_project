# Python program to illustrate # nested functions
import datetime

# Closure
def outerFunction(now = datetime.datetime.now()):
    def innerFunction(): 
        print('Application started at: ', now) 
    innerFunction()


if __name__ == '__main__': 
    outerFunction()
