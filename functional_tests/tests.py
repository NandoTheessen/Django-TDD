import os
import time
import unittest
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
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

        # self.assertTrue(
        # any(row.text == '1: Buy new ink' for row in rows),
        # f"New to-do item did not appear in table. Contents were:\n
        # {table.text}")

        self.wait_for_row_in_list_table('1: Buy new ink')

        # She still has the ability to enter text into the text box
        # She enters "Take out the trash" as her second item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Blue should be very fitting!')
        inputbox.send_keys(Keys.ENTER)

        # After pressing enter, the page updates and a second item shows up:
        # 2: Take out the trash
        self.wait_for_row_in_list_table('1: Buy new ink')
        self.wait_for_row_in_list_table('2: Blue should be very fitting!')

        # Satisfied she goes to bed

    def test_layout_and_styling(self):
        # Eidth goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # she notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # She notices that her list has a unique URL
        edits_list_url = self.browser.current_url
        self.assertRegex(edits_list_url, '/lists/.+')

        # Now a new user, Francis, comes along to the site

        # We use a new browser session to make sure that no information
        # of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page, there is no sign of previous lists
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list bx yentering a new item
        # He is less intresting than Edith
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis get's his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(edits_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edits_list_url)

        # No trace of Edith's list?
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # satisfied both go back to bed
