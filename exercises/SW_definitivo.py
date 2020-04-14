def SW(s1,s2,pen,dic):
	N=len(s1)+1
	M=len(s2)+1
	F=[]
	P=[]
	F=[[0]*(N) for i in range(M)]
	P=[[0]*(N) for i in range(M)]
	for i in range(1,M):
		P[i][0]= 'u'
	for j in range(1,N):
		P[0][j]= 'l'
	for i in range(1,M):        #righe
		for j in range(1,N):    #colonne
			voc={}
			up=F[i-1][j]+pen
			left=F[i][j-1]+pen
			diag=F[i-1][j-1]+int(dic[s1[j-1]+s2[i-1]])
			voc[up]='u'
			voc[left]='l'
			voc[diag]='d'
			max_score=max(up,left,diag)
			if max_score<0:
				F[i][j]=0
			else:  									#add 0 instead of negative values
				F[i][j]=max_score
			P[i][j]=voc.get(max_score)
	return(F,P)

def align(s1,s2,pen,dic):
	F,P=SW(s1,s2,pen,dic)
	sal1=''
	sal2=''
	pipe=''
	N=len(s1)
	M=len(s2)
	value=0
	massimo=0
	maxList=[]
	for i in range(M, 1, -1):
		for j in range(N, 1, -1):
			value=F[i][j]
			if value>massimo:
				massimo=value
				maxList=[]
				maxList.append([value, i, j])
			elif value==massimo:
				maxList.append([value, i, j])
	seqAlign1=[]
	pipeAlign=[]
	seqAlign2=[]
	scores=[]
	for l in range(len(maxList)):
		score=maxList[l][0]
		m=maxList[l][1]
		n=maxList[l][2]
		while F[m][n]!=0:
			if P[m][n]=='u':
				sal1+='-'
				sal2+=s2[m-1]
				pipe+=' '
				m-=1
			elif P[m][n]=='l':
				sal1+=s1[n-1]
				sal2+='-'
				pipe+=' '
				n-=1
			elif P[m][n]=='d':
				sal1+=s1[n-1]
				sal2+=s2[m-1]
				pipe+='|'
				m-=1
				n-=1
		seqAlign1.append(sal1[::-1])
		seqAlign2.append(sal2[::-1])
		pipeAlign.append(pipe[::-1])
		scores.append(score)
		sal1=''
		sal2=''
		pipe=''
	return(seqAlign1, pipeAlign, seqAlign2, scores)

def printAli(s1,s2,pen,dic):
	seqAlign1, pipeAlign, seqAlign2, scores=align(s1,s2,pen,dic)
	for i in range(len(seqAlign1)):
		print(seqAlign1[i], pipeAlign[i], seqAlign2[i],sep='\n')
		print('score:', scores[i])

from input_data import BLOSUM52
pen=-2
seq1='HEAGAWGHEE'
seq2='PAWHEAE'
printAli(seq1, seq2, pen, BLOSUM52)
