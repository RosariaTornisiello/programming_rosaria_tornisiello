from input_data import seq1, seq2, BLOSUM52


def sw(s1, s2, PEN, matrix):
    """
    Takes as input two sequences, gap penalty, BLOSUM or PAM dictionary
    and returns the scoring matrix(F) and traceback matrix(P)
    """
    N = len(s1) + 1
    M = len(s2) + 1
    F = []
    P = []
    F = [[0] * (N) for i in range(M)]
    P = [[0] * (N) for i in range(M)]
    for i in range(1, M):
        P[i][0] = 'u'
    for j in range(1, N):
        P[0][j] = 'l'
    for i in range(1, M):
        for j in range(1, N):
            voc = {}
            up = F[i - 1][j] + PEN
            left = F[i][j - 1] + PEN
            diag = F[i - 1][j - 1] + int(matrix[s1[j - 1] + s2[i - 1]])
            voc[up] = 'u'
            voc[left] = 'l'
            voc[diag] = 'd'
            max_score = max(up, left, diag)
            if max_score < 0:
                F[i][j] = 0
            else:  							# add 0 instead of negative values
                F[i][j] = max_score
            P[i][j] = voc.get(max_score)
    return(F, P)


def align(s1, s2, F, P):
    """
    Takes as input two sequences and F and P matrices, returns 4 lists
    containing the aligned sequences, the pipe string and the scores
    """
    sal1 = ''
    sal2 = ''
    pipe = ''
    N = len(s1)
    M = len(s2)
    value = 0
    massimo = 0
    maxList = []
    for i in range(M, 1, -1):
        for j in range(N, 1, -1):
            value = F[i][j]
            if value > massimo:
                massimo = value
                maxList = []
                maxList.append([value, i, j])
            elif value == massimo:
                maxList.append([value, i, j])
    seq_align1 = []
    pipe_align = []
    seq_align2 = []
    scores = []
    for l in range(len(maxList)):
        score = maxList[l][0]
        m = maxList[l][1]
        n = maxList[l][2]
        while F[m][n] != 0:
            if P[m][n] == 'u':
                sal1 += '-'
                sal2 += s2[m-1]
                pipe += ' '
                m -= 1
            elif P[m][n] == 'l':
                sal1 += s1[n-1]
                sal2 += '-'
                pipe += ' '
                n -= 1
            elif P[m][n] == 'd':
                sal1 += s1[n - 1]
                sal2 += s2[m - 1]
                pipe += '|'
                m -= 1
                n -= 1
        seq_align1.append(sal1[::-1])
        seq_align2.append(sal2[::-1])
        pipe_align.append(pipe[::-1])
        scores.append(score)
        sal1 = ''
        sal2 = ''
        pipe = ''
    return(seq_align1, pipe_align, seq_align2, scores)


def print_ali(seq_align1, pipe_align, seq_align2, scores):
    """
    Takes as input the lists and prints the best local alignment(s)
    and their score(s)
    """
    for i in range(len(seq_align1)):
        print(seq_align1[i], pipe_align[i], seq_align2[i], sep='\n')
        print('score:', scores[i])


PEN = -5
F, P = sw(seq1, seq2, PEN, BLOSUM52)
seq_align1, pipe_align, seq_align2, scores = align(seq1, seq2, F, P)
print_ali(seq_align1, pipe_align, seq_align2, scores)
