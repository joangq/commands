from dataclasses import dataclass

@dataclass
class Expression:
    value: object
    negated: bool
    label: None|str

    def set_label(self, varname: None|str):
        self.label = varname
        return self
    
    def negate(self):
        cls = type(self)
        return cls(self.value, not self.negated, self.label)

    def __invert__(self):
        return self.negate()

    def compile(self):
        string = ''
        if not self.label:
            raise ValueError("Label is empty.")

        string += self.label
        if self.negated:
            string += '!'
        string += '='
        string += self.value

        return string

    def __str__(self):
        return self.compile()

def value(val: object) -> Expression:
    return Expression(val, False, None)

def is_not(val: object) -> Expression:
    return Expression(val, True, None)