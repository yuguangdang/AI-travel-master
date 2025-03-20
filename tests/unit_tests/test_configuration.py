from plus_assistant.configuration import Configuration


def test_configuration_empty() -> None:
    Configuration.from_runnable_config({})


def test_dummy() -> None:
    """A dummy test to get started."""
    assert True
