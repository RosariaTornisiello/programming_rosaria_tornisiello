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
blosum=open("./BLOSUM62_square.txt","r")
lista=createLista(blosum)
dic=createDic(lista)

#s1='AAQQQQAA'
#s2='QQQQQ'

s1='MAGPATQ'
s2='MDTWTVIILL'

#s1='ATCCTATT'
#s2='TCATTTTAATA'

N=len(s1)+1
M=len(s2)+1
scores=[[0]*(N) for i in range(M)]			#crea le 0 matrices
trace_back=[[0]*(N) for i in range(M)]

gap_penalty=-2

for i in range(1,M):
	trace_back[i][0]= 'u'
for j in range(1,N):
	trace_back[0][j]= 'l'


for i in range(1,M):        #righe
	for j in range(1,N):    #colonne
		voc={}
		up=scores[i-1][j]+gap_penalty
		left=scores[i][j-1]+gap_penalty
		diag=scores[i-1][j-1]+int(dic[s1[j-1]+s2[i-1]])
		voc[up]='u'
		voc[left]='l'
		voc[diag]='d'
		max_score=max(up,left,diag)
		scores[i][j]=max_score
		trace_back[i][j]=voc.get(max(up,left,diag))
#print(scores)
#print(trace_back)

sal1=''
sal2=''
pipe=''

#elimina gap laterali
value_c=0			#trova il valore massimo dell'ultima colonna e salva la posizione in l
mc=0
for i in range(1,M):
	value_c=scores[i][len(s1)]
	if value_c>mc:
		mc=value_c
		l=i	

mr=max(scores[len(s2)])		#trova il valore massimo dell'ultima riga
start=max(mc,mr)			#trova il punto di partenza

if start==mr:				#assegna gli indici al punto di partenza
	m=len(s2)
	n=scores[m].index(max(scores[m]))
else:
	n=len(s1)
	m=scores[l][len(s1)]
#print(m, n)

while n!=0 or m!=0:				#costruisce l'allineamento
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
score_al=scores[M-1][N-1]
print(sal1[::-1])
print(pipe[::-1])
print(sal2[::-1])
print(score_al)