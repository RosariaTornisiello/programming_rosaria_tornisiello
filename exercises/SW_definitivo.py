""" pseudocode:

 def sw(sequence1, sequence2, gap penalty, matrix dictionary):
       - initialize 0 matrix(F)
       - initialize 0 matrix(P)
       - fill first row and first column of F and P
       - for each position in F, compute the values from up, left and diagonal
       - memorize the values as keys in a dictionary (voc)
       - add the maximum in F
       - add the maximum direction in P
   return F, P

 def align(sequence1, sequence2, F, P):
       - find the maximum value(s)
       - append maximum value(s) and its indexes in a list of lists (max_list)
       - do the traceback starting from the maximum value(s)
       - append the aligned sequence 1 to the seq_align1 list, the aligned
       sequence2 to the seq_align2 list and the score to the scores list
   return the 3 lists

 def print_ali(lists of aligned sequences and scores):
       - prints the two aligned sequences of the each local alignment
       and its score
"""

from input_data import seq1, seq2, BLOSUM52


def sw(s1, s2, pen, matrix):
    """
    Takes as input two sequences, gap penalty, BLOSUM or PAM dictionary
    and returns the scoring matrix(F) and traceback matrix(P)
    """
    N = len(s1) + 1
    M = len(s2) + 1
    F = []                #initialize scoring matrix(F) and traceback matrix(P)
    P = []
    F = [[0] * (N) for i in range(M)]     # fill F and P with 0, defining
    P = [[0] * (N) for i in range(M)]     # their dimensions
    for i in range(1, M):
        P[i][0] = 'u'
    for j in range(1, N):
        P[0][j] = 'l'
    for i in range(1, M):
        for j in range(1, N):            # core of the function: for each i,j position
            voc = {}                     # the best score is added to F matrix,
            up = F[i - 1][j] + pen       # adding the gap penalty when necessary
            left = F[i][j - 1] + pen     # and its direction to P matrix
            diag = F[i - 1][j - 1] + int(matrix[s1[j - 1] + s2[i - 1]])
            voc[up] = 'u'
            voc[left] = 'l'              # u = up, l = left, d = diagonal
            voc[diag] = 'd'
            max_score = max(up, left, diag)
            if max_score < 0:            # all negative values are excluded and
                F[i][j] = 0              # recorded as 0
            else:
                F[i][j] = max_score  
            P[i][j] = voc.get(max_score)
    return(F, P)


def align(s1, s2, F, P):
    """
    Takes as input two sequences and F and P matrices, returns 3 lists
    containing the aligned sequences and the scores
    """
    N = len(s1)
    M = len(s2)
    value = 0
    maximum = 0
    max_list = []
    for i in range(M, 1, -1):         # this doubly nested for loop finds the
        for j in range(N, 1, -1):     # maximum value(s) in F, memorizing it/them
            value = F[i][j]           # and its/their indexes in a list of lists
            if value > maximum:
                maximum = value
                max_list = []
                max_list.append([value, i, j])
            elif value == maximum:
                max_list.append([value, i, j])
    sal1 = ''                # initialize empty strings for the aligned sequences
    sal2 = ''
    seq_align1 = []                  # initialize 3 empy lists where to store the
    seq_align2 = []                  # aligned sequence(s) and the score(s)
    scores = []
    for l in range(len(max_list)):
        score = max_list[l][0]       # define the score and the starting point
        m = max_list[l][1]           # of the best local alignment(s)
        n = max_list[l][2]
        while F[m][n] != 0:          # core of the function: this while loop does
            if P[m][n] == 'u':       # the traceback untill it finds a 0 in F
                sal1 += '-'          # and constructs the aligned sequences
                sal2 += s2[m-1]      # adding gaps when necessary based on the
                m -= 1               # the direction it finds in the P matrix
            elif P[m][n] == 'l':
                sal1 += s1[n-1]
                sal2 += '-'
                n -= 1
            elif P[m][n] == 'd':
                sal1 += s1[n - 1]
                sal2 += s2[m - 1]
                m -= 1
                n -= 1
        seq_align1.append(sal1[::-1])
        seq_align2.append(sal2[::-1])
        scores.append(score)
        sal1 = ''
        sal2 = ''
    return(seq_align1, seq_align2, scores)


def print_ali(seq_align1, seq_align2, scores):
    """
    Takes as input the lists and prints the best local alignment(s)
    and their score(s)
    """
    for i in range(len(seq_align1)):
        print(seq_align1[i], seq_align2[i], sep='\n')
        print('score:', scores[i])


pen = -5
F, P = sw(seq1, seq2, pen, BLOSUM52)
seq_align1, seq_align2, scores = align(seq1, seq2, F, P)
print_ali(seq_align1, seq_align2, scores)
