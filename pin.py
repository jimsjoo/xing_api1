def foo():
    try:
        foo.counter += 1
    except AttributeError:
        foo.counter = 1
    finally:
        print("Counter is %d" % foo.counter)

if __name__=='__main__':
    for i in range(5):
        foo()

def volBar(cheType, qty):
    try:
        if cheType=='+':
            volBar.sumOfBid += qty
        elif cheType == '-':
            volBar.sumOfAsk += qty     
        volBar.sumOfQty += qty
        if  volBar.sumOfQty > 100:
            volBar.sumOfQty = 0
            volBar.sumOfAsk = 0 
            volBar.sumOfBid = 0        
    except AttributeError:
        volBar.sumOfQty = 0
        volBar.sumOfAsk = 0 
        volBar.sumOfBid = 0
    finally:    
        return volBar.sumOfAsk, volBar.sumOfBid

def truePin(volBar.sumOfAsk, volBar.sumOfBid):
    return abs(volBar.sumOfAsk - volBar.sumOfBid) / (volBar.sumOfAsk + volBar.sumOfBid)

