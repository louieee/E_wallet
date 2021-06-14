<h1>Project Description</h1>
<p>This project is an E-Wallet System</p>

<h2>Project Setup</h2>
<ul>
<li>Clone Project</li>
<li> open your terminal and type <code>pip install -r requirements.txt</code> to install all the project library requirements</li>
<li>Then on the terminal type <code>python manage.py makemigrations</code> to migrate the database model changes onto your db</li>
<li>Then type <code>python manage.py migrate</code> This updates your database schema based on the migration changes.</li>
<li> Then type <code>python manage.py createsuperuser</code> This allows you to create an Admin, so fill up all required fields.</li>
<li>Finally, type <code>python manage.py runserver localhost:8000</code> This starts up the django server, so visit <code>localhost:8000</code> on your browser to view the site.</li>
<li>To view the admin dashboard, visit <code>localhost:8000/admin</code>, then login with the created admin login details and you're in. Voila !</li>
</ul>