import time
import concurrent.futures


def do(t):
    time.sleep(t)
    return "wake now"


print("Starting Task..")
start = time.perf_counter()
with concurrent.futures.ThreadPoolExecutor() as executer:

    threads = []

    for i in range(10):
        thread = executer.submit(do, i)
        threads.append((thread))

    print("All threads started !")

    for thread in threads:
        print(thread.result())

    print("All threads ended.")

end = time.perf_counter()

print(f"Finished in {round(end - start , 2)} second(s)")
