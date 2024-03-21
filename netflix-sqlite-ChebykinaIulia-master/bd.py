import sqlite3


def create_tables(conn, old_conn):
    cursor = conn.cursor()
    cursor.execute("""create table shows(
                        show_id int primary key,
                        title text, 
                        date_added varchar(50),
                        release_year int check(release_year <= 2020),
                        rating varchar(10),
                        type varchar(10) check(type in ('Movie/Minutes', 'TV Show/Seasons')),
                        duration int,
                        description text);""")
    cursor.execute("""create table directors(
                        director varchar(100),
                        show_id int,
                        primary key(director, show_id),
                        FOREIGN KEY (show_id) REFERENCES shows(show_id));""")
    cursor.execute("""create table countries(
                        country varchar(50),
                        show_id int,
                        primary key(country, show_id),
                        FOREIGN KEY (show_id) REFERENCES shows(show_id));""")
    cursor.execute("""create table actors(
                        actor varchar(100),
                        show_id int,
                        primary key(actor, show_id),
                        FOREIGN KEY (show_id) REFERENCES shows(show_id));""")
    cursor.execute("""create table genres(
                        genre varchar(50),
                        show_id int,
                        primary key(genre, show_id),
                        FOREIGN KEY (show_id) REFERENCES shows(show_id));""")

    conn.commit()

    for row in old_conn.execute("""select * from netflix_titles"""):
        show_id, type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description = row
        if type == 'Movie':
            type += '/Minutes'
        else:
            type += '/Seasons'
        duration = int(duration.split()[0])
        shows = show_id, title, date_added, release_year, rating,  type, duration, description
        cursor.execute("insert into shows values(?,?,?,?,?,?,?,?)", shows)
        for d in set(director.split(', ')):
            lst = d, show_id
            cursor.execute("insert into directors values(?,?)", lst)
        for c in set(country.split(', ')):
            lst = c, show_id
            cursor.execute("insert into countries values(?,?)", lst)
        for a in set(cast.split(', ')):
            lst = a, show_id
            cursor.execute("insert into actors values(?,?)", lst)
        for g in set(listed_in.split(', ')):
            lst = g, show_id
            cursor.execute("insert into genres values(?,?)", lst)
    conn.commit()


def main():
    old_conn = sqlite3.connect('netflix.sqlite')
    new_conn = sqlite3.connect('new_netflix.sqlite')
    create_tables(new_conn, old_conn)


if __name__ == '__main__':
    main()
