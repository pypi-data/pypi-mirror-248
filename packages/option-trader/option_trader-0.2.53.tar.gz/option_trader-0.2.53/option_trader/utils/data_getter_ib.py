import pandas as pd
import numpy  as np
import math

from  option_trader.settings import ib_settings
from  option_trader.settings import app_settings   
from  option_trader.admin import quote
from  option_trader.consts import asset as at

from ib_insync import *

import logging


class IBClient:    

    connection = None

    def __init__(self, 
                 host=ib_settings.HostIP, 
                 TWS=ib_settings.TWS, 
                 Live=ib_settings.LIVE, 
                 marketDataType=ib_settings.IBConfig.marketDataType):
        
        self.TWS = TWS
        self.Live = Live
        self.host = host
        self.ib = IB()
        self.marketDataType = marketDataType

        self.logger = logging.getLogger(__name__)

        if TWS:
            self.port = ib_settings.IBConfig.TWS_live.port if Live else ib_settings.IBConfig.TWS_papaer.port
            self.clientID = ib_settings.IBConfig.TWS_live.clientId if Live else ib_settings.IBConfig.TWS_papaer.clientId
        else:
            self.port = ib_settings.IBConfig.Gateway_live.port if Live else ib_settings.IBConfig.Gateway_papaer.port
            self.clientID = ib_settings.IBConfig.Gateway_live.clientId if Live else ib_settings.IBConfig.Gateway_papaer.clientId

        try:
            get_ipython    
            util.startLoop()  # uncomment this line when in a notebook
        except:
            pass      

        try:      
            self.ib= IB()
            self.ib.connect(host, self.port, clientId=self.clientID)            
            # delayed quote
            self.ib.reqMarketDataType(self.marketDataType)            
        except Exception as e:
            self.logger.exception(e)  
            raise e        

    def __enter__(self):
        return self
    def __exit__(self, *args):
        try:
            if self.ib != None:
                self.ib.client.disconnect()
        except Exception as ex:
            self.logger.exception(ex)
            raise ex

    def get_price_history(self, symbol, period="1 Y", interval="1 day", start=None, end=None):    

        contract = Contract()
        contract.symbol = symbol
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        bars = self.ib.reqHistoricalData(
            contract, endDateTime='', durationStr=period,
            barSizeSetting=interval, whatToShow='TRADES', useRTH=True)

        df =  util.df(bars)
        df.rename(columns = {'date':'Date', 'open': quote.OPEN, 'high': quote.HIGH, 'low':quote.LOW,
                             'close':quote.CLOSE, 'volume': quote.VOLUME, 'average': 'Average'}, inplace = True)        
        return df.set_index('Date')
    
    def get_option_leg_details(self, symbol, exp_date, strike, otype):
                            
        if otype == at.CALL:
            otype = 'C'

        if otype == at.PUT:
            otype = 'P'

        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'OPT'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        contract.lastTradeDateOrContractMonth = exp_date #.strftime('%Y%m%d') #'20230512'
        contract.strike = strike
        contract.right = otype
        contract.multiplier = '100'
        self.ib.qualifyContracts(contract) 
        x = self.ib.reqMktData(contract, '', False, False, [])
        self.ib.sleep(5)

        #IBClient.disconnect()    

        if math.isnan(x.bid):
            self.logger.error("Failed to get option quote")
            return None
        
        if x.bid == -1:
            self.logger.error("Cannot get option quote outside market hours")
            return None    

        ne = pd.DataFrame.from_records(quote.option_chain_rec)
        ne.exp_date = exp_date
        ne.strike = strike    
        ne.bid =  x.bid
        ne.bidSize = x.bidSize
        ne.ask = x.ask
        ne.askSize = x.askSize
        ne.lastPrice = x.last
        ne.open = x.open
        ne.high = x.high
        ne.low = x.low
        ne.close = x.close
        ne.openInterest = ne.bidSize
        if x.bidGreeks != None:
            ne.impliedVolatility = x.modelGreeks.impliedVol
            ne.delta = x.modelGreeks.delta
            ne.gamma = x.modelGreeks.gamma
            ne.vega  = x.modelGreeks.vega
            ne.theta = x.modelGreeks.theta
            ne.volume = x.volume
            
        return ne.to_dict('records')[0]

    def get_option_chain(self, symbol, exp_date, stock_price, max_strike_pert=0.05):
             
        x = self.ib.reqMatchingSymbols(symbol)

        conId = x[0].contract.conId

        x = self.ib.reqSecDefOptParams(symbol, "", "STK", conId)
    
        strikes = list(filter(lambda x: x >= stock_price * (1-max_strike_pert) and x <= stock_price * (1+max_strike_pert), x[0].strikes))   
        
        self.ib.reqMarketDataType(3)
            
        call_chain = put_chain = pd.DataFrame()

        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'OPT'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        contract.lastTradeDateOrContractMonth = exp_date #.strftime('%Y%m%d') 

        contract.multiplier = '100'
        
        for strike in strikes:                    
            contract.strike = strike

            contract.right = 'C'   
            self.ib.qualifyContracts(contract) 
            x = self.connection.reqMktData(contract, '', False, False, [])
            self.ib.sleep(5) 

            if math.isnan(x.bid) == False:           
                ne = pd.DataFrame.from_records(quote.option_chain_rec)
                ne.exp_date = exp_date
                ne.strike = strike    
                ne.bid =  x.bid
                ne.bidSize = x.bidSize
                ne.ask = x.ask
                ne.askSize = x.askSize
                ne.lastPrice = x.last
                ne.open = x.open
                ne.high = x.high
                ne.low = x.low
                ne.close = x.close
                ne.openInterest = ne.bidSize

                if x.bidGreeks != None:
                    ne.impliedVolatility = (x.bidGreeks.impliedVol + x.askGreeks.impliedVol) / 2
                    ne.delta = (x.bidGreeks.delta + x.askGreeks.delta) / 2
                    ne.gamma = (x.bidGreeks.gamma + x.askGreeks.gamma) / 2
                    ne.vega =  (x.bidGreeks.vega + x.askGreeks.vega) / 2
                    ne.theta = (x.bidGreeks.theta  + x.askGreeks.theta ) / 2
                    ne.volume = x.volume

                call_chain = pd.concat([call_chain, ne])  

            contract.right = 'P'
            self.connection.qualifyContracts(contract) 
            x = self.connection.reqMktData(contract, '', False, False, [])
            self.connection.sleep(5)                 
        
            if math.isnan(x.bid) == False:           
                ne = pd.DataFrame.from_records(option_chain_rec)
                ne.exp_date = exp_date
                ne.strike = strike    
                ne.bid =  x.bid
                ne.bidSize = x.bidSize
                ne.ask = x.ask
                ne.askSize = x.askSize
                ne.lastPrice = x.last
                ne.open = x.open
                ne.high = x.high
                ne.low = x.low
                ne.close = x.close
                ne.openInterest = ne.bidSize
                                    
                if x.bidGreeks != None:
                    ne.impliedVolatility = (x.bidGreeks.impliedVol + x.askGreeks.impliedVol) / 2
                    ne.delta = (x.bidGreeks.delta + x.askGreeks.delta) / 2
                    ne.gamma = (x.bidGreeks.gamma + x.askGreeks.gamma) / 2
                    ne.vega =  (x.bidGreeks.vega + x.askGreeks.vega) / 2
                    ne.theta = (x.bidGreeks.theta  + x.askGreeks.theta ) / 2
                    ne.volume = x.volume
                    
                put_chain = pd.concat([put_chain, ne])              
                                    
        return call_chain, put_chain

    @staticmethod
    def get_client(host, port, clientID, marketDataType):

        try:
            get_ipython    
            util.startLoop()  # uncomment this line when in a notebook
        except:
            pass        

        if IBClient.connection == None:
            try:      
                ib = IB()
                ib.connect(ic.host, port, clientId=clientID)            
                IBClient.connection = ib
                # delayed quote
                ib.reqMarketDataType(marketDataType)            
                return ib
            except Exception as e:
                #logger.exception(e)          
                return None                  
        else:
            return IBClient.connection
        
    @staticmethod
    def disconnect():
        if IBClient.connection != None:
            IBClient.connection.client.disconnect()
            IBClient.connection = None     

def IB_get_price_history(symbol, period="1 Y", interval="1 day", start=None, end=None):    

    ib = IBClient.get_client()
    
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    bars = ib.reqHistoricalData(
        contract, endDateTime='', durationStr=period,
        barSizeSetting=interval, whatToShow='TRADES', useRTH=True)

    df =  util.df(bars)
    #df.rename(columns = {'date':'Date', 'open':'Open', 'high':'High', 'low':'Low',
    #                     'close':'Close', 'volume':'Volume', 'average':'Average'}, inplace = True)
    
    IBClient.disconnect()
    
    return df.set_index('Date')

from option_trader.consts import asset as at

def get_option_quote(ibClient, symbol, exp_date, strike, otype):

    logger = logging.getLogger(__name__)

    ibClient.ib.reqMarketDataType(3)

    contract = Contract()
    contract.symbol = symbol
    contract.secType = 'OPT'
    contract.exchange = 'SMART'
    contract.currency = 'USD'
    contract.lastTradeDateOrContractMonth = exp_date
    contract.strike = strike
    contract.right = otype
    contract.multiplier = '100'
    ibClient.ib.qualifyContracts(contract) 
    x = ibClient.ib.reqMktData(contract, '', False, False, [])
    ibClient.ib.sleep(ib_settings.SLEEP_TIME)  
    if x.modelGreeks == None:
        logger.warning('No security definition has been found: %s' % str(contract))
        return pd.DataFrame() 

    ne = pd.DataFrame.from_records(quote.option_chain_rec)
    ne.symbol = symbol
    ne.exp_date = exp_date
    ne.strike = strike    
    ne.bid =  x.bid
    ne.bidSize = x.bidSize
    ne.ask = x.ask
    ne.askSize = x.askSize
    ne.lastPrice = x.last
    ne.lastSize = x.lastSize            
    ne.open = x.open
    ne.high = x.high
    ne.low = x.low
    ne.close = x.close
    ne.volume = x.volume

    m = x.modelGreeks                   

    ne.impliedVolatility = m.impliedVol      
    ne.delta = m.delta     
    ne.gamma = m.gamma 
    ne.vega  = m.vega    
    ne.theta = m.theta                                  

    return ne


def get_OTM_geeks(symbol_list, DTE=30, otype='C'):

    logger = logging.getLogger(__name__)

    from datetime import time, date, datetime, timedelta
    from pytz import timezone
    from yahoo_fin import stock_info as si

    df = pd.DataFrame()    
    today = datetime.now(timezone(app_settings.TIMEZONE))    
    with IBClient(ib_settings.HostIP, TWS=ib_settings.TWS, Live=ib_settings.LIVE) as ibClient:
        for symbol in symbol_list:
            logger.debug('Processing %s' % symbol)

            try:
                stock_price = si.get_live_price(symbol)
            except Exception as ex:
                logger.exception(ex)            
                continue

            xs = ibClient.ib.reqMatchingSymbols(symbol)
            x = list(filter(lambda x: (x.contract.secType=='STK') & (x.contract.symbol==symbol) & (x.contract.currency=='USD'), xs))           
            if len(x) == 0:               
                logger.error('%s no match symol' % symbol)
                continue

            conId = x[0].contract.conId
            x = ibClient.ib.reqSecDefOptParams(symbol, "", "STK", conId)
    
            OTM_strike_list = list(filter(lambda x: (x >= (stock_price-2.5)) & (x <= (stock_price+2.5)), x[0].strikes))     
        
            exp_date_target = list(filter(lambda x: (pd.Timestamp(x).tz_localize(timezone(app_settings.TIMEZONE))-today).days - DTE >= 0, x[0].expirations))    
            exp_date = exp_date_target[0]
                    
            for OTM_strike in OTM_strike_list:            
                ne = get_option_quote(ibClient, symbol, exp_date, OTM_strike, 'C')
                if ne.shape[0] == 0:
                    continue
                df = pd.concat([df, ne])  
                break

                #print(exp_date, OTM_strike)
                '''
                contract = Contract()
                contract.symbol = symbol
                contract.secType = 'OPT'
                contract.exchange = 'SMART'
                contract.currency = 'USD'
                contract.lastTradeDateOrContractMonth = exp_date
                contract.strike = OTM_strike
                contract.right = otype
                contract.multiplier = '100'
                ibClient.ib.qualifyContracts(contract) 
                x = ibClient.ib.reqMktData(contract, '', False, False, [])
                #print(x)                
                ibClient.ib.sleep(ib_settings.SLEEP_TIME)  
                if x.modelGreeks == None:
                    logger.warning('No security definition has been found: %s' % str(contract))
                    continue                
                ne = pd.DataFrame.from_records(quote.option_chain_rec)
                ne.exp_date = exp_date
                ne.strike = OTM_strike    
                ne.bid =  x.bid
                ne.bidSize = x.bidSize
                ne.ask = x.ask
                ne.askSize = x.askSize
                ne.lastPrice = x.last
                ne.lastSize = x.lastSize            
                ne.open = x.open
                ne.high = x.high
                ne.low = x.low
                ne.close = x.close
                ne.volume = x.volume
            
                m = x.modelGreeks                   

                ne.impliedVolatility = m.impliedVol      
                ne.delta = m.delta     
                ne.gamma = m.gamma 
                ne.vega  = m.vega    
                ne.theta = m.theta                              
                ne['symbol'] = symbol        
                df = pd.concat([df, ne])  
                break
                '''
    return df

def IB_get_option_leg_details(symbol, exp_date, strike, otype):
    
    logger = logging.getLogger(__name__)

    ib = IBClient.get_client()
    if ib.isConnected() == False:
        logger.error('IB disconnected')

    if otype == at.CALL:
        otype = 'C'

    if otype == at.PUT:
        otype = 'P'

    contract = Contract()
    contract.symbol = symbol
    contract.secType = 'OPT'
    contract.exchange = 'SMART'
    contract.currency = 'USD'
    contract.lastTradeDateOrContractMonth = exp_date.strftime('%Y%m%d') #'20230512'
    contract.strike = strike
    contract.right = otype
    contract.multiplier = '100'
    ib.qualifyContracts(contract) 
    x = ib.reqMktData(contract, '', False, False, [])
    ib.sleep(5)

    #IBClient.disconnect()    

    if math.isnan(x.bid):
        logger.error("Failed to get option quote")
        return None
    
    if x.bid == -1:
        logger.error("Cannot get option quote outside market hours")
        return None    

    ne = pd.DataFrame.from_records(quote.option_chain_rec)
    ne.exp_date = exp_date
    ne.strike = strike    
    ne.bid =  x.bid
    ne.bidSize = x.bidSize
    ne.ask = x.ask
    ne.askSize = x.askSize
    ne.lastPrice = x.last
    ne.lastSize = x.lastSize    
    ne.open = x.open
    ne.high = x.high
    ne.low = x.low
    ne.close = x.close
    ne.openInterest = ne.bidSize
    if x.bidGreeks != None:
        ne.impliedVolatility = x.modelGreeks.impliedVol
        ne.delta = x.modelGreeks.delta
        ne.gamma = x.modelGreeks.gamma
        ne.vega  = x.modelGreeks.vega
        ne.theta = x.modelGreeks.theta
        ne.volume = x.volume
        
    return ne.to_dict('records')[0]

def IB_get_option_chain(symbol, exp_date, stock_price, max_strike_pert=0.05):
        
    logger = logging.getLogger(__name__)  
    try:
        get_ipython    
        util.startLoop()  # uncomment this line when in a notebook
    except:
        pass  

    ib = IBClient.get_client()
    if ib.isConnected() == False:
        logger.error('IB disconnected')

    x = ib.reqMatchingSymbols(symbol)
    conId = x[0].contract.conId

    x = ib.reqSecDefOptParams(symbol, "", "STK", conId)
   
    strikes = list(filter(lambda x: x >= stock_price * (1-max_strike_pert) and x <= stock_price * (1+max_strike_pert), x[0].strikes))   
    
    ib.reqMarketDataType(3)
        
    call_chain = put_chain = pd.DataFrame()

    contract = Contract()
    contract.symbol = symbol
    contract.secType = 'OPT'
    contract.exchange = 'SMART'
    contract.currency = 'USD'
    contract.lastTradeDateOrContractMonth = exp_date.strftime('%Y%m%d') 

    contract.multiplier = '100'
    
    for strike in strikes:                    
        contract.strike = strike

        contract.right = 'C'   
        ib.qualifyContracts(contract) 
        x = ib.reqMktData(contract, '', False, False, [])
        ib.sleep(5) 

        if math.isnan(x.bid) == False:           
            ne = pd.DataFrame.from_records(option_chain_rec)
            ne.exp_date = exp_date
            ne.strike = strike    
            ne.bid =  x.bid
            ne.bidSize = x.bidSize
            ne.ask = x.ask
            ne.askSize = x.askSize
            ne.lastPrice = x.last
            ne.open = x.open
            ne.high = x.high
            ne.low = x.low
            ne.close = x.close
            ne.openInterest = ne.bidSize

            if x.bidGreeks != None:
                ne.impliedVolatility = (x.bidGreeks.impliedVol + x.askGreeks.impliedVol) / 2
                ne.delta = (x.bidGreeks.delta + x.askGreeks.delta) / 2
                ne.gamma = (x.bidGreeks.gamma + x.askGreeks.gamma) / 2
                ne.vega =  (x.bidGreeks.vega + x.askGreeks.vega) / 2
                ne.theta = (x.bidGreeks.theta  + x.askGreeks.theta ) / 2
                ne.volume = x.volume

            call_chain = pd.concat([call_chain, ne])  

        contract.right = 'P'
        ib.qualifyContracts(contract) 
        x = ib.reqMktData(contract, '', False, False, [])
        ib.sleep(5)                 
       
        if math.isnan(x.bid) == False:           
            ne = pd.DataFrame.from_records(option_chain_rec)
            ne.exp_date = exp_date
            ne.strike = strike    
            ne.bid =  x.bid
            ne.bidSize = x.bidSize
            ne.ask = x.ask
            ne.askSize = x.askSize
            ne.lastPrice = x.last
            ne.open = x.open
            ne.high = x.high
            ne.low = x.low
            ne.close = x.close
            ne.openInterest = ne.bidSize
                                
            if x.bidGreeks != None:
                ne.impliedVolatility = (x.bidGreeks.impliedVol + x.askGreeks.impliedVol) / 2
                ne.delta = (x.bidGreeks.delta + x.askGreeks.delta) / 2
                ne.gamma = (x.bidGreeks.gamma + x.askGreeks.gamma) / 2
                ne.vega =  (x.bidGreeks.vega + x.askGreeks.vega) / 2
                ne.theta = (x.bidGreeks.theta  + x.askGreeks.theta ) / 2
                ne.volume = x.volume
                
            put_chain = pd.concat([put_chain, ne])              
                        
    #ib.disconnect()
    
    return call_chain, put_chain


from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from ibapi.utils import floatMaxString, decimalMaxString

from threading import Timer


class get_option_geeks(EWrapper, EClient):

    def __init__(self, mlist):
        EClient.__init__(self, self)
        self.logger = logging.getLogger(__name__)           
        self.mlist = mlist

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
        super().error(reqId, errorCode, errorString, advancedOrderRejectJson)
        self.logger.debug("Error: ", reqId, " ", errorCode, " ", errorString, " ", advancedOrderRejectJson )

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.logger.debug("nextVailid. Id=", orderId)
        self.start(orderId)

    def updatePortfolio(self, contract, position, marketPrice, marketValue,averageCost, unrealizedPNL, realizedPNL, accountName):
        super().updatePortfolio(contract, position, marketPrice, marketValue,averageCost, unrealizedPNL, realizedPNL, accountName)
        self.logger.debug("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:", contract.exchange,
              "Position:", position, "MarketPrice:", marketPrice, "MarketValue:", marketValue, "AverageCost:", averageCost,
              "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL, "AccountName:", accountName)

    def updateAccountValue(self, key, val, currency, accountName):
        super().updateAccountValue(key, val, currency, accountName)
        self.logger.debug("UpdateAccountValue. Key:", key, "Value:", val, "Currency:", currency, "AccountName:", accountName)

    def updateAccountTime(self, timeStamp):
        super().updateAccountTime(timeStamp)
        self.logger.debug("UpdateAccountTime. Time:", timeStamp)

    def accountDownloadEnd(self, accountName):
        super().accountDownloadEnd(accountName)
        self.logger.debug("AccountDownloadEnd. Account:", accountName)

    def tickString(self, reqId, tickType, value):
        super().tickString(reqId, tickType, value)
        self.logger.debug("TickString. TickerId:", reqId, "Type:", TickTypeEnum.toStr(tickType), "Value:", value)

    #def tickSPrice(self, reqId, tickType, value):
    #    super().tickPrice(reqId, tickType, value)
    #    print("TickPrice. TickerId:", reqId, "Type:", TickTypeEnum.toStr(tickType), "Value:", value)

    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        self.logger.debug("TickPrice. TickerId:", reqId, "tickType:", TickTypeEnum.toStr(tickType),"Price:", floatMaxString(price), "CanAutoExecute:", attrib.canAutoExecute,"PastLimit:", attrib.pastLimit, end=' ')
        self.mlist.at[reqId, TickTypeEnum.toStr(tickType)] = price
        if tickType == TickTypeEnum.BID or tickType == TickTypeEnum.ASK:
            self.logger.debug("PreOpen:", attrib.preOpen)

    def tickSize(self, reqId, tickType, size):
        super().tickSize(reqId, tickType, size)
        self.mlist.at[reqId, TickTypeEnum.toStr(tickType)] = size        
        self.logger.debug("TickSize. TickerId:", reqId, "TickType:", TickTypeEnum.toStr(tickType), "Size: ", decimalMaxString(size))            

    def tickGeneric(self, reqId, tickType, value):
        super().tickGeneric(reqId, tickType, value)
        self.logger.debug("TickGeneric. TickerId:", reqId, "TickType:", TickTypeEnum.toStr(tickType), "Value:", floatMaxString(value))

    def marketDataType(self, reqId, marketDataType):
        super().marketDataType(reqId, marketDataType)
        self.logger.debug("marketDataType. ReqId:", reqId, "Type:", marketDataType)

    def managedAccounts(self, accountsList):
        super().managedAccounts(accountsList)
        self.logger.debug(accountsList)

    def tickSnapshotEnd(self, reqId):
        super().tickSnapshotEnd(reqId)
        self.logger.debug("tickSnapshotEnd. ReqId:", reqId)

    """ market data call back for Exchange for Physical
    tickerId -      The request's identifier.
    tickType -      The type of tick being received.
    basisPoints -   Annualized basis points, which is representative of
        the financing rate that can be directly compared to broker rates.
    formattedBasisPoints -  Annualized basis points as a formatted string
        that depicts them in percentage form.
    impliedFuture - The implied Futures price.
    holdDays -  The number of hold days until the lastTradeDate of the EFP.
    futureLastTradeDate -   The expiration date of the single stock future.
    dividendImpact - The dividend impact upon the annualized basis points
        interest rate.
    dividendsToLastTradeDate - The dividends expected until the expiration
        of the single stock future."""
        
    def tickEFP(self,reqId,tickType,basisPoints,formattedBasisPoints,totalDividends,holdDays,
                futureLastTradeDate,dividendImpact,dividendsToLastTradeDate):
        super().tickEFP(reqId,tickType,basisPoints,formattedBasisPoints,totalDividends,holdDays,
                futureLastTradeDate,dividendImpact,dividendsToLastTradeDate)
        
        self.logger.debug("tickEFP. TickerId:", reqId, 
              "TickType:", TickTypeEnum.toStr(tickType), 
              "basePosints:", floatMaxString(basisPoints),
              "formattedBasisPoints:", formattedBasisPoints,
              "totalDividends:", totalDividends,
              "holdDays:", holdDays,
              "futureLastTradeDate:", futureLastTradeDate,
              "dividendImpact:", dividendImpact,
              "dividendsToLastTradeDate:",dividendsToLastTradeDate)
    
    def tickOptionComputation(self,reqId,tickType,tickAttrib,impliedVol,delta,optPrice,pvDividend,gamma,vega,theta,undPrice):
        super().tickOptionComputation(reqId,tickType,tickAttrib,impliedVol,delta,optPrice,pvDividend,gamma,vega,theta,undPrice)
        """This function is called when the market in an option or its
        underlier moves. TWS's option model volatilities, prices, and
        deltas, along with the present value of dividends expected on that
        options underlier are received."""

        #print(self.mlist.at[reqId, 'symbol'], TickTypeEnum.toStr(tickType))
        
        if tickType == TickTypeEnum.DELAYED_MODEL_OPTION or tickType == TickTypeEnum.MODEL_OPTION:
            self.mlist.at[reqId, 'impliedVol'] = impliedVol               
            self.mlist.at[reqId, 'delta'] = delta
            self.mlist.at[reqId, 'gamma'] = gamma
            self.mlist.at[reqId, 'vega'] = vega
            self.mlist.at[reqId, 'theta'] = theta  
            self.mlist.at[reqId, "tickAttrib"] = tickAttrib
            self.mlist.at[reqId, "optPrice"] = optPrice,
            self.mlist.at[reqId, "pvDividend:"] = pvDividend
            self.mlist.at[reqId, "undPrice"] = undPrice                 
    
        self.logger.debug("tickOptionComputation. TickerId:", reqId, 
              "TickType:", TickTypeEnum.toStr(tickType), 
              "tickAttrib:", tickAttrib,
              "impliedVol:", impliedVol,
              "delta:", delta,
              "optPrice:", optPrice,
              "pvDividend:", pvDividend,
              "gamma:", gamma,
              "vega:", vega,
              "theta:",  theta,
              "undPrice:", undPrice)              
    
    def start(self, reqId):
        # Account number can be omitted when using reqAccountUpdates with single account structure
        #self.reqAccountUpdates(True, "U11921459")
        self.reqMarketDataType(3)    
        il = list(self.mlist.index)
        for i in il:  
            symbol = self.mlist.at[i, 'symbol']
            exp_date = self.mlist.at[i, 'exp_date']
            strike = self.mlist.at[i, 'strike']
            if isinstance(exp_date, str) == False:
                self.logger.debug('nan expdate')
                continue
            else:
                self.logger.debug(symbol, exp_date, strike)                   
            contract = Contract()
            contract.symbol = symbol
            contract.secType = 'OPT'
            contract.exchange = 'SMART'
            contract.currency = 'USD'
            contract.lastTradeDateOrContractMonth = exp_date
            contract.strike = strike
            contract.right = 'C'
            contract.multiplier = '100'          
            #self.qualifyContracts(contract) 
            self.reqMktData(i, contract, '', True, False, [])
            import time
            time.sleep(1)

    def stop(self):
        #self.reqAccountUpdates(False, "U11921459")
        self.done = True
        self.disconnect()

class get_account_info(EWrapper, EClient):

    def __init__(self, mlist):
        EClient.__init__(self, self)
        self.logger = logging.getLogger(__name__)           
        self.mlist = mlist

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
        super().error(reqId, errorCode, errorString, advancedOrderRejectJson)
        self.logger.debug("Error: ", reqId, " ", errorCode, " ", errorString, " ", advancedOrderRejectJson )

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.logger.debug("nextVailid. Id=", orderId)
        self.start(orderId)

    def updatePortfolio(self, contract, position, marketPrice, marketValue,averageCost, unrealizedPNL, realizedPNL, accountName):
        super().updatePortfolio(contract, position, marketPrice, marketValue,averageCost, unrealizedPNL, realizedPNL, accountName)
        self.logger.debug("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:", contract.exchange,
              "Position:", position, "MarketPrice:", marketPrice, "MarketValue:", marketValue, "AverageCost:", averageCost,
              "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL, "AccountName:", accountName)

    def updateAccountValue(self, key, val, currency, accountName):
        super().updateAccountValue(key, val, currency, accountName)
        self.logger.debug("UpdateAccountValue. Key:", key, "Value:", val, "Currency:", currency, "AccountName:", accountName)

    def updateAccountTime(self, timeStamp):
        super().updateAccountTime(timeStamp)
        self.logger.debug("UpdateAccountTime. Time:", timeStamp)

    def accountDownloadEnd(self, accountName):
        super().accountDownloadEnd(accountName)
        self.logger.debug("AccountDownloadEnd. Account:", accountName)

    def tickString(self, reqId, tickType, value):
        super().tickString(reqId, tickType, value)
        self.logger.debug("TickString. TickerId:", reqId, "Type:", TickTypeEnum.toStr(tickType), "Value:", value)

    #def tickSPrice(self, reqId, tickType, value):
    #    super().tickPrice(reqId, tickType, value)
    #    print("TickPrice. TickerId:", reqId, "Type:", TickTypeEnum.toStr(tickType), "Value:", value)

    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        self.logger.debug("TickPrice. TickerId:", reqId, "tickType:", TickTypeEnum.toStr(tickType),"Price:", floatMaxString(price), "CanAutoExecute:", attrib.canAutoExecute,"PastLimit:", attrib.pastLimit, end=' ')
        if tickType == TickTypeEnum.BID or tickType == TickTypeEnum.ASK:
            self.logger.debug("PreOpen:", attrib.preOpen)

    def tickSize(self, reqId, tickType, size):
        super().tickSize(reqId, tickType, size)
        self.logger.debug("TickSize. TickerId:", reqId, "TickType:", TickTypeEnum.toStr(tickType), "Size: ", decimalMaxString(size))            

    def tickGeneric(self, reqId, tickType, value):
        super().tickGeneric(reqId, tickType, value)
        self.logger.debug("TickGeneric. TickerId:", reqId, "TickType:", TickTypeEnum.toStr(tickType), "Value:", floatMaxString(value))

    def marketDataType(self, reqId, marketDataType):
        super().marketDataType(reqId, marketDataType)
        self.logger.debug("marketDataType. ReqId:", reqId, "Type:", marketDataType)

    def managedAccounts(self, accountsList):
        super().managedAccounts(accountsList)
        self.logger.debug(accountsList)

    def tickSnapshotEnd(self, reqId):
        super().tickSnapshotEnd(reqId)
        self.logger.debug("tickSnapshotEnd. ReqId:", reqId)

    """ market data call back for Exchange for Physical
    tickerId -      The request's identifier.
    tickType -      The type of tick being received.
    basisPoints -   Annualized basis points, which is representative of
        the financing rate that can be directly compared to broker rates.
    formattedBasisPoints -  Annualized basis points as a formatted string
        that depicts them in percentage form.
    impliedFuture - The implied Futures price.
    holdDays -  The number of hold days until the lastTradeDate of the EFP.
    futureLastTradeDate -   The expiration date of the single stock future.
    dividendImpact - The dividend impact upon the annualized basis points
        interest rate.
    dividendsToLastTradeDate - The dividends expected until the expiration
        of the single stock future."""
        
    def tickEFP(self,reqId,tickType,basisPoints,formattedBasisPoints,totalDividends,holdDays,
                futureLastTradeDate,dividendImpact,dividendsToLastTradeDate):
        super().tickEFP(reqId,tickType,basisPoints,formattedBasisPoints,totalDividends,holdDays,
                futureLastTradeDate,dividendImpact,dividendsToLastTradeDate)
        
        self.logger.debug("tickEFP. TickerId:", reqId, 
              "TickType:", TickTypeEnum.toStr(tickType), 
              "basePosints:", floatMaxString(basisPoints),
              "formattedBasisPoints:", formattedBasisPoints,
              "totalDividends:", totalDividends,
              "holdDays:", holdDays,
              "futureLastTradeDate:", futureLastTradeDate,
              "dividendImpact:", dividendImpact,
              "dividendsToLastTradeDate:",dividendsToLastTradeDate)
    
    def tickOptionComputation(self,reqId,tickType,tickAttrib,impliedVol,delta,optPrice,pvDividend,gamma,vega,theta,undPrice):
        super().tickOptionComputation(reqId,tickType,tickAttrib,impliedVol,delta,optPrice,pvDividend,gamma,vega,theta,undPrice)
        """This function is called when the market in an option or its
        underlier moves. TWS's option model volatilities, prices, and
        deltas, along with the present value of dividends expected on that
        options underlier are received."""

        #print(self.mlist.at[reqId, 'symbol'], TickTypeEnum.toStr(tickType))
        
        if tickType == TickTypeEnum.DELAYED_MODEL_OPTION or tickType == TickTypeEnum.MODEL_OPTION:
            self.mlist.at[reqId, 'delta'] = delta
            self.mlist.at[reqId, 'gamma'] = gamma
            self.mlist.at[reqId, 'vega'] = vega
            self.mlist.at[reqId, 'theta'] = theta    
    
        self.logger.debug("tickOptionComputation. TickerId:", reqId, 
              "TickType:", TickTypeEnum.toStr(tickType), 
              "tickAttrib:", tickAttrib,
              "impliedVol:", impliedVol,
              "delta:", delta,
              "optPrice:", optPrice,
              "pvDividend:", pvDividend,
              "gamma:", gamma,
              "vega:", vega,
              "theta:",  theta,
              "undPrice:", undPrice)              
    
    def start(self, reqId):
        # Account number can be omitted when using reqAccountUpdates with single account structure
        #self.reqAccountUpdates(True, "U11921459")
        self.reqMarketDataType(3)    
        il = list(self.mlist.index)
        for i in il:  
            symbol = self.mlist.at[i, 'symbol']
            exp_date = self.mlist.at[i, 'exp_date']
            strike = self.mlist.at[i, 'strike']
            if isinstance(exp_date, str) == False:
                self.logger.debug('nan expdate')
                continue
            else:
                self.logger.debug(symbol, exp_date, strike)                   
            contract = Contract()
            contract.symbol = symbol
            contract.secType = 'OPT'
            contract.exchange = 'SMART'
            contract.currency = 'USD'
            contract.lastTradeDateOrContractMonth = exp_date
            contract.strike = strike
            contract.right = 'C'
            contract.multiplier = '100'          
            #self.qualifyContracts(contract) 
            self.reqMktData(i, contract, '', True, False, [])
            import time
            time.sleep(1)

    def stop(self):
        #self.reqAccountUpdates(False, "U11921459")
        self.done = True
        self.disconnect()

def build_OTM_option_requests(ml, DTE_list, max_strike_ratio=0.50):
    output = pd.DataFrame()    
    il = list(ml.index)
    #print(il)
    for i in il:
        symbol = ml.at[i, 'symbol']    
        for DTE in DTE_list:
            from  option_trader.utils.data_getter import get_option_chain            
            chain = get_option_chain(symbol, at.CALL, max_strike_ratio=max_strike_ratio, min_days_to_expire=DTE-3, max_days_to_expire=DTE+3)    
            if chain.shape[0] == 0:
                continue
            if chain.shape[0] > 1:
                target = chain.shape[0]//2
            else:
                target = 0
            #print(i, symbol, chain.shape[0], target, output.shape[0])
            df = (chain.iloc[target][['stock_price', 'strike', 'exp_date', 'days to expire', 'delta', 'gamma', 'vega', 'theta']])   
            
            ml.at[i, 'stock_price'] = df.stock_price
            ml.at[i, 'strike'] = df.strike
            ml.at[i, 'exp_date'] = df.exp_date.replace('-','')
            ml.at[i, 'days to expire'] = df['days to expire']
            ml.at[i, 'yahoo delta'] = df.delta
            ml.at[i, 'yahoo gamma'] = df.gamma
            ml.at[i, 'yahoo vega'] = df.vega    
            ml.at[i, 'yahoo theta'] = df.theta        
            output = pd.concat([output, ml.loc[i:i:1]])    
    output.reset_index(drop=True, inplace=True)

    return output

if __name__ == '__main__':

    symbol = 'AAPL'
    exp_date = '2023-11-24'
    stock_price = 190
    host = '127.0.0.1'

    with IBClient(host, TWS=False, Live=True) as tws_live:
        #df = tws_live.get_price_history('AAPL')
        x = tws_live.get_option_leg_details('AAPL', "20231222", 190, at.CALL)        
        print(x)

    #tws_paper = IBClient(host, TWS=True, Live=False)
    #gateway_live = IBClient(host, TWS=False, Live=True)
    #gateway_paper = IBClient(host, TWS=False, Live=False)        

    #print('tws live', tws_live.connection)
    #print('tws papaer', tws_paper.connection)
    #print('gateway live', gateway_live.connection)
    #print('gateway papaer',gateway_paper.connection)


