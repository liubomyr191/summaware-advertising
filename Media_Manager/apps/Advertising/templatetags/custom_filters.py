from itertools import accumulate  # Add this import statement

from django import template

register = template.Library()

@register.filter
def format_gl_code(value):
    # Remove non-numeric characters from the string
    value = ''.join(filter(str.isdigit, value))
    
    # Define segment lengths
    segment_lengths = [2, 3, 2, 2, 4, 3]
    
    # Format the phone number
    formatted = '-'.join(value[start:start+length] for start, length in zip([0]+list(accumulate(segment_lengths)), segment_lengths))
    
    return formatted
