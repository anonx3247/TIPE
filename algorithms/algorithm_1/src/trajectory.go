package main

import (
	"encoding/csv"
	"fmt"
	"math"
	"strconv"
)

const sep int = 2

var color map[string]int = map[string]int{"traj": 3, "addr": 5, "sep": 9}

var right Direction = Direction{Point{1, 0}, "⟶"}
var left = Direction{Point{-1, 0}, "⟵"}
var up = Direction{Point{0, -1}, "↑"}
var down = Direction{Point{0, 1}, "↓"}

type Point struct {
	x int
	y int
}

type Direction struct {
	value Point
	rep   string
}

type Matrix struct {
	length int
	points map[Point]int
}

func blankMatrix(size int) (grid *Matrix) {
	grid = new(Matrix)
	grid.points = make(map[Point]int)
	grid.length = size
	positions := make([]Point, 0)

	// fill the positions slice
	for i := 0; i < size/sep; i++ {
		for j := 0; j < size/sep; j++ {
			positions = append(positions, Point{i * sep, j * sep})

		}
	}
	return
}

func (p *Point) move(dir Direction) {
	p.x += dir.value.x * sep
	p.y += dir.value.y * sep
}

func (p Point) dist(p2 Point) (dist float32) {
	dist = float32(math.Sqrt(float64((p2.x-p.x)*(p2.x-p.x) + (p2.y-p.y)*(p2.y-p.y))))
	return
}

func (m Matrix) Get(p Point) int {
	return m.points[p]
}

func (m Matrix) Set(p Point, v int) {
	m.points[p] = v
}

func (m Matrix) Addr() (addr []Point) {
	addr = make([]Point, 0)
	for k, v := range m.points {
		if v == color["addr"] {
			addr = append(addr, Point{k.x, k.y})
		}
	}
	return
}

func (m Matrix) MeasureTrajectory() int {
	t := 0
	for p := range m.points {
		if m.Get(p) == color["traj"] || m.Get(p) == color["com"] || m.Get(p) == color["orig"] {
			t++
		}
	}
	return t
}

func (m Matrix) ToList() [][]int {
	L := make([][]int, m.length)

	for i := 0; i < m.length; i++ {
		newline := make([]int, m.length)
		L[i] = newline
		for j := 0; j < m.length; j++ {
			L[i][j] = m.Get(Point{j, i}) //for some reason these have to be permuted
		}
	}
	return L
}

func (m Matrix) ToStringList() [][]string {
	L := m.ToList()
	S := make([][]string, m.length)

	for i := 0; i < m.length; i++ {
		s := make([]string, m.length)
		S[i] = s
		for j := 0; j < m.length; j++ {
			S[i][j] = strconv.Itoa(L[i][j])
		}
	}
	return S
}

func visitOrder(start Point, addr []Point) (steps []Point) {
	steps = make([]Point, 0)
	if len(addr) == 0 {
		return
	} else if len(addr) == 1 {
		steps = addr
	} else {
		distances := make([]float32, len(addr))
		for i := 0; i < len(addr); i++ {
			distances[i] = start.dist(addr[i])
		}
		next := minimumIndex(distances)
		newStart := addr[next]
		restOfAddr := append(addr[:next], addr[next+1:]...)
		steps = append(steps, newStart)
		steps = append(steps, visitOrder(newStart, restOfAddr)...)
	}
	return
}

func minimumIndex(list []float32) int {
	i := 0
	var min float32 = math.MaxFloat32

	for j := 0; j < len(list); j++ {
		if list[j] < min && list[j] != 0 {
			i = j
			min = list[j]
		}
	}
	return i
}

func trajectory(pos1 Point, pos2 Point) ([]Direction, Point) {
	dx := (pos2.x - pos1.x) / int(math.Abs(float64(pos2.x-pos1.x)))
	px := Point{dx, 0}
	dy := (pos2.y - pos1.y) / int(math.Abs(float64(pos2.y-pos1.y)))
	py := Point{0, dy}
	lx := int(math.Abs(float64(pos2.x-pos1.x))) / sep
	ly := int(math.Abs(float64(pos2.y-pos1.y))) / sep
	trail := make([]Direction, 0, 2)

	// keeps track of how many directions fail
	failCounter := 0
	for _, i := range []Direction{right, left, up, down} {
		if px == i.value {
			trail = append(trail, mult(i, lx)...)
		} else if py == i.value {
			trail = append(trail, mult(i, ly)...)
		} else {
			failCounter++
		}
	}
	if failCounter >= 3 {
		panic(fmt.Sprint("error! incoherent direction:", px, py))
	}
	return trail, moveOnTrajectory(pos1, trail)
}

func mult(i Direction, times int) (l []Direction) {
	l = make([]Direction, 0)

	for j := 0; j < times; j++ {
		l = append(l, i)
	}
	return
}

func moveOnTrajectory(st_pos Point, trail []Direction) Point {
	pos := st_pos
	for _, i := range trail {
		pos.move(i)
	}
	return pos
}

func (grid Matrix) drawTrajectory(start *Point, trail []Direction) (m Matrix) {
	pos := new(Point)
	*pos = *start
	length := len(trail)

	for i := 0; i < length; i++ {
		grid.Set(*pos, color["traj"])
		grid.fill(trail[i], pos, i == length-1)
		pos.move(trail[i])
	}
	m = grid
	return
}

func (grid *Matrix) fill(dir Direction, posi *Point, last bool) {
	pos := new(Point)
	*pos = *posi
	grid.fillLength(dir, *pos, last)
}

func (grid *Matrix) fillLength(dir Direction, pos Point, last bool) {
	switch dir {
	case right:
		for i := pos.x; i < pos.x+sep; i++ {
			p := Point{i, pos.y}
			grid.Set(p, color["traj"])
		}
		if last {
			p := Point{pos.x + sep, pos.y}
			grid.Set(p, color["traj"])
		}
	case left:
		for i := pos.x - sep; i < pos.x; i++ {
			p := Point{i, pos.y}
			grid.Set(p, color["traj"])
		}
		if last {
			p := Point{pos.x - sep - 1, pos.y}
			grid.Set(p, color["traj"])
		}
	case down:
		for i := pos.y; i < pos.y+sep; i++ {
			p := Point{pos.x, i}
			grid.Set(p, color["traj"])
		}
		if last {
			p := Point{pos.x, pos.y + sep}
			grid.Set(p, color["traj"])
		}
	case up:
		for i := pos.y - sep; i < pos.y; i++ {
			p := Point{pos.x, i}
			grid.Set(p, color["traj"])
		}
		if last {
			p := Point{pos.x, pos.y - sep - 1}
			grid.Set(p, color["traj"])
		}
	default:
		panic("Illegal direction")
	}
}

func trail(ord []Point) (tr []Direction) {
	tr = make([]Direction, 0)
	traj := make([]Direction, len(ord))
	pos := ord[0]
	for i := 1; i < len(ord); i++ {
		traj, pos = trajectory(pos, ord[i])
		tr = append(tr, traj...)
	}
	return
}

func (m Matrix) ToCSV(w csv.Writer) {
	g := m.ToStringList()
	err := w.WriteAll(g)
	if err != nil {
		panic(err)
	}
}
