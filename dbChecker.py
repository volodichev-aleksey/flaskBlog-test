"""
This file contains the database schemas for the app.

The database consists of three tables:
1. Users: stores information about the users, including their username, email, password, profile picture, role, points, creation date, creation time, and verification status.
2. Posts: stores information about the posts, including their title, tags, content, author, date, time, views, last edit date, and last edit time.
3. Comments: stores information about the comments, including the post they are associated with, the comment text, the user who wrote the comment, the date, and the time.

This file contains functions to create the tables if they do not already exist, and to ensure that they have the correct structure.
"""

from helpers import mkdir, exists, message, sqlite3, currentTimeStamp, encryption
from constants import (
    DB_USERS_ROOT,
    DB_POSTS_ROOT,
    DEFAULT_ADMIN,
    DB_FOLDER_ROOT,
    DB_COMMENTS_ROOT,
    DEFAULT_ADMIN_POINT,
    DEFAULT_ADMIN_EMAIL,
    DEFAULT_ADMIN_USERNAME,
    DEFAULT_ADMIN_PASSWORD,
    DEFAULT_ADMIN_PROFILE_PICTURE,
)


# This function checks if the database folder exists, and creates it if it does not.
def dbFolder():
    """
    Checks if the database folder exists, and creates it if it does not.

    Returns:
        None
    """
    # Use the exists function to check if the DB_FOLDER_ROOT constant is a valid path
    match exists(DB_FOLDER_ROOT):
        # If the path exists, print a message with the level 6 (informational) and the folder name
        case True:
            message("6", f'DATABASE FOLDER: "/{DB_FOLDER_ROOT}" FOUND')
        # If the path does not exist, print a message with the level 1 (alert) and the folder name
        case False:
            message("1", f'DATABASE FOLDER: "/{DB_FOLDER_ROOT}" NOT FOUND')
            # Use the mkdir function to create the folder
            mkdir(DB_FOLDER_ROOT)
            # Print a message with the level 2 (success) and the folder name
            message("2", f'DATABASE FOLDER: "/{DB_FOLDER_ROOT}" CREATED')


# This function checks if the users table exists in the database, and creates it if it does not.
def usersTable():
    """
    Checks if the users table exists in the database, and creates it if it does not.
    Checks if default admin is true create admin user with custom admin account settings if it does.

    Returns:
        None
    """
    # Use the exists function to check if the DB_USERS_ROOT constant is a valid path
    match exists(DB_USERS_ROOT):
        # If the path exists, print a message with the level 6 (informational) and the database name
        case True:
            message("6", f'USERS DATABASE: "{DB_USERS_ROOT}" FOUND')
        # If the path does not exist, print a message with the level 1 (alert) and the database name
        case False:
            message("1", f'USERS DATABASE: "{DB_USERS_ROOT}" NOT FOUND')
            # Use the open function with the "x" mode to create a new file for the database
            open(DB_USERS_ROOT, "x")
            # Print a message with the level 2 (success) and the database name
            message("2", f'USERS DATABASE: "{DB_USERS_ROOT}" CREATED')
    # Use the sqlite3 module to connect to the database and get a cursor object
    connection = sqlite3.connect(DB_USERS_ROOT)
    cursor = connection.cursor()
    try:
        # Try to execute a SQL query to select userID records from the users table
        cursor.execute("""SELECT userID FROM users; """).fetchall()
        # If the query succeeds, print a message with the level 6 (informational) and the table name
        message("6", f'TABLE: "Users" FOUND IN "{DB_USERS_ROOT}"')
        # Close the connection to the database
        connection.close()
    except:
        # If the query fails, print a message with the level 1 (alert) and the table name
        message("1", f'TABLE: "Users" NOT FOUND IN "{DB_USERS_ROOT}"')
        # Define a SQL statement to create the users table with the specified columns and constraints
        usersTable = """
        CREATE TABLE IF NOT EXISTS Users(
            "userID"	INTEGER NOT NULL UNIQUE,
            "userName"	TEXT UNIQUE,
            "email"	TEXT UNIQUE,
            "password"	TEXT,
            "profilePicture" TEXT,
            "role"	TEXT,
            "points"	INTEGER,
            "timeStamp"	INTEGER,
            "isVerified"	TEXT,
            PRIMARY KEY("userID" AUTOINCREMENT)
        );"""
        # Execute the SQL statement to create the table
        cursor.execute(usersTable)
        # Check if the DEFAULT_ADMIN constant is True
        match DEFAULT_ADMIN:
            # If True, create a default admin account with the specified values
            case True:
                # Hash the DEFAULT_ADMIN_PASSWORD using the encryption module
                password = encryption.hash(DEFAULT_ADMIN_PASSWORD)
                # Execute a SQL query to insert the default admin account into the users table
                cursor.execute(
                    """
                    INSERT INTO Users(userName,email,password,profilePicture,role,points,timeStamp,isVerified) \
                    values(?,?,?,?,?,?,?,?)
                    """,
                    (
                        DEFAULT_ADMIN_USERNAME,
                        DEFAULT_ADMIN_EMAIL,
                        password,
                        DEFAULT_ADMIN_PROFILE_PICTURE,
                        "admin",
                        DEFAULT_ADMIN_POINT,
                        currentTimeStamp(),
                        "True",
                    ),
                )
                # Commit the changes to the database
                connection.commit()
                # Print a message with the level 2 (success) and the default admin username
                message(
                    "2",
                    f'ADMIN: "{DEFAULT_ADMIN_USERNAME}" ADDED TO DATABASE AS INITIAL ADMIN',
                )
        # Commit the changes to the database
        connection.commit()
        # Close the connection to the database
        connection.close()
        # Print a message with the level 2 (success) and the table name
        message("2", f'TABLE: "Users" CREATED IN "{DB_USERS_ROOT}"')


# This function checks if the posts table exists in the database, and creates it if it does not.
def postsTable():
    """
    Checks if the posts table exists in the database, and creates it if it does not.

    Returns:
        None
    """
    # Use the exists function to check if the DB_POSTS_ROOT constant is a valid path
    match exists(DB_POSTS_ROOT):
        # If the path exists, print a message with the level 6 (informational) and the database name
        case True:
            message("6", f'POSTS DATABASE: "{DB_POSTS_ROOT}" FOUND')
        # If the path does not exist, print a message with the level 1 (alert) and the database name
        case False:
            message("1", f'POSTS DATABASE: "{DB_POSTS_ROOT}" NOT FOUND')
            # Use the open function with the "x" mode to create a new file for the database
            open(DB_POSTS_ROOT, "x")
            # Print a message with the level 2 (success) and the database name
            message("2", f'POSTS DATABASE: "{DB_POSTS_ROOT}" CREATED')
    # Use the sqlite3 module to connect to the database and get a cursor object
    connection = sqlite3.connect(DB_POSTS_ROOT)
    cursor = connection.cursor()
    try:
        # Try to execute a SQL query to select id records from the posts table
        cursor.execute("""SELECT id FROM posts; """).fetchall()
        # If the query succeeds, print a message with the level 6 (informational) and the table name
        message("6", f'TABLE: "Posts" FOUND IN "{DB_POSTS_ROOT}"')
        # Close the connection to the database
        connection.close()
    except:
        # If the query fails, print a message with the level 1 (alert) and the table name
        message("1", f'TABLE: "Posts" NOT FOUND IN "{DB_POSTS_ROOT}"')
        # Define a SQL statement to create the posts table with the specified columns and constraints
        postsTable = """
        CREATE TABLE "posts" (
            "id"	INTEGER NOT NULL UNIQUE,
            "title"	TEXT NOT NULL,
            "tags"	TEXT NOT NULL,
            "content"	TEXT NOT NULL,
            "banner"	BLOB NOT NULL,
            "author"	TEXT NOT NULL,
            "views"	INTEGER,
            "timeStamp"	INTEGER,
            "lastEditTimeStamp"	INTEGER,
            "category"	TEXT NOT NULL,
            PRIMARY KEY("id" AUTOINCREMENT)
        );"""
        # Execute the SQL statement to create the table
        cursor.execute(postsTable)
        # Commit the changes to the database
        connection.commit()
        # Close the connection to the database
        connection.close()
        # Print a message with the level 2 (success) and the table name
        message("2", f'TABLE: "Posts" CREATED IN "{DB_POSTS_ROOT}"')


# This function checks if the comments table exists in the database, and creates it if it does not.
def commentsTable():
    """
    Checks if the comments table exists in the database, and creates it if it does not.

    Returns:
        None
    """
    # Use the exists function to check if the DB_COMMENTS_ROOT constant is a valid path
    match exists(DB_COMMENTS_ROOT):
        # If the path exists, print a message with the level 6 (informational) and the database name
        case True:
            message("6", f'COMMENTS DATABASE: "{DB_COMMENTS_ROOT}" FOUND')
        # If the path does not exist, print a message with the level 1 (alert) and the database name
        case False:
            message("1", f'COMMENTS DATABASE: "{DB_COMMENTS_ROOT}" NOT FOUND')
            # Use the open function with the "x" mode to create a new file for the database
            open(DB_COMMENTS_ROOT, "x")
            # Print a message with the level 2 (success) and the database name
            message("2", f'COMMENTS DATABASE: "{DB_COMMENTS_ROOT}" CREATED')
    # Use the sqlite3 module to connect to the database and get a cursor object
    connection = sqlite3.connect(DB_COMMENTS_ROOT)
    cursor = connection.cursor()
    try:
        # Try to execute a SQL query to select id records from the comments table
        cursor.execute("""SELECT id FROM comments; """).fetchall()
        # If the query succeeds, print a message with the level 6 (informational) and the table name
        message("6", f'TABLE: "Comments" FOUND IN "{DB_COMMENTS_ROOT}"')
        # Close the connection to the database
        connection.close()
    except:
        # If the query fails, print a message with the level 1 (alert) and the table name
        message("1", f'TABLE: "Comments" NOT FOUND IN "{DB_COMMENTS_ROOT}"')
        # Define a SQL statement to create the comments table with the specified columns and constraints
        commentsTable = """
        CREATE TABLE IF NOT EXISTS comments(
            "id"	INTEGER NOT NULL,
            "post"	INTEGER,
            "comment"	TEXT,
            "user"	TEXT,
            "timeStamp"	INTEGER,
            PRIMARY KEY("id" AUTOINCREMENT)
        );"""
        # Execute the SQL statement to create the table
        cursor.execute(commentsTable)
        # Commit the changes to the database
        connection.commit()
        # Close the connection to the database
        connection.close()
        # Print a message with the level 2 (success) and the table name
        message("2", f'TABLE: "Comments" CREATED IN "{DB_COMMENTS_ROOT}"')
