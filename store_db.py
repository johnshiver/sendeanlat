#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite


def drop_table():
    con = lite.connect('tweets.db')

    with con:

        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Tweets")


def create_table():
    con = lite.connect('tweets.db')

    with con:

        cur = con.cursor()
        cur.execute("CREATE TABLE Tweets(screen_name TEXT, tweet TEXT, hash_tag TEXT, match_term TEXT, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)")


def dropAndCreate():
    drop_table()
    create_table()


def execute_query(queryString):
    try:
        con = lite.connect('tweets.db')

        with con:
            cur = con.cursor()
            cur.execute(queryString)
    except lite.Error, e:
        print "There was an Error %s" % e.args[0]