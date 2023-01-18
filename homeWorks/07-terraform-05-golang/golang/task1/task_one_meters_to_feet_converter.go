package main

import "fmt"

const ratioOfFeetToMeters = 0.3048

func main() {
    fmt.Print("Enter a value in meters: ")
    var meters float64
    fmt.Scanf("%f", &meters)

    output := convertMetersToFeet(meters)

    fmt.Println(output)    
}

func convertMetersToFeet(meters float64) float64 {
	return meters / ratioOfFeetToMeters
}