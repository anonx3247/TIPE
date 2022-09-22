package main

import (
	"encoding/binary"
	"bufio"
	"os"
	"bytes"
	"fmt"
)

type Header struct {
	FileCode int32
	FileLength int32
	Version int32
	ShapeType int32
	Xmin float64
	Ymin float64
	Xmax float64
	Ymax float64
}

type Polyline struct {
	Xmin float64
	Ymin float64
	Xmax float64
	Ymax float64
	NumParts int32
	NumPoints int32
	Parts []int32
	Points []Point
}

type Record struct {
	RecordNumber int32
	ContentLength int32
	Content Polyline
}

type Point struct {
	x float64
	y float64
}

func main() {
	data, err := LoadFileToRAM("test.shp")
	check(err)
	
	headerData, recordData := data[:100], data[100:]
	
	header := ParseHeader(headerData)
	
    records := ParseRecords(recordData)
	
	// record, _ := ParseRecord(recordData, 0)
	
	fmt.Println(header)
	fmt.Println(records)
}

func LoadFileToRAM(filename string) ([]byte, error) {
	file, err := os.Open(filename)
	
	if err != nil {
		return nil, err
	}
	
	defer file.Close()
	
	stats, statErr := file.Stat()
	if statErr != nil {
		return nil, statErr
	}
	
	var size int64 = stats.Size()
	bytes := make([]byte, size)
	
	buffr := bufio.NewReader(file)
	_, err = buffr.Read(bytes)
	
	return bytes, err
}

func ParseRecords(data []byte) (records []Record) {
	var init int32 = 0
	records = make([]Record, 0)
	for init < int32(len(data)-1) {
		record, end := ParseRecord(data, init)
		records = append(records, record)
		init = end
	}
	return
}

func ParseRecord(data []byte, init int32) (record Record, end int32) {
	
	// A record has a header of 8 bytes
	// Then it has the contents based on the type, which here is 3, i.e. Polyline
	
	/* HEADER */
	
	rawRecordNumber := bytes.NewReader(data[init:init+4])
	rawContentLength := bytes.NewReader(data[init+4:init+8])
	
	RecordNumber, ContentLength := new(int32), new(int32)
	
	err1 := binary.Read(rawRecordNumber, binary.BigEndian, RecordNumber)
	err2 := binary.Read(rawContentLength, binary.BigEndian, ContentLength)
	check(err1); check(err2)
	
	// ContentLength measures content (so record - header) in 16bit words, 
	// so multiplying by two and adding 8 gives the length of the record in bytes
	end = init + (*ContentLength)*2 + 8
	
	init += 8 // reset init to the beginning of content
	
	/* RECORD CONTENTS */
	
	// See Table6 of ESRI Shapefile Technical Description
	rawNumParts := bytes.NewReader(data[init+36:init+40]) // LE Int
	rawNumPoints := bytes.NewReader(data[init+40:init+44]) // LE Int
	rawXmin := bytes.NewReader(data[init+4:init+12]) // LE float64
	rawYmin := bytes.NewReader(data[init+12:init+20]) // LE float64
	rawXmax := bytes.NewReader(data[init+20:init+28]) // LE float64
	rawYmax := bytes.NewReader(data[init+28:init+36]) // LE float64

	Xmin, Xmax, Ymin, Ymax := new(float64), new(float64), new(float64), new(float64)
	NumParts := new(int32)
	NumPoints := new(int32)

	err3 := binary.Read(rawNumParts, binary.LittleEndian, NumParts)
	err4 := binary.Read(rawNumPoints, binary.LittleEndian, NumPoints)
	err5 := binary.Read(rawXmin, binary.LittleEndian, Xmin)
	err6 := binary.Read(rawYmin, binary.LittleEndian, Ymin)
	err7 := binary.Read(rawXmax, binary.LittleEndian, Xmax)
	err8 := binary.Read(rawYmax, binary.LittleEndian, Ymax)
	
	check(err2); check(err3)
	check(err4); check(err5); check(err6)
	check(err7); check(err8)
	

	partsStart := int(init + 44)
	Parts := make([]int32, *NumParts)
	maxParts := int(*NumParts)
	
	for i := 0; i < maxParts; i++ {
		rawPart := bytes.NewReader(data[partsStart+i*8:partsStart+(i+1)*8])
		Part := new(int32)
		errP := binary.Read(rawPart, binary.LittleEndian, Part)
		check(errP)
		Parts[i] = *Part
	}
	pointsStart := int(init + 44 + 4 * (*NumParts))
	Points := make([]Point, *NumPoints)
	maxPoints := int(*NumPoints)
	
	for i := 0; i < maxPoints; i++ {
		rawX := bytes.NewReader(data[pointsStart+i*8:pointsStart+(i+1)*8])
		rawY := bytes.NewReader(data[pointsStart+(i+1)*8:pointsStart+(i+2)*8])
		X := new(float64)
		Y := new(float64)
		errX := binary.Read(rawX, binary.LittleEndian, X)
		errY := binary.Read(rawY, binary.LittleEndian, Y)
		check(errX); check(errY)
		Points[i] = Point{*X, *Y}
	}
	
	Content := Polyline{*Xmin, *Ymin, *Xmax, *Ymax, *NumParts, *NumPoints, Parts, Points}
	
	record = Record{*RecordNumber, *ContentLength, Content}
	return
}
	
	

func ParseHeader(data []byte) (header Header) {
	rawFileCode := bytes.NewReader(data[:4]) // BE Int
	rawFileLength := bytes.NewReader(data[24:28]) // BE Int
	rawVersion := bytes.NewReader(data[28:32]) // LE Int
	rawShapeType := bytes.NewReader(data[32:36]) // LE Int
	rawXmin := bytes.NewReader(data[36:44]) // LE float64
	rawYmin := bytes.NewReader(data[44:52]) // LE float64
	rawXmax := bytes.NewReader(data[52:60]) // LE float64
	rawYmax := bytes.NewReader(data[60:68]) // LE float64
	
	FileCode := new(int32)
	FileLength := new(int32)
	Version := new(int32)
	ShapeType := new(int32)
	Xmin := new(float64)
	Ymin := new(float64)
	Xmax := new(float64)
	Ymax := new(float64)
	
	err := binary.Read(rawFileCode, binary.BigEndian, FileCode)
	err2 := binary.Read(rawFileLength, binary.BigEndian, FileLength)
	err3 := binary.Read(rawVersion, binary.LittleEndian, Version)
	err4 := binary.Read(rawShapeType, binary.LittleEndian, ShapeType)
	err5 := binary.Read(rawXmin, binary.LittleEndian, Xmin)
	err6 := binary.Read(rawYmin, binary.LittleEndian, Ymin)
	err7 := binary.Read(rawXmax, binary.LittleEndian, Xmax)
	err8 := binary.Read(rawYmax, binary.LittleEndian, Ymax)
	
	check(err); check(err2); check(err3)
	check(err4); check(err5); check(err6)
	check(err7); check(err8)
	
	header = Header{*FileCode, *FileLength, *Version, *ShapeType, *Xmin, *Ymin, *Xmax, *Ymax}
	
	return
}

func check(err error) {
	if err != nil {
		panic(err)
	}
}