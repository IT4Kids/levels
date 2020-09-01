import os
import time
import json
from urllib.parse import urlparse
from selenium import webdriver
import pathlib

pathlib.Path('screenshots').mkdir(parents=True, exist_ok=True) 

summary = json.loads(open('summary.json').read())

urls = map(lambda level: 'https://raw.githubusercontent.com/IT4Kids/levels/master/Templates/' + str(level), [level['filename'] for level in summary if level['template_exists']])

driver = webdriver.Chrome()

count = 0
for url in urls:
	a = urlparse(url)
	base = os.path.basename(a.path)
	driver.get('https://editor.it-for-kids.org/?level=' + url)
	while driver.execute_script('return document.readyState;') != 'complete':
		time.sleep(0.1)
	time.sleep(1)
	image = driver.find_elements_by_css_selector('#pixi-app-container canvas')[0].screenshot_as_png
	f = open('./screenshots/' + base + '.png', 'w+b')
	f.write(image)
	f.close()
	count += 1

driver.close()
