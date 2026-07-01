import sys
import re
from pathlib import Path

def run_validate(spec_file_path: str) -> int:
    spec_path = Path(spec_file_path)
    if not spec_path.is_file():
        print(f"Error: spec file not found: {spec_path}", file=sys.stderr)
        return 1
        
    content = spec_path.read_text(encoding='utf-8')
    lines = content.splitlines()
    
    errors = []
    warnings = []
    
    has_ac = False
    ac_content_lines = 0
    in_ac_section = False
    
    has_non_goals = False
    has_test_considerations = False
    
    # Regex definitions
    ac_re = re.compile(r'(?i)^#+\s+(?:\d+\.\s+)?(?:acceptance\s+criteria|done\s+when|success\s+criteria|expected\s+behavior)')
    non_goals_re = re.compile(r'(?i)^#+\s+(?:\d+\.\s+)?(?:non-?goals?|out\s+of\s+scope|exclusions?)')
    test_re = re.compile(r'(?i)^#+\s+(?:\d+\.\s+)?(?:test\s+considerations?|testing|test\s+strategies?)')
    heading_re = re.compile(r'^#+\s+')
    
    for line in lines:
        if ac_re.search(line):
            has_ac = True
            in_ac_section = True
            continue
        elif non_goals_re.search(line):
            has_non_goals = True
            in_ac_section = False
            continue
        elif test_re.search(line):
            has_test_considerations = True
            in_ac_section = False
            continue
        elif heading_re.match(line):
            in_ac_section = False
            
        if in_ac_section:
            stripped = line.strip()
            # Count bullet points, checkboxes, or numbered items in AC section
            if stripped.startswith('-') or stripped.startswith('*') or re.match(r'^\d+\.', stripped):
                ac_content_lines += 1
                
    # Evaluate Acceptance Criteria
    if not has_ac:
        errors.append("Missing required 'Acceptance Criteria' heading.")
    elif ac_content_lines == 0:
        errors.append("'Acceptance Criteria' section exists but contains no criteria list items.")
        
    # Evaluate Non-Goals
    if not has_non_goals:
        warnings.append("Missing 'Non-Goals / Out of Scope' section. Defining what is out of scope prevents feature drift.")
        
    # Evaluate Test Considerations
    if not has_test_considerations:
        errors.append("Missing 'Test Considerations / Testing' section. High-quality specs require test strategy planning.")
        
    # Output results
    print(f"Auditing spec file: {spec_path}")
    print(f"  Found {len(errors)} error(s), {len(warnings)} warning(s).")
    
    for err in errors:
        print(f"  [ERROR] {err}")
    for warn in warnings:
        print(f"  [WARNING] {warn}")
        
    if errors:
        print("Validation FAILED.")
        return 1
    else:
        print("Validation PASSED.")
        return 0
