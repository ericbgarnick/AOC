package main

import (
	"AOC/2021/go/day01"
	"AOC/2021/go/day02"
	"flag"
	"fmt"
)

func main() {
	day := flag.Int("day", 0, "Day number to run")
	flag.Parse()
	switch *day {
	case 1:
		day01.PartOne()
		day01.PartTwo()
	case 2:
		day02.PartOne()
		day02.PartTwo()
	default:
		fmt.Printf("No code exists for day %d\n", *day)
	}
}
