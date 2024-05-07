from haystack import Pipeline
from haystack.components.routers import ConditionalRouter
from haystack.components.builders.prompt_builder import PromptBuilder

routes = [
    {
        "condition": "{{query|length > 10}}",
        "output": "{{query}}",
        "output_name": "ok_query",
        "output_type": str,
    },
    {
        "condition": "{{query|length <= 10}}",
        "output": "query is too short: {{query}}",
        "output_name": "too_short_query",
        "output_type": str,
    },
]
router = ConditionalRouter(routes=routes)

pipe = Pipeline()
pipe.add_component("router", router)
pipe.add_component(
    "prompt_builder", PromptBuilder("Answer the following query. {{query}}")
)
pipe.connect("router.ok_query", "prompt_builder.query")

res = pipe.run(data={"router": {"query": "Berlin"}})
print(res)
# {'router': {'too_short_query': 'query is too short: Berlin'}}

res = pipe.run(data={"router": {"query": "What is the capital of Italy?"}})
print(res)
# {'generator': {'replies': ['The capital of Italy is Rome.'], ...}
