import pandas as pd
import numpy  as np
import math

from  option_trader.settings import ib_settings
from  option_trader.settings import app_settings   
from  option_trader.admin import quote
from  option_trader.consts import asset as at

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.ticktype import TickTypeEnum
from ibapi.utils import floatMaxString, decimalMaxString
from ibapi.account_summary_tags import AccountSummaryTags
from ibapi.contract import Contract, ComboLeg, ContractDetails
from ibapi.order import *

from threading import Timer

#from ib_insync import *

import logging

class IBClient:    

    def __init__(self, 
                 host=ib_settings.HostIP, 
                 TWS=ib_settings.TWS, 
                 Live=ib_settings.LIVE, 
                 marketDataType=ib_settings.IBConfig.marketDataType):
        
        self.TWS = TWS
        self.Live = Live
        self.host = host

        self.marketDataType = marketDataType

        self.logger = logging.getLogger(__name__)

        if TWS:
            self.port = ib_settings.IBConfig.TWS_live.port if Live else ib_settings.IBConfig.TWS_papaer.port
            self.clientID = ib_settings.IBConfig.TWS_live.clientId if Live else ib_settings.IBConfig.TWS_papaer.clientId
        else:
            self.port = ib_settings.IBConfig.Gateway_live.port if Live else ib_settings.IBConfig.Gateway_papaer.port
            self.clientID = ib_settings.IBConfig.Gateway_live.clientId if Live else ib_settings.IBConfig.Gateway_papaer.clientId
      
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        return

    def get_option_contId(self, symbol, exp_date, strike, otype):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'OPT'
        contract.exchange = 'SMART'
        contract.lastTradeDateOrContractMonth = exp_date
        contract.strike = strike
        contract.right = otype
            #put_contract.multiplier = '100' 
        with contract_details(contract) as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(ib_settings.SLEEP_TIME, app.stop)
            t. start()            
            app.run()
            t.cancel()  
            return app.conId
        
    def get_option_snapshot_guote(self, symbol, exp_date, strike, otype):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'OPT'
        contract.exchange = 'SMART'
        contract.lastTradeDateOrContractMonth = exp_date
        contract.strike = strike
        contract.right = otype

            #put_contract.multiplier = '100' 
        with snapshot_guote(contract) as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(ib_settings.SLEEP_TIME, app.stop)
            t. start()            
            app.run()
            t.cancel()            
            return app.quotes, contract
            
    def get_stock_snapshot_guote(self, symbol):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
            #put_contract.multiplier = '100' 
        with snapshot_guote(contract) as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(ib_settings.SLEEP_TIME, app.stop)
            t. start()            
            app.run()
            t.cancel()  
            return app.quotes, contract

    def get_spread_option_guote(self, symbol, optionLegs):
        spread_contract = Contract()
        spread_contract.symbol = symbol
        spread_contract.secType = "BAG"
        spread_contract.currency = "USD"
        spread_contract.exchange = "SMART"
        spread_contract.comboLegs = optionLegs          
            #put_contract.multiplier = '100' 
        with snapshot_guote(spread_contract) as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(ib_settings.SLEEP_TIME, app.stop)
            t. start()            
            app.run()
            t.cancel()            
            return app.quotes, spread_contract

    def get_accounts_summary(self):
        with accounts_summary() as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(ib_settings.SLEEP_TIME, app.stop)
            t. start()            
            app.run()
            t.cancel()            
            return app.accountSummary_df
        
    def get_accounts_values_profolio(self):
        with accounts_values_profolio() as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(ib_settings.SLEEP_TIME, app.stop)
            t. start()            
            app.run()
            t.cancel()            
            return app.accountValue_dict, app.accountPortfolio_df        

    def get_option_geeks(self, ml):
        with option_geeks(ml) as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(ib_settings.SLEEP_TIME, app.stop)
            t. start()            
            app.run()
            t.cancel()            
            return ml      
        
    def get_accounts_positions(self):
        with accounts_positions() as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(ib_settings.SLEEP_TIME, app.stop)
            t. start()            
            app.run()
            t.cancel()            
            return app.pos  
        
    def get_account_list(self):
        with ib_app_base() as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(1, app.stop)
            t. start()            
            app.run()
            t.cancel()            
            return app.accountList

    def go_place_order(self, contract, order):
        with place_order(contract, order) as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(ib_settings.SLEEP_TIME, app.stop)
            t. start()            
            app.run()
            t.cancel()            
            return app.status  
                                  
class ComboOptionLeg(ComboLeg):
    def __init__(self, symbol, exp_date, strike, otype, ratio, action, conId=None, ibClient=None):
        super().__init__()
        self.symbol = symbol
        self.exp_date = exp_date
        self.strike = strike
        self.otype = otype
        self.ratio = ratio
        self.action = action
        self.exchange = "SMART"        
        self.conId = conId if conId != None else ibClient.get_option_contId(symbol, exp_date, strike, otype)
class ib_app_base(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)
        self.logger = logging.getLogger(__name__)           

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        if self.isConnected():
            self.stop()

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

    def updatePortfolio(
        self,
        contract: Contract,
        position: float,
        marketPrice: float,
        marketValue: float,
        averageCost: float,
        unrealizedPNL: float,
        realizedPNL: float,
        accountName: str,
    ):  
        super().updatePortfolio(contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName)

        self.logger.debug('updatePortfolio position=', position, 
                ' marketPrice=', marketPrice, 
                ' marketValue=', marketValue,
                ' averageCost=', averageCost,
                ' unrealizedPNL=', unrealizedPNL,
                ' realizedPNL=', realizedPNL,
                ' accountName=', accountName)
        
        self.logger.debug("updatePortfolio contract. conId:", contract.conId,
                " symbol=", contract.symbol,
                " secType=", contract.secType,
                " lastTradeDateOrContractMonth=", contract.lastTradeDateOrContractMonth,
                " strike=", contract.strike,
                " right=", contract.right,
                " multiplier=", contract.multiplier,
                " exchange=", contract.exchange,
                " primaryExchange=", contract.primaryExchange,
                " currency=", contract.currency,
                " localSymbol=", contract.localSymbol,
                " tradingClass=", contract.tradingClass,              
                " includeExpired=", contract.includeExpired,   
                " secIdType=", contract.secIdType,   
                " secId=", contract.secId,   
                " description=", contract.description,   
                " issuerId=", contract.issuerId,   
                    # combos              
                " comboLegsDescrip=", contract.comboLegsDescrip,
                " comboLegs=", contract.comboLegs,
                " deltaNeutralContract=", contract.deltaNeutralContract)        

    def tickString(self, reqId, tickType, value):
        super().tickString(reqId, tickType, value)
        self.logger.debug("TickString. TickerId:", reqId, "Type:", TickTypeEnum.toStr(tickType), "Value:", value)

    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        self.logger.debug("TickPrice. TickerId:", reqId, "tickType:", TickTypeEnum.toStr(tickType),"Price:", floatMaxString(price), "CanAutoExecute:", attrib.canAutoExecute,"PastLimit:", attrib.pastLimit, end=' ')

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
        self.accountList = accountsList[:-1].split(",")

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
            
    def accountSummary(self, reqId, account, tag, value, currency):
        """Returns the data from the TWS Account Window Summary tab in
        response to reqAccountSummary()."""        
        super().accountSummary(reqId, account, tag, value, currency)
        self.logger.debug('accountSummary, reqId=%d account=%s tag=%s value=%s, currency=%s' % (reqId, account, tag, str(value), currency))
    
    def accountSummaryEnd(self, reqId: int):
        """This method is called once all account summary data for a
        given request are received."""
        super().accountSummaryEnd(reqId)
        self.logger.debug('accountSummaryEnd, reqId %d' % reqId)
            
    def position(self, account, contract, position, avgCost):
        """This event returns real-time positions for all accounts in
        response to the reqPositions() method."""
        super().position(account, contract, position, avgCost)        
        self.logger.debug("position. account:", account, " position=", position, "avgCost=", avgCost )
        self.logger.debug("contract. conId:", contract.conId,
              " symbol=", contract.symbol,
              " secType=", contract.secType,
              " lastTradeDateOrContractMonth=", contract.lastTradeDateOrContractMonth,
              " strike=", contract.strike,
              " right=", contract.right,
              " multiplier=", contract.multiplier,
              " exchange=", contract.exchange,
              " primaryExchange=", contract.primaryExchange,
              " currency=", contract.currency,
              " localSymbol=", contract.localSymbol,
              " tradingClass=", contract.tradingClass,              
              " includeExpired=", contract.includeExpired,   
              " secIdType=", contract.secIdType,   
              " secId=", contract.secId,   
              " description=", contract.description,   
              " issuerId=", contract.issuerId,   
                # combos              
              " comboLegsDescrip=", contract.comboLegsDescrip,
              " comboLegs=", contract.comboLegs,
              " deltaNeutralContract=", contract.deltaNeutralContract)

    def positionEnd(self):
        """This is called once all position data for a given request are
        received and functions as an end marker for the position() data."""
        super().positionEnd()
        self.logger.debug('positionEnd')

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        """Receives the full contract's definitions. This method will return all
        contracts matching the requested via EEClientSocket::reqContractDetails.
        For example, one can obtain the whole option chain with it."""
        super().contractDetails(reqId, contractDetails)
        contract = contractDetails.contract
        self.logger.debug('contractDetails reqId=', reqId, #, ' contractDetails=', vars(contractDetails))
              "contract. conId:", contract.conId,
              " symbol=", contract.symbol,
              " secType=", contract.secType,
              " lastTradeDateOrContractMonth=", contract.lastTradeDateOrContractMonth,
              " strike=", contract.strike,
              " right=", contract.right,
              " multiplier=", contract.multiplier,
              " exchange=", contract.exchange,
              " primaryExchange=", contract.primaryExchange,
              " currency=", contract.currency,
              " localSymbol=", contract.localSymbol,
              " tradingClass=", contract.tradingClass,              
              " includeExpired=", contract.includeExpired,   
              " secIdType=", contract.secIdType,   
              " secId=", contract.secId,   
              " description=", contract.description,   
              " issuerId=", contract.issuerId,   
                # combos              
              " comboLegsDescrip=", contract.comboLegsDescrip,
              " comboLegs=", contract.comboLegs,
              " deltaNeutralContract=", contract.deltaNeutralContract)
             
        self.logger.debug('minTick =', contractDetails.minTick,
              #'validExchanges', contractDetails.validExchanges,
              #'orderTypes', contractDetails.orderTypes,
              'priceMagnifier', contractDetails.priceMagnifier,
              'underConId', contractDetails.underConId,
              'longName =', contractDetails.longName,
              'contractMonth', contractDetails.contractMonth,
              'industry = ', contractDetails.industry,
              'category = ', contractDetails.category,
              'subcategory = ', contractDetails.subcategory,
              'timeZoneId = ', contractDetails.timeZoneId,
              #'tradingHours =', contractDetails.tradingHours,
              #'liquidHours = ', contractDetails.liquidHours,
              'evRule = ', contractDetails.evRule,
              'evMultiplier = ', contractDetails.evMultiplier,
              'aggGroup = ', contractDetails.aggGroup,
              'underSymbol = ', contractDetails.underSymbol,
              'underSecType = ', contractDetails.underSecType,
              #'marketRuleIds = ', contractDetails.marketRuleIds,
              'secIdList = ', contractDetails.secIdList,
              'realExpirationDate = ', contractDetails.realExpirationDate,
              'lastTradeTime = ', contractDetails.lastTradeTime,
              'stockType = ', contractDetails.stockType,
              'minSize = ', contractDetails.minSize,
              'sizeIncrement = ', contractDetails.sizeIncrement,
              'suggestedSizeIncrement = ', contractDetails.suggestedSizeIncrement)       

    def bondContractDetails(self, reqId: int, contractDetails: ContractDetails):
        super().bondContractDetails(reqId, contractDetails)
        """This function is called when reqContractDetails function
        has been called for bonds."""
        self.logger.debug('bondContractDetails reqId=', reqId, ' contractDetails=', contractDetails)

    def contractDetailsEnd(self, reqId: int):
        super().contractDetailsEnd(reqId)
        """This function is called once all contract details for a given
        request are received. This helps to define the end of an option
        chain."""
        self.logger.debug('contractDetailsEnd reqId=', reqId)

    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        super().orderStatus(orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        self.logger.debug('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        super().openOrder(orderId, contract, order, orderState)
        self.logger.debug('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)
        self.logger.debug('order.status=', orderState.status,
                'initMarginBefore=', orderState.initMarginBefore,
                'maintMarginBefore=',orderState.maintMarginBefore,
                'equityWithLoanBefore=', orderState.equityWithLoanBefore,
                'initMarginChange=', orderState.initMarginChange,
                'maintMarginChange=', orderState.maintMarginChange, 
                'equityWithLoanChange=',orderState.equityWithLoanChange, 
                'initMarginAfter=',orderState.initMarginAfter,
                'maintMarginAfter=', orderState.maintMarginAfter,
                'equityWithLoanAfter=', orderState.equityWithLoanAfter,
                'commission=', orderState.commission,
                'minCommission=', orderState.minCommission,
                'maxCommission=',orderState.maxCommission, 
                'commissionCurrency=', orderState.commissionCurrency,
                'warningText=', orderState.warningText,
                'completedTime=', orderState.completedTime,
                'completedStatus=', orderState.completedStatus)

    def openOrderEnd(self):
        super().openOrderEnd()        
        """This is called at the end of a given request for open orders."""
        self.logger.debug('openOrderEnd')
        
    def execDetails(self, reqId, contract, execution):
        super.execDetails(reqId, contract, execution)
        self.logger.debug('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)

    def start(self, reqId):
        return

    def stop(self):
        self.disconnect()
class option_geeks(ib_app_base):
    
    def __init__(self, mlist):
        super().__init__()     
        self.mlist = mlist

    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        self.mlist.at[reqId, TickTypeEnum.toStr(tickType)] = price
        if tickType == TickTypeEnum.BID or tickType == TickTypeEnum.ASK:
            self.logger.debug("PreOpen:", attrib.preOpen)

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
class accounts_summary(ib_app_base):
    def __init__(self, user=None):
        super().__init__()
        #EClient.__init__(self, self)
        self.user = user

    def managedAccounts(self, accountsList):
        super().managedAccounts(accountsList)
        self.accountSummary_df = pd.DataFrame({'Account': self.accountList})
        self.accountSummary_df.set_index(['Account'], inplace=True)  
                        
    def accountSummary(self, reqId, account, tag, value, currency):
        """Returns the data from the TWS Account Window Summary tab in
        response to reqAccountSummary()."""        
        super().accountSummary(reqId, account, tag, value, currency)       
        self.accountSummary_df.at[account, tag] = value

    def accountSummaryEnd(self, reqId: int):
        """This method is called once all account summary data for a
        given request are received."""
        super().accountSummaryEnd(reqId)
        self.cancelAccountSummary(reqId)        
        self.stop()

    def start(self, reqId):
        self.reqAccountSummary(reqId, "All", AccountSummaryTags.AllTags)               
class accounts_values_profolio(ib_app_base):
    def __init__(self, user=None):
        super().__init__()
        #EClient.__init__(self, self)
        self.user = user
        self.account_index = 0
                              
    def updateAccountValue(self, key, val, currency, accountName):
        super().updateAccountValue(key, val, currency, accountName)

        if accountName not in self.accountValue_dict.keys():
            self.accountValue_dict[accountName] = {}

        self.accountValue_dict[accountName][key] = val

    def accountDownloadEnd(self, accountName):
        super().accountDownloadEnd(accountName)
         
        if self.account_index+1 >= len(self.accountList):
             self.stop()
        else:    
            self.reqAccountUpdates(False, self.accountList[self.account_index])    
            self.account_index += 1              
            self.accountValue_dict[self.accountList[self.account_index]]={}          
            self.reqAccountUpdates(True, self.accountList[self.account_index])  
        
    def updateAccountTime(self, timeStamp):
        super().updateAccountTime(timeStamp)
        
        for key in self.accountValue_dict:        
            self.accountValue_dict[key]['timeStamp'] = timeStamp     
                
        self.accountPortfolio_df['timeStamp'] = timeStamp          

    def updatePortfolio(self,
            contract: Contract,
            position: float,
            marketPrice: float,
            marketValue: float,
            averageCost: float,
            unrealizedPNL: float,
            realizedPNL: float,
            accountName: str):
        
        index = self.accountPortfolio_df.shape[0]        
        self.accountPortfolio_df.at[index, 'position'] = float(position)       
        self.accountPortfolio_df.at[index, 'marketPrice'] =  marketPrice      
        self.accountPortfolio_df.at[index, 'marketValue'] = marketValue      
        self.accountPortfolio_df.at[index, 'averageCost'] = averageCost      
        self.accountPortfolio_df.at[index, 'unrealizedPNL'] = unrealizedPNL          
        self.accountPortfolio_df.at[index, 'realizedPNL'] = realizedPNL   
        self.accountPortfolio_df.at[index, 'accountName'] = accountName          
        
        self.accountPortfolio_df.at[index, 'symbol'] = contract.symbol 
        self.accountPortfolio_df.at[index, 'secType'] = contract.secType         
        
        if contract.secType == 'OPT':
            self.accountPortfolio_df.at[index, 'exp_date'] = contract.lastTradeDateOrContractMonth
            self.accountPortfolio_df.at[index, 'strike'] = contract.strike
            self.accountPortfolio_df.at[index, 'right'] = contract.right          
            self.accountPortfolio_df.at[index, 'comboLegsDescrip'] = contract.comboLegsDescrip            
            self.accountPortfolio_df.at[index, 'comboLegs'] = str(contract.comboLegs)  

    def start(self, reqId):
        if len(self.accountList) == 0:
            self.logger.error('No account found')
            return
        
        self.accountValue_dict = {}
        self.accountPortfolio_df = pd.DataFrame()       
        self.reqAccountUpdates(True, self.accountList[self.account_index])             
class accounts_positions(ib_app_base):
    def __init__(self, user=None):
        super().__init__()
        self.user = user
        self.pos = pd.DataFrame()        
                        
    def position(self, account, contract, position, avgCost):
        """This event returns real-time positions for all accounts in
        response to the reqPositions() method."""
        super().position(account, contract, position, avgCost)        
        index = self.pos.shape[0]
        self.pos.at[index, 'account'] = account     
        self.pos.at[index, 'symbol'] = contract.symbol 
        self.pos.at[index, 'secType'] = contract.secType         
        self.pos.at[index, 'position'] = float(position)
        self.pos.at[index, 'avgCost'] =  float(avgCost) 
        
        if contract.secType == 'OPT':
            self.pos.at[index, 'exp_date'] = contract.lastTradeDateOrContractMonth
            self.pos.at[index, 'strike'] = contract.strike
            self.pos.at[index, 'right'] = contract.right    
            self.pos.at[index, 'comboLegsDescrip'] = contract.comboLegsDescrip
            self.pos.at[index, 'comboLegs'] = str(contract.comboLegs)           

    def positionEnd(self):
        """This is called once all position data for a given request are
        received and functions as an end marker for the position() data."""
        super().positionEnd()
        self.cancelPositions()        
        self.stop()

    def start(self, reqId):             
        self.reqPositions()
class contract_details(ib_app_base):
    def __init__(self, contract):
        super().__init__()    
        self.contract = contract

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        super().contractDetails(reqId, contractDetails )
        """Receives the full contract's definitions. This method will return all
        contracts matching the requested via EEClientSocket::reqContractDetails.
        For example, one can obtain the whole option chain with it."""
        self.contractDetails = contractDetails
        self.conId = contractDetails.contract.conId

    def contractDetailsEnd(self, reqId: int):
        super().contractDetailsEnd(reqId)
        self.stop()
        """This function is called once all contract details for a given
        request are received. This helps to define the end of an option
        chain."""
        
    def start(self, reqId):             
        self.reqContractDetails(reqId, self.contract)
class snapshot_guote(ib_app_base):
    
    def __init__(self, contract):
        super().__init__()     
        self.contract = contract
        self.quotes = {}

    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        self.quotes[TickTypeEnum.toStr(tickType)] = price
        if tickType == TickTypeEnum.BID or tickType == TickTypeEnum.ASK:
            self.quotes["PreOpen"] = attrib.preOpen

    def tickSize(self, reqId, tickType, size):
        super().tickSize(reqId, tickType, size)
        self.quotes[TickTypeEnum.toStr(tickType)] = size        

    def tickGeneric(self, reqId, tickType, value):
        super().tickGeneric(reqId, tickType, value)
        self.quotes[TickTypeEnum.toStr(tickType)] = value    

    def tickSnapshotEnd(self, reqId):
        super().tickSnapshotEnd(reqId)
        self.stop()

    def tickOptionComputation(self,reqId,tickType,tickAttrib,impliedVol,delta,optPrice,pvDividend,gamma,vega,theta,undPrice):
        super().tickOptionComputation(reqId,tickType,tickAttrib,impliedVol,delta,optPrice,pvDividend,gamma,vega,theta,undPrice)
        """This function is called when the market in an option or its
        underlier moves. TWS's option model volatilities, prices, and
        deltas, along with the present value of dividends expected on that
        options underlier are received."""   
        tickTypeStr = TickTypeEnum.toStr(tickType)
        self.quotes[tickTypeStr] = {}
        self.quotes[tickTypeStr]['impliedVol'] = impliedVol               
        self.quotes[tickTypeStr]['delta'] = delta
        self.quotes[tickTypeStr]['gamma'] = gamma
        self.quotes[tickTypeStr]['vega'] = vega
        self.quotes[tickTypeStr]['theta'] = theta  
        self.quotes[tickTypeStr]["tickAttrib"] = tickAttrib
        self.quotes[tickTypeStr]["optPrice"] = optPrice,
        self.quotes[tickTypeStr]["pvDividend:"] = pvDividend
        self.quotes[tickTypeStr]["undPrice"] = undPrice                 
        self.quotes[tickTypeStr]["optPrice"] = optPrice            
        self.quotes[tickTypeStr]["pvDividend"] = pvDividend  

    def start(self, reqId):
        self.reqMarketDataType(ib_settings.IBConfig.marketDataType)    
        self.reqMktData(reqId, self.contract, '', True, False, [])
class place_order(ib_app_base):
    def __init__(self, contract:Contract, order:Order):
        super().__init__()
        self.contract = contract
        self.order = order
        #EClient.__init__(self, self)
    def managedAccounts(self, accountsList):
        super().managedAccounts(accountsList)
 
    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        super().orderStatus(orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        self.logger.debug('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
        self.status = status 
        self.filled = filled
        self.remaining = remaining
        self.avgFullPrice = avgFullPrice
        self.permId = permId
        self.parentId = parentId
        self.lastFillPrice = lastFillPrice
        self.clientId = clientId
        self.whyHeld = whyHeld
        self.mktCapPrice = mktCapPrice

    def openOrder(self, orderId, contract, order, orderState):
        super().openOrder(orderId, contract, order, orderState)

    def openOrderEnd(self):
        super().openOrderEnd()        

    def execDetails(self, reqId, contract, execution):
        super.execDetails(reqId, contract, execution)
        self.logger.debug('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)
        self.stop()

    def start(self, orderId):
        self.orderId = orderId
        self.placeOrder(orderId, self.contract, self.order)         
                  
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

    with IBClient(TWS=True, Live=False) as ibClient:
        #print(ibClient.get_option_contId('NVDA', '20231229', 495, 'P'))
        #print(ibClient.get_option_snapshot_guote('NVDA', '20231229', 495, 'P'))
        #print(ibClient.get_stock_snapshot_guote('NVDA'))
        #legs = []
        #legs.append(ComboOptionLeg('NVDA', '20231229', 495, 'P', 1, 'BUY',  ibClient=ibClient))
        #legs.append(ComboOptionLeg('NVDA', '20231229', 500, 'P', 1, 'SELL', ibClient=ibClient))  
        #legs.append(ComboOptionLeg('NVDA', '20231229', 500, 'C', 1, 'SELL', ibClient=ibClient))
        #legs.append(ComboOptionLeg'NVDA', '20231229', 505, 'C', 1, 'BUY',  ibClient=ibClient))               
        #quote_dict, contract = ibClient.get_spread_option_guote('NVDA', legs)
        #order = Order()
        #order.action = 'BUY'
        #order.totalQuantity = 10
        #order.orderType = 'LMT'
        #order.lmtPrice = quote_dict['DELAYED_BID']
        #print(ibClient.go_place_order(contract, order))
        #print(ibClient.get_accounts_summary())
        #print(ibClient.get_accounts_values_profolio())
        #print(ibClient.get_accounts_positions())
        #print(ibClient.get_account_list())
        from option_trader.admin.site import site
        mysite = site('mysite')        
        ml = mysite.get_monitor_df()

        total_size = ml.shape[0]
        chunk_size = 5
        chunk_number = total_size // chunk_size
        chunks = np.array_split(ml, chunk_number)

        output = pd.DataFrame()
        for i, chunk in enumerate(chunks):
            print(f"Chunk {i+1}:")
            print(chunk['symbol'].unique())      
            app = ibClient.get_option_geeks(build_OTM_option_requests(chunk, [30]))      
            output = pd.concat([output, app.mlist])

        