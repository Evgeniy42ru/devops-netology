package main

import "fmt"

func main() {
	defaulList := []int{48, 96, 86, 68, 57, 82, 63, 70, 37, 34, 83, 27, 19, 97, 9, 17}

	fmt.Printf("Finded min element: %d\n", findMinElement(defaulList))
}

func findMinElement(defaulList []int) int {
	minElement := defaulList[0]

	for i := 1; i < len(defaulList); i++ {
		iElement := defaulList[i]

		if minElement > iElement {
			minElement = iElement
		}
	}

	return minElement
}