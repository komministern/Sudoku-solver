#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy

class Matrix(list):

    def __init__(self, amatrix):
        super(Matrix, self).__init__(amatrix)

    def column(self, n):
        alist = []
        for i in range(len(self)):
            alist.append(self[i][n])
        return alist

    def row(self, n):
        return self[n]

    def size(self):
        return (len(self), len(self[0]))    # (rows, columns)


class Sudoku(Matrix):

    def __init__(self, amatrix):
        super(Sudoku, self).__init__(amatrix)

        self.possibilities = Matrix([ [], [], [], [], [], [], [], [], [] ])
        
    def possible_numbers(self, r, c):   # Returns a set of possible numbers for self[r][c], possibly empty
        if self[r][c] == 0:
            complete_set = set(range(1,10))
            impossible_numbers = set(self.column(c)).union(set(self.row(r)))
            y_quad = r / 3
            x_quad = c / 3

            for rr in range(y_quad*3,y_quad*3+3):
                for cc in range(x_quad*3,x_quad*3+3):
                    impossible_numbers = impossible_numbers.union(set([self[rr][cc]]))
            possible_numbers = complete_set.difference(impossible_numbers)
        else:
            possible_numbers = set([self[r][c]])        
        return possible_numbers

    def firstLNP(self):
        rows, columns = self.size()
        lnp = 9
        for r in range(rows):
            for c in range(columns):
                if len(self.possibilities[r][c]) < lnp and len(self.possibilities[r][c]) > 1:
                    row = r
                    column = c
                    lnp = len(self.possibilities[r][c])
        return (row, column)

    def unknowns(self):         # How many zeros in matrix
        n = 0
        rows, columns = self.size()
        for r in range(rows):
            for c in range(columns):
                if self[r][c] == 0:
                    n += 1
        return n

    def reduce(self):       # Tries to solve the sudoku through simple reductions
                            # This alone will solve an easy sudoku if repeated
        rows, columns = self.size()
        stop_iterate = False
        reductions = 0
        for r in range(rows):
            for c in range(columns):
                self.possibilities[r].append(self.possible_numbers(r, c))
                if len(self.possibilities[r][-1]) == 0:
                    #print 'NO SOLUTION DETECTED'
                    reductions = -1
                    stop_iterate = True
                    
                elif len(self.possibilities[r][-1]) == 1 and self[r][c] == 0:
                    self[r][c] = list(self.possibilities[r][-1])[0]
                    reductions += 1

                if stop_iterate:
                    break
            if stop_iterate:
                break

        return reductions

    def solve(self, depth = 0):

        print depth

        reductions = 1

        while reductions > 0:
            reductions = self.reduce()            # Reduce sudoku as far as possible

        if reductions == -1:
            return None                 # This implies that there is no solution to this grid

        if self.unknowns() == 0:        # This implies that the sudoku is solved
            return self

        else:
    
            row, column = self.firstLNP()

            #print depth
 
            for number in sorted(list(self.possibilities[row][column])):

                newpossibletable = Sudoku(copy.deepcopy(self))  # The deepcopy is make or break!!! Doesn't work with just copy!!!
                newpossibletable[row][column] = number
                solution = newpossibletable.solve(depth + 1)

                if solution:
                    return solution

            return None



if __name__ == '__main__':
    
    easy_sudoku = [ [5,3,0,0,7,0,0,0,0],
                    [6,0,0,1,9,5,0,0,0],
                    [0,9,8,0,0,0,0,6,0],
                    [8,0,0,0,6,0,0,0,3],
                    [4,0,0,8,0,3,0,0,1],
                    [7,0,0,0,2,0,0,0,6],
                    [0,6,0,0,0,0,2,8,0],
                    [0,0,0,4,1,9,0,0,5],
                    [0,0,0,0,8,0,0,7,9] ]

    medium_sudoku = [[0,0,1,0,2,0,0,0,0],
                     [9,0,0,0,0,0,0,0,7],
                     [0,0,0,0,6,0,8,3,0],
                     [5,6,4,0,3,0,0,0,0],
                     [0,3,0,0,0,0,0,0,0],
                     [0,0,0,6,4,0,1,0,0],
                     [0,0,0,2,0,9,6,0,0],
                     [0,1,0,0,0,0,0,0,2],
                     [7,0,0,5,0,3,0,1,0] ]


    hard_sudoku = [ [0,7,0,0,0,0,2,0,0],
                    [0,0,0,0,9,1,0,0,0],
                    [5,0,0,0,0,0,6,0,1],
                    [4,0,0,0,0,0,0,9,3],
                    [3,0,0,0,0,0,0,1,0],
                    [0,0,0,6,0,0,0,0,0],
                    [9,0,0,2,0,0,0,4,5],
                    [0,0,0,5,0,9,7,0,0],
                    [0,0,3,0,0,0,0,0,0] ]

    extreme_sudoku = [[8,0,0,0,0,0,0,0,0],
                    [0,0,3,6,0,0,0,0,0],
                    [0,7,0,0,9,0,2,0,0],
                    [0,5,0,0,0,7,0,0,0],
                    [0,0,0,0,4,5,7,0,0],
                    [0,0,0,1,0,0,0,3,0],
                    [0,0,1,0,0,0,0,6,8],
                    [0,0,8,5,0,0,0,1,0],
                    [0,9,0,0,0,0,4,0,0] ]

    hardest_sudoku = [ [1,0,0,0,0,7,0,9,0],
                    [0,3,0,0,2,0,0,0,8],
                    [0,0,9,6,0,0,5,0,0],
                    [0,0,5,3,0,0,9,0,0],
                    [0,1,0,0,8,0,0,0,2],
                    [6,0,0,0,0,4,0,0,0],
                    [3,0,0,0,0,0,0,1,0],
                    [0,4,0,0,0,0,0,0,7],
                    [0,0,7,0,0,0,3,0,0] ]


    erroneous_sudoku = [[5,3,1,2,7,4,8,0,0],
                    [6,0,0,1,9,5,0,0,0],
                    [0,9,8,0,0,0,0,6,0],
                    [8,0,0,0,6,0,0,0,3],
                    [4,0,0,8,0,3,0,0,1],
                    [7,0,0,0,2,0,0,0,6],
                    [0,6,0,0,0,0,2,8,0],
                    [0,0,0,4,1,9,0,0,5],
                    [0,0,0,0,8,0,0,7,9] ]


    sudoku = Sudoku(extreme_sudoku)

    print repr( sudoku.solve() )


