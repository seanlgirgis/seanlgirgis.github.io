
import yaml
from pathlib import Path

base_dir = Path(__file__).parent
style_path = base_dir / 'config' / 'style.yaml'

with open(style_path, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

print("--- DEBUG CONFIG DUMP ---")
print("Theme Spacing (Raw YAML):")
try:
    print(data.get('theme', {}).get('spacing', {}))
except Exception as e:
    print(e)
