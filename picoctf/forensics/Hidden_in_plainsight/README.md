
    You’re given a seemingly ordinary JPG image. Something is tucked away out of sight inside the file. Your task is to discover the hidden payload and extract the flag.
    wget [https://challenge-files.picoctf.net/c_amiable_citadel/f4d19218cb65d748b6a9b2bfc75caf5ac578f71e284ade9ee300e7367a5df648/img.jpg](https://challenge-files.picoctf.net/c_amiable_citadel/f4d19218cb65d748b6a9b2bfc75caf5ac578f71e284ade9ee300e7367a5df648/img.jpg)

Initial Reconnaissance

I began by inspecting the image file to look for embedded comments or anomalous data blocks:

    file img.jpg: While checking the file format, I noticed an embedded comment containing a Base64-encoded string:

    c3RlZ2hpZGU6Y0VGNmVuZHZjbVE9

    exiftool img.jpg: Ran a follow-up metadata dump to confirm no other fields had hidden clues, keeping my focus on the decoded comment string.

The Solution

The comment I found required a nested decoding process to reveal both the tool to use and the secret password.

    I pasted the encoded comment c3RlZ2hpZGU6Y0VGNmVuZHZjbVE9 into CyberChef and decoded it using the From Base64 recipe. This yielded:

    steghide:cEF6endvcmQ=

    I noticed the second half of the output (cEF6endvcmQ=) was also Base64-encoded. I decoded it a second time, which successfully revealed the password:

    pAzzword

    Knowing the tool was steghide, I returned to my terminal and ran the extraction command:

    steghide extract -sf img.jpg

    When prompted for the passphrase, I entered pAzzword. This extracted a hidden text file containing the flag.

Flag: picoCTF{h1dd3n_1n_1m4g3_5d4cba73}
