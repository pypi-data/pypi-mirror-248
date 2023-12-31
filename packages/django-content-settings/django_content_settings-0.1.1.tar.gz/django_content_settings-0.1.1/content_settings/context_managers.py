from contextlib import contextmanager, ContextDecorator

CONTEXT_STACK = []


@contextmanager
def context(**kwargs):
    CONTEXT_STACK.append(kwargs)
    try:
        yield
    finally:
        CONTEXT_STACK.pop()


def get_context_stack(name):
    for obj in CONTEXT_STACK:
        if name in obj:
            yield obj[name]


class content_settings_context(ContextDecorator):
    def __init__(self, **values) -> None:
        super().__init__()
        self.values_to_update = values
        self.prev_values = {}

    def __enter__(self):
        from content_settings.caching import set_new_value

        for name, new_value in self.values_to_update.items():
            self.prev_values[name] = set_new_value(name, new_value)

    def __exit__(self, *exc):
        from content_settings.caching import set_new_value

        for name, new_value in self.prev_values.items():
            set_new_value(name, new_value)
