class Weapon:
    def __init__(self):
        pass

    def __eq__(self, other):
        return (other is not None) and (self.__dict__ == other.__dict__)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return "{}()".format(type(self).__name__)
