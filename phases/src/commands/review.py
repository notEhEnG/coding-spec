import os
import sys
import re
from pathlib import Path

def run_review(spec_file_path: str, target_dir_path: str | None) -> int:
    spec_path = Path(spec_file_path)
    if not spec_path.is_file():
        print(f"Error: spec file not found: {spec_path}", file=sys.stderr)
        return 1
        
    target_dir = Path(target_dir_path or '.')
    slug = spec_path.stem
    review_output = target_dir / 'docs' / 'plans' / f"{slug}-review.md"
    
    content = spec_path.read_text(encoding='utf-8')
    lines = content.splitlines()
    
    criteria = []
    in_ac_section = False
    
    ac_re = re.compile(r'(?i)^#+\s+(?:acceptance\s+criteria|done\s+when|success\s+criteria|expected\s+behavior)')
    heading_re = re.compile(r'^#+\s+')
    
    for line in lines:
        if ac_re.search(line):
            in_ac_section = True
            continue
        elif heading_re.match(line):
            in_ac_section = False
            
        if in_ac_section:
            stripped = line.strip()
            # Match bullet points or checkbox items in AC section
            match = re.match(r'^[-*]\s+(?:\[[ xX]\]\s+)?(.+)', stripped)
            if match:
                criteria.append(match.group(1))
            elif re.match(r'^\d+\.', stripped):
                criteria.append(re.sub(r'^\d+\.\s+', '', stripped))
                
    # Build review file
    review_lines = [
        f"# Implementation Review: {slug.replace('-', ' ').title()}",
        "",
        "This checklist compares implementation results against original acceptance criteria from the spec.",
        "",
        "## Acceptance Criteria Compliance Checklist",
        ""
    ]
    
    if not criteria:
        review_lines.append("- [ ] No explicit acceptance criteria list items found in the spec file.")
    else:
        for idx, item in enumerate(criteria, start=1):
            # Check if there is some code/test file referencing this (heuristic keywords lookup)
            keywords = [w.lower() for w in re.findall(r'\b\w{4,}\b', item)[:3]]
            matched_files = []
            
            if keywords and target_dir.is_dir():
                for root, _, files in os.walk(target_dir):
                    for file in files:
                        if file.endswith('.py') or file.endswith('.md'):
                            file_path = Path(root) / file
                            # Skip the spec itself, the review output, and phases folder
                            if file_path.resolve() == spec_path.resolve() or file_path.resolve() == review_output.resolve():
                                continue
                            if 'phases' in file_path.parts and 'examples' not in file_path.parts:
                                continue
                            try:
                                f_content = file_path.read_text(encoding='utf-8', errors='ignore').lower()
                                if all(k in f_content for k in keywords):
                                    matched_files.append(file_path.name)
                            except Exception:
                                pass
                                
            status = "[x]" if matched_files else "[ ]"
            evidence = f" (Evidence found in: {', '.join(matched_files)})" if matched_files else " (No matching code evidence found)"
            review_lines.append(f"- {status} {item}{evidence}")
            
    review_lines.append("")
    review_lines.append("## Verification Verdict")
    review_lines.append("- [ ] Passed manual review.")
    review_lines.append("- [ ] Verified in testing sandbox.")
    
    review_output.parent.mkdir(parents=True, exist_ok=True)
    review_output.write_text('\n'.join(review_lines) + '\n', encoding='utf-8')
    print(f"Generated implementation review checklist at: {review_output}")
    return 0
