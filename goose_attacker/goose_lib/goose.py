class GOOSE:
    def __init__(self, appId, gocbRef, timeAllowedToLive, datSet, goId, t, 
                 stNum, sqNum, simulation, confRev, ndsCom, numDatSetEntries, allData):
        self.appId = b"\x00" + appId.to_bytes()
        self.gocbRef = b"\x00\x91\x00\x00\x00\x00a\x81\x86\x80\x1a" + gocbRef
        self.timeAllowedToLive = b"\x81\x03\x00" + timeAllowedToLive.to_bytes(length=2)
        self.datSet = b"\x82\x18" + datSet
        self.goId = b"\x83\x0b" + goId
        self.t =  b"\x84\x08" +  int(t).to_bytes(length=4) + b"\x00\x00\x00\x00"
        self.stNum = b"\x85\x01" + stNum.to_bytes()
        self.sqNum = b"\x86\x01" + sqNum.to_bytes()
        self.simulation = b"\x87\x01" + simulation.to_bytes()
        self.confRev = b"\x88\x01" + confRev.to_bytes()
        self.ndsCom = b"\x89\x01" + ndsCom.to_bytes()
        self.numDatSetEntries = b"\x8a\x01" + numDatSetEntries.to_bytes()
        self.allData = allData
        if self.allData != None:
            self.allData = b"\xab " + allData

    def generate_msg(self):
        goose = self.appId + self.gocbRef + self.timeAllowedToLive + self.datSet + self.goId + self.t + self.stNum + self.sqNum + self.simulation + self.confRev + self.ndsCom + self.numDatSetEntries
        if self.allData != None:
            return (goose + self.allData)
        return (goose)