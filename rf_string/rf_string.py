import re

from rf_string.exceptions import MatchNotFoundError, InconsistentRfStringDefError
from rf_string.formatter import StoredFormatter


class RFString:
    def __init__(self, r_string_spec: str, f_string_spec: str):
        self._r_string = r_string_spec
        self._f_string = f_string_spec
        self._parser = re.compile(self._r_string)
        self._formatter = StoredFormatter(self._f_string)
        self._validate()

    def _test_round_trip(self) -> None:
        dummy_values = {field: idx for idx, field in enumerate(self._formatter.get_field_names_spec().keys())}
        written_str = self.write(dummy_values)
        parsed_values = self.parse(written_str)
        rewritten_str = self.write(parsed_values)
        if rewritten_str != written_str:
            raise InconsistentRfStringDefError(
                f'r-string definition {self._r_string} was not roundtrip compatible'
                f' with f-string definition {self._f_string}'
            )

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

        # Make sure r-string and f-string specified are round trip compatible
        self._test_round_trip()

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
