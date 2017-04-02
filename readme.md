# Chat App
This is a back end implement of chat application.

## Prerequisites
- python 2 or python 3
- mysql

## Set up Environment
Flask and Flask-SQLAlchemy
- ```pip install -r requirements.txt```

Create a new mysql database with name "chat"
- ```mysql> CREATE DATABASE chat;```

Modify SQLALCHEMY_DATABASE_URI at app.py
Following format:
```
mysql://username:password@host:port/database
```


## API
- ```POST /signup```
  ```
  Body:
        form-data:
            |user_name : _user_name
            |password : _password
            |  
  ```

  Create User:
  Takes a username and password and creates a new user in a persisted data store.

- ```POST /send```
  ```
  Body:
      form-data:
          |sender_id : _sender_id
          |recipient_id : _recipient_id
          |body : _body
          |type : _type
  ```

  Send Message: Takes a sender, recipient, and message and saves that to the data store. Three different message types are supported.
  -  basic text-only message.
  -  image link.
  -  video link.

- ```GET /fetch```
    ```
        parameters:
            |sender_id : _sender_id
            |recipient_id : _recipient_id
            |-------------------
            |#optional
            |numperpage : _numperpage
            |page : _page
    ```

    Fetch Messages:
    Takes two users and loads all messages sent between them.
    Two optional parameters: the number of message to show per page and which page to load.

## Schema
Four tables are created for this application.
- User Table
  ```
  |id           :   Integer       #primary_key
  |user_name    :   String(50)
  |password     :   String(50)
  ```

- Message Table
  ```
  |id           :    Integer       # primary_key
  |sender_id    :    Integer
  |recipient_id :    Integer
  |body         :    Text
  |type         :    String(5)
  |send_date    :    timeStamp
  ```

- Image Table
  ```
  |message_id   :    Integer     # primary_key
  |width        :    Integer
  |height       :    Integer
  ```

- Video Table
  ```
  |message_id   :    Integer     # primary_key
  |length       :    Integer
  ```
