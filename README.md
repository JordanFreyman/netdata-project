# Resource Radar

## Overview

Resource Radar is a Flask-based web application designed to help users efficiently manage and track resources. It supports user authentication via Google OAuth and provides an admin panel for managing users. This guide is designed for beginners, particularly undergraduate students, and explains each module in detail.

## Project Structure

```
cop4521-flask/
├── LICENSE
├── README.md
├── app
│   ├── __init__.py
│   ├── admin.py
│   ├── auth.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/dashboard.js
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── login.html
│       ├── manage_users.html
│       └── unauthorized.html
├── config.py
├── pyproject.toml
├── requirements.txt
├── run.py
```

## Files and Directories

- `app`: Contains the main application code.
  - `__init__.py`: Initializes the Flask app, sets up extensions, and registers blueprints.
  - `admin.py`: Configures Flask-Admin, which provides an admin interface for managing users.
  - `auth.py`: Handles user authentication via Google OAuth, including login and logout routes.
  - `models.py`: Defines the database schema, including the `User` model.
  - `routes.py`: Defines the main application routes, such as the dashboard and user management views.
  - `static/`: Contains static files such as CSS and JavaScript for styling and interactivity.
  - `templates/`: Contains HTML templates used to render pages dynamically.
- `config.py`: Stores configuration settings such as database URI and authentication credentials.
- `requirements.txt`: Lists the dependencies required to run the project.
- `run.py`: Entry point for running the Flask application.

## Getting Started

### Prerequisites

Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

### Installation

1. Fork the repository and clone it:
   ```bash
   git clone https://gitlab.com/yourusername/cop4521-flask.git
   ```
2. Navigate to the project directory:
   ```bash
   cd cop4521-flask
   ```
3. Create a virtual environment:
   ```bash
   /opt/python3/bin/python3.13 -m venv venv
   source venv/bin/activate
   ```
   `/opt/bin/python3.13` is the python you have installed in your server. However, you might have python installed at another location in your own computer, so specify python accordingly.

> The rest of the steps assumes your python venv has been correctly activated.

4. Install pip using ensurepip (if you don't have pip already installed).
   ```bash
   python3 -m ensurepip
   ```
   
6. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

## Setting Up Google Authentication Credentials

To enable Google authentication:

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project. You can do this from top left where it says **Select a Project.** If you already have a project, your project name will be in place of **Select a Project.**
3. In **APIs & Services > Oauth consent screen** setup the details of your app. Make sure you set your **Audience** as **External**.
4. Go to **APIs & Services > Credentials** and click on Create credentials, and create **OAuth Client ID**.
5. Make sure the Application type is **Web Application** and the Authorized redirect URIs is set as ```http://127.0.0.1:8000/callback```
6. This creates an Oauth2.0 application, which you can open to see the **Client ID** and **Client Secret**.
7. Create a `.env` file in the project root (the base project folder) and add following credentials. Make sure you replace your-client-id and your-client-secret with the keys given by Oauth2.0.
   ```bash
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   SECRET_KEY=unique-flask-app-identifier
   ```
> To generate the unique flask app identifier, you can do the following in the terminal. There might be other ways of doing the same.
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Database Migrations

Since the project uses Flask-Migrate, you need to initialize and apply database migrations when making changes to the schema.

1. Initialize migrations (only needed the first time):
   ```bash
   flask db init
   ```
2. Generate a migration script whenever the database schema changes:
   ```bash
   flask db migrate -m "Describe changes here"
   ```
3. Apply the migration to update the database:
   ```bash
   flask db upgrade
   ```

## Usage

To run the application, execute:

```bash
python run.py
```
Open the link shown in the terminal (usually http://127.0.0.1:8000) to see your Flask app.
If it's running on a different port (e.g. http://localhost:5000), make sure your callback URL matches it, like http://localhost:5000/callback.

Also, add https://yourwebsite.me/callback to the callback list so it works online too.

## Managing Users via Flask Shell
Now you’ll see a Login with Google button.
If you log in, you’ll probably get an Unauthorized message.
That’s because your app doesn’t know who you are yet—your email isn’t in the database.

To manually add a user to the database, in your terminal:

1. Open the Flask shell:
   ```bash
   flask shell
   ```
2. Import the necessary modules:
   ```python
   from app.models import db, User
   ```
3. Create and add a user:
   ```python
   user = User(username="new_username", email="youremail@gmail.com", type="Admin")
   db.session.add(user)
   db.session.commit()
   ```
Once your email is added, Google verifies you, and the app lets you in as admin.
To add more users, just use the Manage Users link in the app.
## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or suggestions, open an issue or contact the project maintainer at [prms.regmi@gmail.com](mailto\:prms.regmi@gmail.com).
=======
# project3



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/topics/git/add_files/#add-files-to-a-git-repository) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/cop45219911608/project3.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.com/cop45219911608/project3/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/user/project/merge_requests/auto_merge/)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
>>>>>>> 8b28109313aa807c52943c1629b4e803fd26ae40
