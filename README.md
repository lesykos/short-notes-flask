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

### To Do
1. 
