# Heroku Deployment

## Instructions

* To deploy the application to Heroku, following the following steps:

  1. Create the Heroku application
  2. Prepare the Heroku database
  3. Test the App locally
  4. Deploy the App to Heroku

#### Step 1: Creating the Heroku App

  * Login into Heroku CLI in terminal:
    ```sh
    heroku login
    ```
  * Git clone repo at a desired location:
    ```sh
    git clone https://github.com/jvillama/sqlalchemyReview
    ```
  * Create new Heroku app:
    ```sh
    heroku create
    ```
  * Add Heroku Postgress addon:
    ```sh
    heroku addons:create heroku-postgresql:hobby-dev
    ```
  * List the config vars for your app. It will display the URL that your app is using to connect to the database, DATABASE_URL:
    ```sh
    heroku config
    ```
  * Copy value for `DATABASE_URL` variable
  * Create `.env` file based off `.env-example` file in repo
  * Paste copied `DATABASE_URL` value into the `DATABASE_URL` variable in `.env` file (i.e. DATABASE_URL = <your-db-url>)

#### Step 2: Preparing the Database

  * Load sample db into Heroku Postgres (pulled from http://postgresguide.com/setup/example.html)
    ```sh
    heroku pg:backups:restore 'http://cl.ly/173L141n3402/download/example.dump' DATABASE_URL
    ```

  * Connect with to Heroku Postgres database via pgAdmin4 (Note: Set `DB restriction` to only your database)

  * View/Edit primary keys with Pgadmin4 (edit primary keys)

  ```
  -- Add primary key
  ALTER TABLE purchase_items
  ADD PRIMARY KEY (id);

  -- Add combo primary keys, but can't because of duplicates
  -- ERROR:  could not create unique index "purchase_items_pkey"
  -- DETAIL:  Key (purchase_id, product_id)=(601, 12) is duplicated.
  ALTER TABLE purchase_items ADD PRIMARY KEY (purchase_id, product_id);

  -- Remove primary key
  ALTER TABLE purchase_items
  DROP CONSTRAINT purchase_items_pkey;
  ```

#### Step 3: Testing the App locally

  * Test the app locally by first creating a new conda environment just for this app. All of our project dependencies will be installed in this environment. Note: This should only contain python 3.7 and not anaconda.

  ```sh
  conda create -n review_env python=3.7
  ```

  * Make sure to activate this new environment before proceeding.

  ```sh
  conda activate review_env
  ```

  OR

  ```sh
  source activate review_env
  ```

  * Next, we install `gunicorn` with `pip install gunicorn`. Gunicorn is a high performance web server that can run their Flask app in a production environment.

  * Because this app will use Postgres, we also install `psycopg2` with `pip install psycopg2`.

  * Make sure to install any other dependencies that are required by the application. This may be `flask-sqlalchemy`, or any other Python package that is required to run the app. **Test the app locally to make sure that it works!**

  ```
  pip install gunicorn
  pip install psycopg2
  pip install flask
  pip install flask-sqlalchemy
  pip install python-dotenv
  pip install flask-marshmallow
  pip install marshmallow-sqlalchemy
  ```

  * Run the app locally using the following:
  ```sh
  python app.py
  ```

#### Step 4: Deploying the App to Heroku

  * Deploy Flask API application to Heroku
  ```sh
  git push heroku master
  ```

  * Open the application using `heroku open` from the terminal.
