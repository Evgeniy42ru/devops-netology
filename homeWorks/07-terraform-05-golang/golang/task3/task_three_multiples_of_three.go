package three

import "fmt"

func main() {
	var multiple = 3
	var result = 0

	for i := 1; 99 > result; i++ {
		result = multiple * i

		fmt.Println(result)    
	}
}