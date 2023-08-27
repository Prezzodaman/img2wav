import argparse
import wave
import math
from PIL import Image

parser=argparse.ArgumentParser(description="Converts an image to an audio file")
parser.add_argument("input_file", type=argparse.FileType("r"),help="The name of the input image")
parser.add_argument("output_file", type=argparse.FileType("w"),help="The name of the resulting file")
parser.add_argument("sample_rate",type=int,help="Sample rate")
parser.add_argument("sample_size",type=int,help="Sample size (dictates the overall length)")
parser.add_argument("top_frequency",type=int,help="Top frequency")
parser.add_argument("spacing",type=int,help="Spacing between frequencies (smaller images require a lower spacing)")

args=parser.parse_args()

input_file=args.input_file.name
output_file=args.output_file.name
sample_rate=args.sample_rate
sample_size=args.sample_size
top_frequency=args.top_frequency
spacing=args.spacing

print("Img2wav v1.0.1")
print("by Presley Peters, 2023")
print()

file_finished=[]

if top_frequency>sample_rate//2:
	print("Error: Top frequency must be " + str(sample_rate//2) + " or below!")
else:
	if spacing<1:
		print("Warning: Spacing is below 1, using 1...")
		spacing=1
	with Image.open(input_file) as image:
		print("Width: " + str(image.width) + ", Height: " + str(image.height) + ", Top frequency: " + str(top_frequency) + ", Spacing: " + str(spacing))
		image_x=0
		angles=[0]*image.height
		frequency_increase=top_frequency/image.height
		samples_total=0
		sample_size_inc=sample_rate/22050
		for image_x in range(0,image.width):
			for sample in range(0,int(sample_size*sample_size_inc)):
				frequency=0
				byte=0
				print(str(int(samples_total/(sample_size*image.width*sample_size_inc)*100)) + "% done, X: " + str(image_x+1) + "/" + str(image.width) + ", Sample: " + str(int(sample/sample_size_inc)+1) + "/" + str(sample_size) + "       ",end="\r")
				for image_y in range(image.height-1,0,-1):
					pixel=image.getpixel((image_x,image_y))
					shade=(pixel[0]+pixel[1]+pixel[2])/3
					byte+=int((math.sin(angles[image_y])*shade*255)+32768)//image.height
					if image_y*sample_size_inc%int(spacing*sample_size_inc)==0:
						angles[image_y]+=(frequency*math.pi*2)/sample_rate
					frequency+=frequency_increase
				samples_total+=1
				
				byte=(byte+32768) & 65535
				file_finished.append(byte & 255)
				file_finished.append(byte>>8)

		print()
		print("Done!")

		wave_file=wave.open(output_file,"w")
		wave_file.setnchannels(1)
		wave_file.setsampwidth(2)
		wave_file.setframerate(sample_rate)
		wave_file.writeframesraw(bytearray(file_finished))
		wave_file.close()