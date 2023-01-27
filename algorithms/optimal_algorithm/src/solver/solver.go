package solver

import (
	"ctrl-z/salesman/matrix"
	"os"
)

/*
	Solves the travelling salesman problem

Given an adjacency matrix 'm', it solves and gives an optimal solution
in O(n^2 2^n) time complexity
*/
func Solve(m *matrix.Matrix) (solution []int) {
	return
}

// Prints out list of values in a solution int array to a text file
func ToFile(solution []int, f *os.File) error {
	return nil
}
