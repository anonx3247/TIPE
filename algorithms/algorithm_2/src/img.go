package main

import (
	"image"
	"image/color"
	"image/draw"
	"image/png"
	"io"
)

func (m Matrix) Draw(file io.Writer) {
	stretch := 1000 / m.length
	img := image.NewRGBA(
		image.Rect(0, 0, m.length*stretch, m.length*stretch),
	)

	colorValues := map[int]color.Color{
		colors["bkg"]:  color.RGBA{0, 0, 0, 255},
		colors["addr"]: color.RGBA{29, 242, 183, 255},
		colors["sep"]:  color.RGBA{197, 197, 197, 255},
		colors["com"]:  color.RGBA{29, 183, 242, 255},
		colors["orig"]: color.RGBA{242, 29, 29, 255},
		colors["traj"]: color.RGBA{238, 217, 15, 255},
	}

	getColor := func(i int) image.Image {
		return &image.Uniform{colorValues[i]}
	}

	fill := func(p Point, col int) {
		x, y := p.x, p.y
		r := image.Rect(x*stretch, y*stretch, x*stretch+stretch, y*stretch+stretch)
		draw.Draw(
			img, r, getColor(col), image.ZP, draw.Src,
		)

	}
	draw.Draw(
		img, img.Bounds(), getColor(0), image.ZP, draw.Src,
	)

	for point, val := range m.points {
		fill(point, val)
	}

	png.Encode(file, img)

}
