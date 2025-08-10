class Temperature:
    def __init__(self, temp: float):
        self.temp = temp

    def to_celsius(self):
        return self.temp

    def to_fahrenheit(self):
        return self.temp * 9 / 5 + 32
