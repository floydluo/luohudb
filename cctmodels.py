import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Table, Text, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


'''
relationship( "CLASS NAME")

back_pop, 上有Foreigner Key, 加 s
'''

def sdb_connect(basedir, name = 'data'):
    return create_engine('sqlite:///'+os.path.join(basedir, name + '.sqlite'))

def mdb_connect():
    MySQL_DB = 'mysql+pymysql://root:@localhost:3306/cct?charset=utf8'
    return create_engine(MySQL_DB)


Base = declarative_base()

def create_table(engine):
    Base.metadata.create_all(engine)

## Schema

class Patient(Base):
    __tablename__ = 'Patients'
    id = Column(Integer, primary_key=True)
    PatientID = Column(Integer)

    # 1-->n patient --> EPRs, here is 1
    EPRs = relationship("EPR", back_populates = 'Patient')

    # 1-->n patient --> feerecords,      here is 1 
    FeeRecords      = relationship("FeeRecord", back_populates = 'Patient')

    # 1-->n patient --> checkreports,    here is 1
    CheckReports    = relationship("CheckReport", back_populates = 'Patient')

    # 1-->n patient --> tempIteminfo,    here is 1
    TempItemInfos   = relationship("TempItemInfo", back_populates = 'Patient')



######## Data Type 4, 8 TempItemInfo 'Check, Treatment, Drugs'

class TempItemInfo(Base):
    __tablename__ = 'TempItemInfos'
    id = Column(Integer, primary_key=True)
    OEORDRowId = Column(Text)
    ItemName = Column(Text)
    ItemCat = Column(Text)
    InstrDR = Column(Text)
    DoseQty = Column(Text)
    PHFreqDR= Column(Text)
    Remark  = Column(Text)
    Status  = Column(Text)
    PrescNo  = Column(Text)
    Priority= Column(Text)
    ToldType= Column(Text)
    YJDate  = Column(Text)
    Date    = Column(Text)
    Loc     = Column(Text)
    RecLoc  = Column(Text)
    Price   = Column(Text)
    Unit    = Column(Text)
    RecLocID= Column(Text)
    StDate  = Column(Text)
    EtDate  = Column(Text)
    RecLocID= Column(Text)
    RecLocDesc= Column(Text)
    NeedExecTime = Column(Text)
    CommonName = Column(Text)
    YPFlag = Column(Text)

    # 1-->N, here is 1
    TempItemExecInfos = relationship("TempItemExecInfo", back_populates = 'TempItemInfo')

    # 1-->n patient --> FeeRecords, here is n
    Patient_id = Column(Integer, ForeignKey("Patients.id"))
    Patient    = relationship("Patient", back_populates="TempItemInfos")



class TempItemExecInfo(Base):
    __tablename__ = 'TempItemExecInfos'
    id = Column(Integer, primary_key=True)
    ExecTime = Column(Text)
    NeedExecTime = Column(Text)
    ExecDoctor = Column(Text)
    ExecLoc    = Column(Text)
    ExecStatus = Column(Text)

    # 1-->N, here is N
    TempItemInfo_id = Column(Integer, ForeignKey("TempItemInfos.id"))
    TempItemInfo = relationship("TempItemInfo", back_populates="TempItemExecInfos")



######## Data Type 3, 7 Check Report Result

## HEAD
class CheckReport(Base):
    __tablename__ = 'CheckReports' #pural
    id = Column(Integer, primary_key=True)
    HisID = Column(Text)
    Name = Column(Text)
    Sex = Column(Text)
    Age = Column(Text)
    InAdmDate = Column(Text)
    CurLoc = Column(Text)
    CurBed = Column(Text)
    CurWard = Column(Text)
    Diagnosis = Column(Text)

    # 1--> N, here is 1
    CheckReportInfos = relationship("CheckReportInfo", back_populates = 'CheckReport')

    # 1-->n patient --> FeeRecords, here is n
    Patient_id = Column(Integer, ForeignKey("Patients.id"))
    Patient    = relationship("Patient", back_populates="CheckReports")

class CheckReportInfo(Base):
    __tablename__ = 'CheckReportInfos' #pural
    id = Column(Integer, primary_key=True)
    ArcName = Column(Text)
    Date = Column(Text)
    Loc = Column(Text)
    ReportDate = Column(Text)
    ReportDoctor = Column(Text)
    Type = Column(Text)
    OrderID = Column(Text)
    StudyNo = Column(Text)
    
    # 1--> N, here is N
    CheckReport_id = Column(Integer, ForeignKey("CheckReports.id"))
    CheckReport = relationship("CheckReport", back_populates="CheckReportInfos")
    
    # 1--> N, here is 1
    CheckReportItems = relationship("CheckReportItem", back_populates = 'CheckReportInfo')
    

class CheckReportItem(Base):
    __tablename__ = 'CheckReportItems' # pural
    id = Column(Integer, primary_key=True)
    ItemName = Column(Text)
    ExamDetail = Column(Text)
    RefRanger = Column(Text)
    Unit = Column(Text)
    ItemMemo = Column(Text)
    
    # 1--> N, here is N
    CheckReportInfo_id = Column(Integer, ForeignKey("CheckReportInfos.id"))
    CheckReportInfo = relationship("CheckReportInfo", back_populates="CheckReportItems")
    


######## Data Type 2, 6 FeeList of

## HEAD
class FeeRecord(Base):
    __tablename__='FeeRecords' # pural
    id = Column(Integer, primary_key=True)
    Name = Column(Text)
    Sex = Column(Text)
    Age = Column(Text)
    InAdmDate = Column(Text)
    ZYH = Column(Text)
    CurLoc = Column(Text)
    CurBed = Column(Text)
    TotalAmount = Column(Text)
    YBAmount = Column(Text)
    YJAmount = Column(Text)
    CurWard  = Column(Text)
    FeeItems = relationship("FeeItem", back_populates = 'FeeRecord')

    # 1-->n patient --> FeeRecords, here is n
    Patient_id = Column(Integer, ForeignKey("Patients.id"))
    Patient    = relationship("Patient", back_populates="FeeRecords")
    
    
class FeeItem(Base):
    __tablename__ = 'FeeItems' # pural
    id = Column(Integer, primary_key=True)
    PAADM   = Column(Text)
    EMCCate = Column(Text)
    TARIItem = Column(Text)
    UnitPrice = Column(Text)
    BillQty = Column(Text)
    Amount = Column(Text)
    BillType = Column(Text)
    BillStatus = Column(Text) 
    
    FeeRecord_id = Column(Integer, ForeignKey("FeeRecords.id"))
    FeeRecord = relationship("FeeRecord", back_populates="FeeItems")



######## Data Type 5, 9 Electronic Health Record



## HEAD
class EPR(Base):
    __tablename__ = 'EPRs'

    id = Column(Integer, primary_key=True)

    # 1-->n patient --> EPRs, here is n
    Patient_id = Column(Integer, ForeignKey("Patients.id"))
    Patient    = relationship("Patient", back_populates="EPRs")

    # 1-->n EPR --> RANinfos,       here is 1
    RANinfos = relationship("RANinfo", back_populates = 'EPR')

    # 1-->n EPR --> FirstCorinfos,  here is 1
    FirstCorinfos = relationship("FirstCorinfo", back_populates = 'EPR')

    # 1-->n EPR --> DailyRecdata,   here is 1
    DailyRecdatas = relationship("DailyRecdata", back_populates = 'EPR')

    # 1-->n EPR --> GetDisRecordinfos, here is 1
    GetDisRecordinfos = relationship("GetDisRecordinfo", back_populates = 'EPR')

    # 1-->n EPR --> OpEMRDatas, here is 1
    OpEMRDatas = relationship("OpEMRData", back_populates = 'EPR')

    # 1-->n EPR --> DeathRecordinfos, here is 1
    DeathRecordinfos = relationship("DeathRecordinfo", back_populates = 'EPR')

    # 1-->n EPR --> OperRecdatas, here is 1
    OperRecdatas = relationship("OperRecdata", back_populates = 'EPR')

    # 1-->n EPR --> hourRecs, here is 1
    hourRecs = relationship("hourRec", back_populates = 'EPR')


class DeathRecordinfo(Base):
    __tablename__ = 'DeathRecordinfos'

    id = Column(Integer, primary_key=True)
    A1 = Column(Text)
    A2 = Column(Text)
    Ininfo  = Column(Text) 
    Indiag  = Column(Text) 
    Treatment = Column(Text)
    Deathdiag = Column(Text)
    Reasonofdeath = Column(Text)

    # 1-->n EPR --> DeathRecordinfos, here is n
    EPR_id = Column(Integer, ForeignKey("EPRs.id"))
    EPR    = relationship("EPR", back_populates="DeathRecordinfos")



class OperRecdata(Base):
    __tablename__ = 'OperRecdatas'
    id = Column(Integer, primary_key=True)
    A1 = Column(Text)
    A2 = Column(Text)

    # once
    happentime = Column(Text)
    title = Column(Text)
    OperTime = Column(Text)
    OperName = Column(Text)
    Text     = Column(Text)

    # 1-->n EPR --> OperRecdatas, here is n
    EPR_id = Column(Integer, ForeignKey("EPRs.id"))
    EPR    = relationship("EPR", back_populates="OperRecdatas")

class hourRec(Base):
    __tablename__ = 'hourRecs'

    id = Column(Integer, primary_key=True)
    A1 = Column(Text)
    A2 = Column(Text)
    ChiefComplaint = Column(Text)
    Ininfo = Column(Text)
    Indiag = Column(Text)
    Treatment = Column(Text)
    Outdiag   = Column(Text)
    Outoeord  = Column(Text)
    # 1-->n EPR --> hourRecs, here is n
    EPR_id = Column(Integer, ForeignKey("EPRs.id"))
    EPR    = relationship("EPR", back_populates="hourRecs")


class OpEMRData(Base):
    __tablename__ = 'OpEMRDatas'
    id = Column(Integer, primary_key=True)
    A1 = Column(Text)
    A2 = Column(Text)
    Basicinfo = Column(Text)
    AllergicHistoryFlag  = Column(Text)
    Accessoryexamination = Column(Text)
    Tentativediagnosis   = Column(Text)
    TreatMent            = Column(Text)
    AllergicHistory      = Column(Text)

    # 1-->n EPR --> OpEMRData, here is n
    EPR_id = Column(Integer, ForeignKey("EPRs.id"))
    EPR    = relationship("EPR", back_populates="OpEMRDatas")


class RANinfo(Base):
    __tablename__ = 'RANinfos'
    id = Column(Integer, primary_key=True)
    A1 = Column(Text)
    A2 = Column(Text)

    # Basicinfo
    ChiefComplaint = Column(Text)
    Pasthistory    = Column(Text)
    Personalhistory   = Column(Text)
    Obstericalhistory = Column(Text)
    Menstrualhistory  = Column(Text)
    Familyhistory     = Column(Text)

    PhysicalExamination = Column(Text)
    Specialityexamination  = Column(Text)
    Accessoryexamination= Column(Text)
    Tentativediagnosis  = Column(Text)
    Reviseddiagnosis    = Column(Text)
    PresentIllness      = Column(Text)

    # 1-->n EPR --> RANinfos,       here is n
    EPR_id = Column(Integer, ForeignKey("EPRs.id"))
    EPR    = relationship("EPR", back_populates="RANinfos")

class FirstCorinfo(Base):
    __tablename__ = 'FirstCorinfos'
    id = Column(Integer, primary_key=True)
    A1 = Column(Text)
    A2 = Column(Text)
    Basicinfo = Column(Text)
    Characteristics = Column(Text)
    Tentativediag   = Column(Text)
    Diagacord       = Column(Text)
    Diagdiscern     = Column(Text)
    Treatplan       = Column(Text)

    # 1-->n EPR --> FirstCorinfos,       here is n
    EPR_id = Column(Integer, ForeignKey("EPRs.id"))
    EPR    = relationship("EPR", back_populates="FirstCorinfos")

class DailyRecdata(Base):
    __tablename__ = 'DailyRecdatas'
    id = Column(Integer, primary_key=True)
    A1 = Column(Text)
    A2 = Column(Text)
    happentime = Column(Text)
    title      = Column(Text)
    Text       = Column(Text)

    # 1-->n EPR --> RANinfos,       here is n
    EPR_id = Column(Integer, ForeignKey("EPRs.id"))
    EPR    = relationship("EPR", back_populates="DailyRecdatas")


class GetDisRecordinfo(Base):
    __tablename__ = 'GetDisRecordinfos'
    id = Column(Integer, primary_key=True)
    A1 = Column(Text)
    A2 = Column(Text)
    Ininfo = Column(Text)
    Indiag = Column(Text)
    Treatment = Column(Text)
    Outinfo   = Column(Text)
    Outdiag   = Column(Text)
    Outoeord  = Column(Text)

    # 1-->n EPR --> RANinfos,       here is n
    EPR_id = Column(Integer, ForeignKey("EPRs.id"))
    EPR    = relationship("EPR", back_populates="GetDisRecordinfos")




    