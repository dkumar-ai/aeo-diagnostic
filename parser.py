"""
Parser module to extract ranked brands from LLM responses.
"""

def parse_response(response_text):
    """
    Parse LLM response to extract numbered list of brands.
    
    Args:
        response_text (str): Raw response from LLM
    
    Returns:
        list: Ordered list of brand names
    """
    brands = []
    lines = response_text.split('\n')
    
    for line in lines:
        line = line.strip()
        # Match lines that start with a number (1. 2. 3. etc.)
        if line and line[0].isdigit() and '.' in line[:3]:
            # Extract the part after the number and period
            parts = line.split('.', 1)
            if len(parts) > 1:
                brand_text = parts[1].strip()
                # Extract just the brand name (before any dash or reason)
                if ' - ' in brand_text:
                    brand_name = brand_text.split(' - ')[0].strip()
                else:
                    # Take the first few words as the brand name
                    brand_name = brand_text.split()[0] if brand_text else ""
                
                if brand_name:
                    brands.append(brand_name)
    
    return brands


def find_target_brand(brands, target_brand):
    """
    Find target brand in the list and return its position.
    
    Args:
        brands (list): List of brand names from LLM
        target_brand (str): Brand to search for
    
    Returns:
        tuple: (position, rank_string) where position is 0-indexed, 
               rank_string is "1st", "2nd", etc., or "not mentioned"
    """
    if not target_brand:
        return None, "not mentioned"
    
    target_lower = target_brand.lower()
    
    for idx, brand in enumerate(brands):
        brand_lower = brand.lower()
        # Case-insensitive and partial match
        if target_lower in brand_lower or brand_lower in target_lower:
            position = idx + 1
            # Convert position to ordinal
            if position == 1:
                rank_str = "1st"
            elif position == 2:
                rank_str = "2nd"
            elif position == 3:
                rank_str = "3rd"
            else:
                rank_str = f"{position}th"
            return position, rank_str
    
    return None, "not mentioned"


def extract_competitors(all_brands_per_llm, target_brand):
    """
    Extract and rank competitors based on frequency across all LLMs.
    
    Args:
        all_brands_per_llm (list): List of brand lists from each LLM
        target_brand (str): Brand to exclude from competitors
    
    Returns:
        list: Sorted list of (brand_name, frequency) tuples
    """
    competitor_count = {}
    target_lower = target_brand.lower() if target_brand else ""
    
    for brands in all_brands_per_llm:
        for brand in brands:
            brand_lower = brand.lower()
            # Skip the target brand
            if target_lower and (target_lower in brand_lower or brand_lower in target_lower):
                continue
            
            competitor_count[brand] = competitor_count.get(brand, 0) + 1
    
    # Sort by frequency (descending)
    sorted_competitors = sorted(competitor_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_competitors
