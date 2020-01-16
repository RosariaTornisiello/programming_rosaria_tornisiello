def createLista(file):
	lista=[]
	for line in file:
		line=line.rstrip()
		line=line.split()
		lista.append(line)
	return(lista)

def createDic(lista):
	dic={}
	for i in range(len(lista[0])):
		for j in range(1,len(lista)):
			dic[lista[0][i]+lista[j][0]]=lista[i+1][j]
	return(dic)

def scoreAllineamento(seq1,seq2):
	score=0
	for i in range(len(seq1)):
		if '-' in (seq1[i]+seq2[i]):
			score+=-2
		elif (seq1[i]+seq2[i]) not in dic:
			score+=int(dic[seq2[i]+seq1[i]])
		else:
			score+=int(dic[seq1[i]+seq2[i]])
	return(score)

blosum=open("./BLOSUM62_square.txt","r")
PAM=open("./PAM250_square.txt","r")
lista=createLista(blosum)
print(lista)
dic=createDic(lista)
print(dic)
import input_data
align1=input_data.align1
s1=align1[0]
s2=align1[1]
align2=input_data.align2
s3=align2[0]
s4=align2[1]
align3=input_data.align3
s5=align3[0]
s6=align3[1]
scoreallineamento1=scoreAllineamento(s1,s2)
print(scoreallineamento1)
scoreallineamento2=scoreAllineamento(s3,s4)
print(scoreallineamento2)
scoreallineamento3=scoreAllineamento(s5,s6)
print(scoreallineamento3)
#for loop
matrices=[blosum,PAM]
alignments=[align1,align2,align3]
for matrix in matrices:
	for align in alignments:
		S1=align[0]
		S2=align[1]
		score=scoreAllineamento(S1,S2)
		print(score)