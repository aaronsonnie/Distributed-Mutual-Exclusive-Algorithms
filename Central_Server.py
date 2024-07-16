import threading
import time

class CentralServerMutex:
    def __init__(self):
        self.lock = threading.Lock()

    def lock_folder(self, folder_name, process_id):
        print(f"Process {process_id} is requesting access to folder '{folder_name}'.")
        with self.lock:
            print(f"Process {process_id} is granted access to folder '{folder_name}'.")
    def unlock_folder(self, folder_name, process_id):
        with self.lock:
            print(f"Process {process_id} is releasing access to folder '{folder_name}'.")

# Usage Example
def process(process_id, mutex, folders, access_count, response_times): #one thread can access a particular folder at a time by using a lock.
    for _ in range(access_count):
        for folder_name in folders:
            print(f"Process {process_id} is not in the critical section.")
            time.sleep(1) 

            start_time = time.time()

            mutex.lock_folder(folder_name, process_id)
            print(f"Process {process_id} is accessing folder '{folder_name}'.")
            time.sleep(2)  # Simulate work inside the folder
            mutex.unlock_folder(folder_name, process_id)

            end_time = time.time()

            response_times[process_id].append(end_time - start_time)
            # Rest for a while before accessing another folder
            time.sleep(1)
            ##thread (process) simulates accessing multiple folders repeatedly.

if __name__ == "__main__":
    num_processes = 3
    mutex = CentralServerMutex()
    
    folders = ["b", "a", "c"]
    access_count = 3
    response_times = [[] for _ in range(num_processes)]

    threads = []
    for i in range(num_processes):
        t = threading.Thread(target=process, args=(i, mutex, folders, access_count, response_times))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    for i, times in enumerate(response_times): # response_times list is used to record the time taken for each access to a folder.
        if len(times) > 0:
            avg_response_time = sum(times) / len(times)
            print(f"Process {i} - Average Response Time: {avg_response_time} seconds")
