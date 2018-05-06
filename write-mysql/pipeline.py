import os

from sqlalchemy.orm import sessionmaker

from cctmodels import create_table, sdb_connect,  mdb_connect

from cctmodels import Patient
from cctmodels import TempItemInfo, TempItemExecInfo
from cctmodels import CheckReport, CheckReportInfo, CheckReportItem
from cctmodels import FeeRecord, FeeItem
from cctmodels import EPR as EPRecord
from cctmodels import OpEMRData, RANinfo, FirstCorinfo, DailyRecdata, GetDisRecordinfo, DeathRecordinfo, OperRecdata, hourRec

import pandas as pd
import xmltodict



def session_add(session, item):
    try:
        session.add(item)
    except:
        session.rollback()
        raise


def WriteFeeList(dt_dict, session, patt):
    feeRec = dt_dict['Data']['Request']
    if 'FeeList' in feeRec:
        feeItems = feeRec.pop('FeeList')
        feeItems = feeItems['FeeList'] # feeItems may be 1 item, or a list of items
        if type(feeItems) != list:
            feeItems = [feeItems]
    else:
        feeItems = []

    feeRec = FeeRecord(**feeRec)
    
    for fitem in feeItems:
        feeItm = FeeItem(**fitem)
        feeRec.FeeItems.append(feeItm)
        session_add(session, feeItm )
     
    patt.FeeRecords.append(feeRec)
    session_add(session, feeRec)   


def WriteCheckReport(dt_dict, session, patt):
    RPT = dt_dict['Data']['Request']
    
    if 'ReportInfo' in RPT:
        RPTInfos = RPT.pop('ReportInfo')
        RPTInfos = RPTInfos['ReportInfo']
        if type(RPTInfos) != list:
            #print('Only One')
            RPTInfos = [ RPTInfos ] 
    else:
        #print(RPT)
        RPTInfos = []
        
    CckRpt = CheckReport(**RPT)
    
    

    for RPTInfo in RPTInfos:
        if 'ReportItem' in RPTInfo:
            RPTItems = RPTInfo.pop('ReportItem')
            RPTItems = RPTItems['ReportItem']
            if type(RPTItems) != list:
                #print('Only One')
                RPTItems = [ RPTItems]
        else:
            #print(RPTInfo)
            RPTItems = []
            
        CckRptInfo = CheckReportInfo(**RPTInfo)
        
        for RPTItem in RPTItems:
            CckRptItem = CheckReportItem(**RPTItem)
            CckRptInfo.CheckReportItems.append(CckRptItem)
            session_add(session, CckRptItem)
            
        CckRpt.CheckReportInfos.append(CckRptInfo)
        session_add(session, CckRptInfo)
        
    patt.CheckReports.append(CckRpt)
    session_add(session, CckRpt)



def WriteTempItem(dt_dict, session, patt):
    TMPItems = dt_dict['Data']['Request']['TempItemInfo']['TempItemInfo']
    
    if type(TMPItems) != list:
        #print('Only One' )
        TMPItems = [TMPItems]
        
        
    for TMPItem in TMPItems: 
        
        if 'TempItemExecInfoS' in TMPItem:
            TMPIExecs = TMPItem.pop('TempItemExecInfoS')
            TMPIExecs = TMPIExecs['TempItemExecInfo']
            if type(TMPIExecs) != list:
                TMPIExecs = [TMPIExecs]
        else:
            TMPIExecs = []

        TmpItmInfo = TempItemInfo(**TMPItem)

        for TMPIExec in TMPIExecs:
            TmpItmExec = TempItemExecInfo(**TMPIExec)

            TmpItmInfo.TempItemExecInfos.append(TmpItmExec)
            session_add(session, TmpItmExec)

        patt.TempItemInfos.append(TmpItmInfo)
        session_add(session, TmpItmInfo)
    
def WriteEPR(dt_dict, session, patt):

    eprRec = EPRecord()
    
    EPR = dt_dict['Data']['EPRdata']
    if EPR == None:
        print(dt_dict)
        return 
    
    if 'OpEMRData' in EPR:
        OEM = EPR['OpEMRData']
        OEM_data = OpEMRData(**OEM)
        eprRec.OpEMRDatas.append(OEM_data)
        session_add(session, OEM_data)

    if 'RANinfo' in EPR:
        RAN = EPR['RANinfo']

        if 'Basicinfo' in RAN:
            Basicinfo = RAN.pop('Basicinfo')
            if type(Basicinfo) == str:
                Basicinfo = '<xml>'  + Basicinfo+ '</xml>'  
                result = xmltodict.parse(Basicinfo)
                Basicinfo = result['xml']
            RAN_info = RANinfo(**Basicinfo, **RAN)

        else:
            RAN_info = RANinfo(**RAN)
            
        eprRec.RANinfos.append(RAN_info)
        session_add(session, RAN_info)
    
    if 'FirstCorinfo' in EPR:
        FCI = EPR['FirstCorinfo']

        # Deleting the name 
        data = FCI['Basicinfo']
        name = data.split('，')[0].replace('患者', '')
        FCI['Basicinfo'] = data.replace(name, 'XX')
        # FCI['Basicinfo']
        
        FCI_info = FirstCorinfo(**FCI)
        eprRec.FirstCorinfos.append(FCI_info)
        session_add(session, FCI_info)
            
    if 'DailyRecdata' in EPR:
        DRe = EPR['DailyRecdata']
        if 'once' in DRe:
            DailyRecs = DRe.pop('once')
            if type(DailyRecs) != list:
                DailyRecs = [DailyRecs]
        else:
            DailyRecs =[]
        
        for DailyRec in DailyRecs:
            DRe_data = DailyRecdata(**DRe, **DailyRec)
            eprRec.DailyRecdatas.append(DRe_data)
            session_add(session, DRe_data)
        
    if 'OperRecdata' in EPR:
        ORd = EPR['OperRecdata']
        if 'once' in ORd:
            OperRecs = ORd.pop('once')
            if type(OperRecs) != list:
                OperRecs = [OperRecs]
        else:
            OperRecs =[]

        for OperRec in OperRecs:
            OperRec = OperRecdata(**ORd, **OperRec)
            eprRec.OperRecdatas.append(OperRec)
            session_add(session, OperRec)

    if 'GetDisRecordinfo' in EPR:
        GDR = EPR['GetDisRecordinfo']
        GDR_info = GetDisRecordinfo(**GDR)
        eprRec.GetDisRecordinfos.append(GDR_info)
        session_add(session, GDR_info)

    if 'hourRec' in EPR:
        HRe = EPR['hourRec']
        HRe_data = hourRec(**HRe)
        eprRec.hourRecs.append(HRe_data)
        session_add(session, HRe_data)
        
    if 'DeathRecordinfo' in EPR:
        DRe = EPR['DeathRecordinfo']
        DRe_info = DeathRecordinfo(**DRe)  
        eprRec.DeathRecordinfos.append(DRe_info)
        session_add(session, DRe_info)
    
    patt.EPRs.append(eprRec)
    session_add(session, eprRec)
    # print(n)


## Total Function
def WritePatientData(dt_dict, session):

    patt = session.query(Patient).filter_by(PatientID = dt_dict['PatientID']).first()
    # 'dt_dict' means the data_dictionary

    if patt == None:
        patt = Patient(PatientID = dt_dict['PatientID'])
        session_add(session, patt)
    # Here we get the patt 

    if dt_dict['DataType'] in [2, 6]:
        WriteFeeList(dt_dict, session, patt)

    elif dt_dict['DataType'] in [3, 7]:
        WriteCheckReport(dt_dict, session, patt)

    elif dt_dict['DataType'] in [4, 8]:
        WriteTempItem(dt_dict, session, patt)

    elif dt_dict['DataType'] in [5, 9]:
        WriteEPR(dt_dict, session, patt)

    else:
        print('Something Wrong in    !')
        print(dt_dict)


    session_add(session, patt)
    session.commit()




if __name__=="__main__":

    engine = sdb_connect(os.getcwd())

    create_table(engine)
    Session = sessionmaker(bind = engine)
    session = Session()

    df = pd.read_json('data/xml_table.json', orient = 'split')

    for ind, dt in df.iterrows():
        dt_dict = dt.to_dict()
        dt_dict['Data'] = xmltodict.parse(dt_dict['Data'] )
        WritePatientData(dt_dict, session)
    
