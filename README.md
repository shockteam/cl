# Search Craigslist by Multiple CA Regions

Search all or few CA craiglist regions at once

-----------------------

### Installation Instructions (Mac OS)

Install required packages:

    sudo easy_install pip 
    sudo pip install pyCLI
    cd ~/Desktop
    git clone https://github.com/shockteam/cl.git
    cd cl

### Usage examples

To generate HTML page with links to craigslist ads with 'ducati' subject in Bay Area and San Diego areas:

    ./craigslist_search.py -r 'sfbay,sandiego' -k ducati > ducs.html

To open this page in your browser: File > Open File > Desktop > ducs.html

To generate HTML page with links to craigslist ads with 'S1000RR' subject in all California locations:

    ./craigslist_search.py -r all -k s1000rr > bimmers.html

To open this page in your browser: File > Open File > Desktop > bimmers.html
