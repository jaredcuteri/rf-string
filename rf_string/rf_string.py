
class RFstr(str):
    def init(self, r_string_spec, f_string_spec):
        self._r_string = r_string_spec
        self._f_string = f_string_spec

    def _validate(self):
        raise ValueError(f'r_string_spec and f_string_spec are not consistent')

    def parse(self, string: str) -> dict:
        """Parse string into field values."""

    def write(self, field_values: dict) -> str:
        """Write fields to string"""
