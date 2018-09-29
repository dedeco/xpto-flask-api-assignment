# Repo Xpto Software Engineer

1. How do I get set up? Set up Install python 3.x and Create a virtualenv:
    [See here how to](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/)

2. Create and running virtualenv
    ```
    user@server:~$ virtualenv -p python3 xpto
    user@server:~$ source xpto/bin/activate
    ```
3. Install all requeriments to use:
    ```
    (xpto) user@server:~$ pip install -r requirements.txt
    ```
4.  Create tables
    ```
    (xpto) user@server:~$ python create_tables.py
    ```
5.  Running the app
    ```
    (xpto) user@server:~$ python runserver.py
    ```
6.  Running tests (in other terminal window run the virtualenv too and then run this code bellow)
    ```
    (xpto) user@server:~$ python test.py -H 0.0.0.0 -P 5000 --add-data
    ```