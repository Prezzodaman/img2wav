# img2wav
Python program that converts an image file to audio. The result is a 16-bit wave file, and when viewing its spectrogram, the image can be seen! Dark backgrounds are recommended, as lighter shades are louder. Indexed images aren't supported right now.
The only libraries used by this program are Pillow, ArgParse, Wave and Math. No other external libraries are used!

## How's it done?
This program uses additive synthesis to generate the image, by combining multiple sine waves together. Each vertical pixel has its own frequency, spanning the full frequency range. Then, these frequencies are added together, with the current pixel's intensity deciding the amplitude of each one. This is repeated for every horizontal column of pixels. You can change the "sample size" for each one, giving the sine waves more time to oscillate before going to the next column. This results in a better quality image, but it takes longer to render, and the resulting file will be much longer as well.

When frequencies are close together, it produces a "beating" sound, which can distort the quality of an image. To get around this, a "spacing" option is available, which increases the spacing between frequencies. This is recommended for larger images, because as the image increases in size, more frequencies are added, which are closer together.