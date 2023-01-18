package main

import "testing"

func TestFindMinElement(t *testing.T) {
	testlist := []int{1,2,3,4,5}
	expectedResult := 1

	result := findMinElement(testlist)

	if expectedResult != result {
		t.Fatalf("findMinElement result is %d, expected %d", result, expectedResult)
	}
}