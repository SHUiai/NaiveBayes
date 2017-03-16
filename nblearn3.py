import sys
def main():
    trainText = open(sys.argv[1], 'r')
    trainLabel = open(sys.argv[2], 'r')
    textSet = {}
    labelSet = {}
    truthful_negative = {}
    deceptive_negative = {}
    truthful_positive = {}
    deceptive_positive = {}
    truthful_negative_P = {}
    deceptive_negative_P = {}
    truthful_positive_P = {}
    deceptive_positive_P = {}
    
    tp_rate = 0
    tn_rate = 0
    dp_rate = 0
    dn_rate = 0

    splitIntoGroups(trainText, trainLabel, textSet, labelSet, truthful_negative, deceptive_negative, truthful_positive, deceptive_positive)
    tplbsum = 0
    tnlbsum = 0
    dplbsum = 0
    dnlbsum = 0
    for key in labelSet:
        if labelSet[key] == ['truthful', 'positive']:
            tplbsum+=1
        elif labelSet[key] == ['truthful', 'negative']:
            tnlbsum+=1
        elif labelSet[key] == ['deceptive', 'positive']:
            dplbsum+=1
        elif labelSet[key] == ['deceptive', 'negative']:
            dnlbsum+=1
    trian_text_sum = len(textSet)

    tp_rate = tplbsum/trian_text_sum
    tn_rate = tnlbsum/trian_text_sum
    dp_rate = dplbsum/trian_text_sum
    dn_rate = dnlbsum/trian_text_sum          
    countProbability(truthful_positive, truthful_negative, deceptive_positive, deceptive_negative, truthful_positive_P, truthful_negative_P, deceptive_positive_P, deceptive_negative_P)
    tpsum = 0
    tnsum = 0
    dpsum = 0
    dnsum = 0
    for key in truthful_positive:
        # if truthful_positive[key]<250:
            tpsum += truthful_positive[key]
    for key in truthful_negative:
        # if truthful_negative[key]<250:
            tnsum += truthful_negative[key]
    for key in deceptive_positive:
        # if deceptive_positive[key]<250:
            dpsum += deceptive_positive[key]
    for key in deceptive_negative:
        # if deceptive_negative[key]<250:
            dnsum += deceptive_negative[key]
    
    trainText.close()
    trainLabel.close()
    nbmodel = open("nbmodel.txt",'w')
    nbmodel.write("the following are for truthful_positive"+ " "+ str(tpsum)+ " "+ str(tp_rate)+ "\n")
    for key in truthful_positive_P:
        # if truthful_positive[key]<250:
            nbmodel.write(key)
            nbmodel.write(" ")
            nbmodel.write(repr(truthful_positive_P[key])+' '+'/'+' '+ str(tpsum)+'\n')
    nbmodel.write("the following are for truthful_negative"+ " "+ str(tnsum)+" "+ str(tn_rate)+  "\n")
    for key in truthful_negative_P:
        # if truthful_negative[key]<250:
            nbmodel.write(key)
            nbmodel.write(" ")
            nbmodel.write(repr(truthful_negative_P[key])+' '+'/'+' '+ str(tnsum)+'\n')
    nbmodel.write("the following are for deceptive_positive"+ " "+ str(dpsum)+" "+ str(dp_rate)+ "\n")
    for key in deceptive_positive_P:
        # if deceptive_positive[key]<250:
            nbmodel.write(key)
            nbmodel.write(" ")
            nbmodel.write(repr(deceptive_positive_P[key])+' '+'/'+' '+ str(dpsum)+'\n')
    nbmodel.write("the following are for deceptive_negative"+ " "+ str(dnsum)+ " "+ str(dn_rate)+ "\n")
    for key in deceptive_negative_P:
        # if deceptive_negative[key]<250:
            nbmodel.write(key)
            nbmodel.write(" ")
            nbmodel.write(repr(deceptive_negative_P[key])+' '+'/'+' '+ str(dnsum)+'\n')
    nbmodel.close()



    
   
def splitIntoGroups(trainText, trainLabel, textSet, labelSet, truthful_negative, deceptive_negative, truthful_positive, deceptive_positive):
    ##trainLabel (key, labels)
    for line in trainLabel:
        line = line.split(' ')
        tempList = [" ", " "]
        tempList[0] = line[1][:]
        tempList[1] = line[2][:-1]
        labelSet[line[0]] = tempList
    ##trainText (key,wordlist)
    for line in trainText:
        line = line.split(' ')
        temp = line[1:][:]
        temp[-1] = temp[-1][:-1]
        punctuation = ['!',',','.','?',':', '[',']','/', '*','(', ')','-']
        for i in range(len(temp)):
            temp[i]=temp[i].lower()
            for p in punctuation:
                if p in temp[i]:
                    temp[i] = temp[i].replace(p, '')
        while '' in temp:
            temp.remove('')
            
        textSet[line[0]] = temp
    ##truthful_positive
    ##truthful_negative
    ##deceptive_positive
    ##deceptive_negative
    for key in labelSet:
        if labelSet[key] == ['truthful', 'positive']:
            ##put item in truthful_positive and count
            for word in textSet[key]:
                if word in truthful_positive:
                    truthful_positive[word] += 1
                else:
                    truthful_positive[word] = 1
        elif labelSet[key] == ['truthful', 'negative']:
            for word in textSet[key]:
                if word in truthful_negative:
                    truthful_negative[word] += 1
                else:
                    truthful_negative[word] = 1
        elif labelSet[key] == ['deceptive', 'positive']:
            for word in textSet[key]:
                if word in deceptive_positive:
                    deceptive_positive[word] += 1
                else:
                    deceptive_positive[word] = 1
        elif labelSet[key] == ['deceptive', 'negative']:
            for word in textSet[key]:
                if word in deceptive_negative:
                    deceptive_negative[word] += 1
                else:
                    deceptive_negative[word] = 1
    # for key in truthful_positive:
    #     print(key, truthful_positive)
        
def countProbability(truthful_positive, truthful_negative, deceptive_positive, deceptive_negative, truthful_positive_P, truthful_negative_P, deceptive_positive_P, deceptive_negative_P):
    
    ##probability
    for key in truthful_positive:
        truthful_positive_P[key] = truthful_positive[key]
    for key in truthful_negative:
        truthful_negative_P[key] = truthful_negative[key]
    for key in deceptive_positive:
        deceptive_positive_P[key] = deceptive_positive[key]
    for key in deceptive_negative:
        deceptive_negative_P[key] = deceptive_negative[key]



        
if __name__ == "__main__":
    main()
  
    
    
