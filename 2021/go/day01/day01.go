package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
)

func main() {
	dataFile := flag.String("f", "../data/01.txt", "Path to input data file")
	flag.Parse()

	// Process data
	f, err := os.Open(*dataFile)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	scanner := bufio.NewScanner(f)
	inputValues, err := scanInputData(scanner)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}

	// Part 1
	res := singleDepthChanges(inputValues)
	fmt.Printf("Part 1: %d\n", res)

	// Part 2
	res = tripleDepthChanges(inputValues)
	fmt.Printf("Part 2: %d\n", res)
}

// scanInputData returns a slice of ints read from scanner.
func scanInputData(scanner *bufio.Scanner) ([]int, error) {
	var values []int
	for scanner.Scan() {
		v, err := strconv.Atoi(scanner.Text())
		if err != nil {
			return nil, err
		}
		values = append(values, v)
	}
	return values, nil
}

// singleDepthChanges returns the number of depth measurements that are greater than the previous depth.
func singleDepthChanges(values []int) int {
	count := 0
	i := 1
	for i < len(values) {
		if values[i] > values[i-1] {
			count++
		}
		i++
	}
	return count
}

// tripleDepthChanges returns the number of three-value windows that are greater than the previous window.
func tripleDepthChanges(values []int) int {
	count := 0
	window1 := sum(values[:3]...)
	window2 := sum(values[1:4]...)
	if window2 > window1 {
		count++
	}
	end := 4
	for end < len(values) {
		window1 += values[end-1] - values[end-4]
		window2 += values[end] - values[end-3]
		if window2 > window1 {
			count++
		}
		end++
	}
	return count
}

// sum returns the sum of values.
func sum(values ...int) int {
	res := 0
	for _, v := range values {
		res += v
	}
	return res
}
