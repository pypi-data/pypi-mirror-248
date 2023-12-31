from itertools import chain

from django.core.exceptions import ValidationError
from django.template import Context, Template

from .basic import SimpleString, SimpleText


class TemplateObject:
    template_obj_key = "obj"
    help_template_obj = "Main Object"
    test_obj_query = None
    template_static = None

    def get_help_format(self):
        yield "Simple <a href='https://docs.djangoproject.com/en/3.2/topics/templates/' target='_blank'>Django Template</a>. Available objects: <ul>"
        yield f"<li>{self.template_obj_key} - {self.help_template_obj}</li>"
        for name in chain(self.get_static_data().keys(), self.get_test_kwargs().keys()):
            yield f"<li>{name}</li>"
        yield "</ul>"

    def get_static_data(self):
        return self.template_static if self.template_static is not None else {}

    def to_python(self, value):
        template = Template(value.strip())

        def _(obj, **kwargs):
            return template.render(
                Context(
                    dict(
                        **{self.template_obj_key: obj},
                        **self.get_static_data(),
                        **kwargs,
                    )
                )
            )

        return _

    def get_test_obj(self):
        if self.test_obj_query:
            return self.test_obj_query.first()

    def get_test_kwargs(self):
        return {}

    def get_admin_preview_value(self, value, *args):
        obj = self.get_test_obj()
        kwargs = self.get_test_kwargs()

        if obj is not None:
            return self.to_python(value)(obj, **kwargs)

        return "None preview object (get_test_obj)"

    def validate_value(self, value):
        obj = self.get_test_obj()
        kwargs = self.get_test_kwargs()

        if obj is None:
            return

        try:
            return self.to_python(value)(obj, **kwargs)
        except Exception as e:
            raise ValidationError(str(e))


class StringTemplateObject(TemplateObject, SimpleString):
    widget_attrs = {"style": "max-width: 600px; width: 100%"}


class HTMLTemplateObject(TemplateObject, SimpleText):
    pass


class TextTemplateObject(HTMLTemplateObject):
    def get_admin_preview_value(self, value, *args):
        return super().get_admin_preview_value(value, *args).replace("\n", "<br>")
