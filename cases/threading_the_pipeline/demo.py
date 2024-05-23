"""
This is a demonstration of a Haystack pipeline.


"""

from haystack import Pipeline
from haystack.core.component import component
import time


@component
class Component1:
    @component.output_types(text=str)
    def run(self, text: str):
        print("Component1 is running start; text: ", text)
        time.sleep(2)
        print("Component1 is running end; text: ", text)
        return {"text": text}


@component
class Component2:
    @component.output_types(text=str)
    def run(self, text: str):
        print("Component2 is running start; text: ", text)
        time.sleep(2)
        print("Component2 is running end; text: ", text)
        return {"text": text}


pipeline = Pipeline()

pipeline.add_component("c1", Component1())
pipeline.add_component("c2", Component2())
pipeline.connect("c1", "c2")

import threading


def task(user_id):
    result = pipeline.run({"c1": {"text": f"hello {i}"}})
    print(result)


threads = []
start_time = time.time()
for i in range(5):
    thread = threading.Thread(target=task, args=(i,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
end_time = time.time()
print(f"Total time: {end_time - start_time:.2f} seconds")
