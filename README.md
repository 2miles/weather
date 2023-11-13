# Weather app

## This is a simple weather app created using Django.

A user first signs up and or logs in using their email. Then they can enter city name to create a list of weather data for each city entered. The user can then click on any of cities in the list do display a more detailed view of the weather in that city. The more detailed view gives the weather for the next two days in 3hr increments with each increments color corresponding to the temperature for that time period.

# Notes

I created this project purely as a learning experience. Here is a list of some of the things I became familiar with along the way.

- How Django works and how a Django project is structured.
- How APIs work and how to get data from them and present them to the user.
- Using Bootstrap5 classes
- User authentication in Django
- Email validation with SendGrid
- Forms in Django with Crispy Forms

# How to run

### 1. Clone the repository

```
git clone <repository_url>
```

### 2. **Set Up a Virtual Environment**

Once inside the project folder, create a virtual environment.

```
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

```
source venv/bin/activate
```

### 4. Install Dependencies

With the virtual environment active, install the project dependencies listed in the requirements.txt file:

```
pip install -r requirements.txt
```

### 5. Create a .env file

Create a file in the root directory of the project named `.env`

```
DEBUG=True
SECRET_KEY=<your_secret_key>
API_KEY=<your_open_weather_api_key>
```

### 5. Run Migrations

Run database migrations to set up the database schema for the project. Django migrations handle the creation of database tables and other necessary structures:

```
python manage.py migrate
```

After running this command, a Django-supported SQLite3 file will be created. This file will serve as your custom database.

### 6. Create a Superuser (optional)

The superuser has access to the Django admin panel. Here you can manage the users and data.

```
python manage.py createsuperuser
```

### 7. Start the Development Server

Finally, start the Django development server. This command launches the project locally, allowing you to explore its features in your web browser.

```
python manage.py runserver
```

### 8. Access the Project

Open your web browser and go to http://localhost:8000/ to see the Django project.

If you created a superuser, access the admin interface at http://localhost:8000/admin/.
