class MagDataDecoder:
    def __init__(self,filename):
        self.filename = filename
    def bin2dat(self,mode):
        if mode ==1:
            sil = 0
            while(1):
                if sil == 60: break
                print("sil : "+str(sil))
                data = self.dab(self.filename,sil)
                res = self.track1(data)
                res_inv = self.track1(data[::-1])
                print(res)
                print("")
                print(res_inv)
                print("")
                sil += 0.01
        elif mode ==2:
            sil = 0
            while(1):
                if sil == 60: break
                print("sil : " + str(sil))
                data = self.dab(self.filename,sil)
                self.track2(data)
                self.track2(data[::-1])

                sil += 0.01
	def track1(self,data):
        start, end = self.find_sentinel(1, data)
        for i in start:
            for j in end:
                if (i < j) and ((j - i) % 7 == 0):
                    result = ""
                    # print("sentienel index -> "+str(i)+", "+str(j))
                    for idx in range(i, j, 7):
                        if self.parity_chk(data[idx:idx + 7]) == -1:
                            break
                        else:
                            char = chr(int(data[idx:idx + 6][::-1], 2) + 32)
                            result += char
                    print(result)
    def track2(self,data):
        start,end = self.find_sentinel(2,data)
        for i in start:
            for j in end:
                if (i<j) and ((j - i)%5 == 0):
                    result = ""
                    #print("sentienel index -> "+str(i)+", "+str(j))
                    for idx in range(i,j,5):
                        if self.parity_chk(data[idx:idx+5]) == -1:
                            break
                        else:
                            char = chr(int(data[idx:idx + 4][::-1], 2) + 48)
                            result += char
                    print(result)
    def find_sentinel(self,trk,data):
        if trk == 1:
            start = [i for i in range(len(data)) if data.startswith('101000' + '1', i)]
            end = [i for i in range(len(data)) if data.startswith('111110' + '0', i)]
            return start,end
        if trk == 2:
            start = [i for i in range(len(data)) if data.startswith('1101'+'0',i)]
            end = [i for i in range(len(data)) if data.startswith('1111' + '1', i)]
            return start,end
        else:
            print("trk input error....")
            return -99,-99
    def parity_chk(self,dat):
        flag = dat.count('1')
        if flag % 2 == 0:
            return -1
        else:
            return 1
    def wav2bin(self,filename):
        samplerate, data = wavfile.read(filename)
        print(len(data))
        print(type(data))

        epoch = 0
        for i in range(1,len(data)-1):
            if (data[i] > data[i-1] and data[i] > data[i+1])\
                    and data[i] > 20:
                print("point : "+str(i)+" DB : "+str(data[i]))
    def dab(self,filename,sil):
        if sil != 0:
           thresh= 100 / float(sil)
        else:
           thresh= 100 / 33
        track=wave.open(filename)
        params=track.getparams()
        frames=track.getnframes()
        channels=track.getnchannels()
        if not channels == 1:
           sys.stderr.write("track must be mono!")
           return -1
        n= 0
        max= 0
        samples= []
        # determine max sample and build sample list
        while n < frames:
           n += 1
           # make sample an absolute value to simplify things later on
           current= abs(unpack("h",track.readframes(1))[0])
           if current > max:
              max= current
           samples.append(current)
        # set silence threshold
        silence= max / thresh
        # create a list of distances between peak values in numbers of samples
        # this gives you the flux transition frequency
        peak= 0
        ppeak= 0
        peaks= []
        n= 0
        while n < frames:
           ppeak= peak
           # skip to next data
           while n < frames and samples[n] <= silence:
              n= n+1
           peak= 0
           # keep going until we drop back down to silence
           while n < frames and samples[n] > silence:
              if samples[n] > samples[peak]:
                 peak= n
              n= n+1
           # if we've found a peak, store distance
           if peak - ppeak > 0:
              peaks.append(peak - ppeak)
        zerobl = peaks[2]
        n= 2
        # allow some percentage deviation
        freq_thres= 60
        output= ''
        while n < len(peaks) - 1:
           if peaks[n] < ((zerobl / 2) + (freq_thres * (zerobl / 2) / 100)) and peaks[n] > ((zerobl / 2) - (freq_thres * (zerobl / 2) / 100)):
              if peaks[n + 1] < ((zerobl / 2) + (freq_thres * (zerobl / 2) / 100)) and peaks[n + 1] > ((zerobl / 2) - (freq_thres * (zerobl / 2) / 100)):
                 output += '1'
                 zerobl= peaks[n] * 2
                 n= n + 1
           else:
               if peaks[n] < (zerobl + (freq_thres * zerobl / 100)) and peaks[n] > (zerobl - (freq_thres * zerobl / 100)):
                 output += '0'
                 zerobl= peaks[n]
           n= n + 1      
        sys.stderr.write("number of bits: " + str(len(output))+"\n")
        #sys.stderr.write("\n")
        print(output)
        return output