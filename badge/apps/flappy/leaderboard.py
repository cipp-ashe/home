"""
Leaderboard system for Flappy Bird game.
Stores high scores persistently to a file.
"""
import os


class Leaderboard:
    """
    Manages high scores for the Flappy Bird game.
    Stores scores in a simple text file format.
    """
    
    # Use /system/apps/flappy for storage to ensure it's writable
    LEADERBOARD_FILE = "/system/apps/flappy/scores.txt"
    MAX_ENTRIES = 10
    
    @staticmethod
    def save_score(score, player_type="DEMO"):
        """
        Save a score to the leaderboard.
        
        Args:
            score: The score to save
            player_type: Type of player (DEMO or HUMAN)
        """
        try:
            # Read existing scores
            scores = Leaderboard.load_scores()
            
            # Add new score
            scores.append({
                'score': score,
                'type': player_type
            })
            
            # Sort by score (descending)
            scores.sort(key=lambda x: x['score'], reverse=True)
            
            # Keep only top scores
            scores = scores[:Leaderboard.MAX_ENTRIES]
            
            # Write back to file
            Leaderboard._write_scores(scores)
            
        except Exception as e:
            # If we can't save, fail silently to avoid crashing the game
            print(f"Error saving score: {e}")
    
    @staticmethod
    def load_scores():
        """
        Load scores from the leaderboard file.
        
        Returns:
            list: List of score dictionaries
        """
        scores = []
        
        try:
            # Check if file exists
            if not Leaderboard._file_exists(Leaderboard.LEADERBOARD_FILE):
                return scores
            
            # Read scores from file
            with open(Leaderboard.LEADERBOARD_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        # Parse line: "score:type"
                        parts = line.split(':')
                        if len(parts) >= 2:
                            scores.append({
                                'score': int(parts[0]),
                                'type': parts[1]
                            })
        except Exception as e:
            # If we can't read, return empty list
            print(f"Error loading scores: {e}")
            return []
        
        return scores
    
    @staticmethod
    def get_high_score():
        """
        Get the highest score from the leaderboard.
        
        Returns:
            int: The highest score, or 0 if no scores exist
        """
        scores = Leaderboard.load_scores()
        if scores:
            return scores[0]['score']
        return 0
    
    @staticmethod
    def _write_scores(scores):
        """
        Write scores to the leaderboard file.
        
        Args:
            scores: List of score dictionaries to write
        """
        try:
            with open(Leaderboard.LEADERBOARD_FILE, 'w') as f:
                for entry in scores:
                    f.write(f"{entry['score']}:{entry['type']}\n")
        except Exception as e:
            print(f"Error writing scores: {e}")
    
    @staticmethod
    def _file_exists(path):
        """
        Check if a file exists.
        
        Args:
            path: File path to check
            
        Returns:
            bool: True if file exists, False otherwise
        """
        try:
            os.stat(path)
            return True
        except OSError:
            return False
