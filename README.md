## QA Application

### Steps to run app

1. Take a git clone of this rep: https://github.com/Akash3194/QA_Application.git
2. Make sure docker is installed in your system
3. change to QA_Application directory: `cd QA_Application`
4. run: `docker-compose up --build -d`
5. now go to `http://127.0.0.1:8000/docs`, Here you will find the api documentation and you can use the api's as well.

### Note:
1. Any actual machine learning models are not used, Only API's are created for showcasing backend skills.
2. Due to very small project size, code is directly pushed to git master, without following multiple branch development process. 

### Improvements:
1. Postgresql data is not persisted as of now due to time bandwidth issue. It can be added.
2. Logs are not stored in any specific files, you will just find them in `docker logs`.