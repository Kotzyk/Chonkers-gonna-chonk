[![Pylint](https://github.com/J-emi/Chonkers/actions/workflows/pylint.yml/badge.svg)](https://github.com/J-emi/Chonkers/actions/workflows/pylint.yml)
# Chonkers gonna chonk
### Video Demo:  <https://youtu.be/ROvkdhQFTQI>
### Description:

<p align="center"> <img src="https://i.imgur.com/YftE9Vo.png"> </p>
  
#### Introduction
Chonker is a colloquial term for a fat but photogenic cat. I have made a website that allows the user to assess the thickness of the cats in the photos according to a six-point scale. It is a form of fun and a reference to [internet memes](https://knowyourmeme.com/memes/chonk-oh-lawd-he-comin). That being said, I do not support fattening animals on purpose, by malnutrition or negligence. This web-based application was created as a final project for [Harvard CS50x 2021](https://cs50.harvard.edu/x/2021). It shows the skills I acquired during the course.


#### Technologies
The application was written in **Python 3.10.1** using **Flask 2.0.2** framework. The files have been placed in directories according to the MVC design pattern:

 * ***/templates*** - contains all files used to create final HTML.
 * ***/static*** - contains CSS style sheet (styles.css), jquery file helpful to display small messages to users (e.g. validation of password confirmation) and two subdirectories. In the first one /UI you may find elements of User Interface like logo of website and the chart which is a visual aid to assess fatness of cats. Second subdirectory /cats contains 151 different images of cats, which user may rate.
 * ***app.py*** - contains all python code for web server.
 * ***chonkers.db*** - it is database created using **sqlite3**. It consists of two tables. In the first one (Users), the login details are saved. The second table (Ratings) is used to create ratings - how many photos the user has rated.

 Layout responsiveness was obtained using a CSS Gird and relative units. The logo and colors of the website have been designed by myself. 

  
 #### Setup
To run this project, assuming you have a [Python interpreter](https://www.python.org/downloads/) already installed, you install it locally and run using Flask:
```
$ cd chonkers
$ pip install -r requirements.txt
$ flask run
```
 
 #### How does my site work?
Upon entering the website, the user may register (*Register* tab), which is recommended but not necessary. Unregistered users can rate cats, but they will not be included in the ranking (*Leaderboard* tab). All you need to register is a username and password. You can change your password at any time (*Change password* tab). A registered user can log in (*Log in* tab). Images of cats are displayed randomly on the main page, without repetition. Under the image there is chart of cat body-fat indexes. The user can decide which category the cat in the photo belongs to:
 - A Fine Boi, 
 - He Chomnk,
 - A Heckin' Chonker,
 - H E F T Y C H O N K, 
 - M E G A C H O N K E R,
 - OH LAWD HE COMIN. 

 After voting, two pieces of information are displayed instead of the chonk chart - users vote and community raiting. The ranking (*Leaderboard* tab) includes the ten users who rated the highest number of photos. In case of an error on the website, a relevant apology message is displayed.
