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

type Vector struct {
	Point
	length float32
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

func visitOrder(start Point, addr []Point, num int, compound bool) (steps []Point) {
	steps = make([]Point, 0)
	if len(addr) == 0 {
		return
	} else if len(addr) == 1 {
		steps = addr
	} else {
		// returns distsnces of all points to 'start'
		getDists := func(pts []Point) []float32 {
			d := make([]float32, len(pts))
			for i := 0; i < len(pts); i++ {
				d[i] = start.dist(pts[i])
			}
			return d
		}

		distances := getDists(addr)

		// gets the 'n' next closest points's indices in addr
		getNextIndices := func(n int, d []float32) []int {
			next := make([]int, 0)

			minIndexSkip := func(list []float32, toSkip []int) int {
				i := 0
				var min float32 = math.MaxFloat32

				for j := 0; j < len(list); j++ {
					skip := false
					for _, k := range toSkip {
						if k == j {
							skip = true
						}
					}
					if min > list[j] && list[j] != 0 && !skip {
						i = j
						min = list[j]
					}
				}
				return i
			}
			for i := 0; i < n; i++ {
				next = append(next, minIndexSkip(d, next))
			}

			return next
		}

		min := func(a int, b int) int {
			if a < b {
				return a
			} else {
				return b
			}
		}

		// if we only have less than 'num' points left, we shouldn't look for the next num points
		// but the next len(addr) points
		n := min(num, len(addr))
		fmt.Println("n =", n, "len = ", len(addr))
		nexts := getNextIndices(n, distances)
		nextPoints := make([]Point, 0)
		for _, i := range nexts {
			nextPoints = append(nextPoints, addr[i])
		}

		// general direction of trajectory
		dir := getVector(start, nextPoints)

		sortByDeltas := func(nexts []int) (sorted []int) {
			sorted = nexts
			fmt.Println("Nexts:", nexts)
			deltas := make([]float32, n)

			for i := range nexts {
				deltas[i] = vectDelta(dir, vectFromPoints(start, nextPoints[i]))
			}
			fmt.Println("Deltas:", deltas)

			// simple bubble sort
			for j := 1; j < len(nexts)-1; j++ {
				for i := 0; i < len(nexts)-j; i++ {
					if deltas[i] < deltas[i+1] {
						t := sorted[i]
						sorted[i] = sorted[i+1]
						sorted[i+1] = t
						m := deltas[i]
						deltas[i] = deltas[i+1]
						deltas[i+1] = m
					}
				}

			}
			fmt.Println("Sorted:", sorted)
			return sorted

		}

		nexts = sortByDeltas(nexts)

		restOfAddr := make([]Point, 0)
		newStart := Point{0, 0}
		if compound {
			newStart = addr[nexts[n-1]]

			// returns list omitting the 'toOmit' indices
			omit := func(pts []Point, toOmit []int) []Point {
				p := make([]Point, 0)
				for i, pt := range pts {
					omit := false
					for _, j := range toOmit {
						if i == j {
							omit = true
						}
					}
					if !omit {
						p = append(p, pt)
					}
				}
				return p
			}
			restOfAddr = omit(addr, nexts)
			steps = append(steps, nextPoints...)
		} else {
			newStart = addr[nexts[0]]
			restOfAddr = append(addr[:nexts[0]], addr[nexts[0]+1:]...)
			steps = append(steps, newStart)

		}
		steps = append(steps, visitOrder(newStart, restOfAddr, num, compound)...)

	}
	return
}

/*func visitOrder(start Point, addr []Point) (steps []Point) {
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
		next := minIndex(distances)
		newStart := addr[next]
		restOfAddr := append(addr[:next], addr[next+1:]...)
		steps = append(steps, newStart)
		steps = append(steps, visitOrder(newStart, restOfAddr)...)
	}
	return
}*/

func vectDelta(v1 Vector, v2 Vector) float32 {
	dx := float32(v2.x - v1.x)
	dy := float32(v2.y - v1.y)

	return (dx + dy) / 2

}

func vectFromPoints(a Point, b Point) Vector {
	return Vector{Point{b.x - a.x, b.y - a.y}, a.dist(b)}
}

func getVector(start Point, pts []Point) (v Vector) {
	vectors := make([]Vector, len(pts))

	for i := 0; i < len(pts); i++ {
		vectors = append(vectors, vectFromPoints(start, pts[i]))
	}

	avg := func(vects []Vector) Vector {
		x, y, length := 0, 0, float32(0)
		for i := 0; i < len(vects); i++ {
			x += vects[i].x
			y += vects[i].y
			length += vects[i].length
		}

		x /= len(vects)
		y /= len(vects)
		length /= float32(len(vects))
		return Vector{Point{x, y}, length}
	}

	v = avg(vectors)
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
