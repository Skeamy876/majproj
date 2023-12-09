## Book Exchange System


# Might Need to download and install postgres locally for the application

How to Run: 
1. Download python https://www.python.org/downloads/ 
2. Clone Reposiitory 
 ```
 git clone https://github.com/your-username/majproj-BookExchange.git
 ```
3. Create a virtual environment
    ```
    python -m venv [name of env here]

    ```
5. Activate environment
    
    windows:

    ```
    [name of env here]\Scripts\activate

    ```
    linux/macos
    ```
    [name of env here]\bin\activate

    ```


7. Intall Dependencies, 
    ```
    python install -r requirements.txt
    ```

8. Download or set up posgres using docker. Then create database and edit required details for the database in your setting.py file

9. Prepare migrations and runserver
    ```
    python manage.py makemigrations

    python manage.py migrate

    python manage.py createsuperuser

    python manage.py runserver
    ```

10. Register and Enjoy!! PS. you will need to create other users and add books for them to see the prototype functionality. :smile:


