
Highly Minimalistic .env File Wrapper

### Sample:

Suppose you have the following .env file:

```sh
ACCESS_KEY = jriofesdjxifocjewsayiofdlcj
```

Parsing it may look something like this:
```py
>>> import os
>>> from pyenvs import load_dotenv
>>> load_dotenv()
>>> os.environ["ACCESS_KEY"]
jriofesdjxifocjewsayiofdlcj
```