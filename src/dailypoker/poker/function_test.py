from selenium import webdriver
import unittest

# browser = webdriver.Chrome()
# browser.get('http://localhost:8000')
#
# assert 'Poker' in browser.title

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        ## wait 3 seconds before testing
        # self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):

        self.browser.get('http://localhost:8000')
        self.assertIn('Poker', self.browser.title)
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
