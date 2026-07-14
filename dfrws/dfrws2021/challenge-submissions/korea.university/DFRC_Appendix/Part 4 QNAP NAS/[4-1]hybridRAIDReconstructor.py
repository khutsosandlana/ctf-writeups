#!/usr/bin/env python3

import sys
import os
import struct
import argparse

class HybridRAID:
    def __init__(self, InputDirectory, OutputDirectory):
        self.InputPath = InputDirectory
        self.OutputPath = OutputDirectory
        
        self.filePathList = []
        fileList = os.listdir(self.InputPath)
        fileList.sort()
        for filename in fileList:
            filePath = self.InputPath + '\\' + filename
            self.filePathList.append(filePath)

        self.partitionList = []
        self.bvdList = []
        self.vdList = []

    def __del__(self):
        self.fp.close()

    def _ParseMBR(self):
        for file in self.filePathList:
            try:
                print(file)
                self.fp = open(file, 'rb')
                block = self.fp.read(512)
            except IOError:
                print('Error : Could not image file open')

            if block[510:] == b'\x55\xAA':
                type = block[450]
                startOffset = struct.unpack('<i', block[454:458])[0]
                size = struct.unpack('<i', block[458:462])[0]
                if startOffset > 0 and size > 0:
                    self.partitionList.append([file, startOffset*512, size*512])

                type = block[466]
                startOffset = struct.unpack('<i', block[470:474])[0]
                size = struct.unpack('<i', block[474:478])[0]
                if startOffset > 0 and size > 0:
                    self.partitionList.append([file, startOffset*512, size*512])

                type = block[482]
                startOffset = struct.unpack('<i', block[486:490])[0]                
                size = struct.unpack('<i', block[490:494])[0]                
                if startOffset > 0 and size > 0 and type == 15:
                    extendOffset = startOffset

                    while True:
                        self.fp.seek(extendOffset*512)
                        extendBlock = self.fp.read(512)

                        type = extendBlock[450]
                        startOffset = struct.unpack('<i', extendBlock[454:458])[0]
                        size = struct.unpack('<i', extendBlock[458:462])[0]
                        if startOffset > 0 and size > 0:
                            self.partitionList.append([file, (extendOffset+startOffset)*512, size*512])

                        type = extendBlock[466]
                        startOffset = struct.unpack('<i', extendBlock[470:474])[0]
                        size = struct.unpack('<i', extendBlock[474:478])[0]
                        if startOffset > 0 and size > 0 and (type == 5 or type == 15):
                            extendOffset = extendOffset + startOffset
                            continue
                        else:
                            break
                elif startOffset > 0 and size > 0 and type != 15:
                    self.partitionList.append([file, startOffset*512, size*512])

                type = block[498]
                startOffset = struct.unpack('<i', block[502:506])[0]                
                size = struct.unpack('<i', block[506:510])[0]                
                if startOffset > 0 and size > 0 and type == 15:
                    extendOffset = startOffset

                    while True:
                        self.fp.seek(extendOffset*512)
                        extendBlock = self.fp.read(512)

                        type = extendBlock[450]
                        startOffset = struct.unpack('<i', extendBlock[454:458])[0]
                        size = struct.unpack('<i', extendBlock[458:462])[0]
                        if startOffset > 0 and size > 0:
                            self.partitionList.append([file, (extendOffset+startOffset)*512, size*512])

                        type = extendBlock[466]
                        startOffset = struct.unpack('<i', extendBlock[470:474])[0]
                        size = struct.unpack('<i', extendBlock[474:478])[0]
                        if startOffset > 0 and size > 0 and type == 15:
                            extendOffset = extendOffset + startOffset
                            continue
                        else:
                            break
                elif startOffset > 0 and size > 0 and type != 15:
                    self.partitionList.append([file, startOffset*512, size*512])
            else:
                self.partitionList.append([file, 0, os.path.getsize(file)])
            self.fp.close()
        
        if len(self.partitionList) > 0:
            return True
        else:
            return False

    def _ParseGPT(self):
        for file in self.filePathList:
            try:
                self.fp = open(file, 'rb')
                temp = self.fp.read(512)
            except IOError:
                print('Error : Could not image file open')

            if temp[510:] == b'\x55\xAA':
                GPT = self.fp.read(512)
                if GPT[:8] == b'\x45\x46\x49\x20\x50\x41\x52\x54':
                    EntrySize = struct.unpack('<i', GPT[0x54:0x58])[0]

                else:
                    return False
                while True:
                    GPT = self.fp.read(EntrySize)
                    if GPT[:16] == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
                        break
                    startOffset = struct.unpack('<q', GPT[32:40])[0]
                    endOffset = struct.unpack('<q', GPT[40:48])[0]

                    size = endOffset - startOffset

                    self.partitionList.append([file, startOffset * 512, size * 512])

            self.fp.close()

        if len(self.partitionList) > 0:
            return True
        else:
            return False

    def _CreateBVD(self):
        for partition in self.partitionList:
            try:
                self.fp = open(partition[0], 'rb')
                remain = partition[2] % 0x1000
                offset = partition[1] + partition[2] - remain - 0x2000
                self.fp.seek(offset)
                block = self.fp.read(512)
            except IOError:
                print('Error : Could not image file open')
                exit(1)

            self.fp.close()

            signature = block[0:4]
            if signature == b'\xFC\x4E\x2B\xA9':
                UUID = block[16:32]
                RAIDType = struct.unpack('<I', block[72:76])[0]
                stripeMap = struct.unpack('<I', block[76:80])[0]
                chunkSize = struct.unpack('<I', block[88:92])[0]
                numberOfDisks = struct.unpack('<I', block[92:96])[0]
                startOffset = struct.unpack('<Q', block[128:136])[0]
                sizeOfExtents = struct.unpack('<Q', block[136:144])[0]
                diskOrder = struct.unpack('<I', block[160:164])[0]
            else:
                continue

            check = False
            
            for atom in self.bvdList:
                if atom[0] == UUID:
                    # UUID, RAIDType, StripeSize, StripeMap, numberOfDiks, hasLVM, ExtentList
                    # Extent List : filePath, Partition Start offset, Partition Size, ExtentStartOffset, Extent Size, diskOrder                                       
                    atom[5].append([partition[0], partition[1], partition[2], partition[1]+startOffset*512, sizeOfExtents*512, diskOrder])
                    check = True
                    break

            if check is False:
                ExtentList = []
                ExtentList.append([partition[0], partition[1], partition[2], partition[1]+startOffset*512, sizeOfExtents*512, diskOrder])
                self.bvdList.append([UUID, RAIDType, stripeMap, numberOfDisks, False, ExtentList, chunkSize])

        # print BVD info
        index = 1
        for atom in self.bvdList:
            print("RAID Group ", index)
            index = index + 1
            print(" - UUID :", atom[0])
            print(" - RAID Type : RAID Level", atom[1])
            print(" - Chunk Size :", atom[6])
            if atom[1] == 5 or atom[1] == 6:
                if atom[2] == 0:
                    print(" - Stripe Map : left asymmetric")
                elif atom[2] == 1:
                    print(" - Stripe Map : right asymmetric")
                elif atom[2] == 2:
                    print(" - Stripe Map : left symmetric")
                elif atom[2] == 3:
                    print(" - Stripe Map : right symmetric")
            print(" - Number Of Disks :", atom[3])
            print(" - Extent List :")
            for extent in atom[5]:
                print("     image path :", extent[0], ", partition start offset :", extent[1], ", partition size :", extent[2], ", extent start Offset :", extent[3], ", extent size :", extent[4], ", diskOrder :", extent[5])
            print("\n")

    def _CreateVD(self):
        # Parsing the LVM
        for atom in self.bvdList:
            for extent in atom[5]:
                if extent[5] == 0:
                    try:
                        self.fp = open(extent[0], 'rb')
                        self.fp.seek(extent[3]+512)
                        block = self.fp.read(512)
                    except IOError:
                        print('Error : Could not image file open')
                        exit(1)

                    if block[0:8] != b'\x4C\x41\x42\x45\x4C\x4F\x4E\x45':
                        self.fp.close()
                        break
                    else:
                        self.fp.seek(0)
                        self.fp.seek(extent[3]+4096)
                        block = self.fp.read(512)
                        lvmMetadataOffset = struct.unpack('<Q', block[0x28:0x30])[0]
                        lvmMetadataSize = struct.unpack('<Q', block[0x30:0x38])[0]

                        self.fp.seek(0)
                        self.fp.seek(extent[3]+4096+lvmMetadataOffset)
                        block = self.fp.read(lvmMetadataSize)
                        self.vdList.append(block)
                        self.fp.close()

        self.vdList = list(set(self.vdList))
        for atom in self.vdList:
            filepath = self.OutputPath + '\\Logical_Volume_List_info.txt'
            fp = open(filepath, 'w')
            fp.write(atom.decode('ascii'))
            fp.close()
        return True


    def _makeImg(self):
        index = 1
        for atom in self.bvdList:
            filepath = self.OutputPath + '\\Partition_' + str(index)
            fp = open(filepath, 'wb')
            index = index + 1
            raidType = atom[1]

            if raidType == 1:
                file = atom[5][0][0]
                startoffset = atom[5][0][3]
                size = atom[5][0][4]
                self.fp = open(file, 'rb')
                self.fp.seek(startoffset)
                fp.write(self.fp.read(size))
                self.fp.close()

            if raidType == 5:
                chunksize = atom[6] * 0x200
                tmp = atom[6] * 0x200
                parity = 0
                chunkIndex = 0

                #sorting by diskorder
                forlist = sorted(atom[5], key=lambda x: x[5])

                for i in range(len(forlist)):
                    forlist[i].append(forlist[i][5])

                chunktimes = (atom[5][0][4]) // (chunksize)
                remain = (atom[5][0][4]) % chunksize
                exceptRemain = chunktimes * chunksize

                while True:
                    chunk = chunkIndex * chunksize
                    chunkIndex = chunkIndex + 1
                    if chunk == exceptRemain:
                        chunksize = remain
                    parity = parity - 1
                    for i in range(3):
                        if forlist[i][5] != parity % 3:
                            file = open(forlist[i][0],'rb')
                            file.seek(forlist[i][3] + chunk)
                            fp.write(file.read(chunksize))
                    for i in range(3):
                        forlist[i][6] = (forlist[i][6] + 1) % 3
                    forlist = sorted(atom[5], key=lambda x: x[6])
                    if chunksize != tmp:
                        break
            fp.close()


    def run(self):
        if len(self.filePathList) <= 0:
            print('Error : Unable to read file in directory')
            exit()
        else:
            if self._ParseGPT() is False:
                print('Error : Unable to read file in directory')
                exit()
            else:
                if self._CreateBVD() is False:
                    print('Error : Linux RAID Superblock is not found')
                    exit()
                else:
                    self._CreateVD()
                    self._makeImg()

def main(DirectoryPath):

    parser = argparse.ArgumentParser(usage='HybridRAIDReconstructor --i INPUT_DIRECTORY --o OUTPUT_DIRECTORY', description='This tool is a tool to rebuild RAID against Linux based hybrid RAID')

    parser.add_argument('--i', required=False, metavar='InputDirectory', help='Enter directory where raw image exists')
    parser.add_argument('--o', required=True, metavar='OutputDirectory', help='Enter directory to save raw image')

    args = parser.parse_args()

    if os.path.isdir(args.i) is True and os.path.isdir(args.o) is True:
        hybrid = HybridRAID(args.i, args.o)
        hybrid.run()
    else:
        print('Error : Directory path is not exist')

if __name__ == "__main__":
    main(sys.argv)
