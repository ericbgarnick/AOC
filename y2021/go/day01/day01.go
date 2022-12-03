package day01

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func PartOne() {
	f, err := os.Open("../data/01.txt")
	if err != nil {
		log.Fatal(err)
		return
	}

	defer f.Close()

	scanner := bufio.NewScanner(f)

	var (
		prevVal   int64
		curVal    int64
		increases int
	)
	for scanner.Scan() {
		curVal, err = strconv.ParseInt(strings.TrimSpace(scanner.Text()), 10, 64)
		if err != nil {
			log.Fatal(err)
			return
		}
		if prevVal != 0 && curVal > prevVal {
			increases++
		}
		prevVal = curVal
	}
	if err = scanner.Err(); err != nil {
		log.Fatal(err)
		return
	}

	fmt.Printf("Part 1 counted %d increases\n", increases)
}

func PartTwo() {
	f, err := os.Open("../data/01.txt")
	if err != nil {
		log.Fatal(err)
		return
	}

	defer f.Close()

	scanner := bufio.NewScanner(f)

	var (
		window    [4]int64
		increases int
	)
	for scanner.Scan() {
		window[0], err = strconv.ParseInt(strings.TrimSpace(scanner.Text()), 10, 64)

		if err != nil {
			log.Fatal(err)
			return
		}
		if window[3] != 0 && window[0] > window[3] {
			increases++
		}
		window[3] = window[2]
		window[2] = window[1]
		window[1] = window[0]
	}
	if err = scanner.Err(); err != nil {
		log.Fatal(err)
		return
	}

	fmt.Printf("Part 2 counted %d increases\n", increases)
}
