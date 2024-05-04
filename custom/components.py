from haystack import Pipeline, component


@component
class WelcomeTextGenerator:
    """
    A component generating personal welcome message and making it upper case
    """

    @component.output_types(welcome_text=str, note=str)
    def run(self, name: str):
        return {
            "welcome_text": (
                "Hello {name}, welcome to Haystack!".format(name=name)
            ).upper(),
            "note": "welcome message is ready",
        }


def generator_demo():
    generatr = WelcomeTextGenerator()

    result = generatr.run(name="John Doe")

    print(result)


@component
class BeforeLogger:
    """
    A component logging the input and output of the component
    """

    @component.output_types(name=str)
    def run(self, name: str):
        print(f"Input: {name}")
        return {"name": name}


def pipeline_demo():
    pipeline = Pipeline()

    pipeline.add_component("before_logger", BeforeLogger())
    pipeline.add_component("generator", WelcomeTextGenerator())

    pipeline.connect("before_logger", "generator")

    pipeline.run({"before_logger": {"name": "John Doe"}})
