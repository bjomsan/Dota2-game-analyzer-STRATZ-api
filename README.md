# Dota2-game-analyzer-STRATZ-api

In this project I have used the STRATZ API (https://stratz.com/api) to gather information and some basic analysis on Dota 2 games of a specific account.
This is created as a web-application that runs on Flask with python/sqlite/html&css. In the repository, I have included a short video, demonstrating how the application works as well as some images. <br> <br>
For now, the database does not have any ways to auto-update itself when there is new dota2 update/patch. For the database to update, run the file create_database.py. This will overrite the existing and making the complete database updated with the newest data from the api. <br> <br>
!NB! to run the program you need a token from stratz.com/api in the call_database_data.py file

## Files/folders Overview:

- **app.py:** run this file to start the Flask web-application
- **views.py:** contains all the different views/html-pages and manages what data to send to each page <br> <br>

- **datagathering:** Folder with all backend python scripts for gathering and processing data from STRATZ API
   - **accountData.py:** call api for account-data and filter out data that is not needed.
   - **filt_hero.py:** seperate file for hero data, filter out data that is not needed
   - **call_database_data.py:** file with all api calls for the database
   - **create_database.py:** takes the responses from call_database_data.py and create database
   - **match_grids.py:** generated grids of networth/experience lead in specific game
   - **match_data.py:** gathers data on recent matches of account and modifies the data
   - **dota.db:** database with tables: hero, items, region, patchnotes, lobbytype, gamemode, gameversion<br> <br>

- **static:** Folder with all statics, css files and images.
   - **css:** 
       - **base.css:** base css file used on all pages
       - **home_styles.css:** styles for homepage 
       - **accOverview_styles.css:** styles for overview page 
       - **match_details.css:** styles for match analysis page
   - **images:** Folder with images for the webpage such as linkedin/github-logos
       - **grid_images:** Folder with images of networth/experience. (the folder is cleared in views.py every time a new match is loaded) <br> <br>
    
- **templates:** Folder with all html files 
   - **home.html:** homepage
   - **account_overview.html:** account overview page
   - **match_details.html:** match analysis page
 
- **demos:** Folder with a video demo of the application + images of the pages <br> <br>


### Possibilities for further development and improvement:
Most of the data in the database is not beein used currently. For further development it would be possible to both make the analysis more comprenensive, include more than 10 most recent games and some general analysis of the different heroes (e.g find hero with best stat-gains/movement-speed/base damage etc). At the moment the database is NOT normalized, which should also be concidered in future development. Making an even better UX/UI with better coding for different devices and screen sizes is also on the list. 


# Image gallery
![accountOverview_demo](https://github.com/bjomsan/Dota2-game-analyzer-STRATZ-api/assets/124776049/626da49c-dd06-48e1-882f-e8de32c29655) <br> <br>
![matchinfo_demo](https://github.com/bjomsan/Dota2-game-analyzer-STRATZ-api/assets/124776049/23a0245f-c982-4b6c-8aff-d79c94d65f2d)
