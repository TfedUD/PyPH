import PHX._base


class Foundation(PHX._base._Base):
    def __init__(self):
        super(Foundation, self).__init__()
        self.name = "My First Foundation"
        self.floor_type = 5  # None
        self.floor_setting = 6  # User Defined

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Foundation(cls, _dict)
