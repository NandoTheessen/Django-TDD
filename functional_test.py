from selenium import webdriver

# mere has heard of a nice website that she'd like to take a 
# look at, she opens her browser!
browser = webdriver.Firefox()

# She opens the homepage
browser.get('http://localhost:8000')

# and notices that the header mentions a todo list!
assert 'To-Do' in browser.title

# shes invited to enter a to-do item right away

# she enters "Buy new ink" as todo item & when she hits enter the page
# updates and displays a list with one item: 
# 1: Buy new Ink

# She still has the ability to enter text into the text box
# She enters "Take out the trash" as her second item

# After pressing enter, the page updates and a second item shows up:
# 2: Take out the trash

# She wonders if her items will be saved, she sees that the site
# has generated a unique URL for her & there is some explanatory text 
# to that effect

# She visits said URl, her todo list is still there 

# she closes the browser

browser.quit()