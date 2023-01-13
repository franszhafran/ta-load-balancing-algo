package main

type Task struct {
	Length   int
	Deadline int
	Sleep    int
}

func workerService(d chan *Task) {

}

func main() {
	equalMIPS := float64(1)
	worker := 3
	task1 := &Task{
		Length:   4,
		Sleep:    4,
		Deadline: 5,
	}
	task2 := &Task{
		Length:   7,
		Sleep:    7,
		Deadline: 9,
	}
	task3 := &Task{
		Length:   12,
		Sleep:    12,
		Deadline: 12,
	}

	channels := []chan *Task{}
	for i := 0; i < worker; i++ {
		channels = append(channels, make(chan *Task))
		go workerService(channels[i])
	}

	vmMIPS := []float64{equalMIPS, equalMIPS, equalMIPS}

	tasks := []*Task{task1, task2, task3}
	for _, t := range tasks {
		for _, c := range channels {
			c <- t
		}
	}
}
