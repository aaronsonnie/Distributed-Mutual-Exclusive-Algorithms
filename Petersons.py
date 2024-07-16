import threading
import time

class PetersonAlgorithm:
    def __init__(self):
        self.turn = 0
        self.flag = [False, False]
        self.process_count = 2  # Number of processes (in this case, 2)

    def process(self, process_id):
        other_id = 1 - process_id  # Id process is 0 or 1
        self.flag[process_id] = True # interest in entering cs
        self.turn = process_id # process's turn to enter the critical section
        print(f"Process {process_id} wants to enter critical section...")

        #  busy-wait loop is exited (meaning it's safe to proceed), the process enters the critical section.
        while self.flag[other_id] and self.turn == process_id:
            continue

        # Critical section
        print(f"Process {process_id} is in critical section")
        time.sleep(2)
        print(f"Process {process_id} exits critical section")

        # Reset flag to indicate no interest
        self.flag[process_id] = False

    def start_processes(self):
        process0 = threading.Thread(target=self.process, args=(0,))
        process1 = threading.Thread(target=self.process, args=(1,))
        process0.start()
        process1.start()

        #the main thread waits for process0 to finish execution and then waits for process1 to finish

        process0.join()
        process1.join()

if __name__ == "__main__":
    algorithm = PetersonAlgorithm()
    algorithm.start_processes()
