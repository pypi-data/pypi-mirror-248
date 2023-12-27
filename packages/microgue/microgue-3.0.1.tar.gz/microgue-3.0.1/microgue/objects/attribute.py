class Attribute:
    def __init__(self, hidden=False, required=False, unique=False, default=False, default_value=None):
        self.hidden = hidden
        self.required = required
        self.unique = unique
        self.default = default
        self.default_value = default_value
