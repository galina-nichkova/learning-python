# Web Scraping

This programm does the following:
1. sends a get request with some filter criteria to the immobilienscout24 page
2. fetches the content of the response
3. parses HTML to get required details on each apartment offer
4. writes the data from 3. into a local sqlite database

It can be called from command line.
Unit test a located in the separate folder.
