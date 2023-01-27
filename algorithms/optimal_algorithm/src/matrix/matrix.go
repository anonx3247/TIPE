package matrix

import (
	"encoding/csv"
	"fmt"
	"math"
	"math/rand"
	"os"
	"strconv"
	"time"
)

type Point struct {
	x int
	y int
}

// Stores a matrix as a map of integer points to float64 values
type Matrix struct {
	length int
	points map[Point]float64
}

// Generates a 'size' x 'size' matrix filled with random float64 values between 0 and 1
func GenMatrix(size int) (grid *Matrix) {
	s := rand.NewSource(time.Now().UnixNano())
	r := rand.New(s)
	grid = new(Matrix)
	grid.points = make(map[Point]float64)
	grid.length = size

	for i := 0; i < size; i++ {
		for j := 0; j < size; j++ {
			grid.Set(i, j, r.Float64())
		}
	}
	return
}

// returns the value of the matrix at the index (i,j)
func (m Matrix) Get(i int, j int) float64 {
	return m.points[Point{i, j}]
}

// sets the value of the matrix at the index (i,j)
func (m Matrix) Set(i int, j int, v float64) {
	m.points[Point{i, j}] = v
}

// converts the matrix from a 'map'-based representation to a list of lists
func (m Matrix) ToList() [][]float64 {
	L := make([][]float64, m.length)

	for i := 0; i < m.length; i++ {
		newline := make([]float64, m.length)
		L[i] = newline
		for j := 0; j < m.length; j++ {
			L[i][j] = m.Get(j, i) //for some reason these have to be permuted
		}
	}
	return L
}

// converts the matrix to a string representation of a list of lists
func (m Matrix) ToStringList() [][]string {
	L := m.ToList()
	S := make([][]string, m.length)

	for i := 0; i < m.length; i++ {
		s := make([]string, m.length)
		S[i] = s
		for j := 0; j < m.length; j++ {
			S[i][j] = strconv.FormatFloat(L[i][j], 'e', -1, 64)
		}
	}
	return S
}

// returns the index of the maximum for a list of floats
func maxIndex(list []float64) int {
	i := 0
	max := float64(0)

	for j := 0; j < len(list); j++ {
		if list[j] > max {
			i = j
			max = list[j]
		}
	}
	return i
}

// returns the index of the minimum for a list of floats
func minIndex(list []float64) int {
	i := 0
	var min float64 = math.MaxFloat64

	for j := 0; j < len(list); j++ {
		if list[j] < min && list[j] != 0 {
			i = j
			min = list[j]
		}
	}
	return i
}

func (m Matrix) ToCSV(f *os.File) {
	w := csv.NewWriter(f)
	g := m.ToStringList()
	err := w.WriteAll(g)
	if err != nil {
		panic(err)
	}
}

func MatrixFromCSV(r csv.Reader) (m *Matrix) {
	m = new(Matrix)
	m.points = make(map[Point]float64)

	pts, err := r.ReadAll()

	if err != nil {
		panic(err)
	}

	m.length = len(pts)

	for i := 0; i < m.length; i++ {
		for j := 0; j < len(pts[i]); j++ {
			val, err := strconv.ParseFloat(pts[i][j], 64)
			if err != nil {
				panic(fmt.Sprint("improper value:", pts[i][j]))
			}
			m.Set(j, i, val)
		}
	}
	return m
}