package main

import "testing"

func TestConvertMetersToFeet(t *testing.T) {
	meters := 0.6096
	var expectedResult float64 = 2

	result := convertMetersToFeet(meters)

	if result != expectedResult {
		t.Fatalf("convertMetersToFeet result is %f, expected %f", result, expectedResult)
	}
}
