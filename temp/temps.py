import os
import time
import socket
import struct
import hashlib
import logging
import datetime
import traceback
from config import *
from threading import Thread


# Pseudo Constant 
# this constant are like a global variables for data moving and flags

TIMEN = time.strftime("%Y%m%d")
TOTAL_MODULES = 0
EXIT_FLAG = False
TOTAL_RECORDS = 0
RECORD_TIME = {0: datetime.datetime(1980, 1, 1, 0, 0, 0)}
STACK = []
PROGRAM_TIMER = time.time()
ALL_TIMESTAMP:set = set()
CORRUPTION = False
BOOM = True
TRACKED_TIME = b''
 
# TEMPORAY CHOOPED DATA HOLDER [data chopped by socket.recv]...
BUFFER = b''


CSV_FILE_HEADER = "ResOrdNum,BrkNum,TraderNum,AccountNum,BuySell,OrginalVol,DisclosedVol,RemainingVol,RemainingDisclsVol,Price,STORDERFLAGS,Gtd,FillNum,FillQty,FillPrice,VolFilledToday,ActivityTyp,ActivityTime,OpOrdNumber,OpBrkId,Token,InstrumentName,ConSymbol,ConExpiryDate,ConStrikePrice,ConOptionType,ConCALevel,OpenClose,OldOpenClose,BookType,NewVol,OldAccountNum,Participant,ParticipantOld,ADDORDERFLAGS,ProClient,Pan,OldPan,AlgoId,AlgoCategory,LastModifiedTime,NnfField"
GIVE_UP_HEADERS = "ReasonCode,OrderNumber,FillNumber,InstrumentName,Symbol,ExpiryDate,StrikePrice,OptionType,CALevel,FillVolume,FillPrice,BrokerId,BuySell,whether,BookType,LastModifiedDateTime,InitiatedByControl,OpenClose,Participant,GiveupFlag,Deleted"
NOTIS_ABSENCE_DIC = {
# The Notis expects some value that are not present in the DC response ; so they are filled with these predefined default values as provided
    "BookTypeName":"RL",
    "MarketType":1,
    "CoverUncoverFlag":"UNCOVER",
    "OppositeBrokerId":"NIL",
    "TradeStatus":11,
    "BranchNo":0,
}


# This is logger setup,you can wrap the whole logger setup into if VAR_LOGGING,if you don't want to log errors
logging.basicConfig(
    filename=f"Log_{TIMEN}.log",
    format="%(asctime)s %(message)s",
    filemode="a",
)
logger = logging.getLogger()
if VAR_LOGGING:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.ERROR)

NOTIS_SAVE_DATA_CHOICES = []
NOTIS_CSV_FILE_HEADER = ""

# Notis setups
if NOTIS_FORMAT:
    '''
    How SAVE_DATA_CHOICES variable works

    choose which index of data are to be dumped from the orginal CSV_FILE_HEADER
    # Example:-
    SAVE_DATA_CHOICES = [0,1,2,3,]
    will save data with headers:- ResponseOrderNumber,BrokerNumber,TraderNum,AccountNUM
    the SAVE_DATA_CHOICES holds the indexes of the data to be saved into files and it can be changed to make small chunks of data on your own
    
    # More Examples:-
    
    IF you only want the BrokerNumber,BuySell then you can do such
    
    SAVE_DATA_CHOICES = [1,4] 
    
    this will only save BrokerNumber and BuySell into a file
     
    '''
    # Here I am trying to map the notis header with the dc header so that it can be chaanged dynamically latter insted of harcoding the indexes of the CSV_HEADER array
    matches = "FillNum,TradeStatus,InstrumentName,ConSymbol,ConExpiryDate,ConStrikePrice,ConOptionType,ConSymbol,BookType,BookTypeName,MarketType,TraderNum,BranchNo,BuySell,FillQty,FillPrice,ProClient,AccountNum,Participant,OpenClose,CoverUncoverFlag,ActivityTime,LastModifiedTime,OpOrdNumber,OppositeBrokerId,ActivityTime,NnfField"
    NOTIS_SAVE_DATA_CHOICES = [CSV_FILE_HEADER.split(',').index(i) if i in CSV_FILE_HEADER else i for i in matches.split(",")]


    
    NOTIS_CSV_FILE_HEADER = "TradeNumber,TradeStatus,InstrumentType,Symbol,ExpiryDate,StrikePrice,OptionType,SecurityName,BookType,BookTypeName,MarketType,UserId,BranchNo,BuySell,TradeQty,Price,ProClient,Account,Participant,OpenCloseFlag,CoverUncoverFlag,ActivityTime,LastModifiedTime,OrderNo,OppositeBrokerId,OrderEnteredModDateTime,CTCL"

SAVE_DATA_CHOICES = list(range(0,len(CSV_FILE_HEADER.split(','))))


class LimitedList(list):
    def __init__(self,*args,**kwargs):
        super().__init__(*args)

    def append(self, __object) -> None:
        if len(self) > LIMIT:
            self.pop(0)
        return super().append(__object)

BACK_LOG = LimitedList()

def strftimesec(x) -> str:
    gps_epoch = datetime.datetime(1980, 1, 1, 0, 0, 0)
    utc_datetime = gps_epoch + datetime.timedelta(seconds=x)
    # This give date time in this format 29JUN2023
    return utc_datetime

def write_notis(data_stack,on_exit=False):
    with open(
            f"TRADE_{SEGMENT_NAME}_NOTIS_{TIMEN}.csv",
            "a",
        ) as fl:
            # Kaushik - as header disbaled - 26jul2023
            # TOTAL_RECORDS > 1 --> TOTAL_RECORDS > STACK_SIZE
            # by upKiran - removed the if block as dont need this now and never
            fl.write("\n".join([i[1] for i in data_stack if i]))
            fl.write("\n")

def write_drop_copy(save_csv="", on_exit=False):
    global STACK, PROGRAM_TIMER, TOTAL_RECORDS,BOOM,BACK_LOG
    if save_csv not in BACK_LOG:
        STACK.append(save_csv)
        BACK_LOG.append(save_csv)
        TOTAL_RECORDS += 1
    else:
        print("Skipping Duplicates",end="\r")
    
    if (
        len(STACK) >= STACK_SIZE
        or on_exit
        or (STACK_TIMER <= (time.time() - PROGRAM_TIMER))
    ):
        if DC_FORMAT:
            with open(
                f"TRADE_{SEGMENT_NAME}_DC_{TIMEN}.csv",
                "a",
            ) as fl:
                fl.write("\n".join([i[0] for i in STACK if i]))
                fl.write("\n")


        if NOTIS_FORMAT:
            write_notis(STACK,on_exit=on_exit)


        PROGRAM_TIMER = time.time()
        STACK = []

def to_csv(data):
    save_csv = ["",""]
    save_csv[0] = ",".join([f"{data[i]}" for i in SAVE_DATA_CHOICES])
    temp = ""
    for i in  NOTIS_SAVE_DATA_CHOICES:
        if isinstance(i,int):
            temp+=f"{data[i]},"
        else:
            temp+=f"{NOTIS_ABSENCE_DIC.get(i,i)},"


    # removing the tralling ',' from the end by slicing the csv_string ;
    save_csv[1] = temp[:-1]
    return save_csv


class Errors:
    dic = {
        16001: "ERR_INVALID_USER_TYPE",
        16003: "ERR BAD TRANSACTION CODE",
        16004: "ERR_USER _ALREADY_SIGNED_ON",
        16006: "ERR_INVALID _SIGNON",
        16007: "ERR_SIGNON_NOT_POSSIBLE",
        16041: "ERR INVALID BROKER OR BRANCH",
        16042: "ERR_USER NOT FOUND",
        16056: "ERR_PROGRAM_ERROR",
        16104: "ERR_SYSTEM_ERROR",
        16123: "ERR_CANT_COMPLETE_YOUR_REQUEST",
        16134: "ERR_USER IS_DISABLED",
        16148: "ERR_INVALID_USER_ID",
        16154: "ERR_INVALID_TRADER_ID",
        16285: "ERR_BROKER_NOT_ACTIVE",
    }


class TransactionCode:
    dic = {
        2300: "SIGNON_IN(login requests [Client -> Host])",
        2301: "SIGNON_OUT(loginsucees [Host -> Client])",
        8000: "DROP_COPY_MESSAGE_DOWNLOAD(requests [Client -> Host])",
        2222: "TRADE_CONFIRMATION(drop_copy_response_sucess [Client -> Host])",
        2282: "TRADE_CANCEL_CONFIRM [Host -> Client]",
        2286: "TRADE_CANCEL_REJECT [Host -> Client]",
        2287: "TRADE_MODIFY_CONFIRM [Host -> Client]",
        23506: "HEART_BEAT ([Client -> Host])",
    }


class ContractDesc:
    """
    InstrumentName CHAR 6 0
    Symbol CHAR 10 6
    ExpiryDate LONG 4 16
    StrikePrice LONG 4 20
    OptionType CHAR 2 24
    CALevel SHORT 2 26
    """

    def __init__(self, content: bytes):
        self.content = content
        (
            self.instrument_name,
            self.symbol,
            self.expiry_date,
            self.strike_price,
            self.option_type,
            self.CALevel,
        ) = struct.unpack("!6s10sll2sh", content)
        self.expiry_date = strftimesec(self.expiry_date)
        self.strike_price = float(self.strike_price) if str(self.strike_price).isdecimal() else 0
        self.strike_price /=100
        self.string = f"{self.instrument_name.decode().strip()}|{self.symbol.decode().strip()}|{self.expiry_date.strftime('%d-%b-%Y')}|{self.strike_price:.2f}|{self.option_type.decode().strip()}|{self.CALevel}"
        self.summary = f"Instrument {self.instrument_name.decode().strip()} with symbol {self.symbol.decode().strip()}"


class AddOrdFlg:
    def __init__(self, content: bytes):
        self.content = content
        self.COL = bin(struct.unpack("!b", content)[0])[2:].zfill(8)[6]
        self.string = f"{bool(self.COL)}"


class StOdrFlg:
    FLAGS = [
        "ATO",
        "Market",
        "MIT",
        "Day",
        "GTC",
        "IOC",
        "AON",
        "MF",
        "MatchedInd",
        "Traded",
        "Modified",
        "Frozen",
        "PreOpen",
        "__reserved",
        "__reserved",
        "__reserved",
    ]

    def __init__(self, data: bytes):
        self.bits = [bit for bit in "".join([f"{bin(c)[2:].zfill(8)}" for c in data])]
        self.dic = {i: bool(int(j)) for i, j in zip(self.FLAGS[:-3], self.bits[:-3])}
        self.string = "|".join(
            [i for i, j in zip(self.FLAGS[:-3], self.bits[:-3]) if int(j)]
        )



class Packer:
    _sequence = 0

    def __init__(self, messagedata: bytes):
        self.length = 22 + len(messagedata)
        self.checksum = hashlib.md5(messagedata)
        self.checksum = self.checksum.digest()
        Packer._sequence += 1
        self.packet = struct.pack(
            f"!hl16s{len(messagedata)}s",
            self.length,
            Packer._sequence,
            self.checksum,
            messagedata,
        )


class MESSAGE:
    def __init__(
        self,
        TransactionCode: int,
        LogTime: int,
        AlphaChar: str,
        TraderId: int,
        ErrorCode: int,
        TimeStamp: int,
        TimeStamp1: str,
        TimeStamp2: str,
        MessageLength: int,
    ):
        self.TransactionCode = TransactionCode
        self.LogTime = LogTime
        self.AlphaChar = (
            AlphaChar if isinstance(AlphaChar, bytes) else str(AlphaChar).encode()
        )
        self.TraderId = TraderId
        self.ErrorCode = ErrorCode
        self.TimeStamp = TimeStamp
        self.TimeStamp1 = (
            TimeStamp1 if isinstance(TimeStamp1, bytes) else str(TimeStamp1).encode()
        )
        self.TimeStamp2 = (
            TimeStamp2 if isinstance(TimeStamp2, bytes) else str(TimeStamp2).encode()
        )
        self.MessageLength = MessageLength
        self.buffer = self.pack()

    def repack(self):
        self.buffer = self.pack()

    def pack(self):
        return struct.pack(
            "!hl2slhQ8s8sh",
            self.TransactionCode,
            self.LogTime,
            self.AlphaChar,
            self.TraderId,
            self.ErrorCode,
            self.TimeStamp,
            self.TimeStamp1,
            self.TimeStamp2,
            self.MessageLength,
        )

    @staticmethod
    def login(USER_ID, PASSWORD, BROKER_ID, TRADER_ID) -> bytes:
        logging.info(
            f"Login Payload[Message] with datas \n\t\t([+]) userid = {USER_ID} || password = {'*'*len(PASSWORD)} || BROKER_ID = { BROKER_ID} || TraderId = { TRADER_ID}"
        )
        body = LOGIN_BODY(USER_ID, PASSWORD, BROKER_ID)
        header = MESSAGE(2300, 0, 0, TRADER_ID, 0, 0, 0, 0, 40 + len(body.buffer))
        return Packer(header.buffer + body.buffer).packet

    @staticmethod
    def dropcopy(session_header, AlphaChar) -> bytes:
        header = MESSAGE(8000, 0, AlphaChar, session_header.TraderId, 0, 0, 0, 0, 48)
        if not RESUME_DOWNLOAD:
            c = 0
        else:
            c = track_me(None, module=0)
            if len(c)==8:
                c = struct.unpack("!d",c)[0]
            else:
                c=0
        pg = struct.pack("!40sd", header.buffer, float(c))
        logging.info(
            f"DropCopy PayLoad[Message] with datas \n\t\t([+]) TraderId = {header.TraderId} || AlphaChar/ConnectionId = {header.AlphaChar} || timestamp = {float(c)}"
        )
        payload = Packer(pg).packet
        logging.info(f"DropCopy Requests {payload}")
        return payload

    @staticmethod
    def hearbeat(TRADER_ID):
        logging.info(f"HeartBeat....")
        header = MESSAGE(23506, 0, 0, TRADER_ID, 0, 0, 0, 0, 40)
        return Packer(header.buffer).packet

    @staticmethod
    def unpack(data):
        data = data.encode() if isinstance(data, str) else data
        (
            TransactionCode,
            LogTime,
            AlphaChar,
            TraderId,
            ErrorCode,
            TimeStamp,
            TimeStamp1,
            TimeStamp2,
            MessageLength,
        ) = struct.unpack("!hl2slhQ8s8sh", data)
        return MESSAGE(
            TransactionCode,
            LogTime,
            AlphaChar,
            TraderId,
            ErrorCode,
            TimeStamp,
            TimeStamp1,
            TimeStamp2,
            MessageLength,
        )

    def __str__(self):
        return f"""
        TransactionCode:- {self.TransactionCode}
        LogTime:- {self.LogTime}
        AlphaChar:- {self.AlphaChar}
        TraderId:- {self.TraderId}
        ErrorCode:- {self.ErrorCode}
        TimeStamp:- {self.TimeStamp}
        TimeStamp1:- {self.TimeStamp1}
        TimeStamp2:- {self.TimeStamp2}
        Error:- {Errors.dic.get(self.ErrorCode,"No Errors"),self.ErrorCode}
        """


class LOGIN_BODY:
    _resev8 = b"\x00" * 8
    _resev38 = b"\x00" * 38
    _resev117 = b"\x00" * 117
    _resev16 = b"\x00" * 16
    _resev4 = b"\x00"*4

    def __init__(self, userid: int, password: str, bid: str) -> None:
        self.userid = userid
        self.password = password.encode() if isinstance(password, str) else password
        self.bid = bid.encode() if isinstance(bid, str) else bid
        self.buffer = self.pack()

    def pack(self):
        # changes:-
        #  password from 8s -> 12s
        #  after password reserved 8s -> 4s 
        #  after password reserved 117s -> 119s 
        return struct.pack(
            "!l8s12s4s38s5s119s16s16s16s",
            self.userid,
            self._resev8,
            self.password,
            self._resev8,
            self._resev38,
            self.bid,
            self._resev117,
            self._resev16,
            self._resev16,
            self._resev16,
        )

    @staticmethod
    def unpack(data):
        if isinstance(data, str):
            data = data.encode()
        (
            userid,
            _resev8,
            password,
            _resev8,
            _resev38,
            bid,
            _resev117,
            _resev16,
            _resev16,
            _resev16,
        ) = struct.unpack("!l8s8s8s38s5s117s16s16s16s", data)
        return LOGIN_BODY(userid, password, bid)

    def __str__(self):
        return f"""
        UserId:- {self.userid}
        Password:-{self.password.decode()}
        BrokerId:- {self.bid.decode()}
        """


class Response:
    def __init__(self, response_bytes: bytes=None):
        logging.info(
            f"Response Content (for_analysis_if_error) \n\t\t([+]) content = {response_bytes}"
        )
        self.content = response_bytes
        self.unpack()
        self.checksum = self.check_checksum()
        self.error = self.check_errors()

    def unpack(self):
        (
            self.unp_length,
            self.unp_sequence,
            self.unp_checksum,
            self.unp_messagedata,
        ) = struct.unpack(f"!hl16s{len(self.content)-22}s", self.content)

    def check_checksum(self) -> bool:
        if self.unp_checksum != hashlib.md5(self.unp_messagedata).digest():
            logging.info(
                f"Error in Response_Class ([+]) CheckSum Failed !!! [Data is corrupted]"
            )
            return True
        return False

    def check_errors(self) -> bool:
        self.header = MESSAGE.unpack(self.unp_messagedata[:40])
        self.body = self.unp_messagedata[40:]
        err = Errors.dic.get(self.header.ErrorCode, False)
        if err:
            logging.info(f"Error in Response_Class ([+]) error  = {err}")
            print(f"\t\t!!!Error!!!\n\t{err}\n")
        return bool(err)

    def __str__(self):
        return f"{self.content}"


class DropCopy:
    def __init__(self, response_bytes: bytes, th_id: int):
        global RECORD_TIME
        self.data = list(struct.unpack(
            "!d5scl10shlllll2slllll2sld5scl28sccccl10s12s12s1sccc10s10slhqd44s",
            response_bytes
        ))

        # poping the reserved bytes/ padding bytes
        self.data.pop(2)
        self.data.pop(20)
        self.data.pop(25)
        self.data.pop(30)
        self.data.pop(31)
        self.data.pop(37)

        self.clean()

        # self.save_csv = ",".join(
        #     [str(self.data[i]).strip() for i in SAVE_DATA_CHOICES]
        # )
        
        if self.data[17] > RECORD_TIME.get(
            th_id, datetime.datetime(1980, 1, 1, 0, 0, 0)
        ):
            RECORD_TIME[th_id] = self.data[17]
        self.data[17] = self.data[17].strftime("%d %b %Y %H:%M:%S").upper()
        # self.data[-2] = datetime.datetime.fromtimestamp(int(self.data[-2]) / 1e9).strftime("%d %b %Y %H:%M:%S")
        self.data[-2] = strftimesec(int(self.data[-2]) / 1e9).strftime("%d %b %Y %H:%M:%S")
        self.save_csv = to_csv(self.data)
        write_drop_copy(save_csv=self.save_csv)

    def clean(self):
        '''
        You can remove whole bunch of lines from here which has absolute no operation, I have kept their just so 
        it's easier to add any changes like conversion or translation of data later on
        line marked with one '#' are removeable same for CM
        '''

        self.data[0] = int(self.data[0])
        self.data[1] = int(self.data[1])
        self.data[2] = self.data[2] #
        self.data[3] = self.data[3].decode("utf-8").strip()
        self.data[4] = self.data[4] #
        self.data[5] = self.data[5] #
        self.data[6] = self.data[6] #
        self.data[7] = self.data[7] #
        self.data[8] = self.data[8] #
        self.data[9] = f"{float(self.data[9])/100:.2f}" #
        self.data[10] = StOdrFlg(self.data[10]).string
        self.data[11] = self.data[11] #
        self.data[12] = self.data[12] #
        self.data[13] = self.data[13] #
        self.data[14] =  f"{float(self.data[14])/100:.2f}" #wd
        self.data[15] = self.data[15] #
        self.data[16] = self.data[16].decode("utf-8").strip()
        self.data[17] = strftimesec(self.data[17])
        self.data[18] = int(self.data[18])
        self.data[19] = self.data[19].decode("utf-8").strip()
        self.data[20] = self.data[20] #
        self.data[21] = ContractDesc(self.data[21])
        self.data[22] = self.data[22].decode("utf-8").strip()
        self.data[23] = self.data[23].decode("utf-8").strip()
        self.data[24] = self.data[24].decode("utf-8").strip()
        self.data[25] = self.data[25] #
        self.data[26] = self.data[26].decode(
                    "utf-8"
                    ).strip()
        self.data[27] = self.data[27].decode("utf-8").strip()
        self.data[28] = self.data[28].decode(
                "utf-8"
                ).strip()
        self.data[29] = AddOrdFlg(self.data[29]).string
        self.data[30] = self.data[30].decode("utf-8").strip()
        self.data[31] = self.data[31].decode("utf-8").strip()
        self.data[32] = self.data[32].decode("utf-8").strip()
        self.data[33] = self.data[33] #
        self.data[34] = self.data[34] #
        self.data[35] = self.data[35] #
        self.data[36] = int(self.data[36])


        # Here I am spreading the Contract Descriptions into their own column as suggested
        # And due to this the column shifted,so to overcome that I have kept the old ContractDesc column but now it will have a summary of the contract, :D

        # self.data.extend([i for i in self.data[21].string.split('|')])
        # self.data[21] = self.data[21].summary
        self.data[:] = self.data[:21]+[i for i in self.data[21].string.split('|')]+ self.data[22:]


class GiveUp:

    option_type = {
        "CE": "CALL OPTION",
        "PE": "PUT OPTION",
        "XX": "FUTURES Contract"
          }
    
    book_type = {
        1:"Regular lot order",
        2:"Special terms order",
        3:"Stop loss / MIT order"
            }
    

    def __init__(self,content) -> None:
        self.error = False
        if len(content)!=82:
            self.error = True
            return
        self.data = list(struct.unpack("!hdl6s10sll2shll5schhlccc12sccc",content))
        self.clean()

        self.save_csv = ",".join([str(i) for i in self.data])
        with open(f"GIVE_UP_{TIMEN}.csv","a") as fp:
            fp.write(f"{self.save_csv}\n")


    def clean(self):
        self.data[0] = int(self.data[0])
        self.data[1] = int(self.data[1])
        self.data[2] = int(self.data[2])
        self.data[3] = self.data[3].decode("utf-8").strip()
        self.data[4] = self.data[4].decode("utf-8").strip()
        self.data[5] = strftimesec(self.data[5]).strftime("%d-%b-%Y")
        self.data[6] = int(self.data[6])
        self.data[7] = self.option_type.get(self.data[7].decode("utf-8").strip(),' ')
        self.data[8] = int(self.data[8])
        self.data[9] = int(self.data[9])
        self.data[10] = int(self.data[10])
        self.data[11] = self.data[11].decode("utf-8").strip()
        self.data[12] = self.data[12].decode("utf-8").strip()
        self.data[13] = int(self.data[13])
        self.data[14] = self.book_type.get(int(self.data[14]))
        self.data[15] = strftimesec(self.data[15]).strftime("%d-%b-%Y")
        self.data[16] = self.data[16].decode("utf-8").strip()
        self.data[17] = self.data[17].decode("utf-8").strip()
        self.data[18] = self.data[18].decode("utf-8").strip()
        self.data[19] = self.data[19].decode("utf-8").strip()
        self.data[20] = self.data[20].decode("utf-8").strip()
        self.data[21] = self.data[21].decode("utf-8").strip()

        self.data.pop() # poping last filler byte
        self.data.pop(-4) # poping reserved byte/padding byte
        self.data.pop(12)
        

def files_ready():
    '''
    This Function basically sets the file csv header and stuff at the begening and create the file if file doesnot exists;
    This is also responsilbe for removing the old tracker file
    '''

    global TOTAL_RECORDS
    logging.info("Making necessary File adjustments...")
    drop_file = f"TRADE_{SEGMENT_NAME}_DC_{TIMEN}.csv"
    if not os.path.exists(drop_file) and DC_FORMAT:
        with open(drop_file, "w") as fp:
            fp.write(",".join([CSV_FILE_HEADER.split(',')[i] for i in SAVE_DATA_CHOICES]))
            fp.write("\n")

        # Remove the old tracker if their is no DC file associated with exsits
        if os.path.exists("tracker.timeInFloat"):
            os.remove("tracker.timeInFloat")
    else:
        with open(drop_file, "r") as fp:
            TOTAL_RECORDS = len(fp.readlines()) - 1
    if not os.path.exists(f"GIVE_UP_{TIMEN}.csv") and GIVE_UP_SAVE:
        with open(f"GIVE_UP_{TIMEN}.csv","a") as fp:
            fp.write(",".join([i for i in GIVE_UP_HEADERS.split(',')]))
            fp.write("\n")


    notis_path = f"TRADE_{SEGMENT_NAME}_NOTIS_{TIMEN}.csv"
    # commented - kaushik - 26jul2023 - header not needed
    #if not os.path.exists(notis_path) and NOTIS_FORMAT:
    #    with open(notis_path,"w") as fp:
    #        fp.write(",".join([i for i in NOTIS_CSV_FILE_HEADER.split(',')]))

    logging.info("File adjustments Completed.")

def backloger(on_exit=False):
    global BACK_LOG
    if on_exit:
        with open("BACK_LOG.data","w") as fp:
            fp.write("\n".join(BACK_LOG))
            fp.write("\n")
    elif os.path.exists("BACK_LOG.data"):
        with open("BACK_LOG.data","rb") as fp:
            temp = fp.readlines()
            BACK_LOG = LimitedList(temp)



def suspend(till):
    '''
    The Whole purpose of this function is as NOP or No Operation, during this the client wait for a while when it has reached the
    current realtime of data from server
    '''
    period = 0
    while (not EXIT_FLAG) and (period <= till):
        time.sleep(1)
        period += 1

def track_me(timestamp: bytes = None, module=0):
    '''
    This function keeps track of last, 'Time' the dropcopy was rechived inorder to continue from their on next boot or start or restart
    If this file is present
    '''
    if timestamp:
        with open("tracker.timeInFloat", "wb") as fl:
            fl.write(timestamp)
    else:
        if os.path.exists("tracker.timeInFloat"):
            with open("tracker.timeInFloat", "rb") as fl:
                return fl.read()
        else:
            return '\x00'


def chunker(response):
    global BUFFER
    total = BUFFER + response
    BUFFER = b''
    while True and total:
        length = int(struct.unpack(f"!h", total[:2])[0])
        if len(total) < length:
            BUFFER = total
            break
        yield total[:length]
        total = total[length:]



def response_parse(response):
    global CORRUPTION,TRACKED_TIME
    last_rec_time = None
    for chunk in chunker(response):
        SESSION = Response(chunk)
        if SESSION.error or SESSION.checksum:
            CORRUPTION = True
            exit(1)

        elif SESSION.header.TransactionCode == 2222:
            last_rec_time = SESSION.header.TimeStamp1
            TRACKED_TIME = last_rec_time
            # print(struct.unpack("!d",TRACKED_TIME)[0]) #cback
            DropCopy(SESSION.body,0)
        elif SESSION.header.TransactionCode == 4506 or SESSION.header.TransactionCode == 4507:
            last_rec_time = SESSION.header.TimeStamp1
            GiveUp(SESSION.body)
        else:
            print("TransactionCode",SESSION.header.TransactionCode," [+] ",
                TransactionCode.dic.get(SESSION.header.TransactionCode, "Unknown"),end="\r"
            )
            logging.error( f"""TransactionCode,{SESSION.header.TransactionCode}, [+]
                {TransactionCode.dic.get(SESSION.header.TransactionCode,"Unknown")}""")
    
    # track_me(last_rec_time)
        
       




def worker_function(client_socket, SESSION):
    '''
    This function is the main thread of the work or task, It handels data buffring and client server interactions like,
        downloading dropcopy
        sending heartbeat
        handling giveup responses

    This is the mainloop of the program
    '''
    global CORRUPTION
    module = 0
    if not os.path.exists("tracker.timeInFloat"):
        with open("tracker.timeInFloat", "wb") as fl:
            fl.write(b"\x00")
    start_time = time.time()

    while BOOM:
        elapsed_time = time.time() - start_time
        if elapsed_time > 29:
            print("SENDING HEART_BEAT.......", end="\n")
            logging.info("Sending HeartBeat...")
            heart_beat = MESSAGE.hearbeat(SESSION.header.TraderId)
            client_socket.send(heart_beat)
            start_time = time.time()
        try:
            response = client_socket.recv(RECIVE_SIZE)
            logging.info(f"The recived data is {response}")
            response_parse(response)
            
        except socket.timeout:
            logging.info("SocketTimeOut {response}")
            print("[socket timeout]")
            print("Suspending For A while...")

            # recalcuting time as socketmight have hold the time for longer and olde elapsed it decayed
            # dont use `elapsed_time` as it is most probably off by `SOCKT_TIMEOUT` seconds
            elsp = time.time() - start_time
            suspend(29-elsp)
            continue
      
        time.sleep(DELAY_DURATION)

    # Keep track of last proper DropCopy Response 




def display():
    '''
    This is just a pseudo function that's whole job is to show the stat of the current data and lasttime
    '''
    message = f"""Press 'ctrl+c' to exit | TotalRecords: {TOTAL_RECORDS} | Last Record Time Per Module:- """+"/".join([str(i)+'[ ' +str(RECORD_TIME[i]).split(' ')[-1].strip()+' ] ' for i in RECORD_TIME])
    print(message,end="\r")
    
def set_flag():
    '''
    This sets the flag to terminate the program on huge data corruption or keyboard interrupts or any sorts of kill signals
    '''
    global EXIT_FLAG,BOOM
    BOOM=False
    EXIT_FLAG = True

def linear(client_socket, SESSION):
    '''
    This just calls the worker function in a fancier way so that the crash is handles in a nice manner
    '''
    try:
        while not EXIT_FLAG and not CORRUPTION:
            worker_function(client_socket, SESSION)

    except Exception as e:
        with open("Trackback.log","a") as fp:
            fp.write(f"{'#'*5}\t\tError Track Back Of {TIMEN}\t\t{'#'*5}\n\n")
            traceback.print_tb(e.__traceback__, limit=1000, file=fp)
            fp.write(f"\n {'#'*5}\t\t TLDR  error name [ {e} ] \t\t{'#'*5}\n\n")
        set_flag()

def main():
    '''
    This function sets up the ground work like
        calling the file ready function to make all necessary files ready
        logging into the server 
        pining all the server modules for dropcopy requests
        and calling the display function
    '''

    global TOTAL_MODULES
    files_ready()
    backloger()

    logging.info(f"Connection Stablishing.....")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.settimeout(SOCKET_TIMEOUT)
    logging.info(rf"Connection Stablished Sucessfully. ( {HOST}:{PORT} )")

    login_data = MESSAGE.login(USER_ID, PASSWORD, BROKER_ID, TRADER_ID)
    client_socket.send(login_data)
    response = client_socket.recv(1024)
    SESSION = Response(response)
    if SESSION.header.TransactionCode == 2301 and (
        not (SESSION.error or SESSION.checksum)
    ):
        logging.info("SucessFull Login")
        print("Login SucessFull")
    else:
        logging.info("Login Failed")
        print("\tLogin Failed. TryAgain")
        if EXIT_ON_LOGIN_FAIL:
            exit()

    SESSION.header.repack()
    TOTAL_MODULES = SESSION.header.AlphaChar[0]
    for module in range(1, int(SESSION.header.AlphaChar[0])+1):
        print("Making New Drop Copy requests for module :-",module)
        drop_copy = MESSAGE.dropcopy(SESSION.header, module)
        client_socket.send(drop_copy)
    
    th = Thread(target=linear,args = (client_socket,SESSION))
    th.start()
    try:
        while  BOOM:
            display()
            time.sleep(0.2)
    except KeyboardInterrupt as k:
        set_flag()
    th.join()
    
    print("\n\nWriting the STACK data to file before exiting ")
    track_me(TRACKED_TIME)
    write_drop_copy("", on_exit=True)
    backloger(on_exit=True)
    print("Exiting...")


if __name__ == "__main__":
    main()