class TrajectoryDetector:
    def __init__(self, movement_threshold=60):
        """Initialize the trajectory detector
        
        Args:
            movement_threshold (int): Minimum distance to trigger directional detection
        """
        self.movement_threshold = movement_threshold
        self.prev_x = None
        self.prev_y = None
        self.screen_width = None
        self.screen_height = None

    def set_screen_size(self, width: int, height: int):
        """Set the screen dimensions for coordinate normalization
        
        Args:
            width (int): Screen width in pixels
            height (int): Screen height in pixels
        """
        self.screen_width = width
        self.screen_height = height

    def detect_direction(self, x_normalized: float, y_normalized: float) -> str:
        """Detect movement direction based on normalized coordinates
        
        Args:
            x_normalized (float): Normalized x coordinate (0-1)
            y_normalized (float): Normalized y coordinate (0-1)
            
        Returns:
            str: Direction detected ('up', 'down', 'left', 'right', or None if no direction detected)
        """
        if self.screen_width is None or self.screen_height is None:
            raise ValueError("Screen size not set. Call set_screen_size first.")

        x = int(x_normalized * self.screen_width)
        y = int(y_normalized * self.screen_height)
        
        direction = None
        
        if self.prev_x is not None and self.prev_y is not None:
            dx = x - self.prev_x
            dy = y - self.prev_y
            
            if abs(dx) > abs(dy):
                if dx > self.movement_threshold:
                    direction = 'right'
                elif dx < -self.movement_threshold:
                    direction = 'left'
            else:
                if dy > self.movement_threshold:
                    direction = 'down'
                elif dy < -self.movement_threshold:
                    direction = 'up'
                    
        self.prev_x, self.prev_y = x, y
        return direction

    def reset_position(self):
        """Reset the previous position tracking"""
        self.prev_x = None
        self.prev_y = None