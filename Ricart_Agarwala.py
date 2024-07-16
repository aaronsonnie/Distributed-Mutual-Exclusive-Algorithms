import threading
import time
import random


class RicartAgrawala:
    def __init__(self, process_id, num_processes, folders, access_count, response_times):
        self.process_id = process_id
        self.num_processes = num_processes
        self.folders = folders
        self.access_count = access_count
        self.response_times = response_times
        self.requesting = False
        self.timestamp = 0
        self.replies_needed = 0
        self.deferred_queue = []
        self.sock = threading.Lock()

    def start(self):
        for _ in range(self.access_count):
            for folder_name in self.folders:
                print(f"Process {self.process_id} is not in the critical section.")
                time.sleep(1)

                start_time = time.time()

                self.send_request(folder_name)
                self.enter_critical_section(folder_name)
                end_time = time.time()

                self.response_times[self.process_id].append(end_time - start_time)
                # Rest for a while before accessing another folder
                time.sleep(1)

    def send_request(self, folder_name):
        self.sock.acquire() #update the state of the process, sends a request to other processes for access to specific folder.
        self.requesting = True
        self.timestamp += 1
        self.replies_needed = self.num_processes - 1
        print(f"Process {self.process_id} sends request for folder '{folder_name}' with timestamp {self.timestamp}...")

        for i in range(self.num_processes):
            if i != self.process_id:
                threading.Thread(target=self.send_message, args=(i, folder_name, "request", self.timestamp)).start()

        self.sock.release()

    def send_message(self, recipient_id, folder_name, msg_type, timestamp): # (either request or reply)
        self.sock.acquire()
        print(f"Process {self.process_id} sends {msg_type} for folder '{folder_name}' to Process {recipient_id} with timestamp {timestamp}")
        self.sock.release() #handles incoming messages like reply/req

        if msg_type == "request":
            self.receive_request(recipient_id, folder_name, timestamp)
        elif msg_type == "reply":
            self.receive_reply()


    def receive_request(self, from_id, folder_name, timestamp): # determines to reply based on ricart alg
        self.sock.acquire()
        if self.requesting and (timestamp, from_id) < (self.timestamp, self.process_id):
            threading.Thread(target=self.send_message, args=(from_id, folder_name, "reply", None)).start()
        else:
            self.deferred_queue.append((from_id, folder_name, timestamp))
        self.sock.release()

    def receive_reply(self): # exiting the critical section (accessing a folder).
        self.replies_needed -= 1

    def enter_critical_section(self, folder_name):
        print(f"Process {self.process_id} enters critical section for folder '{folder_name}'...")
        time.sleep(random.uniform(1, 3))  # Simulate critical section
        print(f"Process {self.process_id} exits critical section for folder '{folder_name}'")

        self.requesting = False
        self.timestamp += 1

        self.sock.acquire()
        for (from_id, fname, timestamp) in self.deferred_queue:
            threading.Thread(target=self.send_message, args=(from_id, fname, "reply", None)).start()
        self.deferred_queue = []
        self.sock.release()


if __name__ == "__main__":
    num_processes = 3
    folders = ["b", "a", "c"]
    access_count = 3
    response_times = [[] for _ in range(num_processes)]

    processes = []
    for i in range(num_processes):
        process = RicartAgrawala(i, num_processes, folders, access_count, response_times)
        processes.append(process)

    threads = []
    for process in processes:
        t = threading.Thread(target=process.start)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    for i, times in enumerate(response_times):
        if len(times) > 0:
            avg_response_time = sum(times) / len(times)
            print(f"Process {i} - Average Response Time: {avg_response_time} seconds")


#The algorithm ensures that processes coordinate to access critical sections (folders)
# in a distributed and mutually exclusive manner.