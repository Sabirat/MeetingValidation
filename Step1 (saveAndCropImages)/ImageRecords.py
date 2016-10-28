from selenium import webdriver
import MySQLdb, sys
import string
import random
from PIL import Image

conn = MySQLdb.connect (host = "localhost",user = "root", passwd = "",db = "AAMeetings")
cursor = conn.cursor()


def rand_generator(size=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def LoadPageAndTakeScreenShot():
	cursor.execute("SELECT distinct meetingurl from meetinginformation limit 1")
	data = cursor.fetchone()[0]
	cursor.execute("SELECT * from meetinginformation where meetingurl= %s",data)
	
	contents=[]
	for i in range(cursor.rowcount):
		ms = cursor.fetchone()
		contents.append(ms)
		
	if data is None:
		return None
	else:
		browser	= webdriver.PhantomJS("D:\Research\phantomjs.exe")
		elements=[]
		browser.get(data)
				
		alldict={}
		for row in contents:
			tagtofind=row[11]
			if alldict.get(tagtofind) is None:
			
				elemdict={}
				info_elems=browser.find_elements_by_tag_name(row[11])
				for elem in info_elems:
					outerhtml=filter(lambda x: x in string.printable, elem.get_attribute("outerHTML"))
					outerhtml="".join(outerhtml.split()).replace("&nbsp;","")
					elemdict[outerhtml]=elem
				
				alldict[tagtofind]=elemdict
			
		for row in contents:
			tagtofind=row[11]
			dbstring=filter(lambda x: x in string.printable,row[10])
			dbstring="".join(dbstring.split()).replace("nbsp;","")
			
			tagdict=alldict.get(tagtofind)
			element=tagdict.get(dbstring)
			elements.append(element)
					
					
			#print browser.title
		for e in elements:
			highlight(e)
		
		imagerand= 'multiMeetingScreenshot'+str(rand_generator())+'.png'
		browser.save_screenshot(imagerand)
		return imagerand
		
		
def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    #print("highlighting element")
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].style.background='yellow'",
                              element)
    original_style = element.get_attribute('style')
    apply_style("background: yellow; border: 5px solid red;")
    apply_style("border: 5px solid red;")

retval=LoadPageAndTakeScreenShot()
if retval is not None:
	img=Image.open(retval)
	img_width=int(img.size[0])
	img_height=int(img.size[1])
	print img_height
	crop_y=0
	while crop_y<img_height:
		img2 = img.crop((0,crop_y,img_width,crop_y+400))
		path="img"+str(rand_generator())+".png"
		img2.save(path)
		crop_y=crop_y+400
		print crop_y

