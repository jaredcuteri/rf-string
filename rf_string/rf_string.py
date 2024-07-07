import re
from string import Formatter


class _StoredFormatter:
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


class InconsistentRfStringDefError(ValueError):
    """RFstr definition is inconsistent."""


class MatchNotFoundError(ValueError):
    """Match not found for string sample."""


class RFString:
    def __init__(self, r_string_spec: str, f_string_spec: str):
        self._parser = re.compile(r_string_spec)
        self._formatter = _StoredFormatter(f_string_spec)
        self._validate()

    def _validate(self) -> None:
        """Validate that the parser and formatter generated from the r- and f- strings are consistent."""
        # Parse fields from f-string
        formatter_field_specs = self._formatter.get_field_names_spec()
        formatter_field_names = formatter_field_specs.keys()

        # Get groups from the r-string
        parser_fields = self._parser.groupindex.keys()

        # If fields are not found in either string, no validation is needed
        if len(parser_fields) == len(formatter_field_names) == 0:
            return

        # Make sure the fields are consistent
        if len(parser_fields) != len(formatter_field_names):
            raise InconsistentRfStringDefError(
                f'Inconsistent fields provided {parser_fields} in r-string'
                f' and {formatter_field_names} in f-string fields.'
            )

        # Ensure that all field names match
        for parser_field in parser_fields:
            if parser_field not in formatter_field_names:
                raise InconsistentRfStringDefError(
                    f'{parser_field} was specified in r-string but not found in f-string fields {formatter_field_names}'
                )

        # TODO: Ensure that all fields have compatible format specifications

        # TODO: Add check to make sure users isn't using to-be-supported regex

    def parse(self, string: str) -> dict:
        """Parse string into field values."""
        if match := self._parser.fullmatch(string):
            return match.groupdict()
        raise MatchNotFoundError(f'{string} does not match pattern {self._parser.pattern}')

    def write(self, field_values: dict) -> str:
        """Write fields to string"""
        return self._formatter.format(**field_values)
