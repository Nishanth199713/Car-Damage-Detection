import requests
import sys
import argparse
import os
import cv2
from fpdf import FPDF

import base64
import json
#from openalpr import Alpr
cbody_type=""
ccolor=""
cmake=""
cmodel=""
cplate="TN09CD1918"
con=float()
conplate=float()
l=0
def globally_change(body_type,color,make,model,confi):
	global cbody_type
	cbody_type=body_type
	global ccolor
	ccolor=color
	global cmake
	cmake=make
	global cmodel
	cmodel=model
	global con
	con=confi
	
def globally_change_plate(plate):
	global cplate
	cplate=plate
'''def extractImages(pathIn, pathOut):
    count = 0
    vidcap = cv2.VideoCapture(pathIn)
    success,image = vidcap.read()
    success = True
    while success:
      vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))    # added this line
      success,image = vidcap.read()
      print ('Read a new frame: ', success)
      cv2.imwrite( pathOut + "/frame%d.jpg" % count, image)     # save frame as JPEG file
      count = count + 1
	 '''
def detect_plate(path_file):
	'''
	alpr = Alpr("in", "/usr/share/openalpr/config/openalpr.defaults.conf", "/usr/share/openalpr/runtime_data")
	if not alpr.is_loaded():
		 print("Error loading OpenALPR")
		 sys.exit(1)

	alpr.set_top_n(20)
	alpr.set_default_region("md")
	IMAGE_PATH=path_file
	results = alpr.recognize_file(IMAGE_PATH)
	i = 0
	
	platei=""
	platec=float()
	for plate in results['results']:
		 i += 1
		 #print("Plate #%d" % i)
		 #print("   %12s %12s" % ("Plate", "Confidence"))
		 for candidate in plate['candidates']:
			 prefix = "-"
			 if candidate['matches_template']:
				 prefix = "*"

			 #print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))
	if i==0:
		print("No plate")
	else:
		#print(results)
		platei=results['results'][0]['candidates'][0]['plate']
		#print(platei)
		platec=results['results'][0]['candidates'][0]['confidence']
		if l==0:
			conplate=platec
		if conplate<=platec:
			globally_change_plate(platei)
	'''
	SECRET_KEY = 'sk_1e93017a3c2a2aadbdd76754'

	with open(path_file, 'rb') as image_file:
		img_base64 = base64.b64encode(image_file.read())

	url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=in&secret_key=%s' % (SECRET_KEY)
	r = requests.post(url, data = img_base64)


	re=json.loads(r.text)

	body_type=re["results"][0]["vehicle"]["body_type"][0]["name"]
	make=re["results"][0]["vehicle"]["make"][0]["name"]
	color=re["results"][0]["vehicle"]["color"][0]["name"]
	model=re["results"][0]["vehicle"]["make_model"][0]["name"]
	confi=re["results"][0]["vehicle"]["make_model"][0]["confidence"]
	#print(confi)
	print("\n")
	if l==0:
		con=confi
	if con<=confi:
		globally_change(body_type,color,make,model,confi)
	#alpr.unload()
		
if __name__=="__main__":
	'''a = argparse.ArgumentParser()
	a.add_argument("--pathIn", help="path to video")
	a.add_argument("--pathOut", help="path to images")
	args = a.parse_args()
	extractImages(args.pathIn, args.pathOut)'''
	path="test"
	
	filename="test/frame0.jpg"
	detect_plate(filename)
	filename="test/frame1.jpg"
	detect_plate(filename)
	pdf = FPDF()
	pdf.set_margins(40,40,40)
	pdf.add_page()
	pdf.set_font('Arial', 'B', 36)
	pdf.set_y(90)
	pdf.set_x(50)
	pdf.cell(100, 20, 'CAR REPORT', 1, 0, 'C')
	pdf.set_y(170)
	pdf.set_x(170)
	pdf.set_font('Arial', 'B', 16)
	pdf.cell(10, 20, 'Ravikiran', 0, 2, 'R')
	pdf.cell(10, 20, 'Nishanth', 0, 2, 'R')
	pdf.cell(10, 20, 'Arunasalam', 0, 2, 'R')
	pdf.add_page()
	pdf.write(5, 'The captured image is \n ')
	pdf.image('./test/frame0.jpg', x = 10, y = 90, w=150, h=84)
	pdf.add_page()
	pdf.cell(100, 20, 'The body type of the car is :'+cbody_type, 0, 2, 'L')
	pdf.cell(100, 20, 'The car company is :'+cmake, 0, 2, 'L')
	pdf.cell(100, 20, 'The colour of the car is :'+ccolor, 0, 2, 'L')
	pdf.cell(100, 30, 'The model of the car is :'+cmodel, 0, 2, 'L')
	pdf.write(5, 'The license plate is %s ' %cplate) # with confidence of %s
	pdf.add_page()
	pdf.write(5, 'The scratch detected at \n ')
	c=0
	for name in os.listdir('output'):
		if name.endswith("jpg"):
			c=1
			filename='output/'+name
			pdf.image(filename, x = 10, y = 90, w=150, h=84)
	if c==0:
		pdf.cell(100, 20, 'No scratch detected in this car', 0, 2, 'R')
	pdf.output('polo report.pdf', 'F')
