package main

import "fmt"

func main() {
	fmt.Println("Hello, 世界")
	n := 0
	fmt.Scanf("%d", &n)
	for n > 0 {
		number1 := 0
		number2 := 0
		fmt.Scanf("%d", &number1)
		fmt.Scanf("%d", &number2)
		fmt.Printf("Got %d %d\n", number1, number2)
		n--
	}

}
