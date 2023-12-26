class Logo:
    
    def __init__(self, size_x, size_y):
        self.size_x = size_x;
        self.size_y = size_y;

    def draw(self):
        print(f"Drowing Logo of dimention x={self.size_x}, y={self.size_y}")
