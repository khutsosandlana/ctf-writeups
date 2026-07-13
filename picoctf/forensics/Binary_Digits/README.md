This file doesn't look like much... just a bunch of 1s and 0s. But maybe it's not just random noise. Can you recover anything meaningful from this?

wget https://challenge-files.picoctf.net/c_plain_mesa/c443005e8024af39085323276b34da0e92f968746547f8e7f8b650ab37e668d1/digits.bin

How i solved it:

i started of playing around and just looking through the files data and meta data using the tool Exiftool and File. Afterwards i followed by just checking for any hidden data by using binwalk. i used [Strings] to view file data and i was given a binary file meaning everything wsa 1's and 0's. Since i saw it was binary i moved on and took the data and entered it into [Cyberchef] used the [From Binary] option and added the [Magic] to help me more and it actually rendered it as and image that has the flag written on it


