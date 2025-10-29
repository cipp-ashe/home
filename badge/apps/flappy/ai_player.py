"""
AI Player for Flappy Bird that can play the game autonomously.
Uses simple physics-based decision making to avoid obstacles.
"""
from obstacle import Obstacle


class AIPlayer:
    """
    AI that plays Flappy Bird by calculating optimal jump timing
    based on obstacle positions and Mona's current state.
    """
    
    def __init__(self):
        self.look_ahead_distance = 80  # How far ahead to look for obstacles
        self.jump_buffer = 5  # Pixels of safety margin when jumping
        self.last_jump_time = 0
        self.min_jump_interval = 200  # Minimum ms between jumps to prevent spam
    
    def should_jump(self, mona, ticks):
        """
        Determine if Mona should jump based on current game state.
        
        Args:
            mona: The Mona player object
            ticks: Current game ticks (time)
            
        Returns:
            bool: True if Mona should jump, False otherwise
        """
        try:
            if mona.is_dead():
                return False
            
            # Don't jump too frequently
            if ticks - self.last_jump_time < self.min_jump_interval:
                return False
            
            # Get Mona's current position and velocity
            mona_x, mona_y = mona.pos
            mona_velocity = mona.velocity
        except Exception:
            # If there's any issue reading mona's state, don't jump
            return False
        
        # Find the next obstacle in front of Mona
        next_obstacle = self._get_next_obstacle(mona_x)
        
        if next_obstacle is None:
            # No obstacle ahead, maintain safe altitude
            if mona_y > 60:  # If falling too low, jump
                self.last_jump_time = ticks
                return True
            return False
        
        # Calculate where Mona will be when reaching the obstacle
        distance_to_obstacle = next_obstacle.x - mona_x
        
        # Only consider obstacles that are close enough
        if distance_to_obstacle > self.look_ahead_distance:
            # Maintain safe altitude if no immediate obstacle
            if mona_y > 60:
                self.last_jump_time = ticks
                return True
            return False
        
        # Get the gap position
        gap_top = next_obstacle.gap_y
        gap_bottom = next_obstacle.gap_y + next_obstacle.gap_height
        gap_center = (gap_top + gap_bottom) / 2
        
        # Predict Mona's future position using simple physics
        # When to start considering jumping
        if distance_to_obstacle < 40:
            # We're close to the obstacle, make precise adjustments
            
            # Calculate where Mona will be
            predicted_y = mona_y + (mona_velocity * 5)  # Look ahead ~5 frames
            
            # If Mona is above the gap center and falling, let gravity work
            if predicted_y < gap_center - 10 and mona_velocity > 0:
                return False
            
            # If Mona is below the safe zone or heading there, jump
            if predicted_y > gap_center + 5:
                self.last_jump_time = ticks
                return True
            
            # If velocity is taking us toward the bottom pipe, jump
            if mona_velocity > 1 and mona_y > gap_center:
                self.last_jump_time = ticks
                return True
        else:
            # We have time, aim for the gap center
            target_y = gap_center
            
            # If we're significantly below target and falling, jump
            if mona_y > target_y + self.jump_buffer and mona_velocity > -1:
                self.last_jump_time = ticks
                return True
        
        return False
    
    def _get_next_obstacle(self, mona_x):
        """
        Get the next obstacle in front of Mona.
        
        Args:
            mona_x: Mona's current x position
            
        Returns:
            Obstacle or None: The next obstacle ahead, or None if none exists
        """
        next_obstacle = None
        min_distance = float('inf')
        
        for obstacle in Obstacle.obstacles:
            # Only consider obstacles ahead of Mona
            distance = obstacle.x - mona_x
            if distance > 0 and distance < min_distance:
                min_distance = distance
                next_obstacle = obstacle
        
        return next_obstacle
