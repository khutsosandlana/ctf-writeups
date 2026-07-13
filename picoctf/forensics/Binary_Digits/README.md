PicoCTF Write-up: Plain Mesa (digits.bin)
Challenge Description

    This file doesn't look like much... just a bunch of 1s and 0s. But maybe it's not just random noise. Can you recover anything meaningful from this?
    wget https://challenge-files.picoctf.net/c_plain_mesa/c443005e8024af39085323276b34da0e92f968746547f8e7f8b650ab37e668d1/digits.bin

Initial Reconnaissance

I started by gathering metadata and analyzing the file type using standard Linux CLI tools:

    file digits.bin & exiftool digits.bin: Used to check the file type and metadata, but nothing immediately stood out.

    binwalk digits.bin: Checked for hidden embedded files or carved payloads, but returned no major leads.

    strings digits.bin: Running strings revealed that the file consisted entirely of ASCII 1s and 0s (a literal text stream of binary data).

The Solution

Since the file content was entirely raw binary characters (01100001...), I knew I needed to decode it back into its original bytes.

    I loaded the raw text of digits.bin into CyberChef.

    I applied the "From Binary" recipe to convert the text stream back into actual data bytes.

    To determine what kind of file these bytes actually represented, I appended the "Magic" tool to the recipe.

    CyberChef automatically detected that the decoded bytes formed a valid image file and rendered it directly in the output pane, revealing the flag!

Flag: picoCTF{h1dd3n_1n_th3_b1n4ry_cc2099d3}
