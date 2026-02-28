#!/usr/bin/env python3
"""
Generate personalized cover letters based on job posting + template
"""

import json
import os
from datetime import datetime

TEMPLATE_FILE = os.path.join(os.path.dirname(__file__), 'templates/cover-letter-template.md')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'cover-letters')

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_template():
    """Load master cover letter template"""
    if os.path.exists(TEMPLATE_FILE):
        with open(TEMPLATE_FILE, 'r') as f:
            return f.read()
    return "Template not found - awaiting Richard's example"

def generate_cover_letter(job_data):
    """
    Generate personalized cover letter for a job posting
    
    Args:
        job_data: {
            'company': str,
            'position': str,
            'hiring_manager': str (optional),
            'key_requirements': [str],
            'job_description': str
        }
    """
    
    template = load_template()
    
    # TODO: Implement AI personalization using Claude
    # For now, return placeholder
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{job_data.get('company', 'unknown')}_{job_data.get('position', 'position')}_{timestamp}.md"
    
    output_file = os.path.join(OUTPUT_DIR, filename)
    
    with open(output_file, 'w') as f:
        f.write(f"# Cover Letter\n\n")
        f.write(f"**Company:** {job_data.get('company')}\n")
        f.write(f"**Position:** {job_data.get('position')}\n")
        f.write(f"**Generated:** {timestamp}\n\n")
        f.write("---\n\n")
        f.write(template)
    
    print(f"✅ Cover letter draft saved: {filename}")
    return output_file

if __name__ == "__main__":
    # Test
    test_job = {
        'company': 'Novo Nordisk',
        'position': 'Senior Product Manager',
        'hiring_manager': 'Jane Smith',
        'key_requirements': ['product management', 'pharma', 'global teams']
    }
    
    generate_cover_letter(test_job)
