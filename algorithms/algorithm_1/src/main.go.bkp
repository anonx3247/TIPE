package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
)

func main() {

	iCreated := true
	oCreated := true
	iPath := os.Args[1]
	oPath := os.Args[2]

	_, iCheckExists := os.Stat(iPath)

	if iCheckExists != nil {
		iCreated = false
	}

	_, oCheckExists := os.Stat(oPath)

	if oCheckExists != nil {
		oCreated = false
	}

	if iCreated {
		//f3, err3 := os.OpenFile(iPath, os.O_WRONLY, 0644)
		//handleInput(f3, err3)
	} else {
		f3, err3 := os.Create(iPath)
		handleInput(f3, err3)
	}

	if oCreated {
		f2, err2 := os.OpenFile(oPath, os.O_WRONLY, 0644)
		f, err := os.Open(iPath)
		handleOutput(f, err, f2, err2)
	} else {
		f2, err2 := os.Create(oPath)
		f, err := os.Open(iPath)
		handleOutput(f, err, f2, err2)

	}
}

func MatrixFromCSV(r csv.Reader) (m *Matrix) {
	m = new(Matrix)
	m.points = make(map[Point]int)

	pts, err := r.ReadAll()

	if err != nil {
		panic(err)
	}

	m.length = len(pts)

	for i := 0; i < m.length; i++ {
		for j := 0; j < len(pts[i]); j++ {
			p := Point{j, i}
			val, err := strconv.Atoi(pts[i][j])
			if err != nil {
				panic(fmt.Sprint("improper value:", pts[i][j]))
			}
			m.Set(p, val)
		}
	}
	return m
}

func setParams(grid *Matrix) (trails []Direction) {
	start := Point{0, 0}
	addr := grid.Addr()
	ord := visitOrder(start, addr)
	printOrder(ord)
	trails = trail(append([]Point{start}, ord...))
	printTrails(trails)
	return
}

func printTrails(t []Direction) {
	s := "Trail: [ "
	for _, i := range t {
		s += fmt.Sprint(i.rep, " ")
	}
	s += "]"
	fmt.Println(s)
}

func printOrder(ord []Point) {
	s := "Order: [ "
	for _, i := range ord {
		s += fmt.Sprint("(", i.x, i.y, ") ")
	}
	s += "]"
	fmt.Println(s)
}

func handleInput(f *os.File, e error) {
	if e != nil {
		fmt.Println("error on file write: input")
		panic(e)
	}
	w3 := csv.NewWriter(f)
	m := genCity(200, 100)
	m.ToCSV(*w3)
	f.Close()
}

func handleOutput(iFile *os.File, iErr error, oFile *os.File, oErr error) {

	defer iFile.Close()
	defer oFile.Close()
	if iErr != nil {
		fmt.Println("error on file read: input")
		panic(iErr)
	}
	if oErr != nil {
		fmt.Println("error on file write: output")
		panic(oErr)
	}
	r := csv.NewReader(iFile)
	w := csv.NewWriter(oFile)
	grid := MatrixFromCSV(*r)
	start := Point{0, 0}
	trails := setParams(grid)
	grid.drawTrajectory(&start, trails)
	grid.ToCSV(*w)
	fmt.Println("Trajectory length:", grid.MeasureTrajectory())
}
