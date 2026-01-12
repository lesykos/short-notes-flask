# Short Notes App

- The Flask application lives inside a package named **app**.
- **notes.py** defines the Flask application instance.
- config.py stores the configuration settings.

### Start the project:

1. `python -m venv venv`
2. `.\venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. Create `.env` file
5. Run the project:
`flask --app notes run --debug`
6. Open website on `127.0.0.1:5000`


### .env file:
```
DEBUG=True
ADMIN_NAME=
SECRET_KEY=
SUPABASE_URL=
SUPABASE_KEY=
```

### Routes:
```
Endpoint      Methods    Rule
------------  ---------  -----------------------
main.index    GET        /
auth.login    GET, POST  /auth/login
auth.logout   GET        /auth/logout
notes.new     GET, POST  /notes/new
notes.edit    GET, POST  /notes/edit/<int:id>
notes.show    GET        /notes/<int:id>
notes.delete  GET        /notes/delete/<int:id>
tags.index    GET        /tags/
tags.show     GET        /tags/<string:tag>
```
