# run.py  (in the root folder: advocate-assistant/run.py)

import sys
from pathlib import Path

# Add the current directory to Python path so 'backend' and 'shared' can be found
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)