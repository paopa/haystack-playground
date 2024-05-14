"""
This is a demonstration of a Haystack pipeline.

A pipeline consists of two components that can be connected using the `connect` method.
You can add more components to the pipeline as needed.

In the following example, the pipeline demonstrates flexibility in adding and connecting multiple
components. Regardless of how many components have already been connected, the pipeline does not
impose any limitations on adding new ones.


Furthermore thoughts:

Based on the example results, we can construct various pipeline flows using the same set of
components. Other functions can take the pipeline as a parameter, allowing them to add
more components and connect them, thereby enhancing the pipeline's capabilities.

"""

from haystack import Pipeline
from haystack.core.component import component


@component
class Component1:
    @component.output_types(text=str)
    def run(self, text: str):
        print("Component1 is running")
        return {"text": text}


@component
class Component2:
    @component.output_types(text=str)
    def run(self, text: str):
        print("Component2 is running")
        return {"text": text}


pipeline = Pipeline()

pipeline.add_component("c1", Component1())
pipeline.add_component("c2", Component2())
pipeline.connect("c1", "c2")


@component
class Component3:
    @component.output_types(text=str)
    def run(self, text: str):
        print("Component3 is running")
        return {"text": text}


pipeline.add_component("c3", Component3())
pipeline.connect("c2", "c3")

res = pipeline.run({"c1": {"text": "hello"}})

print(res)
