# Repo Xpto Software Engineer

In this exercise, you will help us build part (an Api) of a monitoring system that detects and displays the music that is broadcast on radio stations across the world.

Our fingerprinting team is responsible for building an infrastructure to download radio streams, and running their algorithms to automatically detect what is being played on a given radio station at a given time. Your job is to help them store their results in a database​.

The following information needs to be stored:

- Radio stations, identified by their (unique) names
- Performers, also identified by their names (which you may assume is unique)
- Songs, identified by their names and their performer
- Plays, identified by a song, a radio station, and start and end times (with a precision to the second)

The fingerprinting team needs to be able to do the following tasks:

- Insert a new radio station
- Insert a new artist
- Insert a new song
- Insert a new play
- Get all the plays for a given song between two dates
- Get all the songs played on a given channel between two dates

The Head of Product walks into your meeting by mistake and, after hearing your conversation, decides to add the following requirement in order to impress potential customers:

- Get a top 40 for a given week and a given list of channels: produce a list of 40 songs ordered by the number of times they were broadcast. For each song, provide their performer, play count and the position they had the previous week.

[Here is an article about this repo (on Medium).](https://medium.com/@dedecu/build-a-flask-api-as-assignment-for-the-software-engineer-position-80ddbb6465a1)

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