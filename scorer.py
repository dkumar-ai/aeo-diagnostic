"""
Scorer module to calculate brand visibility scores and grades.
"""

def score_brand_position(position):
    """
    Convert brand position to score (0-10).
    
    Args:
        position (int): Brand rank position (1-indexed), or None if not found
    
    Returns:
        int: Score from 0-10
    """
    if position is None:
        return 0
    elif position == 1:
        return 10
    elif position == 2:
        return 8
    elif position == 3:
        return 6
    elif position == 4:
        return 4
    elif position == 5:
        return 2
    else:
        return 0


def calculate_overall_score(scores):
    """
    Calculate overall visibility score as average of all LLM scores.
    
    Args:
        scores (list): List of individual LLM scores
    
    Returns:
        float: Average score
    """
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def score_to_grade(score):
    """
    Convert numerical score to letter grade.
    
    Args:
        score (float): Score from 0-10
    
    Returns:
        tuple: (grade_letter, color) where color is 'green', 'yellow', or 'red'
    """
    if score >= 9:
        return 'A', 'green'
    elif score >= 7:
        return 'B', 'green'
    elif score >= 5:
        return 'C', 'yellow'
    elif score >= 3:
        return 'D', 'red'
    else:
        return 'F', 'red'


def get_grade_description(score):
    """
    Get visibility description based on score.
    
    Args:
        score (float): Score from 0-10
    
    Returns:
        str: Description of visibility level
    """
    if score >= 9:
        return "Excellent visibility"
    elif score >= 7:
        return "Good visibility"
    elif score >= 5:
        return "Moderate visibility"
    elif score >= 3:
        return "Poor visibility"
    else:
        return "Not visible"


def generate_recommendation(score):
    """
    Generate recommendation text based on score.
    
    Args:
        score (float): Score from 0-10
    
    Returns:
        str: Recommendation text
    """
    if score < 5:
        return (
            "Your brand has low AI visibility. "
            "Consider optimizing product descriptions with keywords that match "
            "how customers search for this category. Focus on review volume and "
            "content quality to improve rankings."
        )
    elif score <= 7:
        return (
            "Your brand has moderate visibility. "
            "Focus on review volume and recency to improve rankings. "
            "Ensure your product descriptions are comprehensive and "
            "include relevant keywords."
        )
    else:
        return (
            "Your brand has strong AI visibility. "
            "Monitor competitor mentions to maintain your position. "
            "Continue optimizing content and gathering customer reviews."
        )
