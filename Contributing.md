<!DOCTYPE html>
<html>
<body>

<h1>CloudProvisioner</h1>

<h2>Setting Up the Project Locally</h2>

<h3>Prerequisites</h3>
<ul>
    <li>Ensure you have Python version 3.12.0 installed on your system.</li>
    <li>Make sure you have <code>git</code> installed on your system.</li>
    <li>If you don't have <code>virtualenv</code> already installed, you can install it using <code>pip</code> (Python package manager).</li>
</ul>

<h3>Installation Steps</h3>

<ol>
    <li><strong>Fork the Repository</strong><br>
        Click the "Fork" button on the top-right corner of this GitHub repository to create a fork in your own GitHub account.
    </li>
    <br>
    <li><strong>Clone your Forked Copy</strong><br>
        Clone your forked copy of the repository to your local machine using the following command:<br>
        <code>git clone https://github.com/&lt;your-username&gt;/cloudprovisioner.git</code>
    </li>
    <br>
    <li><strong>Navigate to the Project Directory</strong><br>
        Change your current directory to the project folder:<br>
        <code>cd cloudprovisioner/</code>
    </li>
    <br>
    <li><strong>Create a New Branch</strong><br>
        Create a new branch to work on your changes. Replace &lt;branch-name&gt; with a descriptive branch name of your choice:<br>
        <code>git checkout -b &lt;branch-name&gt;</code>
    </li>
    <br>
    <li><strong>Create a Virtual Environment</strong><br>
        If you don't have <code>virtualenv</code> installed, you can install it using <code>pip</code>:<br>
        <code>pip install virtualenv</code><br>
        Next, create a new virtual environment in the project folder:<br>
        <code>virtualenv env</code>
    </li>
    <br>
    <li><strong>Activate the Virtual Environment</strong><br>
        - For Linux/Unix OS:<br>
        <code>source env/bin/activate</code><br>
        - For Windows OS:<br>
        <code>env\Scripts\activate</code>
    </li>
    <br>
    <li><strong>Install Project Dependencies</strong><br>
        Install the project's dependencies listed in the <code>requirements.txt</code> file:<br>
        <code>pip install -r requirements.txt</code>
    </li>
    <br>
    <li><strong>Apply Migrations</strong><br>
        Make migrations for the project and apply them to the database:<br>
        <code>python manage.py migrate</code>
    </li>
    <br>
    <li><strong>Run the Development Server</strong><br>
        Start the development server by running the following command:<br>
        <code>python manage.py runserver</code><br>
        Your Cloud Provisioner project should now be running locally. You can access it in your web browser at <a href="http://localhost:8000">http://localhost:8000</a>.
    </li>
    <br>
    <li><strong>You're Good to Go!</strong><br>
        Congratulations! You have successfully set up the Cloud Provisioner project locally.<br>
    </li>
</ol>

</body>
</html>
