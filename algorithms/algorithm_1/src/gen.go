package main

import (
    "math/rand"
    "time"
)

const road = 0
const base = 9
const addrColor = 5

func genCity(size int, addr int) Matrix {
    grid := blankMatrix(size)
    // gen base grid
    for i := 0; i < size; i++ {
        for j := 0; j < size; j++ {
            grid.Set(Point{i, j}, base)
        }
    }

    // add roads
    for i := 0; i < size/sep; i++ {
        for j := 0; j < size; j++ {
            grid.Set(Point{i * sep, j}, road)
        }
    }
    for i := 0; i < size/sep; i++ {
        for j := 0; j < size; j++ {
            grid.Set(Point{j, i * sep}, road)
        }
    }

    // get new random seed from time
    s := rand.NewSource(time.Now().UnixNano())
    r := rand.New(s)
    addresses := make([]Point, addr)

    for i := 0; i < addr; i++ {
        x := r.Intn(size/sep)*sep + 1
        y := r.Intn(size/sep)*sep + 1
        addresses[i] = Point{x, y}
        grid.Set(Point{x, y}, addrColor)
    }
    return *grid
}
