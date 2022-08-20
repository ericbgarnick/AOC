package main

import (
	"AOC/2021/go/day01"
	"flag"
)

func main() {
	day := flag.Int("day", 0, "Day number to run")
	flag.Parse()
	switch *day {
	case 1:
		day01.PartOne()
		day01.PartTwo()
	}
}
