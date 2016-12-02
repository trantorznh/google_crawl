
## Google image crawler 
Using the google image search engines obtains the image url by controlling the chrome.

It modified from pisces[https://github.com/wolfhong/pisces]. Thanks for their job. Our work break the limit of query frequency and add the time limit as google's image search engine.


## Example

if __name__ == '__main__':
    # image search keyword: kitchen fire
    name_test = u'glasses'
    basetime_test = datetime.datetime(2009, 1, 1)
    endtime_test = datetime.datetime(2016, 6, 1)
    day_delta_test = 5
    last_end_test = 1
    main(name_test, basetime_test, endtime_test, day_delta_test, last_end_test, close=True)




## Tip
- The code uses selenuim. Selenium Python bindings provides a simple API to write functional/acceptance tests using Selenium WebDriver. More info to see http://selenium-python.readthedocs.io/installation.html
- tools/chromedriver is only for chrome, to see http://chromedriver.storage.googleapis.com/index.html for more info.

