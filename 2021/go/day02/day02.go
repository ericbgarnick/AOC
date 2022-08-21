package day02

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type position struct {
	horizontal int64
	depth      int64
}

func PartOne() {
	f, err := os.Open("../data/02.txt")
	if err != nil {
		log.Fatal(err)
		return
	}

	defer f.Close()

	scanner := bufio.NewScanner(f)

	p := position{}
	for scanner.Scan() {
		step := strings.TrimSpace(scanner.Text())
		distRE, err := regexp.Compile(`\d+`)
		if err != nil {
			log.Fatal(err)
			return
		}
		dist, err := strconv.ParseInt(distRE.FindString(step), 10, 64)
		if err != nil {
			log.Fatal(err)
			return
		}
		if strings.HasPrefix(step, "up") {
			p.depth -= dist
		} else if strings.HasPrefix(step, "down") {
			p.depth += dist
		} else if strings.HasPrefix(step, "forward") {
			p.horizontal += dist
		} else {
			log.Fatalf("invalid instruction: %s\n", step)
			return
		}
	}
	fmt.Printf("Part 1 final position: %d\n", p.depth*p.horizontal)
}

func PartTwo() {
	f, err := os.Open("../data/02.txt")
	if err != nil {
		log.Fatal(err)
		return
	}

	defer f.Close()

	scanner := bufio.NewScanner(f)

	var aim int64
	p := position{}
	for scanner.Scan() {
		step := strings.TrimSpace(scanner.Text())
		distRE, err := regexp.Compile(`\d+`)
		if err != nil {
			log.Fatal(err)
			return
		}
		dist, err := strconv.ParseInt(distRE.FindString(step), 10, 64)
		if err != nil {
			log.Fatal(err)
			return
		}
		if strings.HasPrefix(step, "up") {
			aim -= dist
		} else if strings.HasPrefix(step, "down") {
			aim += dist
		} else if strings.HasPrefix(step, "forward") {
			p.horizontal += dist
			p.depth += aim * dist
		} else {
			log.Fatalf("invalid instruction: %s\n", step)
			return
		}
	}
	fmt.Printf("Part 2 final position: %d\n", p.depth*p.horizontal)
}
