from obspy import read as pread
from obspy import Stream

def GetSacInfo(fileName):
    stream=pread(fileName)
        
    time=[stream[0].stats.sac.nzyear,
                stream[0].stats.sac.nzjday,
                stream[0].stats.sac.nzhour*3600+
                stream[0].stats.sac.nzmin*60+
                stream[0].stats.sac.nzsec+
                stream[0].stats.sac.nzmsec/1000]
    
    return stream[0].data,time