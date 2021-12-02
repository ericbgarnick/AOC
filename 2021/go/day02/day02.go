package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"regexp"
	"strconv"
)

type instruction struct {
	instrType  string
	instrValue int
}

func main() {
	dataFile := flag.String("f", "", "Path to input data file")
	flag.Parse()

	// Process data
	if *dataFile == "" {
		fmt.Fprintln(os.Stderr, "missing input data file")
		os.Exit(1)
	}
	f, err := os.Open(*dataFile)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	scanner := bufio.NewScanner(f)
	instructions, err := scanInputData(scanner)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}

	// Part 1
	res, err := navigationDepthPosition(instructions)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Printf("Part 1: %d\n", res)

	// Part 2
	res, err = navigationDepthPositionAim(instructions)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Printf("Part 2: %d\n", res)
}

// scanInputData returns a slice of instruction read from scanner.
func scanInputData(scanner *bufio.Scanner) ([]instruction, error) {
	reType := regexp.MustCompile(`\w+`)
	reValue := regexp.MustCompile(`\d+`)
	var instructions []instruction
	for scanner.Scan() {
		i := scanner.Text()
		instrType := reType.FindString(i)
		instrValue, err := strconv.Atoi(reValue.FindString(i))
		if err != nil {
			return nil, err
		}
		instr := instruction{
			instrType,
			instrValue,
		}
		instructions = append(instructions, instr)
	}
	return instructions, nil
}

func navigationDepthPosition(instructions []instruction) (int, error) {
	depth := 0
	position := 0
	for _, instr := range instructions {
		if instr.instrType == "up" {
			depth -= instr.instrValue
		} else if instr.instrType == "down" {
			depth += instr.instrValue
		} else if instr.instrType == "forward" {
			position += instr.instrValue
		} else {
			return 0, fmt.Errorf("unknown instruction type %s", instr.instrType)
		}
	}
	return depth * position, nil
}

func navigationDepthPositionAim(instructions []instruction) (int, error) {
	depth := 0
	position := 0
	aim := 0
	for _, instr := range instructions {
		if instr.instrType == "up" {
			aim -= instr.instrValue
		} else if instr.instrType == "down" {
			aim += instr.instrValue
		} else if instr.instrType == "forward" {
			position += instr.instrValue
			depth += aim * instr.instrValue
		} else {
			return 0, fmt.Errorf("unknown instruction type %s", instr.instrType)
		}
	}
	return depth * position, nil
}
