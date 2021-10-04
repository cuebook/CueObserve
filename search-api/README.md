# ReadMe

The code for flask application can be found in `search` folder
Run given below codes in `search-api` directory

## To setup dev environment
```sh
docker build -t cue-search .
```
=======


## Run Development
``` sh
docker run --network="host" -v $(pwd):/code/ -p 8200:8200 cue-search
```
OR 
```sh
python manage.py run
```
visit http://127.0.0.1:8200/

### Migrations
```sh
flask db migrate
```

## To install package while developing
Exec in container & then install 
```sh
python -m pip install <package-name>
```
