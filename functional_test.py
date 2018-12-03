from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # mere has heard of a nice website that she'd like to take a 
        # look at, she opens her browser!

        # She opens the homepage
        self.browser.get('http://localhost:8000')

        # and notices that the header mentions a todo list!
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # shes invited to enter a to-do item right away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # she enters "Buy new ink" as todo item & when she hits enter the page
        # updates and displays a list with one item: 
        # 1: Buy new Ink
        inputbox.send_keys('Buy new ink')
        inputbox.send_keys(Keys.Enter)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertTrue(
            any(row.text == '1: Buy new ink' for row in rows)
        )

        # She still has the ability to enter text into the text box
        # She enters "Take out the trash" as her second item
        self.fail('Finish the test!')

        # After pressing enter, the page updates and a second item shows up:
        # 2: Take out the trash

        # She wonders if her items will be saved, she sees that the site
        # has generated a unique URL for her & there is some explanatory text 
        # to that effect

        # She visits said URl, her todo list is still there 

        # she closes the browser


if __name__ == '__main__':
    unittest.main(warnings='ignore')
