package main

import (
	"bufio"
	"errors"
	"flag"
	"fmt"
	"os"
	"strconv"
)

const target = 2020

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

	// Part 1 (two sum)
	res, err := twoSum(inputValues)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Printf("Part 1: %d\n", res)

	// Part 2 (three sum)
	res, err = threeSum(inputValues)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
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

// twoSum returns the product of the first two values found that sum to target.
func twoSum(values []int) (int, error) {
	addends := map[int]struct{}{}
	for _, v := range values {
		needed := target - v
		if _, ok := addends[v]; ok {
			return multiply(v, target-v), nil
		}
		addends[needed] = struct{}{}
	}
	return -1, errors.New("two sum not found for given values")
}

// threeSum returns the product of the first three values found that sum to target.
func threeSum(values []int) (int, error) {
	addends := map[int]int{}
	for i, v1 := range values {
		for _, v2 := range values[i:] {
			needed := target - v1 - v2
			if needed > 0 {
				addends[needed] = v1 * v2
			}
		}
	}
	for _, v := range values {
		if prod, ok := addends[v]; ok {
			return multiply(v, prod), nil
		}
	}
	return -1, errors.New("three sum not found for given values")
}

// multiply returns the product of factors.
func multiply(factors ...int) int {
	res := 1
	for _, v := range factors {
		res *= v
	}
	return res
}
