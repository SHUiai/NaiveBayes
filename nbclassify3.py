import sys
import math
def main():
	trainText = open(sys.argv[1], 'r')
	textSet = {}
	splitIntoGroups(trainText, textSet)
	tpSet = {}
	tnSet = {}
	dpSet = {}
	dnSet = {}
	tp_c_sum = 0
	tn_c_sum = 0
	dp_c_sum = 0
	dn_c_sum = 0
	priorTP = 0
	priorTN = 0
	priorDP = 0
	priorDN = 0
	model = open('nbmodel.txt', 'r')
	priorTP, priorTN, priorDP, priorDN, tp_c_sum,tn_c_sum,dp_c_sum,dn_c_sum = readFromModel(model, tpSet, tnSet, dpSet, dnSet, priorTP, priorTN, priorDP, priorDN, tp_c_sum,tn_c_sum,dp_c_sum,dn_c_sum)
	classify(textSet, tpSet, tnSet, dpSet, dnSet, priorTP, priorTN, priorDP, priorDN,tp_c_sum,tn_c_sum,dp_c_sum,dn_c_sum)
	

def splitIntoGroups(trainText, textSet):
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
def readFromModel(model, tpSet, tnSet, dpSet, dnSet, priorTP, priorTN, priorDP, priorDN, tp_c_sum,tn_c_sum,dp_c_sum,dn_c_sum):
	x = model.readline()
	
	x = x.split(' ')
	priorTP = float(x[-1][:-1])
	tp_c_sum = int(x[-2])
	x = model.readline()

	while "the following are for" not in x:
		x = x.split(' ')
		tpSet[x[0]] = int(x[1])
		x = model.readline()
	x = x.split(' ')
	priorTN = float(x[-1][:-1])

	tn_c_sum = int(x[-2])
	x = model.readline()
	while "the following are for" not in x:
		x = x.split(' ')
		tnSet[x[0]] = int(x[1])
		x = model.readline()
	x = x.split(' ')
	priorDP = float(x[-1][:-1])

	dp_c_sum = int(x[-2])
	x = model.readline()
	while "the following are for" not in x:
		x = x.split(' ')
		dpSet[x[0]] = int(x[1])
		x = model.readline()
	x = x.split(' ')
	priorDN = float(x[-1][:-1])
	dn_c_sum = int(x[-2])
	x = model.readline()
	while x!='':
		x = x.split(' ')
		dnSet[x[0]] = int(x[1])
		x = model.readline()
	return priorTP, priorTN, priorDP, priorDN, tp_c_sum,tn_c_sum,dp_c_sum,dn_c_sum
def classify(textSet, tpSet, tnSet, dpSet, dnSet, priorTP, priorTN, priorDP, priorDN,tp_c_sum,tn_c_sum,dp_c_sum,dn_c_sum):
	nboutput = open("nboutput.txt", "w")
	##tpset
	tp_p = math.log(priorTP)
	tn_p = math.log(priorTN)
	dp_p = math.log(priorDP)
	dn_p = math.log(priorDN)
	temp_tp = 0
	temp_tn = 0
	temp_dp = 0 
	temp_dn = 0
	for key in textSet:
		for word in textSet[key]:
			if word not in tpSet:
				temp_tp+=1
		for word in textSet[key]:
			if word not in tnSet:
				temp_tn+=1
		for word in textSet[key]:
			if word not in dpSet:
				temp_dp+=1
		for word in textSet[key]:
			if word not in dnSet:
				temp_dn+=1

	# print(len(tpSet), len(tnSet), len(dpSet), len(dnSet))
	for key in textSet:
		for word in textSet[key]:
			if word in tpSet:
				tp_p += math.log((tpSet[word]+1)/(tp_c_sum+len(tpSet)+temp_tp))
			else:
				tp_p += math.log(1/(tp_c_sum+len(tpSet)+temp_tp))
		for word in textSet[key]:
			if word in tnSet:
				tn_p += math.log((tnSet[word]+1)/(tn_c_sum+temp_tn+len(tnSet)))
			else:
				tn_p += math.log(1/(tn_c_sum+temp_tn+len(tnSet)))
		for word in textSet[key]:
			if word in dpSet:
				dp_p += math.log((dpSet[word]+1)/(dp_c_sum+temp_dp+len(dpSet)))
			else:
				dp_p += math.log(1/(dp_c_sum+temp_dp+len(dpSet)))
		for word in textSet[key]:
			if word in dnSet:
				dn_p += math.log((dnSet[word]+1)/(dn_c_sum+temp_dn+len(dnSet)))
			else:
				dn_p += math.log(1/(dn_c_sum+temp_dn+len(dnSet)))
		if max(tp_p, tn_p, dp_p, dn_p) == tp_p:
			nboutput.write(key+ " "+ "truthful"+ " "+"positive"+"\n")
		elif max(tp_p, tn_p, dp_p, dn_p) == tn_p:
			nboutput.write(key+ " "+ "truthful"+ " "+"negative"+"\n")
		elif max(tp_p, tn_p, dp_p, dn_p) == dp_p:
			nboutput.write(key+ " "+ "deceptive"+ " "+"positive"+"\n")
		elif max(tp_p, tn_p, dp_p, dn_p) == dn_p:
			nboutput.write(key+ " "+ "deceptive"+ " "+"negative"+"\n")
		tp_p = math.log(priorTP)
		tn_p = math.log(priorTN)
		dp_p = math.log(priorDP)
		dn_p = math.log(priorDN)

	nboutput.close()



if __name__ == "__main__":
    main()