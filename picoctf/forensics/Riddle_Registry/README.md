PicoCTF Write-up: Amiable Citadel (confidential.pdf)
Challenge Description

    Hi, intrepid investigator! 📄🔍 You've stumbled upon a peculiar PDF filled with what seems like nothing more than garbled nonsense. But beware! Not everything is as it appears. Amidst the chaos lies a hidden treasure—an elusive flag waiting to be uncovered. Find the PDF file here and uncover the flag within the metadata.
    wget [https://challenge-files.picoctf.net/c_amiable_citadel/a8aa03694837741eed59c479749fc7f5bfd14fa66f4295b83776f16b2003a67d/confidential.pdf](https://challenge-files.picoctf.net/c_amiable_citadel/a8aa03694837741eed59c479749fc7f5bfd14fa66f4295b83776f16b2003a67d/confidential.pdf)

Initial Reconnaissance

I began by running basic reconnaissance on the downloaded file to verify its type and inspect its properties:

    file confidential.pdf: Confirmed that the file was indeed a standard PDF document.

    exiftool confidential.pdf: Since the challenge description explicitly hinted at checking the metadata, I dumped all the metadata tags to look for hidden details.

The Solution

While scanning the exiftool output, the Author field stood out immediately. Instead of a standard name, it contained a distinct, alphanumeric string ending with an = sign:

Author : cGljb0NURntwdXp6bDNkX20zdGFkYXRhX2YwdW5kIV9jMjA3MzY2OX0=

Recognizing the trailing = as a textbook indicator of Base64 encoding, I solved the challenge using the following steps:

    I copied the encoded string from the terminal.

    I pasted the string into CyberChef.

    I applied the "From Base64" recipe to decode the ciphertext, instantly revealing the flag.

Flag: picoCTF{puzzl3d_m3tadata_f0und!_c2073669}
