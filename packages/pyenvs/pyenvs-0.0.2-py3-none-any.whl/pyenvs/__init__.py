"""
Minimalistic .env File Wrapper

sample .env file:

```sh
ACCESS_KEY = jriofesdjxifocjewsayiofdlcj
```

Usage:

```
>>> import os
>>> from pyenvs import load_dotenv
>>> load_dotenv()
>>> os.environ["ACCESS_KEY"]
jriofesdjxifocjewsayiofdlcj
```
"""
from pyenvs.env_loader import load_dotenv
