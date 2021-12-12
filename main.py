from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import unittest
import pprint
import json

address = "https://en.wikipedia.org/wiki/Software_metric"
driver_path = "C:/Users/psolo/Desktop/metrix/geckodriver.exe"
RANGE=10

class TestResults(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=driver_path)
        self.wait = WebDriverWait(self.driver, 10)
        self.address = address

    def test_open_page(self):
        csv_content_count={}
        csv_content_duration = {}
        for i in range(RANGE):
            res = self.driver.get(address)
            #print("RESULT", self.driver.current_url, dir(self.driver))
            self.assertIn(self.address, self.driver.current_url)
            script = "return window.performance.getEntries();"
            perf = self.driver.execute_script(script)
            #print(perf)
            for curr in perf:
                if 'https:' not in curr['name']:
                    continue
                if csv_content_count.get(curr['name'], None):
                    csv_content_count[curr['name']] += 1
                else:
                    csv_content_count[curr['name']] = 1
                csv_content_duration[curr['name']] = csv_content_duration.get(curr['name'], 0) + curr['duration']

        #pprint.pprint(perf)

        dict_for_json = {}
        id = 0
        for key, value in csv_content_duration.items():
            dict_for_json[f'{id}'] = {'name': key, 'duration': round(value / csv_content_count[key])}
            id+=1

        with open("result_perf.json","w") as fh:
            json.dump(dict_for_json, fh, indent=1)
        with open("result_perf.json", "r") as fh:
            res = json.load(fh)
        print(json.dumps(res,  indent=4))

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()