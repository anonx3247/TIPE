package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
)

func main() {

	iPath := os.Args[1]
	oPath := os.Args[2]
	n, e := strconv.Atoi(os.Args[3])

	if e != nil {
		panic("not a number")
	}
	
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

	iFile, created := handlePath(iPath, "r")
	if !created {
		handleInput(iFile, n)
	}

	oFile, _ := handlePath(oPath, "w")

	grid := handleOutput(iFile, oFile)

	if len(os.Args) == 4 {
		imgPath := os.Args[3]
		img, _ := handlePath(imgPath, "w")
		grid.Draw(img)
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

//func setParams(grid *Matrix) (trails []Direction, trailsOrig []Direction) {
func setParams(grid *Matrix) (trails []Direction, c bool) {
	start := Point{0, 0}
	addr := grid.Addr()
	n, com := 3, true
	fmt.Println("n =", n, "c =", com)
	ord := visitOrder(start, addr, n, com)
	printOrder(ord)
	trails = trail(append([]Point{start}, ord...))
	printTrails(trails)
	c = com
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

func handleInput(f *os.File, n int) {
	w3 := csv.NewWriter(f)
	fmt.Println("Generating city...")
	m := genCity(200, n)
	m.ToCSV(*w3)
	//f.Close()
}

func handleOutput(iFile *os.File, oFile *os.File) (grid *Matrix) {
	defer iFile.Close()
	defer oFile.Close()
	r := csv.NewReader(iFile)
	w := csv.NewWriter(oFile)
	grid = MatrixFromCSV(*r)
	start := Point{0, 0}
	//trails, orig := setParams(grid)
	trails, c := setParams(grid)
	grid.drawTrajectory(&start, trails, c)
	//grid.drawTrajectory(&start, orig, false)
	grid.ToCSV(*w)
	fmt.Println("Trajectory length:", grid.MeasureTrajectory())
	return
}
