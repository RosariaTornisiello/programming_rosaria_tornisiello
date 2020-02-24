def dictionary(file):		#define a function that creates a dictionary starting from the blosum62 square matrix
	lista=[]
	for line in file:
		line=line.rstrip()
		line=line.split()
		lista.append(line)
	dic={}
	for i in range(len(lista[0])):
		for j in range(1,len(lista)):
			dic[lista[0][i]+lista[j][0]]=lista[i+1][j]
	return(dic)

def SW(s1,s2,pen,dic):
	N=len(s1)+1
	M=len(s2)+1
	scores=[]
	trace_back=[]
	scores=[[0]*(N) for i in range(M)]
	trace_back=[[0]*(N) for i in range(M)]
	for i in range(1,M):
		trace_back[i][0]= 'u'
	for j in range(1,N):
		trace_back[0][j]= 'l'
	for i in range(1,M):        #righe
		for n in range(1,N):    #colonne
			voc={}
			up=scores[i-1][n]+pen
			left=scores[i][n-1]+pen
			diag=scores[i-1][n-1]+int(dic[s1[n-1]+s2[i-1]])
			voc[up]='u'
			voc[left]='l'
			voc[diag]='d'
			max_score=max(up,left,diag)  
			if max_score>=0:		#add 0 instead of negative values
				scores[i][n]=max_score
			else:
				scores[i][n]=0
			trace_back[i][n]=voc.get(max(up,left,diag))
	return(scores,trace_back)

def align(s1,s2,trace_back,scores):
	sal1=''
	sal2=''
	pipe=''
	N=len(s1)+1
	M=len(s2)+1
	value=0
	massimo=0
	for i in range(1,M):
		for j in range(1,N):
			value=scores[i][j]
			if value>massimo:
				massimo=value
				m=i
				n=j
	score=scores[m][n]
	while scores[m][n]!=0:
		if trace_back[m][n]=='u':
			sal1+='-'
			sal2+=s2[m-1]
			pipe+=' '
			m-=1
		elif trace_back[m][n]=='l':
			sal1+=s1[n-1]
			sal2+='-'
			pipe+=' '
			n-=1
		elif trace_back[m][n]=='d':
			sal1+=s1[n-1]
			sal2+=s2[m-1]
			pipe+='|'
			m-=1
			n-=1
	sal1=sal1[::-1]
	sal2=sal2[::-1]
	pipe=pipe[::-1]
	return(sal1,pipe,sal2,score)
blosum=open("./BLOSUM62_square.txt","r")
dic=dictionary(blosum)
s1='GSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKL'
s2='HGKKVLGAFSDGLAHLDNLKGTFA'
pen=-2
matrices=SW(s1,s2,pen,dic)
scores=matrices[0]				#split the tuple (output of function NW)
trace_back=matrices[1]
allineamento=align(s1,s2,trace_back,scores)
sal1=allineamento[0]			#split the tuple (output of function align)
pipe=allineamento[1]
sal2=allineamento[2]
score=allineamento[3]
print(sal1, pipe, sal2, score, sep='\n')