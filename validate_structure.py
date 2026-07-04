import os
import sys

errors = []
required_fields = ['document_id', 'title', 'version', 'status', 'owner']

dirs_to_check = [
    'engineering-system/05-backend',
    'engineering-system/06-frontend',
    'engineering-system/07-mobile',
    'engineering-system/08-platform',
    'engineering-system/09-ai',
]

print("Validating document frontmatter structure...")
for d in dirs_to_check:
    if not os.path.exists(d):
        continue
    for fname in os.listdir(d):
        if not fname.endswith('.md') or fname == '.gitkeep':
            continue
        fpath = os.path.join(d, fname)
        try:
            with open(fpath, encoding='utf-8') as f:
                content = f.read()
            if not content.startswith('---'):
                errors.append(f"MISSING FRONTMATTER: {fpath}")
                continue
            for field in required_fields:
                if f'{field}:' not in content[:500]:
                    errors.append(f"MISSING FIELD '{field}': {fpath}")
        except Exception as e:
            errors.append(f"ERROR READING {fpath}: {e}")

if errors:
    print("\nDocument validation errors:")
    for e in errors:
        print(f"  ✗ {e}")
    sys.exit(1)
else:
    print("✓ All document structures validated successfully!")
