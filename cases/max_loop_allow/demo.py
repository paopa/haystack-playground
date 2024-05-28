from typing import Optional
from haystack import Pipeline, component
from haystack.components.builders.prompt_builder import PromptBuilder
import random

prompt_builder = PromptBuilder(
    template="hello, {{init}} {% if valid %}valid{% endif %}, {% if invalid %}invalid{% endif %}"
)


@component
class Validator:
    def __init__(self):
        self.counter = 0

    @component.output_types(valid=str, invalid=Optional[str])
    def run(self, prompt: str):
        print(f"counter: {self.counter}, prompt:{prompt}")
        self.counter += 1

        def random_status():
            return random.choice(["valid", "invalid"])

        if "valid" == random_status():
            return dict(valid="hello, valid")

        return dict(invalid="hello, invalid")


pipe = Pipeline(max_loops_allowed=6)

pipe.add_component("builder", prompt_builder)
pipe.add_component("validator", Validator())

pipe.connect("builder", "validator")
pipe.connect("validator.valid", "builder.valid")
pipe.connect("validator.invalid", "builder.invalid")

pipe.draw("cases/max_loop_allow/pipe.png")

res = pipe.run(data={"builder": {"init": "world"}})
print(res)
