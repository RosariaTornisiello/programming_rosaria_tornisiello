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

def NW(s1,s2,pen,dic):
	scores=[]			#initialization of score and traceback matrices
	trace_back=[]
	N=len(s1)+1
	M=len(s2)+1
	scores=[[0]*(N) for i in range(M)]		 #filling of the two matrices with 0		
	trace_back=[[0]*(N) for i in range(M)]
	for i in range(1,M):				#filling of first row and first column of both the matrices						
		scores[i][0]=scores[i-1][0] + pen
		trace_back[i][0]= 'u'
	for j in range(1,N):
		scores[0][j]=scores[0][j-1] + pen
		trace_back[0][j]= 'l'
	for i in range(1,M):        			#rows
		for j in range(1,N):    		#columns
			voc={}
			up=scores[i-1][j]+ pen	#voc is a dictionary that associates up, left and diag to the values for each 
			left=scores[i][j-1]+ pen		#position of the scores matrix
			diag=scores[i-1][j-1]+int(dic[s1[j-1]+s2[i-1]])
			voc[up]='u'
			voc[left]='l'
			voc[diag]='d'
			max_score=max(up,left,diag)
			scores[i][j]=max_score		#fill each position of the scores matrix with the highest value
			trace_back[i][j]=voc.get(max(up,left,diag))#fill each position of the traceback matrix with u,l or d choosing the highest value
	return (scores, trace_back)									

def align(s1,s2,trace_back,scores): #funcion that return the alignment and the score
	sal1=''
	sal2=''
	pipe=''
	n=len(s1)		 
	m=len(s2)
	while n!=0 or m!=0:
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
		else:
			sal1+=s1[n-1]
			sal2+=s2[m-1]
			pipe+='|'
			m-=1
			n-=1
		sal1=sal1[::-1]
		sal2=sal2[::-1]
		pipe=pipe[::-1]
		score=scores[m-1][n-1]		
	return(sal1, pipe,sal2, score)


blosum=open("./BLOSUM62_square.txt","r")
dic=dictionary(blosum)
s1='MAGPATQSPMKLMALQLLLWHSALWTVQEATPLGPASSLPQSFLLKCLE'
s2='MDTWTVIILLQYFLFASLVQSAPVGLPSNLPPAFRETAVEA'
pen=-2
matrices=NW(s1,s2,pen,dic)
scores=matrices[0]
trace_back=matrices[1]
allineamento=align(s1,s2,trace_back,scores)
sal1=allineamento[0]
pipe=allineamento[1]
sal2=allineamento[2]
score=allineamento[3]

print(sal1, pipe, sal2, score, sep='\n')
