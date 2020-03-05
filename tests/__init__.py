import sys
from pathlib import Path

package = Path(sys.path[0]).parent
for d in package.iterdir():
    if d.is_dir() and not d in sys.path:
        sys.path.insert(0, d)

print(sys.path)