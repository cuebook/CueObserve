---
description: Setup for development
---

# Development

#### UI Setup 

```text
cd ui    # go to ui directory
npm i    # install dependencies
```

#### Start UI Server

```text
cd ui
npm start    # start development server
```

#### Backend Setup 

```text
cd api    # go to api directory
python3.7 -m virtualenv myenv    # make python3.7 virtual environment
source myenv/bin/activate         # activate virtual environment
pip install -r requirements.txt     # install dependencies
python manage.py migrate
python manage.py loaddata seeddata/*.json
```

#### Start Backend Server

```text
cd api
source myenv/bin/activate
python manage.py runserver
```





