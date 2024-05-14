"""

This demonstration showcases a Haystack pipeline with cyclic dependencies.
The pipeline cannot handle cyclic dependencies, as illustrated by the following error:

```
ValueError: Input text for component c1 is already sent by ['c3'].
```

This error highlights that the pipeline is designed to function as a Directed Acyclic Graph (DAG).


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


@component
class Component3:
    @component.output_types(text=str)
    def run(self, text: str):
        print("Component3 is running")
        return {"text": text}


pipeline = Pipeline()

pipeline.add_component("c1", Component1())
pipeline.add_component("c2", Component2())
pipeline.add_component("c3", Component3())
pipeline.connect("c1", "c2")
pipeline.connect("c2", "c3")
pipeline.connect("c3", "c1")

res = pipeline.run({"c1": {"text": "hello"}})

print(res)
