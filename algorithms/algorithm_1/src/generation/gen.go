package generation

import (
	"algorithm_1/trajectory"
	"math/rand"
	"time"
)

const road = 0
const base = 9
const addrColor = 5

func GenCity(size int, addr int) trajectory.Matrix {
	grid := trajectory.BlankMatrix(size)
	// gen base grid
	for i := 0; i < size; i++ {
		for j := 0; j < size; j++ {
			grid.Set(trajectory.Point{i, j}, base)
		}
	}

	// add roads
	for i := 0; i < size/trajectory.Sep; i++ {
		for j := 0; j < size; j++ {
			grid.Set(trajectory.Point{i * trajectory.Sep, j}, road)
		}
	}
	for i := 0; i < size/trajectory.Sep; i++ {
		for j := 0; j < size; j++ {
			grid.Set(trajectory.Point{j, i * trajectory.Sep}, road)
		}
	}

	// get new random seed from time
	s := rand.NewSource(time.Now().UnixNano())
	r := rand.New(s)
	addresses := make([]trajectory.Point, addr)

	for i := 0; i < addr; i++ {
		x := r.Intn(size/trajectory.Sep)*trajectory.Sep + 1
		y := r.Intn(size/trajectory.Sep)*trajectory.Sep + 1
		addresses[i] = trajectory.Point{x, y}
		grid.Set(trajectory.Point{x, y}, addrColor)
	}
	return *grid
}
