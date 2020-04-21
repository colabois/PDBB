class BaseType:
    def check_value(self, value):
        """Check if value is good"""
        pass

    def set(self, value):
        """Check and set value"""
        pass

    def get(self):
        """Get value"""
        pass

    def to_save(self):
        """Build a serializable data to save"""
        pass

    def load(self, value):
        """Fill with value"""
        pass
