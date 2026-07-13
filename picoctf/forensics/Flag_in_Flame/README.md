PicoCTF Write-up: Flag in Flame (logs.txt)
Challenge Description

    The SOC team discovered a suspiciously large log file after a recent breach. When they opened it, they found an enormous block of encoded text instead of typical logs. Could there be something hidden within? Your mission is to inspect the resulting file and reveal the real purpose of it. The team is relying on your skills to uncover any concealed information within this unusual log.  

Initial Reconnaissance

I started by gathering information on the massive log file to understand its structure and content:

    file logs.txt: Confirmed the file contained plain ASCII text, but noted it had incredibly long lines (65,536 characters) and no line terminators.

    exiftool logs.txt: Verified it was a ~1.6 MB single-line plain text file.

    grep / strings: Attempting to search directly for the flag pattern (picoCTF{...}) using regular expressions yielded no immediate results, indicating the flag was hidden beneath a layer of encoding or obfuscation.

The Solution

Recognizing that a massive, single-line text block is a hallmark sign of a Base64 encoded file, I adjusted my strategy:

    Decoding the Payload:

    I decoded the massive Base64 text block back into raw data bytes. This revealed that the text block was actually a hidden image file (download.png).

    Optical Character Recognition (OCR):

    The image contained text, but rather than copying it manually, I utilized Tesseract OCR to extract the text strings directly into a text file:
    Bash

    tesseract download.png image.txt

    Hex Decoding:

    Reading the output file (image.txt.txt) revealed a long string of Hex characters:

    7069636F4354467B666F72656E736963735F616E616C797369735F69735F616D617A696E675F35646161346132667D

    Dropping this Hex string into CyberChef (or a terminal converter) and applying the From Hex recipe successfully printed out the cleartext flag.

Flag: picoCTF{forensics_analysis_is_amazing_5daa4a2f}
