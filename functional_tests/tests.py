import time
import unittest
from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn('foo', [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)



    def test_can_start_a_list_and_retrieve_it_later(self):
        # mere has heard of a nice website that she'd like to take a 
        # look at, she opens her browser!

        # She opens the homepage
        self.browser.get(self.live_server_url)

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
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)


        #self.assertTrue(
            #any(row.text == '1: Buy new ink' for row in rows),
            #f"New to-do item did not appear in table. Contents were:\n{table.text}"
        #)

        self.wait_for_row_in_list_table('1: Buy new ink')
        

        # She still has the ability to enter text into the text box
        # She enters "Take out the trash" as her second item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Blue should be very fitting!')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # After pressing enter, the page updates and a second item shows up:
        # 2: Take out the trash
        self.wait_for_row_in_list_table('1: Buy new ink')
        self.wait_for_row_in_list_table('2: Blue should be very fitting!')

        # She wonders if her items will be saved, she sees that the site
        # has generated a unique URL for her & there is some explanatory text 
        # to that effect
        self.fail('Finish the test!')

        # She visits said URl, her todo list is still there 

        # she closes the browser
