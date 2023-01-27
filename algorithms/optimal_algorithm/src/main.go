package main

import (
	"ctrl-z/salesman/matrix"
	"ctrl-z/salesman/solver"
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
)

/*
	Main execution expects three cmd-line arguments, "size", "graphPath", and "solutionPath"

- "size" refers to the size of the graph to generate

- "graphPath" is the path to the file where we store the generated graph

- "solutionPath" is the path to the file to store the solution given by travelling-salesman algorithm
*/
func main() {

	size, err := strconv.Atoi(os.Args[1])
	graphPath := os.Args[2]
	solutionPath := os.Args[3]

	if err != nil {
		panic("Illegal size")
	}

	// Checks if files exists, creates them if they do not
	handlePath := func(path string, rw string) (*os.File, bool) {
		created := true
		_, check := os.Stat(path)
		if check != nil {
			created = false
		}

		if created {
			if rw == "r" {
				f, e := os.Open(path)
				if e != nil {
					panic(e)
				}
				return f, created
			} else if rw == "w" {
				f, e := os.OpenFile(path, os.O_WRONLY, 0644)
				if e != nil {
					panic(e)
				}
				return f, created
			}
		} else {
			f, e := os.Create(path)
			if e != nil {
				panic(e)
			}
			return f, created
		}
		// just because needed but this should NEVER execute
		return os.Stdin, created
	}

	graphFile, created := handlePath(graphPath, "w")

	var graph *matrix.Matrix
	if !created {
		graph = getMatrix(graphFile, size)
	} else {
		r := csv.NewReader(graphFile)
		graph = matrix.MatrixFromCSV(*r)
	}

	solutionFile, _ := handlePath(solutionPath, "r")

	writeSolution(solutionFile, graph)

}

func getMatrix(f *os.File, n int) *matrix.Matrix {
	fmt.Println("Generating graph...")
	m := matrix.GenMatrix(n)
	m.ToCSV(f)
	f.Close()
	return m
}

func writeSolution(solutionFile *os.File, graph *matrix.Matrix) {
	defer solutionFile.Close()
	solution := solver.Solve(graph)
	fmt.Println("Solution:")
	fmt.Println(solution)
	solver.ToFile(solution, solutionFile)
}
