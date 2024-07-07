from string import Formatter


class StoredFormatter:
    """Formatter wrapper that stores the format string"""
    def __init__(self, format_string):
        self._format_string = format_string
        self._fmt = Formatter

    def format(self, *args, **kwargs):
        return self._fmt().format(self._format_string, *args, **kwargs)

    def parse(self):
        """ Returns (literal_text, field_name, format_spec, conversion)"""
        return self._fmt().parse(self._format_string)

    def get_field_names_spec(self):
        name_spec = {}
        for literal_text, field_name, format_spec, conversion in self.parse():
            if field_name is not None:
                name_spec[field_name] = format_spec
        return name_spec
