# Catalog Application
>Eric Brousseau

# About

The catalog application gathers information from the provided database of categories
and presents them to the user. The apps interface is easy to understand and has an intuitive
use. Most of the code has been repurposed from Udacity's oauth2 and CRUD courses.
Rotten tomatoes was used for the film descriptions and Esquire was used for the
book descriptions in the database information.

### Setup
1. Install Vagrant [You can download it from vagrantup.com.](https://www.vagrantup.com/downloads)
2. Install VirtualBox [You can download it from virtualbox.org.](https://www.virtualbox.org/wiki/Downloads)
2. Install python 3.x.x [You van download it from python.org](https://www.python.org/downloads/)
3. Unzip or clone this repository

### To Run
1. Launch Git Bash or similar shell program  
2. CD into the project directory  
3. Run `vagrant up` to launch VirtualBox  
4. Then run `vagrant ssh` to login  
5. run `pip install -r requirements.txt` to ensure app runs smoothly
6. CD into the project directory
7. Initiate the database by using the command `python database_setup.py`
8. Fill the database with the command `python filldatabase.py`
9. Use command `python project.py` to run the program  
10. Visit *http://localhost:5000* to launch app
