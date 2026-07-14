import argparse

extent_size = 8192 * 0x200
pe_start = 2048 * 0x200
extent_count_lv544 = 5194 * extent_size
stripes_lv544 = 0 * extent_size + pe_start
extent_count_tp1_tmeta = 16384 * extent_size
stripes_tp1_tmeta = 5194 * extent_size + pe_start
stripes_tp1_tierdata = 21578 * extent_size + pe_start
extent_count_lv1 = 51200 * extent_size
extent_count_lv2 = 384000 * extent_size

parser = argparse.ArgumentParser(usage=' --i INPUT_FILE', description='Divide logical volume')
parser.add_argument('--i', required=False, metavar='Input file', help='Enter File where raw image you want to divide by LVM')
parser.add_argument('--o', required=True, metavar='OutputDirectory', help='Enter directory to save raw image')
args = parser.parse_args()

input_file = args.i
output_Dir = args.o

file = open(input_file,'rb')

# parse lv544
fp = open(output_Dir + '\\lv544','wb')
file.seek(stripes_lv544)
fp.write(file.read(extent_count_lv544))
fp.close()

# parse tmeta
fp = open(output_Dir + '\\tmeta','wb')
file.seek(stripes_tp1_tmeta)
fp.write(file.read(extent_count_tp1_tmeta))
fp.close()

#parse lv1
fp = open(output_Dir + '\\lv1','wb')
file.seek(stripes_tp1_tierdata)
fp.write(file.read(extent_count_lv1))
fp.close()

#parse lv2
fp = open(output_Dir + '\\lv2','wb')
file.seek(stripes_tp1_tierdata+extent_count_lv1)
fp.write(file.read(extent_count_lv2))
fp.close()


