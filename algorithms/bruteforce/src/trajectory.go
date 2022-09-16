package main

import (
	"encoding/csv"
	"fmt"
	"math"
	"strconv"
)

const sep int = 2

var colors map[string]int = map[string]int{"traj": 8, "addr": 5, "sep": 9, "orig": 3, "com": 1, "bkg": 0}

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

type PathTree struct {
	root              int
	children          []PathTree
	lengthsToChildren []float32
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

func (m Matrix) MeasureTrajectory() int {
	t := 0
	for p := range m.points {
		if m.Get(p) == colors["traj"] || m.Get(p) == colors["com"] || m.Get(p) == colors["orig"] {
			t++
		}
	}
	return t
}

func (m Matrix) Addr() (addr []Point) {
	addr = make([]Point, 0)
	for k, v := range m.points {
		if v == colors["addr"] {
			addr = append(addr, Point{k.x, k.y})
		}
	}
	return
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

func genPathTree(start int, addr []Point, visited []int, adj [][]float32) (paths PathTree) {
	paths.root = start
	paths.children = make([]PathTree, len(addr)-len(visited))
	paths.lengthsToChildren = make([]float32, len(addr)-len(visited))
	fmt.Println(len(paths.children), len(addr))

	isInside := func(a int, b []int) bool {
		k := false
		for _, i := range b {
			if a == i {
				k = true
			}
		}
		return k
	}

	if len(paths.children) == 0 {
		fmt.Println("no children")
		return
	} else {
		iterator := 0
		for i := range addr {
			if !isInside(i, visited) {
				fmt.Println("Is not inside:", i)
				fmt.Println("visited:", visited)
				newVisited := append(visited, i)
				subPaths := genPathTree(i, addr, newVisited, adj)
				paths.children[iterator] = subPaths
				paths.lengthsToChildren[iterator] = adj[start][i]
				iterator += 1
			}
		}
		return
	}

}

func getMinimumPath(root PathTree) (float32, []int) {

	pathInit := make([]int, 1)
	pathInit[0] = root.root

	min := func(l []float32) (float32, int) {
		min := l[0]
		index := 0
		for i, e := range l {
			if e <= min {
				min = e
				index = i
			}
		}
		return min, index
	}

	if len(root.children) == 0 {
		return float32(0), pathInit
	} else {
		lengths := make([]float32, 0)
		subPaths := make([][]int, 0)
		for _, child := range root.children {
			len, path := getMinimumPath(child)

			lengths = append(lengths, len)
			subPaths = append(subPaths, path)
		}
		length, index := min(lengths)
		return length + root.lengthsToChildren[index], append(pathInit, subPaths[index]...)
	}
}

func adjacencyMatrix(addr []Point) (adj [][]float32) {
	adj = make([][]float32, len(addr))

	for i := range addr {
		adj[i] = make([]float32, len(addr))
		for j := range addr {
			adj[i][j] = math.MaxFloat32
		}
	}

	for i := range addr {
		for j := range addr {
			d := addr[i].dist(addr[j])
			adj[i][j] = d
		}
	}
	return
}
func maxIndex(list []float32) int {
	i := 0
	max := float32(0)

	for j := 0; j < len(list); j++ {
		if list[j] > max {
			i = j
			max = list[j]
		}
	}
	return i
}
func minIndex(list []float32) int {
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

func (grid Matrix) drawTrajectory(start *Point, trail []Direction, compound bool) (m Matrix) {
	pos := new(Point)
	*pos = *start
	length := len(trail)

	col := colors["traj"]
	if compound {
		col = colors["com"]
	}

	for i := 0; i < length; i++ {
		grid.Set(*pos, col)
		grid.fill(trail[i], pos, i == length-1, compound)
		pos.move(trail[i])
	}
	m = grid
	return
}

func (grid *Matrix) fill(dir Direction, posi *Point, last bool, compound bool) {
	pos := new(Point)
	*pos = *posi
	grid.fillLength(dir, *pos, last, compound)
}

func (grid *Matrix) fillLength(dir Direction, pos Point, last bool, compound bool) {
	col := colors["traj"]

	if compound {
		col = colors["com"]
	}
	switch dir {
	case right:
		for i := pos.x; i < pos.x+sep; i++ {
			p := Point{i, pos.y}
			grid.Set(p, col)
		}
		if last {
			p := Point{pos.x + sep, pos.y}
			grid.Set(p, col)
		}
	case left:
		for i := pos.x - sep; i < pos.x; i++ {
			p := Point{i, pos.y}
			grid.Set(p, col)
		}
		if last {
			p := Point{pos.x - sep - 1, pos.y}
			grid.Set(p, col)
		}
	case down:
		for i := pos.y; i < pos.y+sep; i++ {
			p := Point{pos.x, i}
			grid.Set(p, col)
		}
		if last {
			p := Point{pos.x, pos.y + sep}
			grid.Set(p, col)
		}
	case up:
		for i := pos.y - sep; i < pos.y; i++ {
			p := Point{pos.x, i}
			grid.Set(p, col)
		}
		if last {
			p := Point{pos.x, pos.y - sep - 1}
			grid.Set(p, col)
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
