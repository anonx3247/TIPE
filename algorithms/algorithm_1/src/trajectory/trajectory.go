package trajectory

import (
	"encoding/csv"
	"fmt"
	"math"
	"strconv"
)

const Sep int = 2

var color map[string]int = map[string]int{"traj": 3, "addr": 5, "sep": 9}

var right Direction = Direction{Point{1, 0}, "⟶"}
var left = Direction{Point{-1, 0}, "⟵"}
var up = Direction{Point{0, -1}, "↑"}
var down = Direction{Point{0, 1}, "↓"}

type Point struct {
	X int
	Y int
}

type Direction struct {
	value Point
	Rep   string
}

type Matrix struct {
	Length int
	Points map[Point]int
}

func BlankMatrix(size int) (grid *Matrix) {
	grid = new(Matrix)
	grid.Points = make(map[Point]int)
	grid.Length = size
	positions := make([]Point, 0)

	// fill the positions slice
	for i := 0; i < size/Sep; i++ {
		for j := 0; j < size/Sep; j++ {
			positions = append(positions, Point{i * Sep, j * Sep})

		}
	}
	return
}

func (p *Point) move(dir Direction) {
	p.X += dir.value.X * Sep
	p.Y += dir.value.Y * Sep
}

func (p Point) dist(p2 Point) (dist float32) {
	dist = float32(math.Sqrt(float64((p2.X-p.X)*(p2.X-p.X) + (p2.Y-p.Y)*(p2.Y-p.Y))))
	return
}

func (m Matrix) Get(p Point) int {
	return m.Points[p]
}

func (m Matrix) Set(p Point, v int) {
	m.Points[p] = v
}

func (m Matrix) Addr() (addr []Point) {
	addr = make([]Point, 0)
	for k, v := range m.Points {
		if v == color["addr"] {
			addr = append(addr, Point{k.X, k.Y})
		}
	}
	return
}

func (m Matrix) MeasureTrajectory() int {
	t := 0
	for p := range m.Points {
		if m.Get(p) == color["traj"] || m.Get(p) == color["com"] || m.Get(p) == color["orig"] {
			t++
		}
	}
	return t
}

func (m Matrix) ToList() [][]int {
	L := make([][]int, m.Length)

	for i := 0; i < m.Length; i++ {
		newline := make([]int, m.Length)
		L[i] = newline
		for j := 0; j < m.Length; j++ {
			L[i][j] = m.Get(Point{j, i}) //for some reason these have to be permuted
		}
	}
	return L
}

func (m Matrix) ToStringList() [][]string {
	L := m.ToList()
	S := make([][]string, m.Length)

	for i := 0; i < m.Length; i++ {
		s := make([]string, m.Length)
		S[i] = s
		for j := 0; j < m.Length; j++ {
			S[i][j] = strconv.Itoa(L[i][j])
		}
	}
	return S
}

func VisitOrder(start Point, addr []Point) (steps []Point) {
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
		steps = append(steps, VisitOrder(newStart, restOfAddr)...)
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
	dx := (pos2.X - pos1.X) / int(math.Abs(float64(pos2.X-pos1.X)))
	px := Point{dx, 0}
	dy := (pos2.Y - pos1.Y) / int(math.Abs(float64(pos2.Y-pos1.Y)))
	py := Point{0, dy}
	lx := int(math.Abs(float64(pos2.X-pos1.X))) / Sep
	ly := int(math.Abs(float64(pos2.Y-pos1.Y))) / Sep
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

func (grid Matrix) DrawTrajectory(start *Point, trail []Direction) (m Matrix) {
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
		for i := pos.X; i < pos.X+Sep; i++ {
			p := Point{i, pos.Y}
			grid.Set(p, color["traj"])
		}
		if last {
			p := Point{pos.X + Sep, pos.Y}
			grid.Set(p, color["traj"])
		}
	case left:
		for i := pos.X - Sep; i < pos.X; i++ {
			p := Point{i, pos.Y}
			grid.Set(p, color["traj"])
		}
		if last {
			p := Point{pos.X - Sep - 1, pos.Y}
			grid.Set(p, color["traj"])
		}
	case down:
		for i := pos.Y; i < pos.Y+Sep; i++ {
			p := Point{pos.X, i}
			grid.Set(p, color["traj"])
		}
		if last {
			p := Point{pos.X, pos.Y + Sep}
			grid.Set(p, color["traj"])
		}
	case up:
		for i := pos.Y - Sep; i < pos.Y; i++ {
			p := Point{pos.X, i}
			grid.Set(p, color["traj"])
		}
		if last {
			p := Point{pos.X, pos.Y - Sep - 1}
			grid.Set(p, color["traj"])
		}
	default:
		panic("Illegal direction")
	}
}

func Trail(ord []Point) (tr []Direction) {
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
