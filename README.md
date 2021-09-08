# Unlimited Studies

web app: flashcard application to learns things like vocabulary.

[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)  
[![forthebadge](http://forthebadge.com/images/badges/powered-by-electricity.svg)](http://forthebadge.com)

### Require

- Python 3.x
- modules from requirements.txt
- postgresql

## Installation and requirements.

### Install require.

- Python 3 _[Download Python](https://www.python.org/downloads/)_

### Install app.

Link to the GitHub repository : [Unlimited Studies](https://github.com/tbuglioni/unlimited-studies.git)

- Fork the project : [Fork a project](https://guides.github.com/activities/forking/)
- Create a directory for the clone.<br>
- Clone : <br><br>`user@computer:~/_path_/$ git clone <repository_url>`<br><br>
- Install [postgresql](https://www.postgresql.org/download/).
- Create a database ([Official Documentation](https://www.postgresql.org/docs/))
- open unlimited_studies/settings/__init__.py and add in "DATABASES" your credentials

### Install Python's modules.

- Install requirements in virtual env. : <br><br>`pipenv install -r requirements.txt`<br>

be careful --> mac os : psycopg2-binary / windows : psycopg2

### Add your own configuration
- run this commande in the terminal :
  python3 manage.py makemigrations
  python3 manage.py migrate
  python3 manage.py run_import
  python3 manage.py runserver

## Versions

1.0

## Production link
206.189.51.144

## Authors

- **Thomas Buglioni** [link](https://github.com/tbuglioni)

## License

his project is licensed under the `MIT License` - see the file [LICENSE.md](LICENSE.md) for further information
