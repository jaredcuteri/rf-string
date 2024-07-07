import re
from string import Formatter


class _StoredFormatter(Formatter):
    """Formatter wrapper that stores the format string"""
    def __init__(self, format_string):
        self._format_string = format_string

    def format(self, *args, **kwargs):
        return super().format(self._format_string, args, kwargs)

    def vformat(self, args, kwargs):
        return super().vformat(self._format_string, args, kwargs)

    def parse(self):
        """ Returns (literal_text, field_name, format_spec, conversion)"""
        return super().parse(self._format_string)

    def get_field_names(self):
        field_names = []
        for literal_text, field_name, format_spec, conversion in self.parse():
            if field_name is not None:
                field_names.append(field_name)
        return field_names


class InconsistentRfStringDefError(ValueError):
    """RFstr definition is inconsistent."""


class RFstr:
    def __init__(self, r_string_spec: str, f_string_spec: str):
        self._parser = re.compile(r_string_spec)
        self._formatter = _StoredFormatter(f_string_spec)
        self._validate()

    def _validate(self) -> None:
        """Validate that the parser and formatter generated from the r- and f- strings are consistent."""
        # Parse fields from f-string
        formatter_fields = self._formatter.get_field_names()

        # Get groups from the r-string
        parser_fields = self._parser.groupindex.keys()

        # If fields are not found in either string, no validation is needed
        if len(parser_fields) == len(formatter_fields) == 0:
            return

        # Make sure the fields are consistent
        if len(parser_fields) != len(formatter_fields):
            raise InconsistentRfStringDefError(
                f'Inconsistent fields provided {parser_fields} in r-string and {formatter_fields} in f-string fields.'
            )

        # Ensure that all field names match
        for parser_field in parser_fields:
            if parser_field not in formatter_fields:
                raise InconsistentRfStringDefError(
                    f'{parser_field} was specified in r-string but not found in f-string fields {formatter_fields}'
                )

        # Ensure that all fields have compatible format specifications



    def parse(self, string: str) -> dict:
        """Parse string into field values."""

    def write(self, field_values: dict) -> str:
        """Write fields to string"""
