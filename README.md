# Backend Description
This backend is written in Python using Django, extended by
the Django Rest Framework. 

## Build Instructions
The dependencies are managed by Pipenv. To activate the 
virtual environment do the following: 

1. `pip install pipenv`
2. `pipenv install --dev`
3. `pipenv shell`

At this point you will need the `.env` file to get the app to run. To get this
file please contact Param at param@theorangeyak.co for further instructions. Or
if you have permission, you will be able to find all the credentials for this
project in the Orange Yak Google Drive folder. Look at: 
    `theorangeyakco/<active_projects|archived_projects>/
    intersection_magazine/notes/credentials.gsheet`.

You will also find the environment variables there.

Now you will need other pre-requisites:
1. `postgresSQL`
    * Please set it up on your machine and create a local database to connect to. Put
    this localhost URL in the `DATABASE_URL` environment variable.
2. `redis`
    * Not currently required.
    
Finally, you can run the app with:
`python manage.py runserver`

Which will start a server at `localhost:8000`.


## Deploy Instructions

The deploy remote of this repo exists on 
`https://github.com/paramkpr/intersection-backend-deploy.git`. 

The `backend/` directory needs to be pushed as a subtree to this
repo. When code is added to the `main` branch on the `deploy` repo, 
it will *auto-deploy* to Heroku. The command is:

* `cd` into project_root = `intersection/`
* `git subtree push --prefix=backend/ deploy main`


