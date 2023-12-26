import datetime
import pandas as pd
import numpy as np

import hbshare
from hbshare.fe.XZ import db_engine
from hbshare.fe.XZ import functionality
from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from sklearn import  preprocessing as pp

util=functionality.Untils()
hbdb=db_engine.HBDB()
localdb=db_engine.PrvFunDB().engine

def get_ticker_expection(zqdm_list,date_list):

    cluster_num=np.ceil(len(zqdm_list)/800)

    outputdf=[]

    for i in range(int(cluster_num)):

        temp_list=zqdm_list[i*800:(i+1)*800]

        sql="select EST_DT,SUBSTR(S_INFO_WINDCODE,1,6) as zqdm ,EST_OPER_REVENUE as EST_OPER_REVENUE_YOY,NET_PROFIT as EST_NET_PROFIT_YOY,EST_ROE AS ROE_FY1 ,EST_PE AS PE_FY1,EST_PEG AS PEG_FY1,ROLLING_TYPE from wind.AShareConsensusRollingData where  SUBSTR(S_INFO_WINDCODE,1,6)  in ({0}) and  EST_DT in ({1}) and ROLLING_TYPE in ('FY1','YOY','FY2','FY3')   "\
            .format(util.list_sql_condition(temp_list),util.list_sql_condition(date_list))
        ticker_expection=hbdb.db2df(sql,db='readonly').drop('ROW_ID',axis=1)

        ticker_expection=pd.merge(ticker_expection[ticker_expection['ROLLING_TYPE'] == 'FY1'][['ZQDM', 'EST_DT', 'PE_FY1','PEG_FY1','ROE_FY1']],
                                  ticker_expection[ticker_expection['ROLLING_TYPE'] == 'YOY'][['ZQDM', 'EST_DT', 'EST_NET_PROFIT_YOY','EST_OPER_REVENUE_YOY']],
                                  how='outer',on=['EST_DT','ZQDM'])
        outputdf.append(ticker_expection)

    outputdf=pd.concat(outputdf,axis=0)

    return  outputdf

def read_hld_fromdb(jjdm_list,if_zc=False,start_date=None,end_date=None,ext_condtion=None):

    jjdm_con=util.list_sql_condition(jjdm_list)

    if((start_date is not None) and (end_date is not None) ):
        date_con="and jsrq>='{0}' and jsrq<='{1}'".format(start_date,end_date)
    elif((start_date is None) and (end_date is None)):
        date_con=''
    else:
        date_con="and jrsq='{}'".format(start_date)

    if(ext_condtion is None):
        ext_condtion=''

    sql = """select jjdm,jsrq,zqdm,zjbl from st_fund.t_st_gm_gpzh where jjdm in ({0}) {1} {2}
    """.format(jjdm_con, date_con,ext_condtion)
    hld =hbdb.db2df(sql, db='funduser')
    hld.reset_index(drop=True, inplace=True)
    hld['date'] = hld['jsrq'].astype(str)
    hld.drop('jsrq', inplace=True, axis=1)

    hld=hld_reportdate2trade_date(hld,date_col='date')

    #take zc only
    if(if_zc):
        hld['zjbl_rank'] = hld.groupby('date')['zjbl'].rank(ascending=False)
        hld=hld[hld['zjbl_rank']<=10]
        hld.drop('zjbl_rank',inplace=True,axis=1)
        hld.reset_index(drop=True, inplace=True)

    return hld

def hld_reportdate2trade_date(hld,date_col):
    for date in hld[date_col].unique():
        hld.loc[hld[date_col]==date,date_col]=util._shift_date(date)
    return  hld

def ticker_weight_history_perjj(hld):

    history_df=pd.DataFrame()

    zqdm_list=hld['zqdm'].unique().tolist()
    date_list=hld['date'].unique().tolist()
    date_list.sort()
    zqdm_list.sort()

    history_df['zqdm']=zqdm_list
    for date in date_list:
        tempdf=hld[hld['date']==date][['zjbl','zqdm']]
        history_df=pd.merge(history_df,tempdf,how='left',on='zqdm')
        history_df.rename(columns={'zjbl':date},inplace=True)

    return  history_df

def get_stock_price(date_list,ticker_list,add_pre_day=False,fre='Q'):

    date_list.sort()
    if(add_pre_day):
        if(fre=='Q'):
            add_days=91
        elif(fre=='M'):
            add_days=30
        elif(fre=='HA'):
            add_days=188
        else:
            print("input fre is not supported")
            raise Exception

        pre_date= (datetime.datetime.strptime(date_list[0], '%Y%m%d')-datetime.timedelta(days=add_days)).strftime('%Y%m%d')
        date_list=[pre_date]+date_list

    date_con=util.list_sql_condition(date_list)

    if(len(ticker_list)>1000):
        sql = """
        select zqdm,jyrq,drjj from st_ashare.t_st_ag_gpjy where jyrq in ({0}) and scdm !='STAS00'
         """.format(date_con)
        stock_price=pd.DataFrame(data=ticker_list,columns=['zqdm'])
        stock_price =pd.merge(stock_price,hbdb.db2df(sql, db='alluser'),how='left',on='zqdm')

    else:
        ticker_con=util.list_sql_condition(ticker_list)
        sql = """
        select zqdm,jyrq,drjj from st_ashare.t_st_ag_gpjy where ZQDM in ({0}) and JYRQ in ({1})
         """.format(ticker_con, date_con)
        stock_price = hbdb.db2df(sql, db='alluser')


    return stock_price.drop('ROW_ID',axis=1)

def stock_price2ret(pricedf):

    pricedf['pctchange']=pricedf.groupby('ZQDM')['DRJJ'].pct_change()

    return pricedf

def hhi_index(arr):

    return np.sum([x**2 for x in arr])

def centralization_level(df,num1=3,num2=5):

    outputdf=pd.DataFrame(index=df.index,columns=['c_level'])

    if(num2==0):
        def cen_func(df,num1,num2):
            for i in range(len(df)):
                outputdf.iloc[i]['c_level'] = df.iloc[i].sort_values()[-1 * num1:].sum() / df.iloc[i].sum()
            return  outputdf
    else:
        def cen_func(df, num1,num2):
            for i in range(len(df)):
                outputdf.iloc[i]['c_level'] = (df.iloc[i].sort_values()[-1 * num1:].sum() +
                                               df.iloc[i].sort_values()[-1 * num2:].sum()) / 2 / df.iloc[i].sum()
            return  outputdf

    outputdf=cen_func(df,num1,num2)

    return outputdf

def calculate_shift_rate(indf):
    indf.sort_index(inplace=True)
    indus_col=indf.columns.tolist()
    indus_col.remove('jjzzc')
    for col in indus_col:
        indf[col+'_mkt']=indf[col]*indf['jjzzc']
    diff=indf[[x+'_mkt' for x in indus_col]].diff(1)
    diff['jjzzc']=indf[[x+'_mkt' for x in indus_col]].sum(axis=1)
    diff['jjzzc']=diff['jjzzc'].rolling(2).mean()
    shift_ratio=diff[[x+'_mkt' for x in indus_col]].abs().sum(axis=1)/2/diff['jjzzc']
    return shift_ratio

def calculate_style_shift_rate(indf):
    indf.sort_index(inplace=True)
    col_list=indf.columns.tolist()
    indf=indf.fillna(0)

    for col in col_list:
        indf[col]=indf[col].diff(1).abs()

    shift_ratio=indf.sum(axis=1)

    return shift_ratio

def groupby_z_socre(arr):

    pp.scale(arr)

    return pp.scale(arr)

def get_ticker_financial_info(zqdm_list,start_date,end_date,with_stock_price=False):


    style_financial_info = pd.DataFrame()
    stock_price = pd.DataFrame()
    max_length=500

    for i in range(int(np.ceil(len(zqdm_list) / max_length))):

        zqdm_con = util.list_sql_condition(zqdm_list[i * max_length:max_length * (i + 1)])

        # read financial info for A stock
        # sql = """select b.InnerCode,b.SecuCode,b.CompanyCode,a. OperatingRevenueYOY,
        # a.NetProfitGrowRate,a.ROE,a.EPS,a.OperCashFlowPS,a.EndDate
        # from hsjy_gg.SecuMain b left join hsjy_gg.LC_QFinancialIndexNew a on a.CompanyCode=b.CompanyCode
        # where b.SecuCode in ({0}) and a.EndDate>=to_date('{1}','yyyymmdd') and a.MARK=2  """.format(zqdm_con,
        #                                                                                             start_date)
        sql = """select b.InnerCode,b.SecuCode,b.CompanyCode,a.OperProfitGrowRate3Y  as OperatingRevenueYOY,
        a.NPPCCGrowRate3Y as NetProfitGrowRate,a.ROETTM as ROE,a.NetProfitRatio,a.GrossIncomeRatio,a.EndDate from hsjy_gg.SecuMain b left join hsjy_gg.LC_MainIndexNew a on a.CompanyCode=b.CompanyCode 
        where b.SecuCode in ({0}) and a.EndDate>=to_date('{1}','yyyymmdd') and a.EndDate<=to_date('{2}','yyyymmdd')  """\
            .format(zqdm_con,start_date,end_date)
        df1 = hbdb.db2df(sql, db='readonly')

        if(len(df1)>0):
            #company_code_con = util.list_sql_condition(df1['COMPANYCODE'].astype(str).unique().tolist())
            inner_code_con = util.list_sql_condition(df1['INNERCODE'].astype(str).unique().tolist())
            trading_date_list = df1['ENDDATE'].astype(str).str[0:10].str.replace("-", "").unique().tolist()
            trading_date_list = [util._shift_date(x) for x in trading_date_list]

            trading_date_con = " to_date(' " + \
                               "','yyyymmdd'), to_date(' ".join(trading_date_list) + \
                               "','yyyymmdd')"

            # sql = """select CompanyCode,NetAssetPS,EndDate
            # from hsjy_gg.LC_MainIndexNew where CompanyCode in ({0}) and EndDate>=to_date('{1}','yyyymmdd') """ \
            #     .format(company_code_con, start_date)
            # df2 = hbdb.db2df(sql, db='readonly')
            sql = "select InnerCode,DividendRatio,TotalMV,PE,PB,PCFTTM as PCF,TradingDay from  hsjy_gg.LC_DIndicesForValuation where InnerCode in ({0}) and TradingDay in ({1})  " \
                .format(inner_code_con, trading_date_con)
            df3 = hbdb.db2df(sql, db='readonly')
            if(len(df3)==0):
                df3=pd.DataFrame(columns=['INNERCODE','TOTALMV','DIVIDENDRATIO','TRADINGDAY','PE','PB','PCFTTM','PCF'])

            # df = pd.merge(df1, df2, how='left', on=['COMPANYCODE', 'ENDDATE'])

            df1['ENDDATE'] = df1['ENDDATE'].astype(str).str[0:7]
            df3['TRADINGDAY'] = df3['TRADINGDAY'].astype(str).str[0:7]

            df = pd.merge(df1, df3, how='left', left_on=['INNERCODE', 'ENDDATE'], right_on=['INNERCODE', 'TRADINGDAY'])
            df.drop_duplicates(subset=['SECUCODE', 'ENDDATE'], inplace=True, keep='last')


            style_financial_info = pd.concat([style_financial_info, df[['SECUCODE', 'ROE',
                                                                        'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY',
                                                                         'DIVIDENDRATIO', 'TOTALMV','NETPROFITRATIO','GROSSINCOMERATIO',
                                                                        'PE', 'PB','PCF',
                                                                        'ENDDATE']]], axis=0)

        ##read financial info for kechuagnban stock
        sql = """select b.CompanyCode,b.InnerCode,a.ROETTM as ROE,a.NetProfitRatio,a.GrossIncomeRatio,b.SecuCode,a.ORComGrowRateThreeY as OperatingRevenueYOY,a.NPPCCGrowRateThreeY as NetProfitYOY,a.EndDate 
        from hsjy_gg.LC_STIBMainIndex a left join hsjy_gg.SecuMain b on a.CompanyCode=b.CompanyCode
         where b.SecuCode in ({0}) and a.EndDate>=to_date('{1}','yyyymmdd') and a.EndDate<=to_date('{2}','yyyymmdd') and a.IfAdjusted=2 and a.IfMerged=1""" \
            .format(zqdm_con,start_date,end_date)
        df1 = hbdb.db2df(sql, db='readonly').rename(columns={'NETPROFITYOY': 'NETPROFITGROWRATE'})
        if(len(df1)>0):
            df1['ENDDATE'] = df1['ENDDATE'].astype(str).str[0:7]
            df1.drop_duplicates(subset=['SECUCODE', 'ENDDATE'], inplace=True, keep='last')

            inner_code_con = util.list_sql_condition(df1['INNERCODE'].astype(str).unique().tolist())

            sql = """select InnerCode,TotalMV,DividendRatio,TradingDay,PETTM as PE,PB,PCFTTM as PCF from hsjy_gg.LC_STIBDIndiForValue 
            where InnerCode in ({0}) and TradingDay in ({1}) 
            """.format(inner_code_con, trading_date_con)
            df2 = hbdb.db2df(sql, db='readonly')
            if(len(df2)>0):
                df2['TRADINGDAY'] = df2['TRADINGDAY'].astype(str).str[0:7]
            else:
                df2=pd.DataFrame(columns=['INNERCODE','TOTALMV','DIVIDENDRATIO','TRADINGDAY','PE','PB','PCF'])

            df_kc = pd.merge(df1, df2, how='left',
                             left_on=['INNERCODE', 'ENDDATE'], right_on=['INNERCODE', 'TRADINGDAY'])

            df_kc.drop_duplicates(subset=['SECUCODE', 'ENDDATE'], inplace=True, keep='last')


            style_financial_info = pd.concat([style_financial_info, df_kc[['SECUCODE', 'ROE',
                                                                           'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY',
                                                                            'DIVIDENDRATIO', 'TOTALMV','NETPROFITRATIO','GROSSINCOMERATIO',
                                                                           'PE', 'PB','PCF',
                                                                           'ENDDATE']]], axis=0)

        style_financial_info['ENDDATE'] = style_financial_info['ENDDATE'].astype(str).str.replace('-', '')
        style_financial_info.loc[style_financial_info['NETPROFITGROWRATE']==0,'NETPROFITGROWRATE']=0.001
        style_financial_info['PEG']=style_financial_info['PE']/style_financial_info['NETPROFITGROWRATE']
        if(with_stock_price):
            stock_price = pd.concat([stock_price,
                                     get_stock_price(trading_date_list, zqdm_list[i * max_length:max_length * (i + 1)])],
                                    axis=0)

    if(with_stock_price):
        stock_price['JYRQ'] = stock_price['JYRQ'].str[0:6]
        style_financial_info = pd.merge(style_financial_info, stock_price, how='left', left_on=['SECUCODE', 'ENDDATE'],
                                        right_on=['ZQDM', 'JYRQ'])

    style_financial_info[[ 'ROE', 'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY',
                                                                           'DIVIDENDRATIO', 'TOTALMV','NETPROFITRATIO','GROSSINCOMERATIO',
                                                                           'PE', 'PB','PCF','PEG']]=style_financial_info[[ 'ROE',
                                                                           'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY',
                                                                            'DIVIDENDRATIO', 'TOTALMV','NETPROFITRATIO','GROSSINCOMERATIO',
                                                                           'PE', 'PB','PCF', 'PEG']].astype(float)

    return style_financial_info

def quantial_for_rolling(arr):


    return (arr.rank(method='min')/len(arr)).tolist()[-1]

def index_industry_distribution():

    asofdate_list=[ '20191231'
        ,  '20200630',  '20201231'
        ,  '20210630', '20211231','20220630','20221231']
    output=[]
    for asofdate in asofdate_list:
        jjdm_list=util.get_930950_funds(asofdate)
        sql="select jjdm,flmc,zzjbl,jsrq from st_fund.t_st_gm_jjhyzhyszb where jjdm in ({0}) and hyhfbz=2 and jsrq>='{1}' and jsrq<='{2}' and zclb=2"\
            .format(util.list_sql_condition(jjdm_list),asofdate[0:6]+'01',asofdate[0:6]+'31')
        hyfb=hbdb.db2df(sql,db='funduser')


        sql="select jjdm,jsrq,jjjzc from st_fund.t_st_gm_zcpz where jjdm in ({0}) and jsrq>='{1}' and jsrq<='{2}' "\
            .format(util.list_sql_condition(jjdm_list),asofdate[0:6]+'01',asofdate[0:6]+'31')
        jj_size=hbdb.db2df(sql,db='funduser')
        jj_size['jjjzc'] = jj_size['jjjzc'] / jj_size['jjjzc'].sum()

        #industry dis
        # hyfb=pd.merge(hyfb,jj_size[['jjdm','jjjzc']])
        # hyfb['zzjbl'] = hyfb['zzjbl'] * hyfb['jjjzc']
        # output.append(hyfb.groupby('flmc')['zzjbl'].sum().to_frame(asofdate))

        #hk stock dis

        sql="select jjdm,zjbl,jsrq from st_fund.t_st_gm_hyzh where jjdm in ({0}) and jsrq>='{1}' and jsrq<='{2}' and hymc='合计' "\
            .format(util.list_sql_condition(jjdm_list),asofdate[0:6]+'01',asofdate[0:6]+'31')
        zjh_ind=hbdb.db2df(sql,db='funduser')

        sql="select jjdm,jsrq,gptzzjb from st_fund.t_st_gm_zcpz where jjdm in ({0}) and jsrq>='{1}' and jsrq<='{2}' "\
            .format(util.list_sql_condition(jjdm_list),asofdate[0:6]+'01',asofdate[0:6]+'31')
        stock_w=hbdb.db2df(sql,db='funduser')

        stock_w['jsrq']=stock_w['jsrq'].astype(str)
        stock_w=pd.merge(stock_w,zjh_ind,
                      how='inner',on=['jjdm','jsrq'])
        stock_w = pd.merge(stock_w, jj_size[['jjdm', 'jjjzc']])
        stock_w['hk_w']=stock_w['gptzzjb']-stock_w['zjbl']
        stock_w['hk_w'] = stock_w['hk_w'] * stock_w['jjjzc']
        output.append(stock_w[['hk_w']].sum().to_frame(asofdate))


    output=pd.concat(output,axis=1)
    output.to_excel('930950港股.xlsx')

class Industry_analysis:

    def __init__(self):


        self.indus_col = ['aerodef', 'agriforest', 'auto', 'bank', 'builddeco', 'chem', 'conmat', 'commetrade',
                          'computer', 'conglomerates', 'eleceqp', 'electronics',
                          'foodbever', 'health', 'houseapp', 'ironsteel', 'leiservice', 'lightindus', 'machiequip',
                          'media', 'mining', 'nonbankfinan', 'nonfermetal',
                          'realestate', 'telecom', 'textile', 'transportation', 'utilities']
        chinese_name = ['国防军工', '农林牧渔', '汽车', '银行', '建筑装饰', '化工', '建筑材料', '商业贸易', '计算机', '综合', '电气设备',
                        '电子', '食品饮料', '医药生物', '家用电器', '钢铁', '休闲服务', '轻工制造', '机械设备', '传媒', '采掘', '非银金融',
                        '有色金属', '房地产', '通信', '纺织服装', '交通运输', '公用事业']
        self.industry_name_map = dict(zip(chinese_name, self.indus_col))
        self.new_col_name=['农林牧渔','基础化工','钢铁','有色金属','电子','家用电器','食品饮料',
                           '纺织服饰','轻工制造','医药生物','公用事业','交通运输','房地产','商贸零售',
                           '社会服务','综合','建筑材料','建筑装饰','电力设备','国防军工','计算机','传媒',
                           '通信','银行','非银金融','汽车','机械设备','煤炭','石油石化','环保','美容护理']
        self.new_col_name2=['IT服务','一般零售','专业工程','互联网电商','休闲食品','保险','元件',
                            '光伏设备','光学光电子','其他家电','农化制品','农商行','出版','化学制品',
                            '化学制药','医疗器械','医疗服务','医药商业','半导体','厨卫电器','国有大型银行',
                            '城商行','多元金融','家居用品','家电零部件','工业金属','工程咨询服务',
                            '影视院线','房地产开发','教育','数字媒体','文娱用品','旅游及景区','橡胶',
                            '汽车服务','汽车零部件','消费电子','游戏','炼化及贸易','照明设备','物流',
                            '玻璃玻纤','生物制品','电力','电子化学品','电池','电网设备','白酒',
                            '自动化设备','航空机场','装修建材','计算机设备','证券','调味发酵品',
                            '轨交设备','软件开发','通信设备','通用设备','造纸','食品加工','饮料乳品',
                            '饰品','饲料','专用设备','化学纤维','基础建设','工程机械','房屋建设',
                            '旅游零售','油服工程','白色家电','股份制银行','航天装备','非白酒','军工电子',
                            '动物保健','商用车','小家电','油气开采','环境治理','能源金属','贵金属'
            ,'非金属材料','专业服务','服装家纺','个护用品','中药','乘用车','其他电源设备','农产品加工',
                            '包装印刷','化妆品','化学原料','医疗美容','地面兵装','塑料','小金属'
            ,'房地产服务','普钢','燃气','特钢','电机','纺织制造','航空装备','装修装饰','贸易',
                            '其他电子','养殖业','种植业','金属新材料','黑色家电','专业连锁','摩托车及其他',
                            '环保设备','酒店餐饮','风电设备','广告营销','水泥','煤炭开采','航海装备','航运港口',
                            '通信服务','铁路公路','电视广播','焦炭','综合','冶钢原料','体育','农业综合'
            ,'渔业','互联网传媒','计算机应用','稀有金属','港口','林业','营销传播','畜禽养殖']
        self.new_col_name3=['IT服务','LED','仓储物流','住宅开发','保险','信托','光伏加工设备',
                            '其他化学制品','其他家电','其他建材','其他生物制品','其他石化','其他自动化设备',
                            '其他计算机设备','其他通用设备','农商行','农药','分立器件','化学制剂','医疗研发外包',
                            '医疗设备','半导体设备','印制电路板','原料药','厨房电器','国有大型银行','国际工程',
                            '垂直应用软件','城商行','培训教育','多业态零售','大众出版','大宗用纸','学历教育',
                            '定制家居','宠物食品','家电零部件','工控设备','工程咨询服务','底盘与发动机系统',
                            '影视动漫制作','成品家居','文化用品','机器人','模拟芯片设计','横向通用软件','橡胶助剂',
                            '汽车电子电气系统','汽车综合服务','消费电子零部件及组装','游戏','火力发电','炼油化工'
            ,'照明设备','玻纤制造','电商服务','电子化学品','电池化学品','电网自动化设备','白酒','线下药店','肉制品',
                            '自然景区','航空运输','视频媒体','证券','调味发酵品','资产管理','超市','轨交设备',
                            '软饮料','通信网络设备及器件','钟表珠宝','钢结构','铜','锂电池','集成电路封测',
                            '零食','乳品','人工景区','其他多元金融','其他酒类','基建市政工程','工程机械整机',
                            '房屋建设','旅游零售','油田服务','涤纶','烘焙食品','热力服务','电能综合服务',
                            '疫苗','空调','股份制银行','能源及重型设备','航天装备','被动元件','锂电专用设备',
                            '仪器仪表','其他专用设备','其他汽车零部件','军工电子','动物保健','半导体材料','厨房小家电',
                            '商用载货车','固废治理','安防设备','数字芯片设计','核力发电','水力发电','油气开采','畜禽饲料',
                            '硅料硅片','血液制品','通信终端及配件','钴','防水材料','非金属材料','面板','食品及饲料添加剂',
                            '黄金','人力资源服务','光伏辅材','医疗耗材','医药流通','图片媒体','机床工具','检测服务',
                            '水务及水治理','金属制品','锦纶','非运动服装','风力发电','中药','中间产品及消费品供应链服务',
                            '会展服务','光学元件','其他农产品加工','其他化学原料','其他化学纤维','其他塑料制品',
                            '其他家居用品','其他小金属','其他电源设备','其他纺织','化妆品制造及其他','医美耗材',
                            '品牌消费电子','地面兵装','塑料包装','大气治理','娱乐用品','氯碱','水产饲料',
                            '涂料油墨','炭黑','燃气','物业管理','特种纸','特钢','瓷砖地板','生活用纸','电动乘用车',
                            '电工仪器仪表','电机','磨具磨料','磷肥及磷化工','粮油加工','综合环境治理','航空装备',
                            '装修装饰','贸易','车身附件及饰件','轮胎轮毂','钢铁管材','体外诊断','其他专业服务',
                            '其他电子','其他金属新材料','冰洗','医院','品牌化妆品','园林工程','彩电','楼宇设备',
                            '清洁小家电','激光设备','纺织鞋类制造','线缆部件及其他','肉鸡养殖','跨境电商',
                            '输变电设备','铝','门户网站','鞋帽及其他','食用菌','专业连锁','光伏发电',
                            '其他专业工程','其他运输设备','工程机械器件','熟食','环保设备','生猪养殖',
                            '纸包装','纺织服装设备','配电设备','酒店','风电零部件','保健品','其他橡胶制品',
                            '其他通信设备','动力煤','化学工程','卫浴制品','卫浴电器','原材料供应链服务','商业地产'
            ,'商业物业经营','啤酒','改性塑料','教育出版','旅游综合','板材','棉纺','水泥制造','港口',
                            '焦煤','煤化工','百货','管材','纺织化学制品','综合乘用车','胶黏剂及胶带',
                            '航海装备','航运','营销代理','跨境物流','通信应用增值服务','通信线缆及配套',
                            '金融控股','铁路运输','高速公路','其他黑色家电','印染','快递','摩托车',
                            '氨纶','涂料','玻璃制造','电视广播','诊断服务','金属包装','长材','院线',
                            '产业地产','光伏电池组件','广告媒体','焦炭','综合','综合电商','聚氨酯',
                            '钛白粉','钼','集成电路制造','预加工食品','其他数字媒体','制冷空调设备',
                            '复合肥','机场','磁性材料','粘胶','耐火材料','公路货运','冶钢辅料','医美服务',
                            '有机硅','逆变器','锂','合成树脂','无机盐','氟化工','电信运营商','稀土','钨',
                            '膜材料','洗衣机','教育运营及其他','民爆制品','其他能源发电','通信工程及服务',
                            '风电整机','钾肥','铅锌','燃料电池','其他医疗服务','文字媒体','期货','体育',
                            '印刷包装机械','油气及炼化工程','租赁','纯碱','商用载客车','铁矿石','种子',
                            '个护小家电','房产租赁经纪','粮食种植','蓄电池及其他电池','其他饰品',
                            '综合电力设备商','农业综合','汽车经销商','金融信息服务','综合包装','家纺',
                            '油品石化贸易','白银','印刷','公交','水产养殖','物流','辅料','互联网信息服务',
                            '国际工程承包','软件开发','洗护用品','餐饮','水泥制品','其他稀有小金属',
                            '运动服装','其他养殖','农用机械','火电设备','果蔬加工','其他种植业',
                            '海洋捕捞','林业','氮肥','其它专用机械','营销服务','生物制品','畜禽养殖','汽车零部件']
        self.new_col_list=[self.new_col_name,self.new_col_name2,self.new_col_name3]
        self.index_code_list=['801010','801030','801040','801050','801080','801110',
                              '801120','801130','801140','801150','801160','801170',
                              '801180','801200','801210','801230','801710','801720',
                              '801730','801740','801750','801760','801770','801780',
                              '801790','801880','801890','801950','801960','801970','801980']
        self.index_code_map=dict(zip(self.index_code_list,self.new_col_name))
        self.industry_name_map_e2c = dict(zip(self.indus_col, chinese_name))

        self.theme_col = ['大金融', '消费', 'TMT', '周期', '制造']
        self.theme_map = dict(zip(self.theme_col,
                             [['银行','非银金融','房地产'],
                              ['食品饮料','家用电器','医药生物','社会服务','农林牧渔','商贸零售','美容护理','纺织服饰'],
                              ['通信','计算机','电子','传媒'],
                              ['钢铁','有色金属','建筑装饰','建筑材料','基础化工','石油石化','煤炭'],
                              ['交通运输','机械设备','汽车','轻工制造','电力设备','环保','公用事业','国防军工']
                              ]
                             ))
        lista=[]
        listb=[]
        for theme in self.theme_col:
            for col in self.theme_map[theme]:
                lista.append(col)
                listb.append(theme)
        self.ind2thememap=pd.DataFrame()
        self.ind2thememap['industry_name']=lista
        self.ind2thememap['theme']=listb


    @staticmethod
    def centralization_level(df,num1=3,num2=5):

        outputdf=pd.DataFrame(index=df.index,columns=['c_level'])

        for i in range(len(df)):
            outputdf.iloc[i]['c_level']=(df.iloc[i].sort_values()[-1*num1:].sum()+df.iloc[i].sort_values()[-1*num2:].sum())/2/df.iloc[i].sum()

        return outputdf

    @staticmethod
    def ind_shift_rate(indf):
        indf.sort_index(inplace=True)
        indus_col=indf.columns.tolist()
        indus_col.remove('jjjzc')
        for col in indus_col:
            indf[col+'_mkt']=indf[col]*indf['jjjzc']
        diff=indf[[x+'_mkt' for x in indus_col]].diff(1)
        diff['jjjzc']=indf[[x+'_mkt' for x in indus_col]].sum(axis=1)
        diff['jjjzc']=diff['jjjzc'].rolling(2).mean()
        shift_ratio=diff[[x+'_mkt' for x in indus_col]].abs().sum(axis=1)/2/diff['jjjzc']
        return shift_ratio

    def style_change_detect_engine(self,q_df,diff1,diff2,q_list,col_list,t1,t2):

        style_change=[]

        for col in col_list:

            potential_date=diff2[diff2[col]<=-1*t1].index.to_list()
            last_added_date=q_list[-1]
            for date in potential_date:
                if(diff1.loc[q_df.index[q_df.index<=date][-3]][col]<=-1*t2):
                    added_date=q_df.index[q_df.index<=date][-3]
                elif(diff1.loc[q_df.index[q_df.index<=date][-2]][col]<=-1*t2):
                    added_date=q_df.index[q_df.index<=date][-2]
                elif(diff1.loc[q_df.index[q_df.index<=date][-1]][col]<=-1*t2):
                    added_date = q_df.index[q_df.index <= date][-1]
                else:
                    added_date = q_df.index[q_df.index <= date][-3]

                if((q_list.index(added_date)-q_list.index(last_added_date)<=2
                        and q_list.index(added_date)-q_list.index(last_added_date)>0) or added_date==q_list[-1]):
                    continue
                else:
                    style_change.append(added_date + "@" + col)
                    last_added_date = added_date

            potential_date = diff2[diff2[col] >= t1].index.to_list()
            last_added_date = q_list[-1]
            for date in potential_date:
                if (diff1.loc[q_df.index[q_df.index <= date][-3]][col] >= t2):
                    added_date = q_df.index[q_df.index <= date][-3]
                elif (diff1.loc[q_df.index[q_df.index <= date][-2]][col] >= t2):
                    added_date = q_df.index[q_df.index <= date][-2]
                elif (diff1.loc[q_df.index[q_df.index <= date][-1]][col] >= t2):
                    added_date = q_df.index[q_df.index <= date][-1]
                else:
                    added_date = q_df.index[q_df.index <= date][-3]

                if (q_list.index(added_date) - q_list.index(last_added_date) <= 2
                        and q_list.index(added_date) - q_list.index(last_added_date) > 0):
                    continue
                else:
                    style_change.append(added_date + "@" + col)
                    last_added_date = added_date

        return style_change

    def style_change_detect_engine2(self, q_df, diff1, col_list, t1, t2):

        style_change=[]
        t3=t2/2

        for col in col_list:

            tempdf=pd.merge(q_df[col],diff1[col],how='left',on='date')
            tempdf['style']=''
            style_num=0
            tempdf['style'].iloc[0:2] = style_num

            for i in range(2,len(tempdf)-1):
                if(tempdf[col+'_y'].iloc[i]>t1 and tempdf[col+'_y'].iloc[i+1]>-1*t3 ):
                    style_num+=1
                    added_date = tempdf.index[i]
                    style_change.append(added_date + "@" + col)
                elif(tempdf[col+'_x'].iloc[i]-tempdf[tempdf['style']==style_num][col+'_x'][0]>t1 and
                     tempdf[col+'_y'].iloc[i]>t2 and tempdf[col+'_y'].iloc[i+1]>-1*t3):
                    style_num += 1
                    added_date=tempdf.index[i]
                    style_change.append(added_date + "@" + col)
                elif(tempdf[col+'_y'].iloc[i]<-1*t1 and tempdf[col+'_y'].iloc[i+1]<t3 ):
                    style_num += 1
                    added_date = tempdf.index[i]
                    style_change.append(added_date + "@" + col)
                elif (tempdf[col + '_x'].iloc[i] - tempdf[tempdf['style'] == style_num][col + '_x'][0] < -1*t1 and
                      tempdf[col + '_y'].iloc[i] < -1*t2 and tempdf[col + '_y'].iloc[i + 1] <  t3):
                    style_num += 1
                    added_date = tempdf.index[i]
                    style_change.append(added_date + "@" + col)

                tempdf['style'].iloc[i] = style_num

        return style_change

    def style_change_detect(self,df,q_list,col_list,t1,t2):

        q_list.sort()
        q_df = df.loc[q_list]
        diff1=q_df.diff(1)

        style_change = self.style_change_detect_engine2(q_df, diff1, col_list, t1, t2)

        return list(set(style_change)),np.array(q_list)

    def shifting_expression(self,change_ret,name,jjdm,style='Total'):

        change_winning_pro_hld = sum(change_ret[3]) / len(change_ret)
        change_winning_pro_nextq=sum(change_ret[2]) / len(change_ret)
        left_ratio = sum(change_ret[0]) / len(change_ret)
        left_ratio_deep = sum(change_ret[1]) / len(change_ret)
        # right_ratio = 1-left_ratio
        # right_ratio_deep = 1 - left_ratio_deep
        one_q_ret = change_ret[4].mean()
        hid_q_ret = change_ret[5].mean()

        return  np.array([style.split('_')[0],len(change_ret),change_winning_pro_hld,change_winning_pro_nextq
                             ,one_q_ret,hid_q_ret,left_ratio,left_ratio_deep])

    def style_change_ret(self,df,q_list,col_list,t1,t2,factor_return):

        style_change,q_list = self.style_change_detect(df,q_list,col_list,t1,t2)
        change_count = len(style_change)
        style_changedf=pd.DataFrame()
        style_changedf['date']=[x.split('@')[0] for x in style_change]
        style_changedf['style']=[x.split('@')[1] for x in style_change]
        style_changedf.sort_values('date',inplace=True,ascending=False)
        style_chang_extret=dict(zip(style_change,style_change))


        def get_factor_return(q_list, first_change_date, style):

            fac_ret_df=factor_return[(factor_return['zqdm']==style.split('_')[0])
                                     &(factor_return.index>=q_list[q_list < first_change_date][-2])
                                     &(factor_return.index<=q_list[-1])]
            return fac_ret_df
        def q_ret(fac_ret_df,q0,q1,time_length=1):
            res=np.power(fac_ret_df.loc[q1]['price']/fac_ret_df.loc[q0]['price'],1/time_length)-1
            return  res


        if(change_count>0):
            for style in style_changedf['style']:

                changedf=style_changedf[style_changedf['style']==style]
                changedf=changedf.sort_values('date')
                first_change_date=changedf['date'].values[0]
                fac_ret_df=get_factor_return(q_list,first_change_date,style)
                fac_ret_df['ma20'] = fac_ret_df.rolling(20, 1)['price'].mean()

                for i in range(len(changedf)):
                    date=changedf.iloc[i]['date']

                    observer_term=np.append(q_list[q_list<date][-2:],q_list[(q_list>=date)][0:2])

                    new_exp=df[style].loc[observer_term[2]]
                    old_exp=df[style].loc[observer_term[1]]

                    q0=observer_term[0]
                    q1=observer_term[1]
                    old_ret=q_ret(fac_ret_df,q0,q1)
                    if_left_deep =( (fac_ret_df['price'].loc[q0:q1]<fac_ret_df['price'].loc[q0:q1].mean()).sum()\
                                   /len(fac_ret_df['price'].loc[q0:q1])>=0.5 )


                    q0=observer_term[1]
                    q1=observer_term[2]
                    current_ret=q_ret(fac_ret_df,q0,q1)
                    if_left = ( (fac_ret_df['price'].loc[q0:q1]<fac_ret_df['price'].loc[q0:q1].mean()).sum()\
                                   /len(fac_ret_df['price'].loc[q0:q1])>=0.5 )

                    q0=observer_term[2]
                    q1=observer_term[3]
                    if(q1>fac_ret_df.index[-1]):
                        q1=fac_ret_df.index[-1]
                    next_ret=q_ret(fac_ret_df,q0,q1)


                    if (i != len(changedf) - 1):
                        q1 = changedf.iloc[i + 1]['date']
                        q2 = q1
                    else:
                        q1 = q_list[-1]
                        q2=fac_ret_df.index[-1]

                    change_date=date
                    time_length = q_list.tolist().index(q1) - q_list.tolist().index(change_date)
                    holding_ret=q_ret(fac_ret_df,q0,q2,time_length=time_length)

                    if_win_next=(new_exp>old_exp)&(next_ret>current_ret)
                    if_win_hld=(new_exp>old_exp)&(holding_ret>current_ret)

                    shift_retur_next= (new_exp-old_exp)*(next_ret-current_ret)
                    shift_retur_hld = (new_exp - old_exp) * (holding_ret - current_ret)

                    style_chang_extret[date+"@"+style]=[if_left,if_left_deep,if_win_next,if_win_hld,shift_retur_next,shift_retur_hld]

        return style_chang_extret

    def style_shifting_analysis(self,df,q_list,col_list,t1,t2,name,jjdm,factor_return):

        # col_list=[x+"_exp_adj" for x in col]
        change_ret=self.style_change_ret(df,q_list,col_list,t1=t1,t2=t2,factor_return=factor_return)
        change_ret = pd.DataFrame.from_dict(change_ret).T
        change_ret['style'] = list([x.split('@')[1] for x in change_ret.index])
        change_ret['date'] = list([x.split('@')[0] for x in change_ret.index])

        data=[]

        if(len(change_ret)>0):
            data.append(self.shifting_expression(change_ret,name,jjdm))
            for style in change_ret['style'].unique():
                tempdf=change_ret[change_ret['style']==style]
                data.append(self.shifting_expression(tempdf,name,jjdm,style))

        shift_df = pd.DataFrame(data=data,columns=['风格类型','切换次数','胜率（直到下次切换）','胜率（下季度）',
                                                   '下季平均收益','持有平均收益','左侧比率','深度左侧比例'])
        # for col in ['胜率（直到下次切换）','胜率（下季度）','下季平均收益','持有平均收益','左侧比率','深度左侧比例']:
        #     shift_df[col] = shift_df[col].astype(float).map("{:.2%}".format)

        return  shift_df

    def save_industry_property2localdb(self,asofdate=datetime.datetime.today().strftime('%Y%m%d'), time_length=3,if_prv=False,fre='Q'):

        if(if_prv):
            localtable='hbs_prv_industry_class'
            if(fre=='M'):
                fre_con="and report_fre = 'monthly'"
            else:
                fre_con=''
        else:
            localtable='hbs_industry_class'
            cen_shift_his_table = 'hbs_cen_shift_ratio_his_industry'
            ind_porperty_table = 'hbs_industry_property'
            theme_exp_his_table = 'hbs_theme_exp'
            fre_con=''

        theme_col = self.theme_col
        collect_df = pd.DataFrame()

        start_date = str(int(asofdate[0:4]) - time_length) + asofdate[4:]

        cen_list = [[],[],[],[]]
        ratio_list =[[],[],[],[]]

        new_jjdm_list = []
        average_ind_num_list = []

        top5_ind = []
        top20_ind_2 = []
        top20_ind_3 = []
        longtoumean=[]
        longtoumed=[]

        theme_exp_his=pd.DataFrame()
        theme_map = self.ind2thememap

        industry_level=['yjxymc','ejxymc','sjxymc']
        target_col = [ 'ROE', 'PB', 'DIVIDENDRATIO', 'PCF',
                      'TOTALMV', 'PE',  'PEG', 'NETPROFITGROWRATE',
                      'OPERATINGREVENUEYOY', 'longtou_zjbl_for_ind']
        cen_list_theme=[]
        ratio_list_theme=[]

        for i in range(3):
            print(i)
            ratio_his=pd.DataFrame()

            collect_df2 = pd.DataFrame()

            df=pd.read_sql("SELECT * from {3}{2}_exp where jsrq>='{0}' and jsrq<='{1}' {4} "
                           .format(start_date,asofdate,i+1,localtable,            fre_con), con = localdb).rename(columns={'zjbl': 'zsbl'})
            df['zsbl'] = df['zsbl'] / df['know_weight']
            jjdm_list = list(set(util.get_stock_funds_pool(asofdate, 2))
                             .intersection(df['jjdm'].unique()))


            industry_class=industry_level[i]
            cen_list_i = []
            ratio_list_i = []



            for jjdm in jjdm_list:
                # print(jjdm)

                tempdf=df[df['jjdm']==jjdm].sort_values('jsrq')

                if(i==0):
                    # get the theme exp from industry exp
                    tempdf=pd.merge(tempdf,theme_map,how='left',right_on='industry_name',left_on='yjxymc').drop('industry_name',axis=1)

                tempdf.set_index('jsrq', inplace=True)

                if(fre=='Q'):
                    q_date = tempdf.loc[[(x[4:6] == '03') | (x[4:6] == '09') for x in tempdf.index]].index.unique().tolist()
                    a_date = tempdf.loc[[(x[4:6] == '06') | (x[4:6] == '12') for x in tempdf.index]].index.unique().tolist()
                    q_list = q_date + a_date
                else:
                    q_list=tempdf.index.unique().tolist()

                q_list.sort()

                # themedf = tempdf[theme_col]

                #for i industry level
                inddf1=pd.DataFrame(data=q_list,columns=['jsrq'])
                inddf1=pd.merge(inddf1,tempdf.reset_index().drop_duplicates('jsrq')[['jsrq','jjjzc']],
                               how='left',on='jsrq')


                for col in self.new_col_list[i]:
                    inddf1=pd.merge(inddf1,tempdf[tempdf[industry_class] == col]['zsbl'],
                                   how='left',left_on='jsrq',right_index=True).rename(columns={'zsbl':col}).fillna(0)
                    # print(col)
                    # print(len(inddf1))
                if (i == 0):
                    tempdftheme=tempdf.groupby(['jsrq','theme']).sum().reset_index()
                    for theme in self.theme_col:
                        inddf1 = pd.merge(inddf1, tempdftheme[tempdftheme['theme'] == theme][['jsrq','zsbl']],
                                          how='left', on='jsrq').rename(
                            columns={'zsbl': theme}).fillna(0)

                inddf1.set_index('jsrq',inplace=True)

                # calculate the industry and theme holding centralization_level
                average_ind_cen_level = self.centralization_level(inddf1[self.new_col_list[i]],3, 5)
                cen_list_i.append(average_ind_cen_level.mean()[0])


                # calculate the industry and theme holding shift ratio
                shift_ratio =calculate_style_shift_rate(inddf1[self.new_col_list[i]])
                ratio_list_i.append(shift_ratio.mean())

                ratio_temp = pd.merge(average_ind_cen_level,shift_ratio.to_frame('shift_ratio'),how='left',
                                      left_index=True,right_index=True)
                ratio_temp['jjdm'] = jjdm

                if(i==0):

                    # average_theme_cen_level=0
                    average_theme_cen_level = self.centralization_level(inddf1[theme_col].loc[q_list], 1, 2)
                    cen_list_theme.append(average_theme_cen_level.mean()[0])
                    shift_ratio_theme = self.ind_shift_rate(inddf1[theme_col + ['jjjzc']].loc[q_list])
                    ratio_list_theme.append(shift_ratio_theme.mean())

                    average_ind_num_list.append((inddf1.loc[q_list][self.new_col_list[i]]>0).sum(axis=1).mean())


                    # get the string list of top 5 industry
                    top5 = inddf1[self.new_col_list[i]].mean().sort_values(ascending=False)[0:5].index.tolist()
                    top5 = util.list_sql_condition(top5)
                    top5_ind.append(top5)

                    longtoumean.append(tempdf.groupby('jsrq').mean()['longtou_zsbl'].mean())
                    longtoumed.append(tempdf.groupby('jsrq').mean()['longtou_zsbl'].median())
                    new_jjdm_list.append(jjdm)

                    temp_theme=inddf1[theme_col]
                    temp_theme['jjdm']=jjdm

                    theme_exp_his=pd.concat([theme_exp_his,temp_theme],axis=0)
                    ratio_temp = pd.merge(ratio_temp, average_theme_cen_level.rename(columns={'c_level':'c_level_theme'}), how='left',
                                          left_index=True, right_index=True)
                    ratio_temp = pd.merge(ratio_temp, shift_ratio_theme.to_frame('shift_ratio_theme'), how='left',
                                          left_index=True, right_index=True)
                elif(i==1):
                    # get the string list of top 5 industry
                    top20 = inddf1[self.new_col_list[i]].mean().sort_values(ascending=False)[0:20].index.tolist()
                    top20 = util.list_sql_condition(top20)
                    top20_ind_2.append(top20)
                else:
                    # get the string list of top 5 industry
                    top20 = inddf1[self.new_col_list[i]].mean().sort_values(ascending=False)[0:20].index.tolist()
                    top20 = util.list_sql_condition(top20)
                    top20_ind_3.append(top20)


                ratio_his=pd.concat([ratio_his,ratio_temp],axis=0)

                report_times=len(tempdf.index.unique())
                #for i industry level
                ind_mean=pd.concat([(tempdf.groupby(industry_class).sum()/report_times)['zsbl']
                                       ,tempdf.groupby(industry_class).mean()[target_col]],axis=1)
                ind_med=tempdf.groupby(industry_class).median()[['zsbl']+target_col]
                ind_mean=pd.merge(ind_mean,ind_med,
                         how='left',left_index=True,right_index=True)

                ind_mean.columns = ind_mean.columns.str.replace('_x','_mean')
                ind_mean.columns = ind_mean.columns.str.replace('_y', '_med')

                ind_mean['jjdm']=jjdm
                collect_df2=pd.concat([collect_df2,ind_mean],axis=0)

            # # save the cen and shift ratio into local db
            sql="delete from {3}{0} where jsrq>='{1}' and jsrq<='{2}'"\
                .format(str(i+1),ratio_his.index.min(),ratio_his.index.max(),cen_shift_his_table)
            #localdb.execute(sql)
            ratio_his.reset_index(drop=False).to_sql('hbs_cen_shift_ratio_his_industry{0}'.format(str(i+1)), con=localdb,
                                                      if_exists='append', index=False)

            # ratio_his.to_excel('ratio_his_{0}.xlsx'.format(str(i+1)))

            cen_list[i]=cen_list_i
            ratio_list[i]=ratio_list_i

            #abs value to rank
            if(if_prv ):
                max_asofdate=pd.read_sql("select max(asofdate) as asofdate from hbs_industry_property_{0}_industry_level"
                                        .format(str(i+1)),con=localdb)['asofdate'][0]
                rank_benchmark=pd.read_sql("select * from hbs_industry_property_{0}_industry_level where asofdate='{1}'"
                                           .format(str(i+1),max_asofdate),con=localdb)

                collect_df2=collect_df2.reset_index()
                temprank=pd.concat([collect_df2,rank_benchmark[collect_df2.columns]],axis=0)
                temprank = temprank.groupby(industry_class).rank(method='min') / len(temprank['jjdm'].unique())
                temprank['growth_mean'] = temprank[
                    ['ROE_mean', 'OPERATINGREVENUEYOY_mean', 'NETPROFITGROWRATE_mean']].mean(axis=1)
                temprank['value_mean'] = temprank[
                    ['PB_mean', 'DIVIDENDRATIO_mean', 'PCF_mean', 'PE_mean']].mean(axis=1)
                temprank['growth_med'] = temprank[['ROE_med', 'OPERATINGREVENUEYOY_med', 'NETPROFITGROWRATE_med']].mean(
                    axis=1)
                temprank['value_med'] = temprank[
                    ['PB_med', 'DIVIDENDRATIO_med', 'PCF_med', 'PE_med']].mean(axis=1)
                temprank.columns = [x + "_rank" for x in temprank.columns.tolist()]
                collect_df2=pd.concat([collect_df2,temprank.iloc[0:len(collect_df2)]],axis=1)
                #merge the fre

                df.loc[(df['report_fre']=='monthly')|(df['report_fre']=='fund_stats'),
                       'report_fre']='quartetly'
                collect_df2=pd.merge(collect_df2,df.drop_duplicates('jjdm')[['jjdm', 'report_fre']],
                                     how='left',on='jjdm')
                collect_df2.set_index(industry_class,inplace=True)
            else:
                temprank = collect_df2.groupby(industry_class).rank(method='min') / len(jjdm_list)
                temprank['growth_mean']=temprank[['ROE_mean','OPERATINGREVENUEYOY_mean','NETPROFITGROWRATE_mean']].mean(axis=1)
                temprank['value_mean'] = temprank[['PB_mean','DIVIDENDRATIO_mean','PCF_mean','PE_mean']].mean(axis=1)
                temprank['growth_med']=temprank[['ROE_med','OPERATINGREVENUEYOY_med','NETPROFITGROWRATE_med']].mean(axis=1)
                temprank['value_med'] = temprank[['PB_med','DIVIDENDRATIO_med','PCF_med','PE_med']].mean(axis=1)
                temprank.columns=[x+"_rank" for x in temprank.columns.tolist()]
                collect_df2=pd.concat([collect_df2,temprank],axis=1)

            collect_df2['asofdate'] = asofdate
            collect_df2 = collect_df2.reset_index().rename(columns={'index': 'industryname'})
            collect_df2.drop('jjdm_rank',axis=1,inplace=True)


            sql = "delete from {2}_{1}_industry_level where asofdate='{0}'".format(asofdate,i+1,ind_porperty_table)
            localdb.execute(sql)
            collect_df2.to_sql('{1}_{0}_industry_level'.format(i+1,ind_porperty_table), index=False, if_exists='append',
                               con=localdb,chunksize=5000)

            print("industry level {} done".format(i+1))

        theme_exp_his.reset_index(drop=False,inplace=True)
        # theme_exp_his.reset_index(drop=False).to_excel('theme_exp.xlsx',index=False)
        sql = "delete from {2} where jsrq>='{0}' and jsrq<='{1}'" \
            .format( theme_exp_his['jsrq'].min(), theme_exp_his['jsrq'].max(),theme_exp_his_table)
        localdb.execute(sql)
        theme_exp_his.to_sql(theme_exp_his_table, con=localdb,
                                                      if_exists='append', index=False)

        collect_df['cen_ind_1'] = cen_list[0]
        collect_df['ratio_ind_1'] = ratio_list[0]
        collect_df['cen_ind_2'] = cen_list[1]
        collect_df['ratio_ind_2'] = ratio_list[1]
        collect_df['cen_ind_3'] = cen_list[2]
        collect_df['ratio_ind_3'] = ratio_list[2]

        collect_df['jjdm'] = new_jjdm_list

        collect_df['cen_theme'] = cen_list_theme
        collect_df['ratio_theme'] = ratio_list_theme
        collect_df['longtou_mean'] = longtoumean
        collect_df['longtou_med'] = longtoumed
        collect_df['industry_num'] = average_ind_num_list
        collect_df['top5'] = top5_ind
        collect_df['top20_2'] = top20_ind_2
        collect_df['top20_3'] = top20_ind_3

        if(if_prv and fre=='Q'):
            max_asofdate=pd.read_sql('select max(asofdate) as asofdate from hbs_industry_property_new'
                                     ,con=localdb)['asofdate'][0]
            rank_benchmark=pd.read_sql("select * from hbs_industry_property_new where asofdate='{0}'"
                                       .format(max_asofdate),con=localdb)

            collect_df=pd.concat([collect_df,rank_benchmark[collect_df.columns.tolist()]],axis=0)



        collect_df['cen_ind_1_rank'] = collect_df['cen_ind_1'].rank(method='min') / len(collect_df)
        collect_df['ratio_ind_1_rank'] = collect_df['ratio_ind_1'].rank(method='min') / len(collect_df)

        collect_df['cen_ind_2_rank'] = collect_df['cen_ind_2'].rank(method='min') / len(collect_df)
        collect_df['ratio_ind_2_rank'] = collect_df['ratio_ind_2'].rank(method='min') / len(collect_df)

        collect_df['cen_ind_3_rank'] = collect_df['cen_ind_3'].rank(method='min') / len(collect_df)
        collect_df['ratio_ind_3_rank'] = collect_df['ratio_ind_3'].rank(method='min') / len(collect_df)


        collect_df['cen_theme_rank'] = collect_df['cen_theme'].rank(method='min') / len(collect_df)
        collect_df['ratio_theme_rank'] = collect_df['ratio_theme'].rank(method='min') / len(collect_df)

        collect_df['longtou_mean_rank']=collect_df['longtou_mean'].rank(method='min')/len(collect_df)
        collect_df['longtou_med_rank']=collect_df['longtou_med'].rank(method='min')/len(collect_df)

        collect_df['asofdate'] = asofdate

        if(if_prv):
            collect_df=collect_df.iloc[0:len(jjdm_list)]

        # collect_df.to_csv('collectdf.csv', index=False,encoding='gbk')

        # check if data already exist
        sql = "delete from hbs_industry_property_new where asofdate='{0}'".format(asofdate)
        # localdb.execute(sql)

        collect_df.to_sql('hbs_industry_property_new', index=False, if_exists='append', con=localdb)

    def save_industry_shift_property2localdb(self,asofdate=datetime.datetime.today().strftime('%Y%m%d'), time_length=3,if_prv=False):

        if(if_prv):
            industry_shift_table='hbs_prv_industry_shift_property'
            theme_shift_table='hbs_prv_theme_shift_property'
        else:
            industry_shift_table='hbs_industry_shift_property_new'
            theme_shift_table='hbs_theme_shift_property_new'

        collect_df = pd.DataFrame()
        collect_df_theme=pd.DataFrame()
        start_date = str(int(asofdate[0:4]) - time_length) + asofdate[4:]

        theme_col = self.theme_col
        # theme_map = self.theme_map

        def get_factor_return(start_date, asofdate,style_list):

            # sql="select fldm,flmc,zsdm from st_market.t_st_zs_hyzsdmdyb where hyhfbz='2' and fljb='1' "
            # industry_index_code=hbdb.db2df(sql,db='alluser')
            # industry_index_code['name_eng']=[self.industry_name_map[x] for x in industry_index_code['flmc']]
            #
            # style=util.list_sql_condition(
            #     [industry_index_code[industry_index_code['name_eng']==x.split('_')[0]]['zsdm'].iloc[0] for x in style_list])

            style=util.list_sql_condition(style_list)
            sql="select zqdm,jyrq,spjg from st_market.t_st_zs_hqql where zqdm in ({0}) and jyrq>='{1}' and  jyrq<='{2}'  "\
                .format(style,start_date,asofdate)
            fac_ret_df=hbdb.db2df(sql, db='alluser')
            fac_ret_df['jyrq']=fac_ret_df['jyrq'].astype(str)
            fac_ret_df.set_index('jyrq', drop=True, inplace=True)

            fac_ret_df['price'] = fac_ret_df['spjg']

            fac_ret_df['zqdm'] = [self.index_code_map[x] for x in fac_ret_df['zqdm']]

            return fac_ret_df

        def get_factor_return_theme(start_date,asofdate):

            factor_return_theme_raw = pd.read_sql(
                "select * from nav_theme_ret_new where TRADE_DATE>='{0}' and TRADE_DATE<='{1}' "
                .format(start_date, asofdate), con=localdb).rename(columns={'TRADE_DATE': "jyrq"})
            factor_return_theme_raw['jyrq']=factor_return_theme_raw['jyrq'].astype('str')
            factor_return_theme_raw.set_index('jyrq', inplace=True, drop=True)
            factor_return_theme_raw = factor_return_theme_raw + 1
            factor_return_theme_raw = factor_return_theme_raw.rolling(len(factor_return_theme_raw), 1).apply(np.prod)

            factor_return_theme = pd.DataFrame()
            for col in theme_col:
                temp_theme = factor_return_theme_raw['大金融'].to_frame('price')
                temp_theme['zqdm'] = col
                factor_return_theme = pd.concat([factor_return_theme, temp_theme], axis=0)

            return  factor_return_theme

        factor_return=get_factor_return(start_date,asofdate,self.index_code_list)

        factor_return_theme=get_factor_return_theme(start_date,asofdate)

        if(if_prv):
            exp_table='hbs_prv_industry_class1_exp'
        else:
            exp_table = 'hbs_industry_class1_exp'

        df = pd.read_sql("SELECT jsrq,jjdm,yjxymc,zjbl,know_weight from {2} where jsrq>='{0}' and jsrq<='{1}' "
                         .format(start_date,asofdate,exp_table), con=localdb)
        df_new=df.groupby(['jjdm','jsrq']).mean()['know_weight'].reset_index()

        #zjbl to zsbl
        for col in self.new_col_name:
            df_new=pd.merge(df_new,df[df['yjxymc']==col][['jjdm','jsrq','zjbl']],
                            how='left',on=['jjdm','jsrq']).rename(columns={'zjbl':col})
            df_new[col]=df_new[col]/df_new['know_weight']

        del df


        jjdm_list=df_new['jjdm'].unique().tolist()
        jjdm_list.sort()
        df_new.rename(columns={'jsrq': 'date'},inplace=True)
        df_new.set_index('date',inplace=True)
        df_new=df_new.fillna(0)

        #get the theme exp from industry exp
        for col in theme_col:
            df_new[col]=df_new[self.theme_map[col]].sum(axis=1)
        #540007,530003,519752
        for jjdm in jjdm_list:

            try:
                tempdf=df_new[df_new['jjdm']==jjdm]
                # df, q_list = ba.ret_div(jjdm, start_date, asofdate, True)
                q_date = tempdf.loc[[(x[4:6] == '03') | (x[4:6] == '09') for x in tempdf.index]].index
                a_date = tempdf.loc[[(x[4:6] == '06') | (x[4:6] == '12') for x in tempdf.index]].index
                q_list = q_date.to_list() + a_date.to_list()
                q_list.sort()


                ind_shift_df=pd.merge(pd.Series(['Total']+self.new_col_name).to_frame('风格类型'),
                                      self.style_shifting_analysis(
                    tempdf[self.new_col_name].astype(float),
                    q_list, self.new_col_name,
                    t1=0.1 , t2=0.05 , name='industry', jjdm=jjdm,factor_return=factor_return),how='left',
                                      on=['风格类型'])

                theme_shift_df=pd.merge(pd.Series(['Total']+theme_col).to_frame('风格类型'),
                                      self.style_shifting_analysis(
                    tempdf[theme_col].astype(float),
                    q_list, theme_col,
                    t1=0.2 , t2=0.5*0.2 , name='theme', jjdm=jjdm,factor_return=factor_return_theme),how='left',
                                      on=['风格类型'])

                ind_shift_df=ind_shift_df.T
                ind_shift_df.columns=ind_shift_df.loc['风格类型']
                ind_shift_df.drop('风格类型',axis=0,inplace=True)
                ind_shift_df['jjdm'] = jjdm
                ind_shift_df.reset_index(drop=False,inplace=True)

                #
                theme_shift_df=theme_shift_df.T
                theme_shift_df.columns=theme_shift_df.loc['风格类型']
                theme_shift_df.drop('风格类型',axis=0,inplace=True)
                theme_shift_df['jjdm'] = jjdm
                theme_shift_df.reset_index(drop=False,inplace=True)

                collect_df=pd.concat([collect_df,ind_shift_df],axis=0)
                collect_df_theme=pd.concat([collect_df_theme,theme_shift_df],axis=0)

                print('{} done'.format(jjdm))

            except Exception as e:
                print(jjdm)
                print(e)


        collect_df[['Total']+self.new_col_name] = collect_df[['Total']+self.new_col_name].astype(
            float)
        collect_df_theme[['Total']+theme_col] = collect_df_theme[['Total']+theme_col].astype(
            float)

        collect_df.rename(columns=self.industry_name_map_e2c, inplace=True)

        collect_df.rename(columns={'index': '项目名'}, inplace=True)
        collect_df_theme.rename(columns={'index': '项目名'}, inplace=True)

        if(if_prv):
            max_asofdate=pd.read_sql("select max(asofdate) as asofdate from hbs_industry_shift_property_new",
                                     con=localdb)['asofdate'][0]
            rank_benchmark=pd.read_sql("select * from hbs_industry_shift_property_new where asofdate='{}'"
                                       .format(max_asofdate),
                                     con=localdb)
            orginal_len=len(collect_df)
            collect_df=pd.concat([collect_df,rank_benchmark[collect_df.columns.tolist()]],axis=0)
            collect_df[self.new_col_name]=collect_df[self.new_col_name].astype(float)

            rank_benchmark=pd.read_sql("select * from hbs_theme_shift_property_new where asofdate='{}'"
                                       .format(max_asofdate),
                                     con=localdb)
            orginal_len_theme=len(collect_df_theme)
            collect_df_theme=pd.concat([collect_df_theme,rank_benchmark[collect_df_theme.columns.tolist()]],
                                       axis=0)
            collect_df_theme[theme_col] = collect_df_theme[theme_col].astype(float)

        collect_df[[x+'_rank' for
                    x in ['Total']+
                    list(self.new_col_name)
                    ]]=collect_df.groupby('项目名').rank(method='min')[['Total']+
                                                                       list(self.new_col_name)]\
                       /collect_df.groupby('项目名').count()[['Total']+
                                                                       list(self.new_col_name)].loc['切换次数']

        collect_df_theme[[x+'_rank' for
                    x in ['Total']+
                    theme_col
                    ]]=collect_df_theme.groupby('项目名').rank(method='min')[['Total']+
                                                                       theme_col]\
                       /collect_df_theme.groupby('项目名').count()[['Total']+
                                                                       theme_col].loc['切换次数']

        if(if_prv):
            collect_df=collect_df.iloc[0:orginal_len]
            collect_df_theme = collect_df_theme.iloc[0:orginal_len_theme]

        collect_df['asofdate']=df_new.index.max()
        collect_df_theme['asofdate']=df_new.index.max()

        # collect_df.to_excel('industry_shit.xlsx',index=False)
        # collect_df_theme.to_excel('theme_shit.xlsx',index=False)

        #check if already exist
        sql="delete from {1} where asofdate='{0}'".format(df_new.index.max(),industry_shift_table)
        # localdb.execute(sql)
        collect_df.to_excel('test.xlsx')
        collect_df.to_sql(industry_shift_table,index=False,if_exists='append',con=localdb)

        #check if already exist
        sql="delete from {1} where asofdate='{0}'".format(df_new.index.max(),theme_shift_table)
        # localdb.execute(sql)
        collect_df_theme.to_excel('test2.xlsx')
        collect_df_theme.to_sql(theme_shift_table,index=False,if_exists='append',con=localdb)

class Style_analysis:

    def __init__(self):

        self.value_col = ['399370', '399371']
        self.size_col=['399314','399315','399316']
        self.bond_col=['CBA00301']

        self.index_map=dict(zip(self.value_col+self.size_col,['成长','价值','大盘','中盘','小盘']))

        self.index_map2=dict(zip(['成长','价值','大盘','中盘','小盘'],self.value_col+self.size_col))

        # start_year=str(int(asofdate[0:4])-time_length)
        #
        # if(asofdate[4:6]<='03'):
        #     Q=1
        # elif(asofdate[4:6]>'03' and asofdate[4:6]<='06'):
        #     Q=2
        # elif(asofdate[4:6]>'06' and asofdate[4:6]<='09'):
        #     Q=3
        # elif(asofdate[4:6]>'09' and asofdate[4:6]<='12'):
        #     Q=4
        # start_date=start_year+"Q"+str(Q)
        #
        # self.val_date=self.get_jj_valuation_date(jjdm_list,asofdate)
        # self.asofdate=asofdate
        # self.start_date=start_date

    @staticmethod
    def read_style_expfromdb(asofdate,time_length,if_prv,fre='Q'):

        fre_con=''
        start_date=str(int(asofdate[0:4])-time_length)+asofdate[4:6]+'01'

        if(if_prv):
            style_exp_table='hbs_prv_style_exp'
            size_exp_table='hbs_prv_size_exp'
            if(fre=='M'):
                fre_con="where report_fre='monthly'"
        else:
            style_exp_table='hbs_style_exp'
            size_exp_table='hbs_size_exp'

        sql="select * from {0} where jsrq>='{2}' and jsrq<='{3}' {1}"\
            .format(style_exp_table,fre_con,start_date,asofdate)
        style_exp=pd.read_sql(sql,con=localdb)

        style_exp['month']=style_exp['jsrq'].astype(str).str[4:6]
        if(fre=='Q'):
            style_exp=style_exp[(style_exp['month']=='03')|(style_exp['month']=='06')|(style_exp['month']=='09')|(style_exp['month']=='12')]
        style_exp.drop('month',axis=1,inplace=True)

        # style_exp=pd.merge(style_exp[style_exp['style_type']=='价值'][['jjdm','jsrq','zjbl','jjzzc']].rename(columns={'zjbl':'价值'}),
        #                    style_exp[style_exp['style_type']=='成长'][['jjdm','jsrq','zjbl','jjzzc']].rename(columns={'zjbl':'成长'}),
        #                    how='outer',on=['jjdm','jsrq']).fillna(0)
        # if(if_prv):
        #     style_exp['jjzzc']=100
        # else:
        #     style_exp['jjzzc']=style_exp[['jjzzc_x','jjzzc_y']].max(axis=1)
        # style_exp.drop(['jjzzc_x', 'jjzzc_y'], axis=1, inplace=True)

        style_exp=pd.merge(style_exp.pivot_table('zjbl',['jjdm','jsrq'],'style_type').reset_index()
                           ,style_exp[['jsrq','jjdm','jjzzc']].drop_duplicates(['jsrq','jjdm']),
                 how='left',on=['jsrq','jjdm'])


        sql="select * from {0} where jsrq>='{2}' and jsrq<='{3}' {1}"\
            .format(size_exp_table,fre_con,start_date,asofdate)
        tempdf=pd.read_sql(sql,con=localdb)

        # size_exp=pd.merge(tempdf[tempdf['size_type']=='大盘'][['jjdm','jsrq','zjbl','jjzzc']].rename(columns={'zjbl':'大盘'}),
        #                   tempdf[tempdf['size_type']=='中盘'][['jjdm','jsrq','zjbl','jjzzc']].rename(columns={'zjbl':'中盘'}),
        #                   how='outer',on=['jjdm','jsrq'])
        #
        # size_exp=pd.merge(size_exp,
        #                   tempdf[tempdf['size_type']=='小盘'][['jjdm','jsrq','zjbl','jjzzc']].rename(columns={'zjbl':'小盘'}),
        #                   how='inner',on=['jjdm','jsrq']).rename(columns={'jjzzc':'jjzzc_z'})
        # if(if_prv):
        #     size_exp['jjzzc']=100
        # else:
        #     size_exp['jjzzc'] = size_exp[['jjzzc_x', 'jjzzc_y','jjzzc_z']].sum(axis=1)
        # size_exp.drop(['jjzzc_x', 'jjzzc_y','jjzzc_z'],axis=1,inplace=True)

        size_exp=pd.merge(tempdf.pivot_table('zjbl',['jjdm','jsrq'],'size_type').reset_index()
                           ,tempdf[['jsrq','jjdm','jjzzc']].drop_duplicates(['jsrq','jjdm']),
                 how='left',on=['jsrq','jjdm'])

        style_exp['jsrq']=style_exp['jsrq'].astype(str)
        size_exp['jsrq']=size_exp['jsrq'].astype(str)

        return style_exp,size_exp

    def save_style_property2db(self,asofdate, time_length=3,if_prv=False,fre='Q'):

        if(fre=='Q'):
            fre_table=''
        else:
            fre_table='_monthly'

        if(if_prv):
            ratio_his_table='hbs_prv_cen_shift_ratio_his_style{}'.format(fre_table)
            style_property_table='hbs_prv{}_style_property'.format(fre_table)
            size_property_table='hbs_prv{}_size_property'.format(fre_table)

        else:
            ratio_his_table='hbs_cen_shift_ratio_his_style'
            style_property_table='hbs_style_property'
            size_property_table='hbs_size_property'

        style_exp, size_exp=self.read_style_expfromdb(asofdate, time_length,if_prv,fre=fre)

        #take year and half year report only
        style_exp['month'] = style_exp['jsrq'].str[4:6]
        style_exp=style_exp[style_exp['month'].isin(['12','06'])]

        size_exp['month'] = size_exp['jsrq'].str[4:6]
        size_exp=size_exp[size_exp['month'].isin(['12','06'])]


        style_property=pd.DataFrame()
        size_property=pd.DataFrame()

        cen_s_list=[]
        cen_size_list=[]
        shift_ratio_s_list=[]
        shift_ratio_size_list=[]
        value_exp_list=[]
        growth_exp_list=[]
        balance_exp_list = []
        b_exp=[]
        s_exp=[]
        ratio_his=pd.DataFrame()

        jjdm_list=list(set(util.get_stock_funds_pool(asofdate,2))
                       .intersection(style_exp['jjdm'].unique()) )+['010381','011251']


        # for level in range(3):
        #     start_date=str(int(style_exp['jsrq'].max()[0:4]) - (i+1))+style_exp['jsrq'].max()[4:6]+'31'
        for jjdm in jjdm_list:
            print(jjdm)
            tempdf=style_exp[style_exp['jjdm']==jjdm]

            #standardlize
            total_weight=tempdf[['价值','成长']].sum(axis=1)
            total_weight2 = tempdf[['价值', '均衡', '成长']].sum(axis=1)
            for col in ['价值','成长','均衡']:
                tempdf[col+'_调整后']=tempdf[col]/total_weight
                tempdf[col]=tempdf[col]/total_weight2

            cen_lv=centralization_level(tempdf.set_index('jsrq')[['价值_调整后','成长_调整后']].fillna(0),1,0)
            shift_ratio=calculate_style_shift_rate(tempdf.set_index('jsrq')[['价值_调整后','成长_调整后']].fillna(0))
            cen_s_list.append(cen_lv.mean()[0])
            shift_ratio_s_list.append(shift_ratio.mean())
            value_exp_list.append(tempdf['价值'].fillna(0).mean())
            growth_exp_list.append(tempdf['成长'].fillna(0).mean())
            balance_exp_list.append(tempdf['均衡'].fillna(0).mean())
            temp_ratio=pd.merge(cen_lv.rename(columns={'c_level':'c_level_style'}),
                                shift_ratio.to_frame('shift_ratio_style'),how='outer',
                                left_index=True,right_index=True)


            tempdf=size_exp[size_exp['jjdm']==jjdm]
            tempdf['中小盘']=tempdf['中盘']+tempdf['小盘']
            tempdf.drop(['中盘','小盘'],axis=1,inplace=True)
            #standardlize
            # total_weight = tempdf[ ['大盘','中盘','小盘']].sum(axis=1)
            total_weight = tempdf[ ['大盘','中小盘']].sum(axis=1)
            for col in ['大盘','中小盘']:
                tempdf[col]=tempdf[col]/total_weight

            # cen_lv=centralization_level(tempdf.set_index('jsrq')[['大盘','中盘','小盘']],1,2)
            cen_lv=centralization_level(tempdf.set_index('jsrq')[['大盘','中小盘']].fillna(0),1,0)
            shift_ratio=calculate_style_shift_rate(tempdf.set_index('jsrq')[['大盘','中小盘']].fillna(0))
            cen_size_list.append(cen_lv.mean()[0])
            shift_ratio_size_list.append(shift_ratio.mean())
            b_exp.append(tempdf['大盘'].fillna(0).mean())
            # m_exp.append(tempdf['中盘'].mean())
            s_exp.append(tempdf['中小盘'].fillna(0).mean())
            temp_ratio=pd.merge(temp_ratio,cen_lv.rename(columns={'c_level':'c_level_size'}),
                                how='outer',
                                left_index=True,right_index=True)
            temp_ratio=pd.merge(temp_ratio,
                                shift_ratio.to_frame('shift_ratio_size'),
                                how='outer',left_index=True,right_index=True)
            temp_ratio.reset_index(inplace=True)
            temp_ratio['jjdm'] = jjdm
            ratio_his=pd.concat([ratio_his,temp_ratio],axis=0)

        # save the cen and shift ratio into local db
        sql = "delete from {2} where jsrq>={0} and jsrq<={1}" \
            .format(ratio_his['jsrq'].min(), ratio_his['jsrq'].max(),ratio_his_table)
        localdb.execute(sql)
        ratio_his.to_sql(ratio_his_table, con=localdb,
                                                     if_exists='append', index=False)

        style_property['cen_lv']=cen_s_list
        style_property['shift_lv'] = shift_ratio_s_list
        style_property['成长'] = growth_exp_list
        style_property['价值'] = value_exp_list
        style_property['均衡'] = balance_exp_list


        size_property['cen_lv'] = cen_size_list
        size_property['shift_lv'] = shift_ratio_size_list
        size_property['大盘'] = b_exp
        # size_property['中盘'] = m_exp
        size_property['中小盘'] = s_exp

        if(if_prv and fre=='Q'):
            max_asofdate=pd.read_sql("select max(asofdate) as afd from hbs_style_property",con=localdb)['afd'][0]
            rank_benchmark=pd.read_sql("select cen_lv,shift_lv,`成长`,`价值` from hbs_style_property where asofdate='{0}'"
                                       .format(max_asofdate),con=localdb)
            orginal_style_len=len(style_property)
            style_property=pd.concat([style_property,rank_benchmark],axis=0)

            max_asofdate=pd.read_sql("select max(asofdate) as afd from hbs_size_property",con=localdb)['afd'][0]
            rank_benchmark=pd.read_sql("select cen_lv,shift_lv,`大盘`,`中小盘` from hbs_size_property where asofdate='{0}'"
                                       .format(max_asofdate),con=localdb)
            orginal_size_len=len(size_property)
            size_property=pd.concat([size_property,rank_benchmark],axis=0)

        for col in style_property.columns:
            style_property[col+'_rank']=(style_property[col].fillna(0)).rank(method='min')/len(style_property)

        for col in size_property.columns:
            size_property[col+'_rank']=(size_property[col].fillna(0)).rank(method='min')/len(size_property)

        if(if_prv and fre=='Q'):
            style_property=style_property.iloc[0:orginal_style_len]
            size_property=size_property.iloc[0:orginal_size_len]

        style_property['jjdm']=jjdm_list
        size_property['jjdm'] = jjdm_list
        style_property['asofdate']=style_exp['jsrq'].max()
        size_property['asofdate']=size_exp['jsrq'].max()

        # #check if date already exist
        sql="delete from {1} where asofdate='{0}'".format(style_exp['jsrq'].max(),style_property_table)
        localdb.execute(sql)
        style_property.to_sql(style_property_table,index=False,if_exists='append',con=localdb)

        sql="delete from {1} where asofdate='{0}'".format(size_exp['jsrq'].max(),size_property_table)
        localdb.execute(sql)
        size_property.to_sql(size_property_table,index=False,if_exists='append',con=localdb)

    #below is for further analysis

    def style_change_detect_engine(self,q_df,diff1,diff2,q_list,col_list,t1,t2):

        style_change=[]

        for col in col_list:

            potential_date=diff2[diff2[col]<=-1*t1].index.to_list()
            last_added_date=q_list[-1]
            for date in potential_date:
                if(diff1.loc[q_df.index[q_df.index<=date][-3]][col]<=-1*t2):
                    added_date=q_df.index[q_df.index<=date][-3]
                elif(diff1.loc[q_df.index[q_df.index<=date][-2]][col]<=-1*t2):
                    added_date=q_df.index[q_df.index<=date][-2]
                elif(diff1.loc[q_df.index[q_df.index<=date][-1]][col]<=-1*t2):
                    added_date = q_df.index[q_df.index <= date][-1]
                else:
                    added_date = q_df.index[q_df.index <= date][-3]

                if((q_list.index(added_date)-q_list.index(last_added_date)<=2
                        and q_list.index(added_date)-q_list.index(last_added_date)>0) or added_date==q_list[-1]):
                    continue
                else:
                    style_change.append(added_date + "@" + col)
                    last_added_date = added_date

            potential_date = diff2[diff2[col] >= t1].index.to_list()
            last_added_date = q_list[-1]
            for date in potential_date:
                if (diff1.loc[q_df.index[q_df.index <= date][-3]][col] >= t2):
                    added_date = q_df.index[q_df.index <= date][-3]
                elif (diff1.loc[q_df.index[q_df.index <= date][-2]][col] >= t2):
                    added_date = q_df.index[q_df.index <= date][-2]
                elif (diff1.loc[q_df.index[q_df.index <= date][-1]][col] >= t2):
                    added_date = q_df.index[q_df.index <= date][-1]
                else:
                    added_date = q_df.index[q_df.index <= date][-3]

                if (q_list.index(added_date) - q_list.index(last_added_date) <= 2
                        and q_list.index(added_date) - q_list.index(last_added_date) > 0):
                    continue
                else:
                    style_change.append(added_date + "@" + col)
                    last_added_date = added_date

        return style_change

    def style_change_detect_engine2(self, q_df, diff1, col_list, t1, t2):

        style_change=[]
        t3=t2/2

        for col in col_list:

            tempdf=pd.merge(q_df[col],diff1[col],how='left',on='date')
            tempdf['style']=''
            style_num=0
            tempdf['style'].iloc[0:2] = style_num

            for i in range(2,len(tempdf)-1):
                if(tempdf[col+'_y'].iloc[i]>t1 and tempdf[col+'_y'].iloc[i+1]>-1*t3 ):
                    style_num+=1
                    added_date = tempdf.index[i]
                    style_change.append(added_date + "@" + col)
                elif(tempdf[col+'_x'].iloc[i]-tempdf[tempdf['style']==style_num][col+'_x'].iloc[0]>t1 and
                     tempdf[col+'_y'].iloc[i]>t2 and tempdf[col+'_y'].iloc[i+1]>-1*t3):
                    style_num += 1
                    added_date=tempdf.index[i]
                    style_change.append(added_date + "@" + col)
                elif(tempdf[col+'_y'].iloc[i]<-1*t1 and tempdf[col+'_y'].iloc[i+1]<t3 ):
                    style_num += 1
                    added_date = tempdf.index[i]
                    style_change.append(added_date + "@" + col)
                elif (tempdf[col + '_x'].iloc[i] - tempdf[tempdf['style'] == style_num][col + '_x'].iloc[0] < -1*t1 and
                      tempdf[col + '_y'].iloc[i] < -1*t2 and tempdf[col + '_y'].iloc[i + 1] <  t3):
                    style_num += 1
                    added_date = tempdf.index[i]
                    style_change.append(added_date + "@" + col)

                tempdf['style'].iloc[i] = style_num

        return style_change

    def style_change_detect(self,df,q_list,col_list,t1,t2):

        q_list.sort()
        q_df = df.loc[q_list]
        diff1=q_df.diff(1)
        # diff2=q_df.rolling(3).mean().diff(2)
        # diff4 = q_df.rolling(3).mean().diff(4)

        # style_change_short=self.style_change_detect_engine(q_df,diff1,diff2,q_list,col_list,t1,t2)
        # style_change_long=self.style_change_detect_engine(q_df,diff1,diff4,q_list,col_list,t1,t2)
        # style_change=style_change_short+style_change_long

        style_change = self.style_change_detect_engine2(q_df, diff1, col_list, t1, t2)

        return list(set(style_change)),np.array(q_list)

    def shifting_expression(self,change_ret,name,jjdm,style='Total'):

        change_winning_pro_hld = sum(change_ret[3]) / len(change_ret)
        change_winning_pro_nextq=sum(change_ret[2]) / len(change_ret)
        left_ratio = sum(change_ret[0]) / len(change_ret)
        left_ratio_deep = sum(change_ret[1]) / len(change_ret)
        # right_ratio = 1-left_ratio
        # right_ratio_deep = 1 - left_ratio_deep
        one_q_ret = change_ret[4].mean()
        hid_q_ret = change_ret[5].mean()

        return  np.array([style.split('_')[0],len(change_ret),change_winning_pro_hld,change_winning_pro_nextq
                             ,one_q_ret,hid_q_ret,left_ratio,left_ratio_deep])

    def style_change_ret(self,df,q_list,col_list,t1,t2,factor_ret):

        style_change,q_list = self.style_change_detect(df,q_list,col_list,t1,t2)
        change_count = len(style_change)
        style_changedf=pd.DataFrame()
        style_changedf['date']=[x.split('@')[0] for x in style_change]
        style_changedf['style']=[x.split('@')[1] for x in style_change]
        style_changedf.sort_values('date',inplace=True,ascending=False)
        style_chang_extret=dict(zip(style_change,style_change))


        # def get_factor_return(q_list, first_change_date, style):
        #
        #     # get value index ret :
        #     sql="select zqdm,jyrq,spjg from st_market.t_st_zs_hqql where zqdm='{0}' and jyrq>='{1}' and jyrq<='{2}'"\
        #         .format(style, q_list[q_list < first_change_date][-2]+'01', q_list[-1]+'31')
        #
        #     fac_ret_df=hbdb.db2df(sql,db='alluser')
        #     fac_ret_df['jyrq']=fac_ret_df['jyrq'].astype(str)
        #
        #     fac_ret_df['ym']=fac_ret_df['jyrq'].str[0:6]
        #     tempdf=fac_ret_df.drop_duplicates('ym', keep='last')[['jyrq','ym']]
        #     fac_ret_df=pd.merge(fac_ret_df,tempdf,how='left',on='jyrq').fillna('').drop('ym_x',axis=1)
        #
        #     # fac_ret_df['jyrq'] = fac_ret_df['ym']
        #     fac_ret_df.set_index('ym_y', drop=True, inplace=True)
        #
        #     fac_ret_df['price'] = fac_ret_df['spjg']
        #
        #     return fac_ret_df

        def q_ret(fac_ret_df,q0,q1,time_length=1):
            res=np.power(fac_ret_df.loc[q1]['price']/fac_ret_df.loc[q0]['price'],1/time_length)-1
            return  res


        if(change_count>0):
            for style in style_changedf['style']:

                changedf=style_changedf[style_changedf['style']==style]
                changedf=changedf.sort_values('date')
                first_change_date=changedf['date'].values[0]
                fac_ret_df=factor_ret[(factor_ret['zqdm'] == style) & (
                            factor_ret['jyrq'] >= q_list[q_list < first_change_date][-2]) & (
                                       factor_ret['jyrq'] <= q_list[-1] )]
                # fac_ret_df=get_factor_return(q_list,first_change_date,style)


                for i in range(len(changedf)):
                    date=changedf.iloc[i]['date']

                    observer_term=np.append(q_list[q_list<date][-2:],q_list[(q_list>=date)][0:2])

                    new_exp=df[style].loc[observer_term[2]]
                    old_exp=df[style].loc[observer_term[1]]

                    q0=observer_term[0]
                    q1=observer_term[1]
                    old_ret=q_ret(fac_ret_df,q0,q1)
                    #if_left_deep = fac_ret_df['price'].loc[q0:q1].mean() > fac_ret_df['price'].loc[q1]
                    if_left_deep =( (fac_ret_df['price'].loc[(fac_ret_df['jyrq']>=q0+'31')
                                                             &(fac_ret_df['jyrq']<=q1+'31')].mean()
                                     > fac_ret_df['price'].loc[q0:q1]).sum()\
                                   /len(fac_ret_df['price'].loc[q0:q1])>=0.5 )

                    q0=observer_term[1]
                    q1=observer_term[2]
                    current_ret=q_ret(fac_ret_df,q0,q1)
                    if_left=( (fac_ret_df['price'].loc[(fac_ret_df['jyrq']>=q0+'31')
                                                             &(fac_ret_df['jyrq']<=q1+'31')].mean()
                                     > fac_ret_df['price'].loc[q0:q1]).sum()\
                                   /len(fac_ret_df['price'].loc[q0:q1])>=0.5 )

                    q0=observer_term[2]
                    q1=observer_term[3]
                    next_ret=q_ret(fac_ret_df,q0,q1)


                    if (i != len(changedf) - 1):
                        q1 = changedf.iloc[i + 1]['date']
                        # q2 = q1
                    else:
                        q1 = q_list[-1]
                        # q2=fac_ret_df.index[-1]

                    change_date=date
                    time_length = q_list.tolist().index(q1) - q_list.tolist().index(change_date)
                    holding_ret=q_ret(fac_ret_df,q0,q1,time_length=time_length)

                    if_win_next=(new_exp>old_exp)&(next_ret>current_ret)
                    if_win_hld=(new_exp>old_exp)&(holding_ret>current_ret)

                    shift_retur_next= (new_exp-old_exp)*(next_ret-current_ret)
                    shift_retur_hld = (new_exp - old_exp) * (holding_ret - current_ret)

                    style_chang_extret[date+"@"+style]=[if_left,if_left_deep,if_win_next,if_win_hld,shift_retur_next,shift_retur_hld]

        return style_chang_extret

    def style_shifting_analysis(self,df,q_list,col_list,t1,t2,name,jjdm,factor_ret):

        # col_list=[x+"_exp_adj" for x in col]
        change_ret=self.style_change_ret(df,q_list,col_list,t1=t1,t2=t2,factor_ret=factor_ret)
        change_ret = pd.DataFrame.from_dict(change_ret).T
        change_ret['style'] = list([x.split('@')[1] for x in change_ret.index])
        change_ret['date'] = list([x.split('@')[0] for x in change_ret.index])

        data=[]

        if(len(change_ret)>0):
            data.append(self.shifting_expression(change_ret,name,jjdm))
            for style in change_ret['style'].unique():
                tempdf=change_ret[change_ret['style']==style]
                data.append(self.shifting_expression(tempdf,name,jjdm,style))

        shift_df = pd.DataFrame(data=data,columns=['风格类型','切换次数','胜率（直到下次切换）','胜率（下季度）',
                                                   '下季平均收益','持有平均收益','左侧比率','深度左侧比例'])
        # for col in ['胜率（直到下次切换）','胜率（下季度）','下季平均收益','持有平均收益','左侧比率','深度左侧比例']:
        #     shift_df[col] = shift_df[col].astype(float).map("{:.2%}".format)

        return  shift_df

    def style_shift_analysis(self,asofdate, time_length=3,if_prv=False):

        if(if_prv):
            value_shift_table='hbs_prv_shift_property_value'
            size_shift_table='hbs_prv_shift_property_size'
        else:
            value_shift_table='hbs_shift_property_value'
            size_shift_table='hbs_shift_property_size'

        #read style exp
        value_exp, size_exp = self.read_style_expfromdb(asofdate, time_length,if_prv)

        value_exp.drop('均衡',axis=1,inplace=True)
        value_exp.rename(columns=self.index_map2, inplace=True)
        size_exp.rename(columns=self.index_map2, inplace=True)
        value_exp.rename(columns={'jsrq':'date'}, inplace=True)
        size_exp.rename(columns={'jsrq':'date'}, inplace=True)

        jjdm_list=list(set(value_exp['jjdm'].unique()).intersection(set(size_exp['jjdm'].unique())))
        jjdm_list.sort()

        #shift the exp from real exp  to relative exp between exp col,so that the total exp is 100
        total_w=value_exp[self.value_col].sum(axis=1)
        for col in self.value_col:
            value_exp[col]=value_exp[col]/total_w

        total_w=size_exp[self.size_col].sum(axis=1)
        for col in self.size_col:
            size_exp[col]=size_exp[col]/total_w


        value_exp.set_index('date',inplace=True,drop=True)
        size_exp.set_index('date', inplace=True, drop=True)

        collect_df_size=pd.DataFrame()
        collect_df_value = pd.DataFrame()

        def get_factor_return(style_list,start_date,end_date):

            style=util.list_sql_condition(style_list)

            # get value index ret :
            sql="select zqdm,jyrq,spjg from st_market.t_st_zs_hqql where zqdm in({0}) and jyrq>='{1}' and jyrq<='{2}'"\
                .format(style, start_date,end_date)

            fac_ret_df=hbdb.db2df(sql,db='alluser')
            fac_ret_df['jyrq']=fac_ret_df['jyrq'].astype(str)

            # fac_ret_df['ym']=fac_ret_df['jyrq'].str[0:6]
            # tempdf=fac_ret_df.drop_duplicates('ym', keep='last')[['jyrq','ym']]
            # fac_ret_df=pd.merge(fac_ret_df,tempdf,how='left',on='jyrq').fillna('').drop('ym_x',axis=1)

            fac_ret_df.set_index('jyrq', drop=False, inplace=True)
            fac_ret_df['price'] = fac_ret_df['spjg']

            return fac_ret_df

        value_factor_ret=get_factor_return(self.value_col+self.size_col,start_date=value_exp.index.min(),end_date=value_exp.index.max())

        for jjdm in jjdm_list:

            print("{} start ".format(jjdm))

            try:

                tempdf =  value_exp[value_exp['jjdm'] == jjdm]

                q_list = tempdf.index.unique().tolist()
                q_list.sort()

                style_shift_df=pd.merge(pd.Series(['Total'] + self.value_col).to_frame('风格类型'),
                self.style_shifting_analysis(
                    tempdf[self.value_col],
                    q_list, self.value_col,
                    t1=0.35 , t2=0.35*0.75 , name='value', jjdm=jjdm,factor_ret=value_factor_ret),how='left',on=['风格类型'])

                style_shift_df = style_shift_df.T
                style_shift_df.columns = style_shift_df.loc['风格类型']
                style_shift_df.drop('风格类型', axis=0, inplace=True)
                style_shift_df['jjdm'] = jjdm
                style_shift_df.reset_index(drop=False, inplace=True)

                collect_df_value = pd.concat([collect_df_value, style_shift_df], axis=0)

                tempdf = size_exp[size_exp['jjdm'] == jjdm]

                q_list = tempdf.index.unique().tolist()
                q_list.sort()

                style_shift_df=pd.merge(pd.Series(['Total'] + self.size_col).to_frame('风格类型'),
                self.style_shifting_analysis(
                    tempdf[self.size_col],
                    q_list, self.size_col,
                    t1=0.2 , t2=0.2*0.75 , name='value', jjdm=jjdm,factor_ret=value_factor_ret),how='left',on=['风格类型'])

                style_shift_df = style_shift_df.T
                style_shift_df.columns = style_shift_df.loc['风格类型']
                style_shift_df.drop('风格类型', axis=0, inplace=True)
                style_shift_df['jjdm'] = jjdm
                style_shift_df.reset_index(drop=False, inplace=True)

                collect_df_size = pd.concat([collect_df_size, style_shift_df], axis=0)


            except Exception as e:
                print(jjdm)
                print(e)


        collect_df_value[['Total']+self.value_col] = collect_df_value[['Total']+self.value_col].astype(
            float)
        collect_df_size[['Total']+self.size_col] = collect_df_size[['Total']+self.size_col].astype(
            float)

        orginal_value_len = len(collect_df_value)
        orginal_size_len = len(collect_df_size)

        if(if_prv):
            max_asofdate=pd.read_sql("select max(asofdate) as afd from hbs_shift_property_value",con=localdb)['afd'][0]
            style_rank_benchmark=pd.read_sql("select `项目名`,Total,`成长`,`价值`,jjdm from hbs_shift_property_value where asofdate='{0}'"
                                       .format(max_asofdate),con=localdb).rename(columns={'项目名':'index',
                                                                                          '成长':'399370',
                                                                                          '价值':'399371'
                                                                                          })

            collect_df_value=pd.concat([collect_df_value,style_rank_benchmark],axis=0)

            max_asofdate=pd.read_sql("select max(asofdate) as afd from hbs_shift_property_size",con=localdb)['afd'][0]
            size_rank_benchmark=pd.read_sql("select `项目名`,Total,`大盘`,`中盘`,`小盘`,jjdm from hbs_shift_property_size where asofdate='{0}'"
                                       .format(max_asofdate),con=localdb).rename(columns={'项目名':'index',
                                                                                          '大盘':'399314',
                                                                                          '中盘':'399315',
                                                                                          '小盘': '399316'
                                                                                          })

            collect_df_size=pd.concat([collect_df_size,size_rank_benchmark],axis=0)

        for i in range(2):

            collect_df=[collect_df_value,collect_df_size][i]
            orginal_len=[orginal_value_len,orginal_size_len][i]

            collect_df.rename(columns=self.index_map, inplace=True)

            col_name_list=collect_df.columns.to_list()
            col_name_list.remove('index')
            col_name_list.remove('jjdm')


            collect_df[[x+'_rank' for
                        x in col_name_list
                        ]]=collect_df.groupby('index').rank(method='min')[col_name_list]\
                           /collect_df.groupby('index').count()[col_name_list].loc['切换次数']

            collect_df.rename(columns={'index': '项目名'}, inplace=True)
            collect_df=collect_df.iloc[0:orginal_len]

            collect_df['asofdate']=value_exp.index.max()


            if(len(collect_df.columns)==9):
                # check if already exist
                sql="delete from {1} where asofdate='{0}' "\
                    .format(value_exp.index.max(),value_shift_table)
                localdb.execute(sql)
                collect_df.to_sql(value_shift_table,index=False,if_exists='append',con=localdb)
            else:
                # check if already exist
                sql="delete from {1} where asofdate='{0}'"\
                    .format(value_exp.index.max(),size_shift_table)
                localdb.execute(sql)
                collect_df.to_sql(size_shift_table, index=False, if_exists='append', con=localdb)

        print('Done')

class General_holding:

    def __init__(self):
        self.indus_col=['aerodef','agriforest','auto','bank','builddeco','chem','conmat','commetrade','computer','conglomerates','eleceqp','electronics',
        'foodbever','health','houseapp','ironsteel','leiservice','lightindus','machiequip','media','mining','nonbankfinan','nonfermetal',
        'realestate','telecom','textile','transportation','utilities']
        chinese_name=['国防军工','农林牧渔','汽车','银行','建筑装饰','化工','建筑材料','商业贸易','计算机','综合','电气设备',
                      '电子','食品饮料','医药生物','家用电器','钢铁','休闲服务','轻工制造','机械设备','传媒','采掘','非银金融',
                      '有色金属','房地产','通信','纺织服装','交通运输','公用事业']
        self.industry_name_map=dict(zip(chinese_name,self.indus_col))

        self.industry_name_map_e2c = dict(zip(self.indus_col,chinese_name))

    @staticmethod
    def update_fund_holding_local_file(last_date,new_date):

        # data = \
        #     pd.read_pickle(r"E:\GitFolder\docs\基金画像更新数据\基金持仓数据\fund_holds_{}".format(last_date))
        data=\
            pd.read_pickle(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\Cache\File\2023-07\fund_holds")
        jjdm_list = util.get_all_mutual_stock_funds(new_date)
        sql = "select zjbl, zqmc, zlbl, ccsl, jjdm, jsrq, zqdm,ccsz,sszt,zgbl,ggrq from st_fund.t_st_gm_gpzh where jsrq>'{1}' and jjdm in ({0}) " \
            .format(util.list_sql_condition(jjdm_list),last_date)
        new_data = hbdb.db2df(sql, db='funduser')

        data = data[data['jsrq'] <= int(new_date)]
        data = pd.concat([data, new_data], axis=0)
        data.to_pickle(r"E:\GitFolder\docs\基金画像更新数据\基金持仓数据\fund_holds_{}".format(new_date))

    def get_cal_and_trade_cal(self, start, end):
        """
        获取交易日期
        """
        cal = HBDB().read_cal(start, end)
        cal = cal.rename(
            columns={'JYRQ': 'TRADE_DATE', 'SFJJ': 'IS_OPEN', 'SFZM': 'IS_WEEK_END', 'SFYM': 'IS_MONTH_END'})
        cal['IS_OPEN'] = cal['IS_OPEN'].astype(int).replace({0: 1, 1: 0})
        cal['IS_WEEK_END'] = cal['IS_WEEK_END'].fillna(0).astype(int)
        cal['IS_MONTH_END'] = cal['IS_MONTH_END'].fillna(0).astype(int)
        cal = cal.sort_values('TRADE_DATE')
        trade_cal = cal[cal['IS_OPEN'] == 1]
        trade_cal['RECENT_TRADE_DATE'] = trade_cal['TRADE_DATE']
        trade_cal['PREV_TRADE_DATE'] = trade_cal['TRADE_DATE'].shift(1)
        trade_cal = trade_cal[
            ['TRADE_DATE', 'RECENT_TRADE_DATE', 'PREV_TRADE_DATE', 'IS_OPEN', 'IS_WEEK_END', 'IS_MONTH_END']]
        cal = cal.merge(trade_cal[['TRADE_DATE', 'RECENT_TRADE_DATE']], on=['TRADE_DATE'], how='left')
        cal['RECENT_TRADE_DATE'] = cal['RECENT_TRADE_DATE'].fillna(method='ffill')
        cal = cal.merge(trade_cal[['TRADE_DATE', 'PREV_TRADE_DATE']], on=['TRADE_DATE'], how='left')
        cal['PREV_TRADE_DATE'] = cal['PREV_TRADE_DATE'].fillna(method='bfill')
        cal = cal[['TRADE_DATE', 'RECENT_TRADE_DATE', 'PREV_TRADE_DATE', 'IS_OPEN', 'IS_WEEK_END', 'IS_MONTH_END']]
        return cal, trade_cal

    @staticmethod
    def read_hld_fromdb(start_date,end_date,jjdm,keyholdonly=False,from_local_db=False):

        if(from_local_db):
            sql="""select jjdm,jsrq,zqdm,zjbl from artificial_quartly_full_hld where jjdm in {0} and jsrq>='{1}' and jsrq<='{2}'
            """.format(tuple(jjdm),start_date,end_date)
            hld=pd.read_sql(sql,con=localdb)
        else:

            sql="""select jjdm,jsrq,zqdm,zjbl from st_fund.t_st_gm_gpzh where jjdm='{0}' and jsrq>='{1}' and jsrq<='{2}'
            """.format(jjdm,start_date,end_date)
            hld=hbdb.db2df(sql,db='funduser')
        #take only key holding
        if(keyholdonly):
            hld['rank'] = hld.groupby('jsrq').rank(method='min',ascending=False)
            hld=hld[hld['rank']<=10]


        hld['jsrq']=hld['jsrq'].astype(str)
        return hld

    @staticmethod
    def read_hld_fromlocal(start_date,end_date,jjdm_list,keyholdonly=False,from_local_db=False):


        data=\
            pd.read_pickle(r"E:\GitFolder\docs\基金画像更新数据\基金持仓数据\fund_holds_20230630")
        # data=pd.read_pickle(r"E:\GitFolder\docs\本地数据\持仓补全数据20230630")
        hld=data[(data['jjdm'].isin(jjdm_list))&
                 (data['jsrq'].astype(str)>=start_date)&
                 (data['jsrq'].astype(str)<=end_date)][['jjdm','jsrq','zqdm','zjbl']]
        del data
        hld['jsrq']=hld['jsrq'].astype(str)
        #take only key holding
        if(keyholdonly):
            hld['rank'] = hld.groupby(['jsrq','jjdm']).rank(method='min',ascending=False)
            hld=hld[hld['rank']<=10]


        hld['jsrq']=hld['jsrq'].astype(str)
        return hld

    @staticmethod
    def read_hld_list_fromdb(start_date,end_date,jjdm_list,keyholdonly=False,from_local=False):

        if(from_local):

            sql="select jjdm,jsrq,zqdm,zjbl from artificial_quartly_full_hld where jjdm in ({0}) and jsrq>='{1}' and jsrq<='{2}' "\
                .format(util.list_sql_condition(jjdm_list),start_date,end_date)
            hld=pd.read_sql(sql,con=localdb)



        else:

            sql="""select jjdm,jsrq,zqdm,zjbl,ccsl from st_fund.t_st_gm_gpzh where jjdm in ({0}) and jsrq>='{1}' and jsrq<='{2}'
            """.format(util.list_sql_condition(jjdm_list),start_date,end_date)
            hld=hbdb.db2df(sql,db='funduser')
        #take only key holding
        if(keyholdonly):
            hld['rank'] = \
                hld.groupby(['jjdm','jsrq'])['zjbl'].rank(method='min',ascending=False)
            hld=hld[hld['rank']<=10]


        hld['jsrq']=hld['jsrq'].astype(str)

        hld['zjbl'] = hld['zjbl'] / 100

        return hld

    @staticmethod
    def hld_compenzation(hlddf,fund_allocation):

        q_date=hlddf.loc[[(x[4:6] == '03') | (x[4:6] == '09') for x in hlddf['jsrq']]]['jsrq'].unique().tolist()
        a_date=hlddf.loc[[(x[4:6] == '06') | (x[4:6] == '12') for x in hlddf['jsrq']]]['jsrq'].unique().tolist()
        q_list=hlddf['jsrq'].unique().tolist()
        q_list.sort()

        hld_H=pd.DataFrame()
        hld_L = pd.DataFrame()
        #get heavy hld for annual and half_annual report
        for date in a_date:
            hld_H=pd.concat([hld_H,hlddf[hlddf['jsrq']==date].sort_values('zjbl')[-10:].reset_index(drop=True)],axis=0)
            hld_L=pd.concat([hld_L,hlddf[hlddf['jsrq']==date].sort_values('zjbl')[0:-10].reset_index(drop=True)],axis=0)
        for date in q_date:
            hld_H=pd.concat([hld_H,hlddf[hlddf['jsrq']==date]],axis=0)


        for i in range(len(q_list)):
            t1=q_list[i]
            if((i>0) and (t1[4:6] == '03') or  (t1[4:6] == '09')):
                t0=q_list[i-1]
            else:
                continue
            #calculate the no hevay hld for quarter report data by the mean of two annaul data if next annaul report exists
            if(i!=len(q_list)-1):
                t2=q_list[i+1]
                temp=pd.merge(hlddf[hlddf['jsrq']==t0].sort_values('zjbl')[0:-10],
                              hlddf[hlddf['jsrq']==t2].sort_values('zjbl')[0:-10],
                              how='outer',on='zqdm').fillna(0)
                temp.set_index('zqdm',inplace=True)
                if(len(temp)==0):
                    continue
                drop_list=list(set(temp.index).intersection( set(hlddf[hlddf['jsrq']==t1]['zqdm'])))
                temp.drop(drop_list,axis=0,inplace=True)
                temp['zjbl']=(temp['zjbl_x']+temp['zjbl_y'])/2
                temp['zjbl']=temp['zjbl']*((fund_allocation[fund_allocation['jsrq'] == t1]['gptzzjb']*100-hld_H[hld_H['jsrq']==t1]['zjbl'].sum()).values[0]/temp['zjbl'].sum())
                temp['jsrq']=t1
                temp.reset_index(drop=False,inplace=True)
                hld_L=pd.concat([hld_L,temp[['zjbl','jsrq','zqdm']]],axis=0)

            else:
                temp=hlddf[hlddf['jsrq']==t0].sort_values('zjbl')[0:-10]
                temp['zjbl']=temp['zjbl']/temp['zjbl'].sum()
                temp['zjbl']=temp['zjbl']*(fund_allocation[fund_allocation['jsrq'] == t1]['gptzzjb']*100-hld_H[hld_H['jsrq']==t1]['zjbl'].sum()).values[0]
                temp['jsrq']=t1
                temp.reset_index(drop=False,inplace=True)
                hld_L=pd.concat([hld_L,temp[['zjbl','jsrq','zqdm']]],axis=0)
        return pd.concat([hld_H,hld_L],axis=0).sort_values('jsrq').reset_index(drop=True)

    @staticmethod
    def fund_asset_allocation(jjdm,date_list):

        sql="select jjdm,jsrq,jjzzc,gptzzjb from st_fund.t_st_gm_zcpz where jjdm='{2}' and jsrq>='{0}' and jsrq<='{1}'"\
            .format(date_list[0],date_list[-1],jjdm)
        fund_allocation=hbdb.db2df(sql,db='funduser')
        fund_allocation['gptzzjb']=fund_allocation['gptzzjb']/100
        fund_allocation['jsrq']=fund_allocation['jsrq'].astype(str)
        return fund_allocation

    @staticmethod
    def get_fund_jjjzc(jjdm_list,start_date,end_date):

        sql="select jjdm,jsrq,jjjzc,gptzzjb,hbzjzjb,zqzszzjb from st_fund.t_st_gm_zcpz where jjdm in ({2}) and jsrq>='{0}' and jsrq<='{1}'"\
            .format(start_date,end_date,util.list_sql_condition(jjdm_list))
        fund_allocation=hbdb.db2df(sql,db='funduser').fillna(0)
        fund_allocation['jsrq']=fund_allocation['jsrq'].astype(str)
        return fund_allocation

    @staticmethod
    def stock_centralization_lv(hld):

        # top3w=(hld[(hld.groupby('jsrq').rank(ascending=False,method='min')<=3)['zjbl']]
        #        .groupby('jsrq')['zjbl'].sum()).mean()
        # top5w=(hld[(hld.groupby('jsrq').rank(ascending=False,method='min')<=5)['zjbl']]
        #        .groupby('jsrq')['zjbl'].sum()).mean()
        # top10w=(hld[(hld.groupby('jsrq').rank(ascending=False,method='min')<=10)['zjbl']]
        #        .groupby('jsrq')['zjbl'].sum()).mean()

        top3w=(hld[(hld.groupby('jsrq').rank(ascending=False,method='min')<=3)['zjbl']]
               .groupby('jsrq')['zjbl'].sum())
        top5w=(hld[(hld.groupby('jsrq').rank(ascending=False,method='min')<=5)['zjbl']]
               .groupby('jsrq')['zjbl'].sum())
        top10w=(hld[(hld.groupby('jsrq').rank(ascending=False,method='min')<=10)['zjbl']]
               .groupby('jsrq')['zjbl'].sum())


        result=(top10w+top3w+top5w)/3


        return result,top3w.mean(),top5w.mean(),top10w.mean()

    @staticmethod
    def get_fund_financial_info(jjdm_list,start_date,end_date):

        jjdm_con=util.list_sql_condition(jjdm_list)

        sql="""
        select jjdm,jsrq,pe,pb,roe,dividend from st_fund.t_st_gm_jjggfg 
        where jsrq>='{0}' and jsrq<='{1}' and jjdm in ({2}) and zclb=2
        """\
            .format(start_date,end_date,jjdm_con)

        df=hbdb.db2df(sql,db='funduser')

        if(len(df)>0):

            df['jsrq']=df['jsrq'].astype(str)

            for col in ['pe','pb','roe','dividend']:
                df.loc[df[col]==99999,col]=np.nan
        else:

            df=pd.DataFrame(columns=['jjdm','jsrq','pe','pb','roe','dividend'])

        return  df

    @staticmethod
    def get_stock_price(zqdm_list=None,date_list=None):

        count=0
        if(zqdm_list is not None):
            zqdm_con="SYMBOL in ({0})".format(util.list_sql_condition(zqdm_list))
            count+=1
        else:
            zqdm_con=""

        if(date_list is not None):
            date_con="TDATE in ({0})".format(util.list_sql_condition(date_list))
            count += 1
        else:
            date_con=""

        if(count==2):
            joint="and"
        else:
            joint=""


        sql="""
        select SYMBOL as ZQDM,TDATE as JYRQ,TCLOSE as SPJG from finchina.CHDQUOTE where {0} {2} {1} and TCLOSE!=99999 and TCLOSE!=0
         """.format(zqdm_con,date_con,joint)

        stock_price=hbdb.db2df(sql,db='readonly')

        return stock_price.drop('ROW_ID',axis=1)

    def fund_holding_date_manufacture(self,jjdm_list,start_date,end_date,if_zstockbl=True
                                      ,if_hldcom=False,keyholdonly=False,from_local_db=False):

        hld=pd.DataFrame()
        fund_allocation = pd.DataFrame()
        new_jjdm_list=[]
        if(from_local_db):
            all_holding=self.read_hld_fromdb(start_date, end_date, jjdm_list, keyholdonly, from_local_db)
        else:
            all_holding = self.read_hld_fromlocal(start_date, end_date, jjdm_list, keyholdonly, from_local_db)
        for jjdm in jjdm_list:
            # print(jjdm)
            try:
                # temphld=self.read_hld_fromdb(start_date,end_date,jjdm,keyholdonly,from_local_db)
                temphld=all_holding[all_holding['jjdm']==jjdm].sort_values('jsrq')
                tempfunallo=self.fund_asset_allocation(jjdm, temphld['jsrq'].unique().tolist())
                if(if_hldcom):
                    temphld=self.hld_compenzation(temphld,tempfunallo)
                    temphld['jjdm']=jjdm

                #read holding info
                hld=pd.concat([hld,temphld]
                              ,axis=0)

                # get fund asset allocation info
                fund_allocation =pd.concat([fund_allocation,
                                            tempfunallo],axis=0)
                # #remove HK stock
                # tickerlist=tempdf['zqdm'][~tempdf['zqdm'].dropna().str.contains('H')].unique()

                new_jjdm_list.append(jjdm)

            except Exception as e:
                print('{0}@{1}'.format(jjdm,e))

        if(len(hld)>0):
            #shift the report date to trading date
            org_date_list=hld['jsrq'].unique().tolist()
            date_list = [util._shift_date(x) for x in org_date_list]
            date_map=dict(zip(org_date_list,date_list))
            changed_date=set(org_date_list).difference(set(date_list))

            #read the fund pe,pb,roe,dividend information from db
            financial_df=self.get_fund_financial_info(new_jjdm_list,start_date,end_date)

            #transfor report date to trading date
            for date in changed_date:
                hld.loc[hld['jsrq']==date,'jsrq']=date_map[date]
                fund_allocation.loc[fund_allocation['jsrq'] == date, 'jsrq'] = date_map[date]
                financial_df.loc[financial_df['jsrq']==date,'jsrq']=date_map[date]

            hld=pd.merge(hld,fund_allocation,how='inner',on=['jsrq','jjdm'])
            hld = pd.merge(hld, financial_df, how='left', on=['jsrq', 'jjdm'])
            if(if_zstockbl):
                hld['zjbl']=hld['zjbl']/100/hld['gptzzjb']
            hld.set_index('jsrq',inplace=True,drop=True)

        return  hld,new_jjdm_list

    def save_holding_trading_2db(self,jjdm_list,start_date,end_date):

        #backward the start date one quarter more and make the holding of this quarter as history holding
        last_quarter=(datetime.datetime.strptime(start_date, '%Y%m%d')-datetime.timedelta(days=93))\
            .strftime('%Y%m%d')

        #get the cleaning holding data
        hld, new_jjdm_list = self.fund_holding_date_manufacture(jjdm_list, last_quarter, end_date)
        print('holding_data_load_done')
        date_list = hld.index.unique().tolist()
        date_list.sort()
        ticker_findata=get_ticker_financial_info(hld['zqdm'].unique().tolist(),
                                  hld.index.min()[0:6] + '01', hld.index.max())
        print('ticker_finance_data_load_done')
        financial_factors=['ROE', 'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY',
       'DIVIDENDRATIO', 'TOTALMV', 'NETPROFITRATIO', 'GROSSINCOMERATIO', 'PE',
       'PB', 'PCF', 'PEG',  'NetProfitRatio', 'GrossIncomeRatio']
        #get the week end date list and use this list to collect stock price data
        sql_script = "SELECT jyrq JYRQ FROM st_main.t_st_gg_jyrl WHERE jyrq >= {} and jyrq <= {} and sfzm=1 and sfjj=0".format(
            str(int(date_list[0][0:4])-1)+date_list[0][4:],date_list[-1])
        jyrl=hbdb.db2df(sql_script,db='alluser')
        jyrl=jyrl.sort_values('JYRQ')

        date_list_new=list(set(date_list+jyrl['JYRQ'].tolist()))
        date_list_new.sort()

        #get the stock price which will be used in calculating the MA price later
        stock_price=pd.DataFrame()

        for i in range(int(len(date_list_new)/10)+1):
            tempdate_list=date_list_new[i*10:(i+1)*10]
            if(len(tempdate_list)>0):
                stock_price=pd.concat([stock_price,
                                       self.get_stock_price(date_list=tempdate_list)],
                                      axis=0)

        print('stock_price_data_load_done')
        stock_price['JYRQ'] = stock_price['JYRQ'].astype(str)
        stock_price.sort_values(['ZQDM', 'JYRQ'], inplace=True)
        stock_price.reset_index(drop=True,inplace=True)

        #calculate the average price for last 26,52weeks
        avgprice=stock_price.groupby('ZQDM').rolling(26)['SPJG'].mean().reset_index(drop=True).to_frame('26weeks_mean')
        avgprice['52weeks_mean']=stock_price.groupby('ZQDM').rolling(52)['SPJG'].mean().reset_index(drop=True)
        stock_price=pd.concat([stock_price,avgprice],axis=1)
        stock_price=stock_price.set_index('JYRQ')
        stock_price=stock_price.loc[date_list]
        stock_price=stock_price.reset_index(drop=False)


        # sql="""
        # select a.zqdm,b.yjxymc,b.yjxydm,b.ejxydm,b.ejxymc,b.xxfbrq from
        # st_ashare.t_st_ag_zqzb a left join
        # st_ashare.t_st_ag_gshyhfb b on a.gsdm=b.gsdm
        # where b.xyhfbz={0} and b.xxfbrq='20210730' """\
        #     .format(38)
        # ind_map=hbdb.db2df(sql,db='alluser')
        # stock_price=pd.merge(stock_price,ind_map,how='left',left_on='ZQDM',right_on='zqdm')

        #stock_price.to_excel('hdb_stock_price_rawdata.xlsx',encoding='gbk')


        outputdf = pd.DataFrame()
        print('calculating start.....')
        for jjdm in new_jjdm_list:
            # print(jjdm)
            hld_jj=hld[hld['jjdm']==jjdm]

            key_hld=hld_jj[(hld_jj.groupby('jsrq').rank(ascending=False,method='min')<=10)['zjbl']]

            a_date = list(hld_jj.index.unique()[[(x[4:6] == '06') | (x[4:6] == '12') for x in hld_jj.index.unique()]])

            date_list=list(key_hld.index.unique())
            history_key_hld=pd.DataFrame()
            history_key_hld['zqdm']=key_hld.loc[date_list[0]]['zqdm']
            history_key_hld['in_date']=date_list[0]
            history_key_hld['out_date']=np.NAN
            history_key_hld.reset_index(drop=True,inplace=True)
            last_key_hld=history_key_hld

            #find the date that jj get in and get out of the key holding
            for date in date_list[1:]:
                tempdf=key_hld.loc[date]

                if(date in a_date):
                    for zqdm in list(set(history_key_hld[history_key_hld['out_date'].isnull()]['zqdm']).
                                             difference(set(hld_jj.loc[date]['zqdm']))):

                        history_key_hld.loc[(history_key_hld['zqdm'] == zqdm)&(history_key_hld['out_date'].isnull()),
                                            'out_date'] = date

                new_adding_zq=pd.DataFrame()
                #get the zqdm that is entering the key holding for the first time
                new_adding_zq['zqdm']=list(set(tempdf['zqdm'])
                                           .difference(
                    set(history_key_hld[history_key_hld['out_date'].isnull()]['zqdm'])
                )
                )

                new_adding_zq['in_date']=date
                new_adding_zq['out_date'] = np.NAN
                history_key_hld=pd.concat([history_key_hld,new_adding_zq],axis=0)
                #edit the out date for zq leave the key holding
                for zqdm in list(set(last_key_hld[last_key_hld['out_date'].isnull()]['zqdm']).
                                         difference(set(tempdf['zqdm']))):

                    last_key_hld.loc[(last_key_hld['zqdm']==zqdm)&(last_key_hld['out_date'].isnull()),'out_date']=date
                #get the zq that entering the key holding while is not in the key holding last report date
                new_adding_zq = pd.DataFrame()
                new_adding_zq['zqdm']=list(set(tempdf['zqdm'])
                                            .difference(
                     set(last_key_hld[last_key_hld['out_date'].isnull()]['zqdm'])
                 )
                 )
                new_adding_zq['in_date']=date
                new_adding_zq['out_date'] = np.NAN
                last_key_hld = pd.concat([last_key_hld, new_adding_zq], axis=0)

            #from the in and out date, get the in and out price

            history_key_hld[['in_date','out_date']]=history_key_hld[['in_date','out_date']].astype(object)

            history_key_hld['ym']=history_key_hld['in_date'].str[0:6]

            history_key_hld=pd.merge(history_key_hld,stock_price,how='left',
                                     left_on=['zqdm','in_date'],right_on=['ZQDM','JYRQ'])\
                .drop(['ZQDM','JYRQ'],axis=1).rename(columns={'SPJG':'in_price',
                                                              '26weeks_mean':'26weeks_mean_in',
                                                              '52weeks_mean':'52weeks_mean_in'})


            history_key_hld=pd.merge(history_key_hld,ticker_findata,how='left',
                                     left_on=['zqdm','ym'],right_on=['SECUCODE','ENDDATE'])\
                .drop(['SECUCODE','ENDDATE'],axis=1).rename(columns=dict(zip(financial_factors,
                                                                             [x+"_in" for x in financial_factors])))

            history_key_hld['ym']=history_key_hld['out_date'].str[0:6]
            history_key_hld=pd.merge(history_key_hld,stock_price,how='left',
                                     left_on=['zqdm','out_date'],right_on=['ZQDM','JYRQ'])\
                .drop(['ZQDM','JYRQ'],axis=1).rename(columns={'SPJG':'out_price',
                                                              '26weeks_mean':'26weeks_mean_out',
                                                              '52weeks_mean':'52weeks_mean_out'})

            history_key_hld=pd.merge(history_key_hld,ticker_findata,how='left',
                                     left_on=['zqdm','ym'],right_on=['SECUCODE','ENDDATE'])\
                .drop(['SECUCODE','ENDDATE','ym'],axis=1).rename(columns=dict(zip(financial_factors,
                                                                             [x+"_out" for x in financial_factors])))

            history_key_hld['jjdm']=jjdm
            # history_key_hld['asofdate'] = date
            history_key_hld['type']='all'
            outputdf=pd.concat([outputdf,history_key_hld],axis=0)

            last_key_hld[['in_date','out_date']]=last_key_hld[['in_date','out_date']].astype(object)

            last_key_hld['ym'] = last_key_hld['in_date'].str[0:6]

            last_key_hld = pd.merge(last_key_hld, stock_price, how='left',
                                       left_on=['zqdm', 'in_date'], right_on=['ZQDM', 'JYRQ']) \
                .drop(['ZQDM','JYRQ'],axis=1).rename(columns={'SPJG':'in_price',
                                                              '26weeks_mean':'26weeks_mean_in',
                                                              '52weeks_mean':'52weeks_mean_in'})
            last_key_hld=pd.merge(last_key_hld,ticker_findata,how='left',
                                     left_on=['zqdm','ym'],right_on=['SECUCODE','ENDDATE'])\
                .drop(['SECUCODE','ENDDATE'],axis=1).rename(columns=dict(zip(financial_factors,
                                                                             [x+"_in" for x in financial_factors])))

            last_key_hld['ym'] = last_key_hld['out_date'].str[0:6]
            last_key_hld = pd.merge(last_key_hld, stock_price, how='left',
                                       left_on=['zqdm', 'out_date'], right_on=['ZQDM', 'JYRQ']) \
                .drop(['ZQDM','JYRQ'],axis=1).rename(columns={'SPJG':'out_price',
                                                              '26weeks_mean':'26weeks_mean_out',
                                                              '52weeks_mean':'52weeks_mean_out'})
            last_key_hld=pd.merge(last_key_hld,ticker_findata,how='left',
                                     left_on=['zqdm','ym'],right_on=['SECUCODE','ENDDATE'])\
                .drop(['SECUCODE','ENDDATE'],axis=1).rename(columns=dict(zip(financial_factors,
                                                                             [x+"_out" for x in financial_factors])))


            last_key_hld['jjdm']=jjdm
            # last_key_hld['asofdate'] = date
            last_key_hld['type']='key'
            outputdf=pd.concat([outputdf,last_key_hld],axis=0)
        print('calculating done.....')
        #check if data already exist
        # sql="delete from hbs_stock_trading_data  "
        # localdb.execute(sql)
        # outputdf.to_excel('temp.xlsx',index=False)
        outputdf.to_excel('trading_date.xlsx')
        outputdf.to_sql('hbs_stock_trading_data', con=localdb, index=False, if_exists='append')
        print('hbs_stock_trading_data saved done ')

    @staticmethod
    def get_holding_trading_analysis(asofdate):
        print(asofdate)
        jjdm_list=util.get_stock_funds_pool(asofdate,2)

        #get the saved trading data in the local db
        date_list=pd.read_sql("SELECT distinct(in_date) as date from hbs_stock_trading_data where in_date<='{}' ".format(asofdate)
                              ,con=localdb)['date'].tolist()
        date_list.sort()
        sql="select * from hbs_stock_trading_data where in_date in ({0}) and jjdm in ({1})".\
            format(util.list_sql_condition(date_list[-11:]),util.list_sql_condition(jjdm_list))
        rawdata=pd.read_sql(sql,con=localdb)
        print('raw_trading_data load done')

        financial_left_date=pd.read_sql("select * from financial_left_data where jjdm in ({0}) and buytime>='{1}' and buytime<='{2}'"
                                        .format(util.list_sql_condition(jjdm_list),date_list[-11],date_list[-1][0:6]+'31'),con=localdb)
        financial_left_date['ym']=financial_left_date['buytime'].str[0:6].values
        rawdata['ym']= rawdata['in_date'].astype(str).str[0:6].values
        rawdata=pd.merge(rawdata,financial_left_date,how='left',on=['jjdm','zqdm','ym'])


        rawdata['left_flag_26']=(rawdata['in_price']<=rawdata['26weeks_mean_in'])
        rawdata['left_flag_52'] = (rawdata['in_price'] <= rawdata['52weeks_mean_in'])


        rawdata.loc[rawdata['left_flag_26'],'left_level_26']=rawdata[rawdata['left_flag_26']]['26weeks_mean_in']\
                                                             /rawdata[rawdata['left_flag_26']]['in_price']
        rawdata.loc[rawdata['left_flag_52'], 'left_level_52'] = rawdata[rawdata['left_flag_52']]['52weeks_mean_in'] \
                                                                / rawdata[rawdata['left_flag_52']]['in_price']

        rawdata['new_stock_flag'] = (rawdata['in_price'].notnull())&(rawdata['26weeks_mean_in'].isnull())
        rawdata['less_new_stock_flag'] = (rawdata['in_price'].notnull()) & (rawdata['26weeks_mean_in'].notnull())\
                                         & (rawdata['52weeks_mean_in'].isnull())
        rawdata['flag'] = rawdata['flag'] * rawdata['left_flag_26']
        jjdm_list=rawdata['jjdm'].unique().tolist()

        avg_holding_length_all = []
        avg_holding_length_key = []
        abs_return_all = []
        abs_return_key = []
        left_26_ratio_all=[]
        left_52_ratio_all=[]
        left_26_lv_all=[]
        left_52_lv_all=[]
        left_26_ratio_key=[]
        left_52_ratio_key=[]
        left_26_lv_key=[]
        left_52_lv_key=[]
        new_ratio_all=[]
        new_ratio_key=[]
        less_new_ratio_all=[]
        less_new_ratio_key=[]

        revise_ratio_all = []
        revise_ratio_key = []

        avg_roe_in_all=[]
        avg_roe_in_key = []
        avg_roe_out_all = []
        avg_roe_out_key = []

        avg_netgrowth_in_all=[]
        avg_netgrowth_in_key = []
        avg_netgrowth_out_all = []
        avg_netgrowth_out_key = []

        avg_div_in_all=[]
        avg_div_in_key = []
        avg_div_out_all= []
        avg_div_out_key = []

        avg_pe_in_all=[]
        avg_pe_in_key = []
        avg_pe_out_all = []
        avg_pe_out_key = []

        avg_pb_in_all=[]
        avg_pb_in_key = []
        avg_pb_out_all = []
        avg_pb_out_key = []

        avg_gir_in_all=[]
        avg_gir_in_key = []
        avg_gir_out_all = []
        avg_gir_out_key = []

        avg_nir_in_all=[]
        avg_nir_in_key = []
        avg_nir_out_all = []
        avg_nir_out_key = []
        
        avg_peg_in_all=[]
        avg_peg_in_key = []
        avg_peg_out_all = []
        avg_peg_out_key = []
        
        avg_pcf_in_all=[]
        avg_pcf_in_key = []
        avg_pcf_out_all = []
        avg_pcf_out_key = []

        ratio_pb_roe_in_all=[]
        ratio_pb_roe_in_key = []
        ratio_pb_roe_out_all = []
        ratio_pb_roe_out_key = []
        
        ratio_peg1_in_all=[]
        ratio_peg1_in_key = []
        ratio_peg1_out_all = []
        ratio_peg1_out_key = []



        #get the hsl data
        sql="select jjdm,hsl,tjqj,jsrq from st_fund.t_st_gm_jjhsl where jjdm in ({0}) and jsrq>='{1}' and jsrq<='{2}' and tjqj!=2 and hsl!=99999 and hsl>0"\
            .format(util.list_sql_condition(jjdm_list),rawdata['in_date'].min(),rawdata['in_date'].max()[0:6]+'31')
        hsl=hbdb.db2df(sql,db='funduser')
        hsl=hsl.groupby('jjdm').mean()['hsl'].to_frame('换手率')
        print("calculating features.....")
        for jjdm in jjdm_list:


            history_key_hld=rawdata[(rawdata['jjdm']==jjdm)&(rawdata['type']=='all')]
            last_key_hld = rawdata[(rawdata['jjdm'] == jjdm) & (rawdata['type'] == 'key')]

            revise_ratio_all.append((history_key_hld['flag']==1).sum()/len(history_key_hld))
            revise_ratio_key.append((last_key_hld['flag'] == 1).sum() / len(last_key_hld))

            left_26_ratio_all.append(history_key_hld['left_flag_26'].sum()/len(history_key_hld))
            left_52_ratio_all.append(history_key_hld['left_flag_52'].sum() / len(history_key_hld))

            left_26_ratio_key.append(last_key_hld['left_flag_26'].sum()/len(last_key_hld))
            left_52_ratio_key.append(last_key_hld['left_flag_52'].sum() / len(last_key_hld))

            left_26_lv_all.append(history_key_hld['left_level_26'].mean() )
            left_52_lv_all.append(history_key_hld['left_flag_52'].mean())

            left_26_lv_key.append(last_key_hld['left_level_26'].mean())
            left_52_lv_key.append(last_key_hld['left_flag_52'].mean())

            new_ratio_all.append(history_key_hld['new_stock_flag'].sum()/len(history_key_hld))
            new_ratio_key.append(last_key_hld['less_new_stock_flag'].sum()/len(last_key_hld))
            less_new_ratio_all.append(history_key_hld['new_stock_flag'].sum()/len(history_key_hld))
            less_new_ratio_key .append(last_key_hld['less_new_stock_flag'].sum()/len(last_key_hld))

            avg_roe_in_all.append(history_key_hld['ROE_in'].mean())
            avg_roe_in_key .append(last_key_hld['ROE_in'].mean())
            avg_roe_out_all .append(history_key_hld['ROE_out'].mean())
            avg_roe_out_key .append(last_key_hld['ROE_out'].mean())

            avg_netgrowth_in_all .append(history_key_hld['NETPROFITGROWRATE_in'].mean())
            avg_netgrowth_in_key .append(last_key_hld['NETPROFITGROWRATE_in'].mean())
            avg_netgrowth_out_all .append(history_key_hld['NETPROFITGROWRATE_out'].mean())
            avg_netgrowth_out_key .append(last_key_hld['NETPROFITGROWRATE_out'].mean())

            avg_div_in_all .append(history_key_hld['DIVIDENDRATIO_in'].mean())
            avg_div_in_key .append(last_key_hld['DIVIDENDRATIO_in'].mean())
            avg_div_out_all .append(history_key_hld['DIVIDENDRATIO_out'].mean())
            avg_div_out_key .append(last_key_hld['DIVIDENDRATIO_out'].mean())

            avg_pe_in_all .append(history_key_hld['PE_in'].mean())
            avg_pe_in_key .append(last_key_hld['PE_in'].mean())
            avg_pe_out_all .append(history_key_hld['PE_out'].mean())
            avg_pe_out_key .append(last_key_hld['PE_out'].mean())

            avg_pb_in_all .append(history_key_hld['PB_in'].mean())
            avg_pb_in_key .append(last_key_hld['PB_in'].mean())
            avg_pb_out_all .append(history_key_hld['PB_out'].mean())
            avg_pb_out_key .append(last_key_hld['PB_out'].mean())

            avg_gir_in_all .append(history_key_hld['GROSSINCOMERATIO_in'].mean())
            avg_gir_in_key .append(last_key_hld['GROSSINCOMERATIO_in'].mean())
            avg_gir_out_all .append(history_key_hld['GROSSINCOMERATIO_out'].mean())
            avg_gir_out_key .append(last_key_hld['GROSSINCOMERATIO_out'].mean())

            avg_nir_in_all .append(history_key_hld['NETPROFITRATIO_in'].mean())
            avg_nir_in_key .append(last_key_hld['NETPROFITRATIO_in'].mean())
            avg_nir_out_all .append(history_key_hld['NETPROFITRATIO_out'].mean())
            avg_nir_out_key .append(last_key_hld['NETPROFITRATIO_out'].mean())

            avg_peg_in_all .append(history_key_hld['PEG_in'].mean())
            avg_peg_in_key .append(last_key_hld['PEG_in'].mean())
            avg_peg_out_all .append(history_key_hld['PEG_out'].mean())
            avg_peg_out_key .append(last_key_hld['PEG_out'].mean())

            avg_pcf_in_all .append(history_key_hld['PCF_in'].mean())
            avg_pcf_in_key .append(last_key_hld['PCF_in'].mean())
            avg_pcf_out_all .append(history_key_hld['PCF_out'].mean())
            avg_pcf_out_key .append(last_key_hld['PCF_out'].mean())


            his_out=history_key_hld[history_key_hld['ROE_out'].notnull()]
            last_out = last_key_hld[last_key_hld['ROE_out'].notnull()]
            ratio_pb_roe_in_all .append((history_key_hld['ROE_in']/history_key_hld['PB_in']>=4).sum()/len(history_key_hld))
            ratio_pb_roe_in_key .append((last_key_hld['ROE_in']/last_key_hld['PB_in']>=4).sum()/len(last_key_hld))
            ratio_pb_roe_out_all .append((his_out['ROE_out']/his_out['PB_out']<his_out['ROE_in']/his_out['PB_in']).sum()/len(his_out))
            ratio_pb_roe_out_key .append((last_out['ROE_out']/last_out['PB_out']<last_out['ROE_in']/last_out['PB_in']).sum()/len(last_out))

            ratio_peg1_in_all .append((history_key_hld['PEG_in']<=1).sum()/len(history_key_hld))
            ratio_peg1_in_key .append((last_key_hld['PEG_in']<=1).sum()/len(last_key_hld))
            ratio_peg1_out_all .append((his_out['PEG_out']>his_out['PEG_in']).sum()/len(his_out))
            ratio_peg1_out_key .append((last_out['PEG_out']>last_out['PEG_in']).sum()/len(last_out))
            
            
            tempdf = history_key_hld[history_key_hld['out_date'].notnull()]
            tempdf['out_date'] = [datetime.datetime.strptime(x, '%Y%m%d') for x in tempdf['out_date']]
            tempdf['in_date'] = [datetime.datetime.strptime(x, '%Y%m%d') for x in tempdf['in_date']]
            if(len(tempdf)==0):
                avg_holding_length_all.append(365*3)
            else:
                avg_holding_length_all.append(int(
                    np.mean((tempdf['out_date'] - tempdf['in_date']).values / (3600 * 24 * 1000000000))))

            abs_return_all.append((history_key_hld['out_price']/history_key_hld['in_price']-1).mean())

            tempdf = last_key_hld[last_key_hld['out_date'].notnull()]
            tempdf['out_date'] = [datetime.datetime.strptime(x, '%Y%m%d') for x in tempdf['out_date']]
            tempdf['in_date'] = [datetime.datetime.strptime(x, '%Y%m%d') for x in tempdf['in_date']]
            if(len(tempdf)==0):
                avg_holding_length_key.append(365*3)
            else:
                avg_holding_length_key.append(int(
                    np.mean((tempdf['out_date'] - tempdf['in_date']).values / (3600 * 24 * 1000000000))))

            abs_return_key.append((last_key_hld['out_price']/last_key_hld['in_price']-1).mean())

        print("calculation done")
        outputdf=pd.DataFrame()
        outputdf['jjdm']=jjdm_list
        outputdf['平均持有时间（出重仓前）']=avg_holding_length_key
        outputdf['平均持有时间（出持仓前）'] = avg_holding_length_all
        outputdf['出重仓前平均收益率'] =abs_return_key
        outputdf['出全仓前平均收益率'] =abs_return_all

        outputdf['左侧概率（出重仓前,半年线）']=left_26_ratio_key
        outputdf['左侧概率（出持仓前,半年线）'] = left_26_ratio_all
        outputdf['左侧概率（出重仓前,年线）']=left_52_ratio_key
        outputdf['左侧概率（出持仓前,年线）'] = left_52_ratio_all

        outputdf['左侧程度（出重仓前,半年线）']=left_26_lv_key
        outputdf['左侧程度（出持仓前,半年线）'] = left_26_lv_all
        outputdf['左侧程度（出重仓前,年线）']=left_52_lv_key
        outputdf['左侧程度（出持仓前,年线）'] = left_52_lv_all


        outputdf['新股概率（出重仓前）']=new_ratio_key
        outputdf['新股概率（出持仓前）'] = new_ratio_all
        outputdf['次新股概率（出重仓前）'] = less_new_ratio_key
        outputdf['次新股概率（出持仓前）'] = less_new_ratio_all



        outputdf['买入 ROE（出重仓前）']=avg_roe_in_key
        outputdf['买入 ROE（出持仓前）'] = avg_roe_in_all
        outputdf['卖出 ROE（出重仓前）'] = avg_roe_out_key
        outputdf['卖出 ROE（出持仓前）'] = avg_roe_out_all

        outputdf['买入 净利润增速（出重仓前）']=avg_netgrowth_in_key
        outputdf['买入 净利润增速（出持仓前）'] = avg_netgrowth_in_all
        outputdf['卖出 净利润增速（出重仓前）'] = avg_netgrowth_out_key
        outputdf['卖出 净利润增速（出持仓前）'] = avg_netgrowth_out_all

        outputdf['买入 股息率（出重仓前）']=avg_div_in_key
        outputdf['买入 股息率（出持仓前）'] = avg_div_in_all
        outputdf['卖出 股息率（出重仓前）'] = avg_div_out_key
        outputdf['卖出 股息率（出持仓前）'] = avg_div_out_all

        outputdf['买入 PE（出重仓前）']=avg_pe_in_key
        outputdf['买入 PE（出持仓前）'] = avg_pe_in_all
        outputdf['卖出 PE（出重仓前）'] = avg_pe_out_key
        outputdf['卖出 PE（出持仓前）'] = avg_pe_out_all

        outputdf['买入 PB（出重仓前）']=avg_pb_in_key
        outputdf['买入 PB（出持仓前）'] = avg_pb_in_all
        outputdf['卖出 PB（出重仓前）'] = avg_pb_out_key
        outputdf['卖出 PB（出持仓前）'] = avg_pb_out_all

        outputdf['买入 毛利率（出重仓前）']=avg_gir_in_key
        outputdf['买入 毛利率（出持仓前）'] = avg_gir_in_all
        outputdf['卖出 毛利率（出重仓前）'] = avg_gir_out_key
        outputdf['卖出 毛利率（出持仓前）'] = avg_gir_out_all

        outputdf['买入 净利率（出重仓前）']=avg_nir_in_key
        outputdf['买入 净利率（出持仓前）'] = avg_nir_in_all
        outputdf['卖出 净利率（出重仓前）'] = avg_nir_out_key
        outputdf['卖出 净利率（出持仓前）'] = avg_nir_out_all

        outputdf['买入 PEG（出重仓前）']=avg_peg_in_key
        outputdf['买入 PEG（出持仓前）'] = avg_peg_in_all
        outputdf['卖出 PEG（出重仓前）'] = avg_peg_out_key
        outputdf['卖出 PEG（出持仓前）'] = avg_peg_out_all


        outputdf['买入 PCF（出重仓前）']= avg_pcf_in_key
        outputdf['买入 PCF（出持仓前）'] = avg_pcf_in_all
        outputdf['卖出 PCF（出重仓前）'] = avg_pcf_out_key
        outputdf['卖出 PCF（出持仓前）'] = avg_pcf_out_all

        outputdf['买入 ROE-PB比例（出重仓前）']= ratio_pb_roe_in_key
        outputdf['买入 ROE-PB比例（出持仓前）'] = ratio_pb_roe_in_all
        outputdf['卖出 ROE-PB比例（出重仓前）'] = ratio_pb_roe_out_key
        outputdf['卖出 ROE-PB比例（出持仓前）'] = ratio_pb_roe_out_all

        outputdf['买入 PEG比例（出重仓前）']= ratio_peg1_in_key
        outputdf['买入 PEG比例（出持仓前）'] = ratio_peg1_in_all
        outputdf['卖出 PEG比例（出重仓前）'] = ratio_peg1_out_key
        outputdf['卖出 PEG比例（出持仓前）'] = ratio_peg1_out_all

        outputdf['逆向买入比例（出重仓前）'] = revise_ratio_key
        outputdf['逆向买入比例（出持仓前）'] = revise_ratio_all


        outputdf=pd.merge(outputdf,hsl,how='left',on='jjdm')

        for col in ['平均持有时间（出重仓前）','平均持有时间（出持仓前）','出重仓前平均收益率','出全仓前平均收益率',
                    '左侧概率（出重仓前,半年线）','左侧概率（出持仓前,半年线）','左侧概率（出重仓前,年线）','左侧概率（出持仓前,年线）',
                    '新股概率（出重仓前）','新股概率（出持仓前）','次新股概率（出重仓前）','次新股概率（出持仓前）','换手率','买入 ROE（出重仓前）', '买入 ROE（出持仓前）', '卖出 ROE（出重仓前）', '卖出 ROE（出持仓前）',
       '买入 净利润增速（出重仓前）', '买入 净利润增速（出持仓前）', '卖出 净利润增速（出重仓前）', '卖出 净利润增速（出持仓前）',
       '买入 股息率（出重仓前）', '买入 股息率（出持仓前）', '卖出 股息率（出重仓前）', '卖出 股息率（出持仓前）',
       '买入 PE（出重仓前）', '买入 PE（出持仓前）', '卖出 PE（出重仓前）', '卖出 PE（出持仓前）',
       '买入 PB（出重仓前）', '买入 PB（出持仓前）', '卖出 PB（出重仓前）', '卖出 PB（出持仓前）',
       '买入 毛利率（出重仓前）', '买入 毛利率（出持仓前）', '卖出 毛利率（出重仓前）', '卖出 毛利率（出持仓前）',
       '买入 净利率（出重仓前）', '买入 净利率（出持仓前）', '卖出 净利率（出重仓前）', '卖出 净利率（出持仓前）',
       '买入 PEG（出重仓前）', '买入 PEG（出持仓前）', '卖出 PEG（出重仓前）', '卖出 PEG（出持仓前）',
       '买入 PCF（出重仓前）', '买入 PCF（出持仓前）', '卖出 PCF（出重仓前）', '卖出 PCF（出持仓前）',
       '买入 ROE-PB比例（出重仓前）', '买入 ROE-PB比例（出持仓前）', '卖出 ROE-PB比例（出重仓前）',
       '卖出 ROE-PB比例（出持仓前）', '买入 PEG比例（出重仓前）', '买入 PEG比例（出持仓前）',
       '卖出 PEG比例（出重仓前）', '卖出 PEG比例（出持仓前）','逆向买入比例（出重仓前）', '逆向买入比例（出持仓前）']:
            outputdf[col+"_rank"]=outputdf[col].rank(method='min')/len(outputdf)

        for col in ['左侧程度（出重仓前,半年线）','左侧程度（出持仓前,半年线）',
                    '左侧程度（出重仓前,年线）','左侧程度（出持仓前,年线）']:
            outputdf[col]=outputdf[col].rank(method='min')/len(outputdf)

        outputdf['asofdate'] = asofdate

        sql="delete from hbs_stock_trading_property where asofdate='{}'".format(asofdate)
        localdb.execute(sql)

        outputdf.to_sql('hbs_stock_trading_property',con=localdb,index=False,if_exists='append')
        outputdf.to_excel('test.xlsx')
        print('hbs_stock_trading_property save done')

    def get_hld_property(self,start_date,end_date,add=False):
        jjdm_list=util.get_stock_funds_pool(end_date,2)
        hld,new_jjdm_list=self.fund_holding_date_manufacture(jjdm_list, start_date, end_date,if_hldcom=True)
        print('holding data load done for asofdate {}'.format(end_date))
        zqdm_list=hld['zqdm'].unique().tolist()
        date_list=hld.index.unique().tolist()

        ticker_findata=get_ticker_financial_info(zqdm_list,
                                  hld.index.min()[0:6] + '01', hld.index.max())
        print('ticker finance data load done')

        # ticker_financial_data=[]
        # ticker_financial_exp_data = []
        # for i in range(int(np.ceil(len(zqdm_list)/500))):
        #     # ticker_financial_data.append(get_ticker_financial_info(zqdm_list[i*500:(i+1)*500],date_list[0],date_list[-1]
        #     #                                                        ))
        #     ticker_financial_exp_data.append(get_ticker_expection(zqdm_list[i * 500:(i + 1) * 500],date_list)
        #                                      )
        hld['ym']=hld.index.str[0:6]
        hld=pd.merge(hld.reset_index(),ticker_findata
                     ,how='left',left_on=['zqdm','ym'],right_on=['SECUCODE','ENDDATE']).drop(['SECUCODE','ENDDATE','ym'],axis=1).set_index('jsrq')

        outputdf=pd.DataFrame()
        cen_lv_list=[]
        hhi_list=[]
        top10_list=[]
        top5_list = []
        top3_list = []
        avg_stock_num_list=[]
        avg_stock_weight=[]
        stock_weigth_hsl=[]
        pe_list=[]
        pb_list=[]
        roe_list=[]
        dividend_list=[]
        netgrowth_list=[]
        peg_list=[]
        pcf_list=[]
        nir_list=[]
        gir_list = []
        mv_list=[]
        pe_m_list=[]
        pb_m_list=[]
        roe_m_list=[]
        dividend_m_list=[]
        asofdate=np.max(hld.index)
        cen_lv_his=pd.DataFrame()

        print('calculating features.....')
        for jjdm in new_jjdm_list:

            hld_jj=hld[hld['jjdm']==jjdm]

            a_date = list(hld_jj.index.unique()[[(x[4:6] == '06') | (x[4:6] == '12') for x in hld_jj.index.unique()]])

            full_hld = hld_jj.loc[a_date]

            #key_hld=hld_jj[(hld_jj.groupby('jsrq').rank(ascending=False,method='min')<=10)['zjbl']]
            hhi_lv=full_hld.groupby('jsrq')['zjbl'].apply(hhi_index).mean()
            cen_lv,top3w,top5w,top10w=self.stock_centralization_lv(hld_jj)
            avg_stock_num=full_hld.groupby('jsrq')['jjdm'].count().mean()

            top10_list.append(top10w)
            top5_list.append(top5w)
            top3_list.append(top3w)

            hhi_list.append(hhi_lv)
            cen_lv_list.append(cen_lv.mean())
            avg_stock_num_list.append(avg_stock_num)

            #save cen history
            cen_lv=cen_lv.to_frame().reset_index()
            cen_lv['jjdm']=jjdm
            cen_lv_his=pd.concat([cen_lv_his,cen_lv],axis=0)

            gpzb=full_hld.groupby('jsrq').mean()['gptzzjb'].to_frame('zzjb')
            gpzb['diff'] = gpzb['zzjb'].diff().abs()
            gpzb['sum2'] = gpzb.rolling(2)['zzjb'].sum()
            avg_stock_weight.append(gpzb['zzjb'].mean())
            stock_weigth_hsl.append((gpzb['diff']/gpzb['sum2']).mean())

            financial_property=full_hld.groupby('jsrq').mean()[['pe','pb','roe','dividend','NETPROFITGROWRATE','PEG',
                                                                'PCF','NETPROFITRATIO','GROSSINCOMERATIO','TOTALMV']].mean()
            pe_list.append(financial_property['pe'])
            pb_list.append(financial_property['pb'])
            roe_list.append(financial_property['roe'])
            dividend_list.append(financial_property['dividend'])
            netgrowth_list.append(financial_property['NETPROFITGROWRATE'])
            peg_list.append(financial_property['PEG'])
            pcf_list.append(financial_property['PCF'])
            nir_list.append(financial_property['NETPROFITRATIO'])
            gir_list.append(financial_property['GROSSINCOMERATIO'])
            mv_list.append(financial_property['TOTALMV'])


            financial_property = full_hld.groupby('jsrq').mean()[['pe', 'pb', 'roe', 'dividend']].median()
            pe_m_list.append(financial_property['pe'])
            pb_m_list.append(financial_property['pb'])
            roe_m_list.append(financial_property['roe'])
            dividend_m_list.append(financial_property['dividend'])

        print('calculation done')

        # save cen history 2 localdb
        sql="delete from hbs_stock_cenlv_his where jsrq>='{0}' and jsrq<='{1}'"\
            .format(cen_lv_his['jsrq'].min(),cen_lv_his['jsrq'].max())
        localdb.execute(sql)
        cen_lv_his.rename(columns={'zjbl':'cenlv'},inplace=True)
        cen_lv_his.to_sql('hbs_stock_cenlv_his'
                          ,con=localdb,if_exists='append',index=False)
        # raise Exception

        outputdf['jjdm']=new_jjdm_list
        outputdf['个股集中度']=cen_lv_list
        outputdf['hhi']=hhi_list
        outputdf['持股数量']=avg_stock_num_list
        outputdf['前三大'] = top3_list
        outputdf['前五大'] = top5_list
        outputdf['前十大'] = top10_list
        outputdf['平均仓位']=avg_stock_weight
        outputdf['仓位换手率'] = stock_weigth_hsl
        outputdf['PE'] = pe_list
        outputdf['PB'] = pb_list
        outputdf['ROE'] = roe_list
        outputdf['股息率'] = dividend_list
        outputdf['PEG'] = peg_list
        outputdf['PCF'] = pcf_list
        outputdf['净利率'] = nir_list
        outputdf['毛利率'] = gir_list
        outputdf['市值'] = mv_list
        outputdf['净利增速'] = netgrowth_list
        outputdf['PE_中位数'] = pe_m_list
        outputdf['PB_中位数'] = pb_m_list
        outputdf['ROE_中位数'] = roe_m_list
        outputdf['股息率_中位数'] = dividend_m_list
        outputdf['asofdate']=asofdate


        outputdf[['个股集中度','hhi']]=\
            outputdf[['个股集中度','hhi']].rank(method='min')/len(outputdf)


        outputdf[[x+"_rank" for x in ['PE','PB','ROE','股息率','PEG', 'PCF', '毛利率', '净利率', '市值', '净利增速','PE_中位数','PB_中位数','ROE_中位数','股息率_中位数','仓位换手率']]]=\
            outputdf[['PE','PB','ROE','股息率','PEG', 'PCF', '毛利率', '净利率', '市值', '净利增速','PE_中位数','PB_中位数','ROE_中位数','股息率_中位数','仓位换手率']]\
                .rank(method='min')/len(outputdf)

        #check the same data has already exist
        sql="delete from hbs_holding_property where asofdate='{0}'"\
            .format(asofdate)
        localdb.execute(sql)

        #outputdf.to_csv('hbs_holding_property.csv',index=False,encoding='gbk')
        outputdf.to_sql('hbs_holding_property',con=localdb,index=False,if_exists='append')

        print('Done')

    #re write the industry analysis part of the old barra_anaylsis

    @staticmethod
    def read_hld_ind_fromstock(hld,start_date,end_date,hfbz=38,financial_data=True):

        sql="select b.IndustryNum,a.SecuCode,b.ExcuteDate from hsjy_gg.HK_SecuMain a left join hsjy_gg.HK_ExgIndustry b on a.CompanyCode=b.CompanyCode where  b.Standard={} "\
            .format(hfbz)
        hk_ind_map=\
            hbdb.db2df(sql,db='readonly').sort_values('EXCUTEDATE').drop_duplicates('SECUCODE',keep='last').drop(['EXCUTEDATE','ROW_ID'],axis=1)
        sql="select IndustryNum,UpdateTime,FirstIndustryName as yjxymc,SecondIndustryName as ejxymc,ThirdIndustryName as sjxymc from hsjy_gg.CT_IndustryType where Standard={}"\
            .format(hfbz)
        hk_ind_map = pd.merge(hk_ind_map
                              ,hbdb.db2df(sql,db='readonly').sort_values('UPDATETIME').drop_duplicates('INDUSTRYNUM',keep='last') .drop(['ROW_ID','UPDATETIME'],axis=1)
                              ,how='left',on='INDUSTRYNUM').drop('INDUSTRYNUM',axis=1)

        hk_ind_map.columns=['zqdm','sjxymc','yjxymc','ejxymc']

        sql="select a.zqdm,b.yjxymc,b.xxfbrq,b.ejxymc,b.sjxymc from st_ashare.t_st_ag_zqzb a left join st_ashare.t_st_ag_gshyhfb b on a.gsdm=b.gsdm where a.zqlb=1 and b.xyhfbz={0} and a.sszt=1 "\
            .format(hfbz)
        ind_map=hbdb.db2df(sql,db='alluser')
        ind_map.reset_index(drop=True,inplace=True)
        ind_map.sort_values(['zqdm','xxfbrq'],inplace=True)
        temp=ind_map['zqdm']
        temp.drop_duplicates(keep='last', inplace=True)
        ind_map=ind_map.loc[temp.index][['zqdm','yjxymc','ejxymc','sjxymc']]

        ind_map=pd.concat([ind_map,hk_ind_map],axis=0).reset_index(drop=True)

        hld.reset_index(drop=False,inplace=True)
        ind_hld=pd.merge(hld,ind_map,how='left',on='zqdm')

        #read financial info for tickers in holding
        zqdm_list = list(
            set(ind_hld['zqdm'].unique().tolist()))

        if(financial_data):

            style_financial_info=get_ticker_financial_info(zqdm_list, start_date[0:6]+'01',end_date,with_stock_price=False)

            ind_hld['ym']= ind_hld['jsrq'].astype(str).str[0:6]

            ind_hld=pd.merge(ind_hld,
                             style_financial_info,
                             how='left',right_on=['SECUCODE','ENDDATE'],left_on=['zqdm','ym'])

        return ind_hld

    @staticmethod
    def get_ind_map(hfbz=2):

        sql="select zqdm,flmc,fljb from st_fund.t_st_gm_zqhyflb where sfyx=1 and  hyhfbz={}"\
            .format(hfbz)
        tempdf=hbdb.db2df(sql,db='funduser')

        ind_map=pd.DataFrame(data=tempdf['zqdm'].unique().tolist()
                             ,columns=['zqdm'])


        map_dict=dict(zip(['1','2','3'],['yjxymc','ejxymc','sjxymc']))
        for fljb in ['1','2','3']:
            ind_map=pd.merge(ind_map,tempdf[tempdf['fljb']==fljb][['zqdm','flmc']]
                             ,how='left',on='zqdm').rename(columns={'flmc':map_dict[fljb]})

        return ind_map.drop_duplicates('zqdm')

    @staticmethod
    def save_style_indexhistory2db():

        value_df=pd.read_excel(r"E:\GitFolder\docs\基金画像更新数据\价值权重历史.xlsx")
        value_df['代码']=value_df['代码'].str[0:6]
        value_df['type']='价值'
        value_df['日期']=value_df['日期'].str.replace('-','')

        growth_df = pd.read_excel(r"E:\GitFolder\docs\基金画像更新数据\成长权重历史.xlsx")
        growth_df['代码'] = growth_df['代码'].str[0:6]
        growth_df['type'] = '成长'
        growth_df['日期']=growth_df['日期'].str.replace('-','')

        # raw_style_date=pd.concat([df,df2],axis=0)

        date_list = []
        for year in range(int(growth_df['日期'].unique().min()[0:4]),
                          int(growth_df['日期'].unique().max()[0:4])+1):
            for month in ['03', '06', '09', '12']:
                date_list.append(str(year) + month)

        ouputdf=pd.DataFrame()
        for raw_style_date in [value_df,growth_df]:

            index_pools = raw_style_date[raw_style_date['日期'] == '20100104'][['日期', '代码', '简称', 'type']]
            index_pools['asofdate'] = '201003'
            for i in range(len(date_list) - 1):

                t0 = date_list[i] + '01'
                t1 = date_list[i + 1] + '01'
                pool = index_pools[index_pools['asofdate'] == date_list[i]]
                changes = raw_style_date[(raw_style_date['日期'] >= t0) & (raw_style_date['日期'] <= t1)][['日期',
                                                                                                       '代码', '简称', 'type',
                                                                                                       '纳入/剔除']]
                if (len(changes) > 0):
                    pool = pd.merge(pool, changes[['代码', '纳入/剔除']], how='left', on='代码')
                    pool = pool[pool['纳入/剔除'].isnull()]

                    pool = pd.concat([pool, changes[changes['纳入/剔除'] == '纳入']], axis=0)
                    pool.drop('纳入/剔除', axis=1, inplace=True)
                    pool['asofdate'] = date_list[i + 1]
                    index_pools = pd.concat([index_pools, pool], axis=0)
                    print(len(pool))

                else:
                    pool['asofdate'] = date_list[i + 1]
                    index_pools = pd.concat([index_pools, pool], axis=0)

            ouputdf=pd.concat([ouputdf,index_pools],axis=0)


        #check if data already exist
        sql="delete from style_index_history"
        localdb.execute(sql)

        ouputdf.to_sql('style_index_history', index=False, if_exists='append', con=localdb)

    @staticmethod
    def save_size_indexhistory2db():

        big_df=pd.read_excel(r"E:\GitFolder\docs\基金画像更新数据\大盘权重历史.xlsx")
        big_df['代码']=big_df['代码'].str[0:6]
        big_df['type']='大盘'
        big_df['日期']=big_df['日期'].str.replace('-','')

        med_df = pd.read_excel(r"E:\GitFolder\docs\基金画像更新数据\中盘权重历史.xlsx")
        med_df['代码'] = med_df['代码'].str[0:6]
        med_df['type'] = '中盘'
        med_df['日期']=med_df['日期'].str.replace('-','')


        small_df = pd.read_excel(r"E:\GitFolder\docs\基金画像更新数据\小盘权重历史.xlsx")
        small_df['代码'] = small_df['代码'].str[0:6]
        small_df['type'] = '小盘'
        small_df['日期']=small_df['日期'].str.replace('-','')

        # raw_style_date=pd.concat([df,df2],axis=0)

        date_list = []
        for year in range(int(small_df['日期'].unique().min()[0:4]),
                          int(small_df['日期'].unique().max()[0:4])+1):
            for month in ['03', '06', '09', '12']:
                date_list.append(str(year) + month)
        date_list.sort()
        ouputdf=pd.DataFrame()
        for raw_style_date in [big_df,med_df,small_df]:

            index_pools = raw_style_date[raw_style_date['日期'] == '20050203'][['日期', '代码', '简称', 'type']]
            index_pools['asofdate'] = '200503'
            for i in range(len(date_list) - 1):

                t0 = date_list[i] + '01'
                t1 = date_list[i + 1] + '01'
                pool = index_pools[index_pools['asofdate'] == date_list[i]]
                changes = raw_style_date[(raw_style_date['日期'] >= t0) & (raw_style_date['日期'] <= t1)][['日期',
                                                                                                       '代码', '简称', 'type',
                                                                                                       '纳入/剔除']]
                if (len(changes) > 0):
                    pool = pd.merge(pool, changes[['代码', '纳入/剔除']], how='left', on='代码')
                    pool = pool[pool['纳入/剔除'].isnull()]

                    pool = pd.concat([pool, changes[changes['纳入/剔除'] == '纳入']], axis=0)
                    pool.drop('纳入/剔除', axis=1, inplace=True)
                    pool['asofdate'] = date_list[i + 1]
                    index_pools = pd.concat([index_pools, pool], axis=0)
                    print(len(pool))

                else:
                    pool['asofdate'] = date_list[i + 1]
                    index_pools = pd.concat([index_pools, pool], axis=0)

            ouputdf=pd.concat([ouputdf,index_pools],axis=0)


        #check if data already exist
        sql="delete from size_index_history"
        localdb.execute(sql)

        ouputdf.to_sql('size_index_history', index=False, if_exists='append', con=localdb)

    @staticmethod
    def read_hld_style_fromstock(hld,start_date,end_date,if_prv=False,from_local_db=False):
        if(not if_prv):
            hld=hld.drop(['pb', 'pe', 'roe','dividend'],axis=1)
        new_threshold=False
        if(new_threshold):

            hld['ym']=hld.index.astype(str).str[0:6]
            hld['jsrq'] = hld.index.astype(str)

            sql = "select zqdm,zqjc,ssrq from st_ashare.t_st_ag_zqzb where zqlb=1 and sszt=1 and zqsc in (90,83,18) "
            zqdm_list = hbdb.db2df(sql, db='alluser')
            style_financial_info = get_ticker_financial_info(zqdm_list['zqdm'].tolist(),
                                                             start_date[0:6] + '01', end_date)
            style_financial_info=style_financial_info.sort_values(['SECUCODE', 'ENDDATE'])
            style_financial_info['TOTALMV']=style_financial_info.groupby('SECUCODE').rolling(2, 1).mean()['TOTALMV'].values
            style_financial_info[['PE', 'PB', 'PCF']]=1/style_financial_info[['PE', 'PB', 'PCF']]

            outdf=pd.DataFrame()

            for date in hld['ym'].unique().tolist():
                print(date)

                #methdo1 culumative weight
                hld['mv']=hld['zjbl']*hld['jjzzc']
                tempdf=pd.merge(hld[hld['ym'] == date][['zqdm', 'mv']].groupby('zqdm').sum().reset_index(),
                                style_financial_info[(style_financial_info['ENDDATE'] == date)
                                                     & (style_financial_info['SECUCODE']
                                                        .isin(zqdm_list[(zqdm_list['ssrq'] <=
                                                                         int((datetime.datetime.strptime(date + '28',
                                                                                                         '%Y%m%d') - datetime.timedelta(
                                                                             days=180)).strftime('%Y%m%d')))][
                                                                  'zqdm'].tolist()))],
                                how='left',left_on='zqdm',right_on='SECUCODE')
                tempdf=tempdf.sort_values('TOTALMV', ascending=False)
                tempdf['cum_mv']=tempdf['mv'].cumsum()
                tempdf=tempdf[tempdf['cum_mv']<=tempdf['cum_mv'].max()*0.8].drop('cum_mv',axis=1)
                print(len(tempdf))


                tempdf2=style_financial_info[(style_financial_info['ENDDATE']==date)
                                            &(style_financial_info['SECUCODE']
                                              .isin(zqdm_list[(zqdm_list['ssrq']<=
                                                               int((datetime.datetime.strptime(date+'28',
                                                                                               '%Y%m%d')-datetime.timedelta(days=180)).strftime('%Y%m%d')))]['zqdm'].tolist()))]

                scale = pp.StandardScaler().fit(tempdf[['PB', 'DIVIDENDRATIO', 'PCF',
                                                                 'PE', 'ROE', 'NETPROFITGROWRATE',
                                                                 'OPERATINGREVENUEYOY']].values)

                tempdf[['PB', 'DIVIDENDRATIO', 'PCF',
                                 'PE', 'ROE', 'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY']] = scale.transform(
                    tempdf[['PB', 'DIVIDENDRATIO', 'PCF',
                                     'PE', 'ROE', 'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY']].values)

                tempdf2[['PB', 'DIVIDENDRATIO', 'PCF',
                                 'PE', 'ROE', 'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY']] = scale.transform(
                    tempdf2[['PB', 'DIVIDENDRATIO', 'PCF',
                                     'PE', 'ROE', 'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY']].values)

                for col in ['ROE','NETPROFITGROWRATE','OPERATINGREVENUEYOY']:
                    up10=tempdf[col].quantile(0.9)
                    lower10=tempdf[col].quantile(0.1)
                    tempdf.loc[tempdf[col]<=lower10,col]=lower10
                    tempdf.loc[tempdf[col] >= up10, col] = up10

                growth_threshold=tempdf[['ROE','NETPROFITGROWRATE','OPERATINGREVENUEYOY']].mean(axis=1).quantile(0.668)
                value_threshold=tempdf[['PB','DIVIDENDRATIO','PCF','PE']].mean(axis=1).quantile(0.668)
                big_threshold=tempdf['TOTALMV'].quantile(0.8)
                med_threshold =tempdf['TOTALMV'].quantile(0.5)

                tempdf2.loc[(tempdf2[
                                         ['ROE','NETPROFITGROWRATE','OPERATINGREVENUEYOY']].mean(axis=1)>=growth_threshold)
                           &(tempdf2[
                                         ['PB','DIVIDENDRATIO','PCF','PE']].mean(axis=1)<value_threshold),
                                     'style_type']='成长'
                tempdf2.loc[(tempdf2[
                                         ['PB','DIVIDENDRATIO','PCF','PE']].mean(axis=1)>=value_threshold)
                           &(tempdf2[
                                         ['ROE','NETPROFITGROWRATE','OPERATINGREVENUEYOY']].mean(axis=1)<growth_threshold),
                                     'style_type']='价值'
                tempdf2.loc[tempdf2[
                                         'TOTALMV']>=big_threshold,
                                     'size_type']='大盘'
                tempdf2.loc[(tempdf2[
                                         'TOTALMV']>=med_threshold)&(tempdf2[
                                         'TOTALMV']<big_threshold),
                                     'size_type']='中盘'
                tempdf2.loc[tempdf2[
                                         'TOTALMV']<=med_threshold,
                                     'size_type']='小盘'

                tempdf2.to_sql('stock_style_lable_new3', index=False, con=localdb, if_exists='append')

                outdf=\
                    pd.concat([outdf,
                               pd.merge(hld[hld['ym']==date],
                                        tempdf2,how='left',left_on=['ym','zqdm']
                                        ,right_on=['ENDDATE','SECUCODE']).drop('ENDDATE',axis=1)]
                              ,axis=0)

            return  outdf[['jjdm','jsrq','zqdm','zjbl','style_type','size_type','jjzzc', 'gptzzjb',
                            'PE','PB','PEG','DIVIDENDRATIO', 'PCF',
                            'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY','ROE','TOTALMV']]

        else:

            #read style index tickers history
            sql="select * from style_index_history where asofdate<='{0}' and asofdate>='{1}'"\
                .format(end_date[0:6],start_date[0:6])
            raw_style_date=pd.read_sql(sql,con=localdb)
            raw_style_date=raw_style_date.sort_values('日期')
            raw_style_date=raw_style_date.drop_duplicates(['代码', 'asofdate'],keep='last')
            raw_style_date.rename(columns={'type':'style_type'},inplace=True)


            sql="select * from size_index_history where asofdate<='{0}' and asofdate>='{1}'"\
                .format(end_date[0:6],start_date[0:6])
            raw_size_date=pd.read_sql(sql,con=localdb)
            raw_size_date=raw_size_date.sort_values('日期')
            raw_size_date=raw_size_date.drop_duplicates(['代码', 'asofdate'],keep='last')
            raw_size_date.rename(columns={'type':'size_type'},inplace=True)

            index_history=pd.merge(raw_size_date,raw_style_date,how='left',
                                   on=['asofdate','代码','简称'])

            hld.reset_index(drop=False,inplace=True)

            index_date=index_history['asofdate'].unique()
            index_date.sort()

            if (if_prv):
                hld['ym']=[ index_date[index_date<=x[0:6]][-1] for x in hld['jsrq'].astype(str)]
            else:
                hld['ym'] = hld['jsrq'].astype(str).str[0:6]
            # index_history=index_history[index_history['asofdate']>=str(int(end_date[0:4])-4)+end_date[4:6]]

            hld=pd.merge(hld,index_history,how='left',
                         left_on=['zqdm','ym'],right_on=['代码','asofdate']).drop('代码',axis=1)



            labledf_hld=hld[hld['size_type'].notnull()]
            nolable_hld=hld[hld['size_type'].isnull()]


            if(from_local_db):

                end_date_list=pd.read_sql("select max(ENDDATE) as max_date, min(ENDDATE) as min_date from stock_style_lable"
                                          ,con=localdb)

                nolable_hld.loc[nolable_hld['ym'] > end_date_list['max_date'].iloc[0], 'ym'] = \
                end_date_list['max_date'].iloc[0]

                nolable_hld.loc[nolable_hld['ym']  < end_date_list['min_date'].iloc[0], 'ym'] = \
                end_date_list['min_date'].iloc[0]

                sql="select * from stock_style_lable where ENDDATE in ({0}) "\
                    .format(util.list_sql_condition(nolable_hld['ym'].unique().tolist()))
                stock_style=pd.read_sql(sql,con=localdb)
                hld_after_labeled=pd.merge(nolable_hld.drop(['style_type', 'size_type'],axis=1)
                                     ,stock_style,
                                     how='left',left_on=['zqdm','ym'],
                                     right_on=['SECUCODE','ENDDATE']).drop(['SECUCODE','ENDDATE'],axis=1)

            else:

                hld_date_list=hld['ym'].unique().tolist()
                hld_date_list.sort()

                hld_after_labeled=pd.DataFrame()


                #for zqdm not in mapped

                sql = "select zqdm,zqjc,ssrq from st_ashare.t_st_ag_zqzb where zqlb=1 and sszt=1 and zqsc in (90,83,18) "
                zqdm_list = hbdb.db2df(sql, db='alluser')

                # zqdm_list = list(
                #     set(hld[hld['size_type'].isnull()]['zqdm'].unique().tolist() + index_history['代码'].unique().tolist()))
                #
                #read financial info for ticker not in zhognzheng 1000
                style_financial_info=get_ticker_financial_info(zqdm_list['zqdm'].tolist(),start_date[0:6]+'01',end_date)
                style_financial_info=style_financial_info.sort_values(['SECUCODE', 'ENDDATE'])
                style_financial_info['TOTALMV']=style_financial_info.groupby('SECUCODE').rolling(2, 1).mean()['TOTALMV'].values

                # style_financial_info=style_financial_info[style_financial_info['ENDDATE']>'201803']
                style_financial_info[['PE', 'PB', 'PCF']]=1/style_financial_info[['PE', 'PB', 'PCF']]
                index_history=pd.merge(index_history,
                                        style_financial_info,how='left',left_on=['代码','asofdate'],
                                        right_on=['SECUCODE','ENDDATE'])

                nolable_hld = pd.merge(nolable_hld, style_financial_info, how='left',
                                       left_on=['zqdm', 'ym'], right_on=['SECUCODE', 'ENDDATE'])

                for i in range(len(hld_date_list)):
                    if(if_prv):
                        hld_date=index_date[index_date<=hld_date_list[i]][-1]
                    else:
                        hld_date=hld_date_list[i]
                    print(hld_date)

                    temp_style_info=index_history[(index_history['asofdate']==hld_date)]

                    temp_nolable_hld=nolable_hld[nolable_hld['ym']==hld_date]

                    tempdf=style_financial_info[(style_financial_info['ENDDATE']==hld_date)
                                                &(style_financial_info['SECUCODE']
                                                  .isin(zqdm_list[(zqdm_list['ssrq']<=
                                                                   int((datetime.datetime.strptime(hld_date+'28',
                                                                                                   '%Y%m%d')-datetime.timedelta(days=180)).strftime('%Y%m%d')))]['zqdm'].tolist()))]


                    for col in ['ROE','NETPROFITGROWRATE','OPERATINGREVENUEYOY']:
                        up10=temp_style_info[col].quantile(0.9)
                        lower10=temp_style_info[col].quantile(0.1)
                        temp_style_info.loc[temp_style_info[col]<=lower10,col]=lower10
                        temp_style_info.loc[temp_style_info[col] >= up10, col] = up10
                    if(len(temp_style_info)>0):

                        scale=pp.StandardScaler().fit(temp_style_info[['PB', 'DIVIDENDRATIO', 'PCF',
                    'PE', 'ROE', 'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY']].values)

                        temp_style_info[['PB', 'DIVIDENDRATIO', 'PCF',
                                          'PE', 'ROE', 'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY']]=scale.transform(temp_style_info[['PB', 'DIVIDENDRATIO', 'PCF',
                    'PE', 'ROE', 'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY']].values)

                        temp_nolable_hld[['PB', 'DIVIDENDRATIO', 'PCF',
                                          'PE', 'ROE', 'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY']] = scale.transform(
                            temp_nolable_hld[['PB', 'DIVIDENDRATIO', 'PCF',
                                          'PE', 'ROE', 'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY']].values)
                        tempdf[['PB', 'DIVIDENDRATIO', 'PCF',
                                          'PE', 'ROE', 'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY']] = scale.transform(
                            tempdf[['PB', 'DIVIDENDRATIO', 'PCF',
                                          'PE', 'ROE', 'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY']].values)

                    growth_threshold=temp_style_info[['ROE','NETPROFITGROWRATE','OPERATINGREVENUEYOY']].mean(axis=1).quantile(0.668)
                    value_threshold=temp_style_info[['PB','DIVIDENDRATIO','PCF','PE']].mean(axis=1).quantile(0.668)
                    big_threshold=temp_style_info['TOTALMV'].quantile(0.8)
                    med_threshold =temp_style_info['TOTALMV'].quantile(0.5)


                    tempdf.loc[(tempdf[
                                             ['ROE','NETPROFITGROWRATE','OPERATINGREVENUEYOY']].mean(axis=1)>=growth_threshold)
                               &(tempdf[
                                             ['PB','DIVIDENDRATIO','PCF','PE']].mean(axis=1)<value_threshold),
                                         'style_type']='成长'
                    tempdf.loc[(tempdf[
                                             ['PB','DIVIDENDRATIO','PCF','PE']].mean(axis=1)>=value_threshold)
                               &(tempdf[
                                             ['ROE','NETPROFITGROWRATE','OPERATINGREVENUEYOY']].mean(axis=1)<growth_threshold),
                                         'style_type']='价值'
                    tempdf.loc[tempdf[
                                             'TOTALMV']>=big_threshold,
                                         'size_type']='大盘'
                    tempdf.loc[(tempdf[
                                             'TOTALMV']>=med_threshold)&(tempdf[
                                             'TOTALMV']<big_threshold),
                                         'size_type']='中盘'
                    tempdf.loc[tempdf[
                                             'TOTALMV']<med_threshold,
                                         'size_type']='小盘'

                    temp_nolable_hld.loc[(temp_nolable_hld[
                                             ['ROE','NETPROFITGROWRATE','OPERATINGREVENUEYOY']].mean(axis=1)>=growth_threshold)
                                         &(temp_nolable_hld[
                                             ['PB','DIVIDENDRATIO','PCF','PE']].mean(axis=1)<value_threshold),
                                         'style_type']='成长'
                    temp_nolable_hld.loc[(temp_nolable_hld[
                                             ['ROE','NETPROFITGROWRATE','OPERATINGREVENUEYOY']].mean(axis=1)<growth_threshold)
                                         &(temp_nolable_hld[
                                             ['PB','DIVIDENDRATIO','PCF','PE']].mean(axis=1)>=value_threshold),
                                         'style_type']='价值'
                    temp_nolable_hld.loc[temp_nolable_hld[
                                             'TOTALMV']>=big_threshold,
                                         'size_type']='大盘'
                    temp_nolable_hld.loc[(temp_nolable_hld[
                                             'TOTALMV']>=med_threshold)&(temp_nolable_hld[
                                             'TOTALMV']<big_threshold),
                                         'size_type']='中盘'
                    temp_nolable_hld.loc[temp_nolable_hld[
                                             'TOTALMV']<med_threshold,
                                         'size_type']='小盘'

                    localdb.execute('delete from stock_style_lable where ENDDATE in ({})'
                                    .format(util.list_sql_condition(tempdf['ENDDATE'].unique().tolist())))
                    tempdf[['SECUCODE', 'ROE', 'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY',
       'DIVIDENDRATIO', 'TOTALMV', 'NETPROFITRATIO', 'GROSSINCOMERATIO', 'PE',
       'PB', 'PCF', 'ENDDATE', 'PEG', 'style_type', 'size_type']].to_sql('stock_style_lable', index=False, con=localdb, if_exists='append')

                    hld_after_labeled=pd.concat([hld_after_labeled,temp_nolable_hld],axis=0)

            hld=pd.concat([labledf_hld,hld_after_labeled],axis=0).sort_values(['jjdm','jsrq'])

            print('auto labeled : {0}, manually label :{1}'
                  .format(len(labledf_hld)/len(hld),len(hld_after_labeled)/len(hld)))

            if(if_prv):
                return hld[['jjdm','jsrq','zqdm','zjbl','style_type','size_type',
                            'PE','PB','PEG','DIVIDENDRATIO', 'PCF',
                            'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY','ROE']]
            else:
                return hld[['jjdm','jsrq','zqdm','zjbl','style_type','size_type','jjzzc', 'gptzzjb',
                            'PE','PB','PEG','DIVIDENDRATIO', 'PCF',
                            'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY','ROE','TOTALMV']]

    @staticmethod
    def read_hld_size_fromstock(hld):

        sql="select * from size_index_history"
        raw_style_date=pd.read_sql(sql,con=localdb)
        raw_style_date=raw_style_date.sort_values('日期')
        raw_style_date=raw_style_date.drop_duplicates(['代码', 'asofdate'],keep='last')
        raw_style_date.rename(columns={'type':'size_type'},inplace=True)

        hld['ym']=hld['jsrq'].str[0:6]

        hld=pd.merge(hld,raw_style_date,how='left',
                     left_on=['zqdm','ym'],right_on=['代码','asofdate'])


        return hld[['jsrq', 'zjbl', 'jjdm', 'zqdm', 'jjzzc', 'gptzzjb', 'pb', 'pe', 'roe',
       'dividend', 'yjxymc', 'style_type','size_type']]

    @staticmethod
    def get_industry_exp(hld,new_jjdm_list,if_prv=False):

        industry_hld_1c = pd.DataFrame()
        industry_hld_2c = pd.DataFrame()
        industry_hld_3c = pd.DataFrame()

        industry_hld_list=[industry_hld_1c,industry_hld_2c,industry_hld_3c]
        class_list=['yjxymc','ejxymc','sjxymc']

        financial_col=['ROE', 'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY',
       'DIVIDENDRATIO', 'TOTALMV', 'PE', 'PB','PCF', 'PEG']
        if(if_prv):
            fund_allocation_df=pd.DataFrame()
        else:
            fund_allocation_df=hbdb.db2df("select jjdm,jsrq,jjjzc from st_fund.t_st_gm_zcpz where jjdm in ({0}) and jsrq>='{1}' and jsrq<='{2}'"
                                          .format(util.list_sql_condition(new_jjdm_list),hld['jsrq'].min()[0:6]+'01',hld['jsrq'].max()[0:6]+'31')
                                          ,db='funduser')

            fund_allocation_df['ym']=fund_allocation_df['jsrq'].astype(str).str[0:6]
            fund_allocation_df.drop('jsrq',axis=1,inplace=True)
            fund_allocation_df.drop_duplicates(['jjdm','ym'],keep='last',inplace=True)


        industry_basis_info=pd.read_sql(
            "SELECT * from hbs_industry_financial_stats where ENDDATE>='{0}'  and ENDDATE<='{1}'"
                .format(hld['ym'].min(),hld['ym'].max()),con=localdb)


        for col in financial_col:
            hld[col] = hld[col] * hld['zjbl']

        for jjdm in new_jjdm_list:

            for i in range(3):

                class_level=class_list[i]
                temp_industry_basis_info=industry_basis_info[industry_basis_info['class_level']==str(i+1)].rename(
                    columns={'industry_name':class_level,'ENDDATE':'ym'})


                industry_total_weight=hld[hld['jjdm'] == jjdm][[ 'jsrq','zjbl',
                                                   'jjdm', 'zqdm',class_level]].groupby(['jsrq', class_level],
                                                                                    as_index=False).sum().rename(columns={'zjbl':'ind_tw'})
                tempdf =pd.merge(hld[hld['jjdm'] == jjdm],industry_total_weight,
                                 how='left',on=['jsrq',class_level])

                tempdf=pd.merge(tempdf,
                                temp_industry_basis_info[[class_level,'ym','TOP90%MV']],how='left',
                                on=['ym',class_level])

                #get the longtou ticker
                tempdf['longtou_zjbl_for_ind']=(tempdf['TOTALMV']>=tempdf['TOP90%MV'])*tempdf['zjbl']
                tempdf['longtou_zjbl'] = (tempdf['TOTALMV'] >= tempdf['TOP90%MV']) * tempdf['zjbl']

                for col in financial_col+['longtou_zjbl_for_ind']:
                    tempdf[col]=tempdf[col]/tempdf['ind_tw']


                tempdf = tempdf[[ 'jsrq','zjbl',
                                                   'jjdm', 'zqdm',
                                                   class_level,
                                                    'ROE', 'DIVIDENDRATIO', 'TOTALMV','PE', 'PB','PCF', 'PEG',
                                                    'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY','longtou_zjbl_for_ind','longtou_zjbl'
                                                    ]].groupby(['jsrq', class_level], as_index=False).sum()

                know_weight=tempdf[['jsrq','zjbl','longtou_zjbl']].groupby(['jsrq']).sum().rename(
                    columns={'zjbl':'know_weight','longtou_zjbl':'longtou_zqjbl'})
                know_weight['longtou_zsbl']=know_weight['longtou_zqjbl']/know_weight['know_weight']*100

                tempdf=pd.merge(tempdf,know_weight,how='left',on='jsrq')
                tempdf['longtou_zjbl_for_ind']=tempdf['longtou_zjbl_for_ind']*100
                tempdf['jjdm'] = jjdm
                industry_hld_list[i] = pd.concat([industry_hld_list[i], tempdf], axis=0)

        if (not if_prv):
            for i in range(3):

                industry_hld_list[i]['ym']=industry_hld_list[i]['jsrq'].astype(str).str[0:6]

                industry_hld_list[i]=pd.merge(industry_hld_list[i],fund_allocation_df,
                                              how='left',on=['jjdm','ym'])
                industry_hld_list[i]['ym'] = industry_hld_list[i]['jsrq'].str[0:6]

                industry_hld_list[i].drop('ym',axis=1,inplace=True)

        return industry_hld_list

    @staticmethod
    def get_style_exp(hld, new_jjdm_list):

        style_hld = pd.DataFrame()
        size_hld=pd.DataFrame()
        label_hld=pd.DataFrame()

        hld['style_type']=hld['style_type'].fillna('均衡')
        hld['label']=hld['size_type']+hld['style_type']

        for jjdm in new_jjdm_list:

            tempdf1 = hld[hld['jjdm'] == jjdm].groupby(['jsrq', 'style_type'],
                                                      as_index=False).sum()[['jsrq','style_type','zjbl']]
            tempdf1['jjdm']=jjdm

            tempdf3=hld[hld['jjdm'] == jjdm].groupby(['jsrq'],as_index=False).sum()[['jsrq','jjzzc']]
            tempdf1=pd.merge(tempdf1,tempdf3,
                             how='left',on='jsrq')

            tempdf2 = hld[hld['jjdm'] == jjdm].groupby(['jsrq', 'size_type'],
                                                      as_index=False).sum()[['jsrq','size_type','zjbl']]
            tempdf2['jjdm'] = jjdm

            tempdf2=pd.merge(tempdf2,tempdf3,
                             how='left',on='jsrq')

            tempdf4 = hld[hld['jjdm'] == jjdm].groupby(['jsrq', 'label'],
                                                      as_index=False).sum()[['jsrq','label','zjbl']]
            tempdf4['jjdm'] = jjdm

            tempdf4=pd.merge(tempdf4,tempdf3,
                             how='left',on='jsrq')

            style_hld=pd.concat([style_hld,tempdf1],axis=0)
            size_hld=pd.concat([size_hld,tempdf2],axis=0)
            label_hld=pd.concat([label_hld,tempdf4],axis=0)


        return style_hld,size_hld,label_hld

    def save_industry_exp2db(self,jjdm_list,start_date,end_date):
        #for normal use
        hld,new_jjdm_list=self.fund_holding_date_manufacture(jjdm_list,
                                                             start_date,end_date,
                                                             if_zstockbl=False,if_hldcom=True,keyholdonly=False,from_local_db=False)

        # #for mimic holding  use
        # hld,new_jjdm_list=self.fund_holding_date_manufacture(jjdm_list,
        #                                                      start_date,end_date,
        #                                                      if_zstockbl=False,if_hldcom=False,keyholdonly=False,from_local_db=True)

        if(len(hld)>0):
            hld=self.read_hld_ind_fromstock(hld,start_date,end_date,hfbz=38)
            industry_hld_list = self.get_industry_exp(hld, new_jjdm_list)
        else:
            industry_hld_list=[]

        return industry_hld_list

    def save_industry_exp2db_prv(self,start_date,end_date):

        sql="select jjdm,ticker,sec_name,weight,trade_date from st_hedge.r_st_sm_subjective_fund_holding where weight!=99999 and trade_date>='{0}' and trade_date<='{1}'"\
            .format(start_date,end_date)
        hld=hbdb.db2df(sql,db='highuser').rename(columns={'ticker':'zqdm',
                                                          'trade_date':'jsrq',
                                                          'weight':'zjbl'})

        # sql="select jjdm,ticker,sec_name,weight,trade_date from prv_fund_holding where jjdm='S99999'"
        #
        # hld=pd.read_sql(sql,con=localdb).rename(columns={'ticker':'zqdm',
        #                                                   'trade_date':'jsrq',
        #                                                   'weight':'zjbl'})
        # hld['jsrq']=hld['jsrq'].astype(int)

        hld=self.read_hld_ind_fromstock(hld,end_date,hfbz=38).drop('index',axis=1)
        hld['month']=hld['jsrq'].astype(str).str[4:6]
        #hld=hld[(hld['month']=='03')|(hld['month']=='06')|(hld['month']=='09')|(hld['month']=='12')]
        hld.sort_values(['jjdm','jsrq'],inplace=True)
        hld=hld[hld['yjxymc'].notnull()]
        fre = hld.drop_duplicates(['jjdm', 'jsrq'])[['jjdm', 'jsrq']]
        fre['fre']=fre.groupby('jjdm').diff()
        fre=fre.groupby('jjdm').median().reset_index()

        fre.loc[fre['fre']<=7,'report_fre']='fund_stats'
        fre.loc[(fre['fre'] <=130 )&(fre['fre']>7), 'report_fre'] = 'monthly'
        fre.loc[(fre['fre'] <= 330) & (fre['fre'] > 130), 'report_fre'] = 'quartetly'
        fre.loc[(fre['fre'] <= 630) & (fre['fre'] > 330), 'report_fre'] = 'half-yearly'
        fre.loc[(fre['fre'] <= 10030) & (fre['fre'] > 630), 'report_fre'] = 'yearly'

        jjdm_list=hld['jjdm'].unique().tolist()
        industry_hld_list = self.get_industry_exp(hld, jjdm_list,if_prv=True)


        for i in range(3):
            # #check if data already exist
            sql="delete from hbs_prv_industry_class{2}_exp where jsrq>='{0}' and jsrq<='{1}'"\
                .format(industry_hld_list[i]['jsrq'].min(),industry_hld_list[i]['jsrq'].max(),i+1)
            localdb.execute(sql)

            industry_hld_list[i]['jsrq'] = industry_hld_list[i]['jsrq'].astype(str)
            industry_hld_list[i]['jjjzc']=100
            industry_hld_list[i] = pd.merge(industry_hld_list[i], fre[['jjdm', 'report_fre']], on='jjdm')
            industry_hld_list[i].to_sql('hbs_prv_industry_class{0}_exp'.format(i+1),index=False,if_exists='append',con=localdb)

        print('')

    def save_style_exp2db(self,jjdm_list,start_date,end_date,if_885001=False):

        #for normal use
        hld,new_jjdm_list=self.fund_holding_date_manufacture(jjdm_list,
                                                             start_date,end_date,
                                                             if_zstockbl=False,if_hldcom=True,keyholdonly=False,from_local_db=False)

        #for mimic holding  use
        # hld,new_jjdm_list=self.fund_holding_date_manufacture(jjdm_list,
        #                                                      start_date,end_date,
        #                                                      if_zstockbl=False,if_hldcom=False,keyholdonly=False,from_local_db=True)

        # sql = "select zqdm,zqjc,ssrq from st_ashare.t_st_ag_zqzb where zqlb=1 and sszt=1 and zqsc in (90,83,18) "
        # zqdm_list = hbdb.db2df(sql, db='alluser')
        # hld=pd.DataFrame(columns=['pb', 'pe', 'roe','dividend'])
        # hld['zqdm']=zqdm_list['zqdm']
        # hld['jsrq'] = "20230331"

        hld=self.read_hld_style_fromstock(hld,start_date,end_date,from_local_db=False)

        # hld.drop_duplicates(['jsrq','zqdm']).sort_values(['jsrq','zqdm']).\
        #     to_sql('stock_style_lable_fund_holding_new3',index=False,con=localdb,if_exists='append')
        # hld.drop('TOTALMV',axis=1,inplace=True)

        style_hld,size_hld,label_hld=self.get_style_exp(hld,new_jjdm_list)

        if(if_885001):
            table_name='885001_'
        else:
            table_name=''

        style_hld.to_excel(table_name+'style_hld.xlsx',index=False)
        size_hld.to_excel(table_name+'size_hld.xlsx',index=False)
        label_hld.to_excel(table_name+'label_hld.xlsx',index=False)

        # sql="delete from {2}hbs_style_exp where jsrq>='{0}' and jsrq<='{1}'"\
        #     .format(style_hld['jsrq'].min(),style_hld['jsrq'].max(),table_name)
        # localdb.execute(sql)
        # sql="delete from {2}hbs_size_exp where jsrq>='{0}' and jsrq<='{1}'"\
        #     .format(size_hld['jsrq'].min(),size_hld['jsrq'].max(),table_name)
        # localdb.execute(sql)

        # style_hld.to_sql(table_name+'hbs_style_exp',index=False,if_exists='append',con=localdb)
        # size_hld.to_sql(table_name+'hbs_size_exp', index=False, if_exists='append', con=localdb)

    def save_prv_style_exp2db(self,start_date,end_date):

        sql = "select jjdm,ticker,sec_name,weight,trade_date from st_hedge.r_st_sm_subjective_fund_holding where weight!=99999 and trade_date>='{0}' and trade_date<='{1}'" \
            .format(start_date, end_date)
        hld = hbdb.db2df(sql, db='highuser').rename(columns={'ticker': 'zqdm',
                                                             'trade_date': 'jsrq',
                                                             'weight': 'zjbl'})
        new_jjdm_list=hld['jjdm'].unique().tolist()


        # sql="select jjdm,ticker,sec_name,weight,trade_date from prv_fund_holding where jjdm='S99999'"
        #
        # hld=pd.read_sql(sql,con=localdb).rename(columns={'ticker':'zqdm',
        #                                                   'trade_date':'jsrq',
        #                                                   'weight':'zjbl'})
        # hld['jsrq']=hld['jsrq'].astype(int)
        # new_jjdm_list = hld['jjdm'].unique().tolist()

        hld=self.read_hld_style_fromstock(hld,end_date,if_prv=True)
        hld['jjzzc']=100

        fre = hld.drop_duplicates(['jjdm', 'jsrq'])[['jjdm', 'jsrq']]
        fre['fre']=fre.groupby('jjdm').diff()
        fre=fre.groupby('jjdm').median().reset_index()

        fre.loc[fre['fre']<=7,'report_fre']='fund_stats'
        fre.loc[(fre['fre'] <=130 )&(fre['fre']>7), 'report_fre'] = 'monthly'
        fre.loc[(fre['fre'] <= 330) & (fre['fre'] > 130), 'report_fre'] = 'quartetly'
        fre.loc[(fre['fre'] <= 630) & (fre['fre'] > 330), 'report_fre'] = 'half-yearly'
        fre.loc[(fre['fre'] <= 10030) & (fre['fre'] > 630), 'report_fre'] = 'yearly'

        style_hld,size_hld,label_hld=self.get_style_exp(hld,new_jjdm_list)

        style_hld=pd.merge(style_hld,fre[['jjdm','report_fre']],how='left',on='jjdm')
        size_hld = pd.merge(size_hld, fre[['jjdm', 'report_fre']], how='left', on='jjdm')

        sql="delete from hbs_prv_style_exp where jsrq>='{0}' and jsrq<='{1}'"\
            .format(style_hld['jsrq'].min(),style_hld['jsrq'].max())
        localdb.execute(sql)

        sql="delete from hbs_prv_size_exp where jsrq>='{0}' and jsrq<='{1}'"\
            .format(size_hld['jsrq'].min(),size_hld['jsrq'].max())
        localdb.execute(sql)

        style_hld['jjzzc']=100
        size_hld['jjzzc']=100

        style_hld.to_sql('hbs_prv_style_exp',index=False,if_exists='append',con=localdb)
        size_hld.to_sql('hbs_prv_size_exp', index=False, if_exists='append', con=localdb)

    @staticmethod
    def save_industry_financial_stats2db(start_date,end_date,hfbz=38):

        sql="select a.zqdm,b.yjxymc,b.xxfbrq,b.ejxymc,b.sjxymc from st_ashare.t_st_ag_zqzb a left join st_ashare.t_st_ag_gshyhfb b on a.gsdm=b.gsdm where a.zqlb=1 and b.xyhfbz={0} and (a.zqsc=18 or a.zqsc=83 or a.zqsc=90) and sszt=1"\
            .format(hfbz)
        ind_map=hbdb.db2df(sql,db='alluser')
        ind_map.reset_index(drop=True,inplace=True)
        ind_map.sort_values(['zqdm','xxfbrq'],inplace=True)
        ind_map=ind_map.drop_duplicates(['zqdm'], keep='last')
        ind_map.reset_index(drop=True,inplace=True)

        zqdm_list=ind_map['zqdm'].unique().tolist()


        style_financial_info=get_ticker_financial_info(zqdm_list,start_date,end_date,with_stock_price=False)
        # for col in ['EPS','OPERCASHFLOWPS','NETASSETPS']:
        #     style_financial_info[col]=style_financial_info[col]/style_financial_info['DRJJ']

        ind_map=pd.merge(style_financial_info,ind_map,how='left',left_on='SECUCODE',right_on='zqdm')


        financial_col = ['ROE','NETPROFITGROWRATE', 'OPERATINGREVENUEYOY',
                         'DIVIDENDRATIO', 'PE', 'PB','PCF', 'PEG']


        industry_basis_info_df=pd.DataFrame()
        class_list=['yjxymc','ejxymc','sjxymc']

        for i in range(3):

            class_type=class_list[i]

            industry_total_MV=ind_map.groupby([class_type,'ENDDATE']).sum()['TOTALMV'].reset_index()
            industry_average=ind_map.groupby([class_type,
                                              'ENDDATE']).mean()['TOTALMV'].reset_index().rename(columns={'TOTALMV':'AVERAGEMV'})
            industry_90=ind_map.groupby([class_type,
                                         'ENDDATE']).quantile(0.9)['TOTALMV'].reset_index().rename(columns={'TOTALMV':'TOP90%MV'})
            industry_50=ind_map.groupby([class_type,
                                         'ENDDATE']).quantile(0.5)['TOTALMV'].reset_index().rename(columns={'TOTALMV':'TOP50%MV'})
            industry_75 = ind_map.groupby([class_type,
                                           'ENDDATE']).quantile(0.75)['TOTALMV'].reset_index().rename(
                columns={'TOTALMV': 'TOP75%MV'})
            industry_25 = ind_map.groupby([class_type, 'ENDDATE']).quantile(0.25)['TOTALMV'].reset_index().rename(
                columns={'TOTALMV': 'TOP25%MV'})


            tempdf=pd.merge(ind_map,industry_total_MV,how='left',on=[class_type,'ENDDATE'])


            for col in financial_col:
                tempdf[col] = tempdf[col] * tempdf['TOTALMV_x']/tempdf['TOTALMV_y']

            tempdf=tempdf.groupby([class_type,
                                   'ENDDATE']).sum()[financial_col].reset_index()
            tempdf['class_level']=str(i+1)
            tempdf=pd.merge(tempdf,industry_average,how='left',on=[class_type,'ENDDATE'])
            tempdf = pd.merge(tempdf, industry_90, how='left', on=[class_type, 'ENDDATE'])
            tempdf = pd.merge(tempdf, industry_total_MV, how='left', on=[class_type, 'ENDDATE'])
            tempdf = pd.merge(tempdf, industry_50, how='left', on=[class_type, 'ENDDATE'])
            tempdf = pd.merge(tempdf, industry_75, how='left', on=[class_type, 'ENDDATE'])
            tempdf = pd.merge(tempdf, industry_25, how='left', on=[class_type, 'ENDDATE'])

            tempdf.rename(columns={class_type:'industry_name'},inplace=True)

            industry_basis_info_df=pd.concat([industry_basis_info_df,tempdf],axis=0)


        #delete outofdate data

        sql="delete from hbs_industry_financial_stats where ENDDATE>='{0}' and ENDDATE<='{1}'"\
            .format(ind_map['ENDDATE'].min(),ind_map['ENDDATE'].max())
        localdb.execute(sql)
        industry_basis_info_df.to_sql('hbs_industry_financial_stats',index=False
                                      ,if_exists='append',con=localdb)

    def ticker_contribution(self,jjdm_list,start_date,end_date):


        hld,new_jjdm_list=self.fund_holding_date_manufacture(jjdm_list,
                                                             start_date,end_date,
                                                             if_zstockbl=False,if_hldcom=True)
        hld['gpsz']=hld['zjbl']*hld['jjzzc']
        hld.drop(['jjzzc', 'gptzzjb', 'pb', 'pe', 'roe',
       'dividend'],axis=1,inplace=True)
        date_list=hld.index.unique().sort_values().tolist()

        #get mutual fund nav
        sql="select jjdm,jzrq,ljjz from st_fund.t_st_gm_jjjz where jzrq in ({0}) and jjdm in ({1})"\
            .format(util.list_sql_condition(date_list),util.list_sql_condition(new_jjdm_list))
        fund_nav=hbdb.db2df(sql,db='funduser')
        fund_nav['pct_change'] = fund_nav.groupby('jjdm').pct_change()['ljjz']
        fund_nav['jzrq']=fund_nav['jzrq'].astype(str)

        zqdm_list=hld['zqdm'].unique().tolist()
        price_df=[]
        price_hk=[]
        for m in range(int(np.ceil(len(zqdm_list)/500))):

            sql = """
            select zqmd ZQDM ,jyrq JYRQ ,spjg SPJG from st_ashare.t_st_ag_gpjy where  drjj is not null and jyrq in ({0}) and zqdm in ({1})
             """.format(util.list_sql_condition(date_list),
                        util.list_sql_condition(zqdm_list[m*500:(m+1)*500]))
            price_df.append(hbdb.db2df(sql, db='alluser').drop('ROW_ID', axis=1))
            for date in date_list:
                sql = "select a.ClosePrice as SPJG,a.TradingDay as JYRQ,b.SecuCode as ZQDM from hsjy_gg.QT_HKDailyQuoteIndex a left join hsjy_gg.HK_SecuMain b on a.InnerCode=b.InnerCode where a.TradingDay=to_date('{0}','yyyymmdd') and b.SecuCode in ({1})   "\
                    .format(date,util.list_sql_condition(zqdm_list[m*500:(m+1)*500]))
                price_hk_temp = \
                    hbdb.db2df(sql, db='readonly')
                if(len(price_hk_temp)>0):

                    price_hk_temp['JYRQ']=date
                    price_hk.append(price_hk_temp.drop('ROW_ID', axis=1))

        price_df=pd.concat(price_df,axis=0)
        if(len(price_hk)>0):
            price_hk=pd.concat(price_hk,axis=0)
        else:
            price_hk = pd.DataFrame(columns=price_df.columns.to_list())
        price_df=pd.concat([price_df,price_hk],axis=0)
        coutribution_df=pd.DataFrame()

        for i in range(1,len(date_list)):

            t0=date_list[i-1]
            t1=date_list[i]
            average_weight=pd.merge(hld[['jjdm','zqdm','zjbl']].loc[t0],hld[['jjdm','zqdm','zjbl']].loc[t1],
                                    how='outer',on=['jjdm','zqdm']).fillna(0)
            average_weight=pd.merge(average_weight,
                                    price_df[price_df['JYRQ']==t0][['ZQDM','SPJG']]
                                    ,how='left',left_on='zqdm',right_on='ZQDM').drop('ZQDM',axis=1)
            average_weight=pd.merge(average_weight,
                                    price_df[price_df['JYRQ']==t1][['ZQDM','SPJG']]
                                    ,how='left',left_on='zqdm',right_on='ZQDM').drop('ZQDM',axis=1)
            average_weight['contribution']=(average_weight['SPJG_y']/average_weight['SPJG_x']-1)\
                                           *average_weight[['zjbl_x','zjbl_y']].mean(axis=1)/100
            average_weight['trade_date']=t1

            #adjust the contribution by jj real return
            average_weight=pd.merge(average_weight
                                    ,average_weight.groupby('jjdm').sum()['contribution'].to_frame('total_con')
                                    ,how='left',on='jjdm')

            average_weight=pd.merge(average_weight,fund_nav[fund_nav['jzrq']==t1],how='left',on='jjdm')
            average_weight['contribution']=\
                average_weight['contribution']*(average_weight['pct_change']/average_weight['total_con'])


            coutribution_df=pd.concat([coutribution_df,
                                       average_weight[['trade_date','jjdm','zqdm','contribution']]],axis=0)

        coutribution_df=coutribution_df.groupby(['jjdm','zqdm']).sum().reset_index()
        df_list=[]


        #get the ticker industry info
        sql="select b.IndustryNum,a.SecuCode,b.ExcuteDate from hsjy_gg.HK_SecuMain a left join hsjy_gg.HK_ExgIndustry b on a.CompanyCode=b.CompanyCode where  b.Standard=38 "
        hk_ind_map=\
            hbdb.db2df(sql,db='readonly').sort_values('EXCUTEDATE').drop_duplicates('SECUCODE',keep='last').drop(['EXCUTEDATE','ROW_ID'],axis=1)
        sql="select IndustryNum,UpdateTime,FirstIndustryName as yjxymc,SecondIndustryName as ejxymc,ThirdIndustryName as sjxymc from hsjy_gg.CT_IndustryType where Standard=38"
        hk_ind_map = pd.merge(hk_ind_map
                              ,hbdb.db2df(sql,db='readonly').sort_values('UPDATETIME').drop_duplicates('INDUSTRYNUM',keep='last') .drop(['ROW_ID','UPDATETIME'],axis=1)
                              ,how='left',on='INDUSTRYNUM').drop('INDUSTRYNUM',axis=1)

        hk_ind_map.columns=['zqdm','sjxymc','yjxymc','ejxymc']

        sql="select a.zqdm,b.yjxymc,b.xxfbrq,b.ejxymc,b.sjxymc from st_ashare.t_st_ag_zqzb a left join st_ashare.t_st_ag_gshyhfb b on a.gsdm=b.gsdm where a.zqlb=1 and b.xyhfbz={0} and a.sszt=1 "\
            .format(38)
        ind_map=hbdb.db2df(sql,db='alluser')
        ind_map.reset_index(drop=True,inplace=True)
        ind_map.sort_values(['zqdm','xxfbrq'],inplace=True)
        temp=ind_map['zqdm']
        temp.drop_duplicates(keep='last', inplace=True)
        ind_map=ind_map.loc[temp.index][['zqdm','yjxymc','ejxymc','sjxymc']]

        ind_map=pd.concat([ind_map,hk_ind_map],axis=0).reset_index(drop=True)

        #get the zqjc info
        sql = "select SecuCode,ChiNameAbbr from hsjy_gg.SecuMain where  SecuCategory in (1,2)"
        stock_base_info = hbdb.db2df(sql, db='readonly').drop('ROW_ID', axis=1)
        stock_base_info.drop_duplicates(keep='last', inplace=True)

        sql = "select SecuCode,ChiName as ChiNameAbbr from hsjy_gg.HK_SecuMain where  SecuCategory in (3,51)"
        hks_base_info = hbdb.db2df(sql, db='readonly').drop('ROW_ID', axis=1)
        hks_base_info.drop_duplicates(keep='last', inplace=True)
        stock_base_info=pd.concat([stock_base_info,hks_base_info],axis=0)


        coutribution_df=pd.merge(coutribution_df,stock_base_info,how='left',
                                 left_on='zqdm',right_on='SECUCODE').drop('SECUCODE',axis=1)

        coutribution_df['name_per']=coutribution_df['CHINAMEABBR'].astype(str)+"("\
                                       +(coutribution_df['contribution']*100).astype(str).str[0:4]+"%),"

        ind_contribution_list=[]
        df_list2=[]
        ind_contribution=pd.merge(coutribution_df,ind_map,how='left',on='zqdm')
        for industry_lv in ['yjxymc','ejxymc','sjxymc']:
            tempdf=ind_contribution.groupby(['jjdm',
                                             industry_lv]).sum().reset_index()
            tempdf['industry_lv']=industry_lv

            ind_contribution.sort_values('contribution',ascending=False,inplace=True)
            tempdf2=ind_contribution[['jjdm',industry_lv,'name_per']].groupby(['jjdm',
                                             industry_lv]).sum().reset_index().rename(columns={'name_per':'个股贡献'})
            tempdf=pd.merge(tempdf,tempdf2,how='left',on=['jjdm',industry_lv]).rename(columns={industry_lv:'industry_name'})

            ind_contribution_list.append(tempdf)

        coutribution_df.drop('name_per',axis=1,inplace=True)

        for jjdm in coutribution_df['jjdm'].unique():
            df_list.append(coutribution_df[coutribution_df['jjdm']==jjdm].nlargest(columns='contribution',n=20))
            df_list.append(coutribution_df[coutribution_df['jjdm'] == jjdm].nsmallest(columns='contribution', n=5))
            for i in range(3):
                df_list2.append(ind_contribution_list[i][ind_contribution_list[i]['jjdm']==jjdm].nlargest(columns='contribution',n=20))
                df_list2.append(
                    ind_contribution_list[i][ind_contribution_list[i]['jjdm'] == jjdm].nsmallest(columns='contribution',
                                                                                                n=5))


        ticker_con=pd.concat(df_list,axis=0)
        ticker_con['asofdate']=date_list[-1]

        ind_con=pd.concat(df_list2,axis=0)
        ind_con['asofdate'] = date_list[-1]


        sql="delete from hbs_ticker_contribution where asofdate='{}'".format(date_list[-1])
        localdb.execute(sql)
        ticker_con.to_sql('hbs_ticker_contribution',con=localdb,index=False,if_exists='append')
        #
        sql="delete from hbs_industry_contribution where asofdate='{}'".format(date_list[-1])
        localdb.execute(sql)
        ind_con.to_sql('hbs_industry_contribution', con=localdb, index=False, if_exists='append')

    def adjusted_hldquant(self,jjdm_list,start_date,end_date):

        hld, new_jjdm_list = self.fund_holding_date_manufacture(jjdm_list,
                                                                start_date, end_date,
                                                                if_zstockbl=False, if_hldcom=True)
        hld['gpsz'] = hld['zjbl'] * hld['jjzzc']
        hld.drop(['jjzzc', 'gptzzjb', 'pb', 'pe', 'roe',
                  'dividend'], axis=1, inplace=True)
        date_list = hld.index.unique().sort_values().tolist()


        #get the ticker industry info
        sql="select a.zqdm,b.yjxymc,b.xxfbrq,b.ejxymc,b.sjxymc from st_ashare.t_st_ag_zqzb a left join st_ashare.t_st_ag_gshyhfb b on a.gsdm=b.gsdm where a.zqlb=1 and b.xyhfbz={0} and a.sszt=1 "\
            .format(38)
        ind_map=hbdb.db2df(sql,db='alluser')
        ind_map.reset_index(drop=True,inplace=True)
        ind_map.sort_values(['zqdm','xxfbrq'],inplace=True)
        temp=ind_map['zqdm']
        temp.drop_duplicates(keep='last', inplace=True)
        ind_map=ind_map.loc[temp.index][['zqdm','yjxymc','ejxymc','sjxymc']]

        # get trade_date calander
        sql_script = "SELECT jyrq JYRQ,sfzm SFZM FROM st_main.t_st_gg_jyrl WHERE jyrq >= {} and jyrq <= {} and sfjj=0 and sfzm=1".format(
            date_list[0], date_list[-1])
        calander = hbdb.db2df(sql_script, db='alluser')
        calander=list(set(calander['JYRQ'].tolist()+date_list))
        calander.sort()

        zqdm_list=hld['zqdm'].unique().tolist()
        price_df=[]
        for m in range(int(np.ceil(len(zqdm_list)/500))):

            sql = """
            select zqdm ZQDM ,jyrq JYRQ ,spjg SPJG from st_ashare.t_st_ag_gpjy where  drjj is not null and jyrq in ({0}) and zqdm in ({1})
             """.format(util.list_sql_condition(calander),
                        util.list_sql_condition(zqdm_list[m*500:(m+1)*500]))
            spjg=hbdb.db2df(sql, db='alluser')
            if(len(spjg)>0):
                price_df.append(spjg)

        price_df=pd.concat(price_df,axis=0)

        # calculate the adjusted quant for top 10 ticker for each jj

        hld = pd.merge(hld, price_df, how='left', left_on=['zqdm', 'jsrq'],
                       right_on=['ZQDM', 'JYRQ']).drop('ZQDM', axis=1)
        hld['sl'] = hld['gpsz'] / hld['SPJG']

        # get jj nav and share info
        sql = "select jjdm,jjjz,jzrq from st_fund.t_st_gm_jjjz where jjdm in ({0}) and jzrq in ({1})" \
            .format(util.list_sql_condition(new_jjdm_list), util.list_sql_condition(calander))
        jjjz = hbdb.db2df(sql, db='funduser')
        jjjz['jzrq'] = jjjz['jzrq'].astype(str)

        sql = "select jjdm,jsrq,qsrq,qcfe,qmfe,cfzjfe from st_fund.t_st_gm_febd where jjdm in ({0}) and jsrq in ({1})" \
            .format(util.list_sql_condition(new_jjdm_list), util.list_sql_condition(date_list))
        jjshares = hbdb.db2df(sql, db='funduser').fillna(0)
        jjshares = jjshares.sort_values(['jjdm', 'jsrq', 'qsrq']).drop_duplicates(['jjdm', 'jsrq'], keep='last')
        jjshares['share_changed'] = jjshares['qmfe'] - jjshares['qcfe'] - jjshares['cfzjfe']

        hld = hld[hld['JYRQ'] >= '20190628']
        hld = pd.merge(hld, jjshares[['jjdm', 'jsrq', 'share_changed']]
                       , how='left', left_on=['jjdm', 'JYRQ'], right_on=['jjdm', 'jsrq']).drop('jsrq', axis=1)
        hld = pd.merge(hld, ind_map, how='left', on='zqdm')


        sql="SELECT REPORT_DATE,INDUSTRY_NAME,INDUSTRY_TYPE,EST_NET_PROFIT_YOY as EST_NET_PROFIT_YOY,EST_OPER_REVENUE_YOY as EST_OPER_REVENUE_YOY,EST_ROE_FY1 as ROE_FY1,EST_PE_FY1 as PE_FY1,EST_PEG_FY1 as PEG_FY1 from industry_consensus "
        industry_expectation_stats=pd.read_sql(sql,con=localdb)
        industry_expectation_stats['REPORT_DATE']=industry_expectation_stats['REPORT_DATE'].astype(str).str[0:6]
        industry_expectation_stats['INDUSTRY_TYPE']=industry_expectation_stats['INDUSTRY_TYPE'].astype(str)

        sql="SELECT industry_name,ENDDATE,ROE,NETPROFITGROWRATE,OPERATINGREVENUEYOY,PE,PEG,class_level from hbs_industry_financial_stats "
        industry_financial_stats=pd.read_sql(sql,con=localdb)


        industry_financial_stats=\
            pd.merge(industry_financial_stats,industry_expectation_stats,
                                          how='left',left_on=['ENDDATE','industry_name','class_level'],
                                          right_on=['REPORT_DATE','INDUSTRY_NAME','INDUSTRY_TYPE']).drop(['REPORT_DATE','INDUSTRY_NAME','INDUSTRY_TYPE'],
                                                                                                         axis=1)

        financial_col=['ROE', 'NETPROFITGROWRATE','OPERATINGREVENUEYOY','PE', 'PEG', 'EST_NET_PROFIT_YOY',
                       'EST_OPER_REVENUE_YOY', 'ROE_FY1','PE_FY1','PEG_FY1']
        financial_rank_col=[x+'_rank' for x in financial_col]
        industry_financial_stats[financial_rank_col]=\
            industry_financial_stats[financial_col].rolling(8).apply(quantial_for_rolling)
        hld['joint_date'] = hld['JYRQ'].str[0:6]
        hld=pd.merge(hld,industry_financial_stats[industry_financial_stats['class_level']=='1'],how='left',
                     left_on=['yjxymc','joint_date'],
                     right_on=['industry_name','ENDDATE']).rename(columns=dict(zip(financial_col+financial_rank_col,
                                                                                   [x+'_yj' for x in financial_col+financial_rank_col]))).drop(['industry_name','ENDDATE','class_level'],axis=1)
        hld=pd.merge(hld,industry_financial_stats[industry_financial_stats['class_level']=='2'],how='left',
                     left_on=['ejxymc','joint_date'],
                     right_on=['industry_name','ENDDATE']).rename(columns=dict(zip(financial_col+financial_rank_col,
                                                                                   [x+'_ej' for x in financial_col+financial_rank_col]))).drop(['industry_name','ENDDATE','class_level'],axis=1)
        hld=pd.merge(hld,industry_financial_stats[industry_financial_stats['class_level']=='3'],how='left',
                     left_on=['sjxymc','joint_date'],
                     right_on=['industry_name','ENDDATE']).rename(columns=dict(zip(financial_col+financial_rank_col,
                                                                                   [x+'_sj' for x in financial_col+financial_rank_col]))).drop(['industry_name','ENDDATE','class_level'],axis=1)

        hls_sl_history = []
        #get the average ticker price for each quarter gap
        new_price_df=pd.DataFrame(data=hld['zqdm'].unique().tolist(),columns=['zqdm'])
        for i in  range(1,len(hld['JYRQ'].unique().tolist())):
            t1=hld['JYRQ'].unique().tolist()[i]
            t0=hld['JYRQ'].unique().tolist()[i-1]
            new_price_df=pd.merge(new_price_df,
                                  (price_df[(price_df['JYRQ'] >= t0) & (price_df['JYRQ'] <= t1)].groupby('ZQDM').mean()).rename(columns={'SPJG':t1}),
                                  how='left',left_on='zqdm',right_on='ZQDM')

        top10_list=[]
        #850088
        for jjdm in hld['jjdm'].unique().tolist():
            print(jjdm)
            tempdf = hld[hld['jjdm'] == jjdm].set_index('JYRQ')
            new_date_list = tempdf.index.unique()[tempdf.index.unique() >= '20190628'].tolist()
            top_10_ticker_exp = []
            zqdm_list = tempdf.groupby('zqdm').sum().sort_values('zjbl', ascending=False)[0:10].index
            top10_list+=zqdm_list.tolist()
            # tempdf=tempdf[tempdf['zqdm'].isin(zqdm_list)]
            for n in range(1, len(new_date_list)):
                t0 = new_date_list[n - 1]
                t1 = new_date_list[n]
                flow_in_money = jjjz[(jjjz['jjdm']==jjdm)&(jjjz['jzrq']>=t0)&(jjjz['jzrq']<=t1)]['jjjz'].mean() * \
                                tempdf.loc[t1:t1]['share_changed'].unique()[0]

                df1 = pd.merge(tempdf.loc[t0:t0][['zqdm', 'zjbl']],new_price_df[['zqdm',t1]],
                               how='right', on='zqdm')
                df1 = df1[df1['zjbl'] > 0]
                df1['zgbl'] = df1['zjbl'] / df1['zjbl'].sum()
                df1['adjust_sl'] = (flow_in_money * df1['zjbl']) / df1[t1]

                df1 = pd.merge(tempdf.loc[t1:t1], df1[['zqdm', 'adjust_sl']],
                               how='left', on='zqdm').fillna(0)
                df1['adjuested_sl'] = df1['sl'] - df1['adjust_sl']
                df1['trade_date'] = t1
                top_10_ticker_exp.append(df1.drop(['gpsz', 'SPJG', 'share_changed',],axis=1))
            if(len(top_10_ticker_exp)>0):
                top_10_ticker_exp = pd.concat(top_10_ticker_exp, axis=0)
                top_10_ticker_exp = top_10_ticker_exp[top_10_ticker_exp['zqdm'].isin(zqdm_list)]
                hls_sl_history.append(top_10_ticker_exp)



        hls_sl_history = pd.concat(hls_sl_history, axis=0)

        #get ticker financial info

        style_financial_info = get_ticker_financial_info(list(set(top10_list)),
                                                         '20170630',end_date, with_stock_price=False)
        style_expectation_info=get_ticker_expection(list(set(top10_list)),
                                                    hls_sl_history['trade_date'].unique().tolist())
        style_expectation_info['EST_DT']=style_expectation_info['EST_DT'].astype(str).str[0:6]

        style_financial_info=pd.merge(style_financial_info[['SECUCODE','ROE', 'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY',
                                                            'PE', 'PEG', 'ENDDATE']],
                                      style_expectation_info,how='left',left_on=['SECUCODE','ENDDATE'],
                                      right_on=['ZQDM','EST_DT']).drop(['ZQDM','EST_DT'],axis=1)

        style_financial_info[financial_rank_col] = \
            style_financial_info[financial_col].rolling(
                8).apply(quantial_for_rolling)


        hls_sl_history=pd.merge(hls_sl_history,style_financial_info,
                                how='left',
                                left_on=['zqdm','joint_date'],
                                right_on=['SECUCODE','ENDDATE']).rename(columns=dict(zip(financial_col+financial_rank_col,
                                                                                   [x+'_ticker' for x in financial_col+financial_rank_col]))).drop(['joint_date','SECUCODE','ENDDATE','adjust_sl'],axis=1)
        hls_sl_history['asofdate'] = date_list[-1]
        return hls_sl_history

    @staticmethod
    def get_stock_price_mv(date_list=None,zqdm_list=None):

        count=0
        if(zqdm_list is not None):
            zqdm_con="zqdm in ({0})".format(util.list_sql_condition(zqdm_list))
            count+=1
        else:
            zqdm_con=""

        if(date_list is not None):
            date_con="jyrq in ({0})".format(util.list_sql_condition(date_list))
            count += 1
        else:
            date_con=""

        if(count==2):
            joint="and"
        else:
            joint=""

        trunk_size=1000
        stock_price=[]
        for i in range(0,int(np.floor(len(zqdm_list)/trunk_size)+1)):

            temp_jjdm_list=zqdm_list[i*trunk_size:(i+1)*trunk_size]
            zqdm_con = "zqdm in ({0})".format(util.list_sql_condition(temp_jjdm_list))

            sql="""
            select zqdm,jyrq,spjg,zjsz from st_ashare.t_st_ag_gpjy where {0} {2} {1} and spjg!=99999 and spjg!=0 and scdm in ('CNSESZ','CNSESH','CNSEBJ')
             """.format(zqdm_con,date_con,joint)

            stock_price.append(hbdb.db2df(sql,db='alluser'))

        stock_price=pd.concat(stock_price,axis=0)
        stock_price=stock_price.drop_duplicates('zqdm',keep='last')

        return stock_price

    @staticmethod
    def get_stock_daily_return(zqdm_list,start_date,end_date):

        trunk_size=1000
        return_data=[]
        for i in range(0,int(np.floor(len(zqdm_list)/trunk_size)+1)):

            temp_zqdm_list=zqdm_list[i*trunk_size:(i+1)*trunk_size]

            sql="select zqdm,jyrq,zdfd from st_ashare.t_st_ag_gpjy where zqdm in ({0}) and jyrq>='{1}' and jyrq<='{2}' and zdfd!=99999"\
                .format(util.list_sql_condition(temp_zqdm_list),start_date,end_date)
            return_data_trunk=hbdb.db2df(sql,db='alluser')
            return_data.append(return_data_trunk)

        return pd.concat(return_data,axis=0)

    @staticmethod
    def get_fund_daily_return(jjdm_list,start_date,end_date):

        sql="select jjdm,jzrq,hbdr from st_fund.t_st_gm_rhb where jjdm in ({0}) and jzrq>='{1}' and jzrq<='{2}' and hbdr!=99999"\
            .format(util.list_sql_condition(jjdm_list),start_date,end_date)
        daily_return=hbdb.db2df(sql,db='funduser')

        return daily_return

    @staticmethod
    def get_overlap_hld(jjdm,jjdm_list,last_date,asofdate,last_hld,
                        current_hld,knowing_weight,max_stock_weight):

        # get related fund manager
        sql = "select rydm from st_fund.t_st_gm_jjjl where jjdm='{0}' and rzrq<='{1}' and lrrq>='{1}' and ryzw='基金经理'" \
            .format(jjdm, last_date, asofdate)
        manager_list = hbdb.db2df(sql, db='funduser')['rydm'].astype(str).tolist()

        sql = "select jjdm from st_fund.t_st_gm_jjjl where rydm in ({0}) and rzrq<='{1}' and lrrq>='{1}' and ryzw='基金经理'" \
            .format(util.list_sql_condition(manager_list), last_date, asofdate)
        relate_jjdm_list = \
            list(
                (set(hbdb.db2df(sql, db='funduser')['jjdm'].tolist()).intersection(set(jjdm_list))).difference(
                    set([jjdm]))
            )

        # calculate the holding overlap rate
        overlap_jjdm_list = []
        for related_jjdm in relate_jjdm_list:
            relate_hld = last_hld[last_hld['jjdm'] == related_jjdm]
            relate_hld = pd.merge(last_hld[last_hld['jjdm'] == jjdm][['zqdm', 'zjbl']], relate_hld[['zqdm', 'zjbl']]
                                  , how='left', on='zqdm').fillna(0)
            if ((relate_hld[['zjbl_x', 'zjbl_y']].min(axis=1)).sum() / relate_hld['zjbl_x'].sum() >= 0.5):
                overlap_jjdm_list.append(related_jjdm)

        overlap_hld = current_hld[current_hld['jjdm'].isin(overlap_jjdm_list)]
        overlap_hld = \
            (overlap_hld.groupby('zqdm')['zjbl'].sum() / len(overlap_jjdm_list)).reset_index()
        overlap_hld = \
            overlap_hld[~overlap_hld['zqdm'].isin(knowing_weight['zqdm'].tolist())]
        overlap_hld.loc[overlap_hld['zjbl'] > max_stock_weight, 'zjbl'] = max_stock_weight

        overlap_hld=pd.merge(overlap_hld,
                             current_hld[['zqdm','zjh_industry','yjxymc']].drop_duplicates(['zqdm']),how='left',on='zqdm')


        return  overlap_hld

    @staticmethod
    def get_theme_map():

        theme_map = dict(zip(['大金融', '消费', 'TMT', '周期', '制造'],
                             [['银行', '非银金融', '房地产'],
                              ['食品饮料', '家用电器', '医药生物', '社会服务', '农林牧渔', '商贸零售', '美容护理'],
                              ['通信', '计算机', '电子', '传媒', '国防军工'],
                              ['钢铁', '有色金属', '建筑装饰', '建筑材料', '基础化工', '石油石化', '煤炭', '环保', '公用事业'],
                              ['交通运输', '机械设备', '汽车', '纺织服饰', '轻工制造', '电力设备']
                              ]
                             ))

        lista = []
        listb = []
        for theme in ['大金融', '消费', 'TMT', '周期', '制造']:
            for col in theme_map[theme]:
                lista.append(col)
                listb.append(theme)
        ind2thememap = pd.DataFrame()
        ind2thememap['industry_name'] = lista
        ind2thememap['theme'] = listb

        return ind2thememap

    @staticmethod
    def get_the_initial_constrains(jj_zjh_industry_data,jjdm,last_hld_key,last_hld,
                                   current_hld,company_jj_list,ind2thememap,adjusted_weight):

        # get the initial industry constrains
        industry_constrains = jj_zjh_industry_data[jj_zjh_industry_data['jjdm'] == jjdm]
        industry_constrains = \
            (industry_constrains.rename(columns={'hymc': 'zjh_industry'})).set_index('zjh_industry')[['zjbl']]

        # transform 制造业 constrains to 5+1 theme constrains
        if (industry_constrains.loc['制造业']['zjbl'] > 0):
            # get the 制造业 change
            last_theme_dis = (last_hld_key[(last_hld_key['zjh_industry'].isin(ind2thememap['theme'].unique().tolist()))
                                           & (last_hld_key['jjdm'].isin(company_jj_list))]).groupby('zjh_industry')[
                'zjbl'].sum()
            last_theme_dis = last_theme_dis / last_theme_dis.sum()
            current_dis = (current_hld[(current_hld['zjh_industry'].isin(ind2thememap['theme'].unique().tolist()))
                                       & (current_hld['jjdm'].isin(company_jj_list))]).groupby('zjh_industry')[
                'zjbl'].sum()
            current_dis = current_dis / current_dis.sum()
            change=pd.merge(last_theme_dis,current_dis,how='left',left_index=True,right_index=True)
            change['change']=change['zjbl_y']-change['zjbl_x']


            # get the last holding distribution
            last_dis = last_hld[(last_hld['jjdm'] == jjdm)
                                &(last_hld['zjh_industry'].isin(ind2thememap['theme'].unique().tolist()))].groupby('zjh_industry')['zjbl'].sum()
            last_dis=last_dis/last_dis.sum()
            last_dis=pd.merge(last_dis,change[['change']],how='outer',
                              left_index=True,right_index=True).fillna(0)

            #deal with the case that certain industry may have no orginal weight and is reduced by change
            last_dis.loc[last_dis['change'] + last_dis['zjbl'] < 0,'change']=last_dis['zjbl']
            if(last_dis['change'].sum()>=0.0001):
                last_dis.loc[last_dis['change']!=0,'change']=\
                    last_dis[last_dis['change']!=0]['change']-last_dis['change'].sum()/(last_dis['change']!=0).sum()


            last_dis['zjbl']=last_dis['zjbl']+last_dis['change']
            last_dis['zjbl']=last_dis['zjbl']*industry_constrains.loc['制造业']['zjbl']

            last_dis = pd.merge(last_dis, adjusted_weight * 100, how='left',
                                on='zjh_industry').fillna(0)
            count=0
            while((len(last_dis.loc[last_dis['zjbl']<last_dis['adjusted_zjbl']])>0)&(count<=20)):
            # if(len(last_dis.loc[last_dis['zjbl']<last_dis['adjusted_zjbl']])>0):
                c1=last_dis.loc[last_dis['zjbl']<last_dis['adjusted_zjbl']]
                c2=last_dis.loc[last_dis['zjbl']>=last_dis['adjusted_zjbl']]

                c1['zjbl']=c1['adjusted_zjbl']
                c2['zjbl']=c2['zjbl']/c2['zjbl'].sum()*(industry_constrains.loc['制造业']['zjbl']-c1['zjbl'].sum())

                last_dis=pd.concat([c1,c2],axis=0)
                count+=1
            industry_constrains = \
                pd.concat([industry_constrains, last_dis[['zjbl']]], axis=0).drop('制造业', axis=0)



        industry_constrains['zjbl']=industry_constrains['zjbl']/100

        return industry_constrains

    @staticmethod
    def insert_zq_with_constrains(industry_constrains,overlap_hld,first_holding,max_stock_weight):

        for zqdm in overlap_hld['zqdm'].unique().tolist():
            tempdf = overlap_hld[overlap_hld['zqdm'] == zqdm]
            if(tempdf['zjh_industry'].iloc[0]  not in industry_constrains.index):
                continue
            else:
                if (industry_constrains.loc[tempdf['zjh_industry']]['zjbl'].iloc[0] > 0):
                    if (tempdf['zjbl'].iloc[0] > industry_constrains.loc[tempdf['zjh_industry']]['zjbl'].iloc[0]):
                        tempdf['zjbl'] =np.min([industry_constrains.loc[tempdf['zjh_industry'].iloc[0]]['zjbl'],max_stock_weight])
                    else:
                        tempdf['zjbl'].iloc[0] = np.min(
                            [tempdf['zjbl'].iloc[0], max_stock_weight])

                    # if condition passed them insert
                    first_holding.append(tempdf)
                    # update the industry constrains as well
                    industry_constrains.loc[tempdf['zjh_industry'].iloc[0], 'zjbl'] = \
                        industry_constrains.loc[tempdf['zjh_industry'].iloc[0]]['zjbl'] - tempdf['zjbl'].iloc[0]
                    # update the total left weight
                    industry_constrains.loc['合计', 'zjbl'] = \
                        industry_constrains.loc['合计']['zjbl'] - tempdf['zjbl'].iloc[0]

        return first_holding,industry_constrains

    @staticmethod
    def insert_zq_for_regression_pool(company_holding,totalnum,not_filled_industry_list,
                                      industry_constrains,regression_holding,max_stock_weight):

        # holding_missed_industry_list=[]

        if (len(company_holding) > 0):
            while (totalnum < 20 and len(not_filled_industry_list)>0 and len(company_holding) > 0):
                for industry in not_filled_industry_list:
                    if(industry in  company_holding['zjh_industry'].unique().tolist()):
                        tempdf = company_holding[company_holding['zjh_industry'] == industry].iloc[[0]]
                        if (industry_constrains.loc[industry]['zjbl'] > 0):
                            if (tempdf['zjbl'].iloc[0]> industry_constrains.loc[tempdf['zjh_industry'].iloc[0]]['zjbl']):
                                tempdf['zjbl'].iloc[0] = np.min([industry_constrains.loc[industry]['zjbl'],max_stock_weight])
                            else:
                                tempdf['zjbl'].iloc[0] = np.min(
                                    [tempdf['zjbl'].iloc[0], max_stock_weight])

                            # if condition passed them insert
                            regression_holding.append(tempdf)
                            # update the industry constrains as well
                            industry_constrains.loc[industry, 'zjbl'] = \
                                industry_constrains.loc[industry]['zjbl'] - tempdf['zjbl'].iloc[0]
                            # update the total left weight
                            industry_constrains.loc['合计', 'zjbl'] = \
                                industry_constrains.loc['合计']['zjbl'] - tempdf['zjbl'].iloc[0]

                            totalnum += 1
                            company_holding = \
                                company_holding[(company_holding['zqdm'] != tempdf['zqdm'].iloc[0])]
                        else:
                            not_filled_industry_list.remove(industry)
                    else:
                        # holding_missed_industry_list.append(industry)
                        not_filled_industry_list.remove(industry)

            pd.concat(regression_holding, axis=0).groupby('zjh_industry')['zqdm'].count() * max_stock_weight


        # not_filled_industry_list+=holding_missed_industry_list
        return  company_holding,totalnum,not_filled_industry_list,\
                industry_constrains,regression_holding

    def key_holding_expantation(self,jjdm_list,asofdate,last_date,
                                regression_strat_date,regression_end_date,from_local=False):

        #get the jj company info of the jj
        sql="select jjdm,glrm from st_fund.t_st_gm_jjxx where jjdm in ({})"\
            .format(util.list_sql_condition(jjdm_list))
        jj_company_info=hbdb.db2df(sql,db='funduser')

        # jjdm_list=jj_company_info[jj_company_info['glrm']=='80049689']['jjdm'].tolist()
        current_hld = self.read_hld_list_fromdb(asofdate[0:6]+'01', asofdate,
                                            jjdm_list, True)


        last_hld = self.read_hld_list_fromdb(last_date[0:6] + '01', last_date,
                                             jjdm_list, False, from_local)


        jjdm_list=list(set(current_hld['jjdm']).intersection(set(last_hld['jjdm'])))

        # get regression stock ret data
        return_data = \
            self.get_stock_daily_return(list(set(current_hld['zqdm'].unique().tolist()+
                                                           last_hld['zqdm'].unique().tolist())), regression_strat_date, regression_end_date)
        # get regression fund ret data
        jj_ret_data = \
            self.get_fund_daily_return(jjdm_list, regression_strat_date, regression_end_date)
        jj_ret_data=jj_ret_data[jj_ret_data['jzrq'].isin(return_data['jyrq'].unique().tolist())]

        # get the bond ret
        sql="select hbdr,jyrq from st_market.t_st_zs_rhb where zqdm='CBA00301' and jyrq>='{0}' and jyrq<='{1}' "\
            .format( regression_strat_date, regression_end_date)
        bond_ret=hbdb.db2df(sql,db='alluser').rename(columns={'hbdr':'CBA00301'})

        fund_jjjzc=self.get_fund_jjjzc(jjdm_list,
                                       asofdate[0:6]+'01', asofdate)

        #calculate the ccsl by price and zjbl
        if(from_local):
            trade_date_1=util._shift_date(last_date)
            stock_price=self.get_stock_price_mv(date_list=[trade_date_1]
                                        ,zqdm_list=last_hld['zqdm'].unique().tolist())
            last_hld=pd.merge(last_hld,stock_price[['zqdm','spjg']],how='left',on='zqdm')
            last_hld=pd.merge(last_hld,fund_jjjzc[['jjdm','jjjzc']],how='left',on='jjdm')
            last_hld['ccsl']=last_hld['jjjzc']*last_hld['zjbl']/last_hld['spjg']
            last_hld.drop(['spjg','jjjzc'],axis=1,inplace=True)


        #read the zjh industry dis
        sql="select jjdm,hymc,zjbl from st_fund.t_st_gm_hyzh where jjdm in ({0}) and jsrq>='{1}' and jsrq<='{2}'"\
            .format(util.list_sql_condition(jjdm_list),asofdate[0:6]+'01', asofdate)
        jj_zjh_industry_data=hbdb.db2df(sql,db='funduser')


        #merge the industry and theme info to holding data
        stock_zjhind_map\
            =self.get_ind_map(3)
        stock_swind_map\
            =self.get_ind_map(2)

        current_hld=pd.merge(current_hld,stock_zjhind_map[['zqdm','yjxymc']]
                             ,how='left',on='zqdm').rename(columns={'yjxymc':'zjh_industry'})
        last_hld=pd.merge(last_hld,stock_zjhind_map[['zqdm','yjxymc']]
                             ,how='left',on='zqdm').rename(columns={'yjxymc':'zjh_industry'})
        current_hld=pd.merge(current_hld,stock_swind_map[['zqdm','yjxymc']]
                             ,how='left',on='zqdm')
        last_hld=pd.merge(last_hld,stock_swind_map[['zqdm','yjxymc']]
                             ,how='left',on='zqdm')

        #get index weight
        sql = "select cfgdm,qz from st_market.t_st_zs_zscfgqz where zqdm='000906' "
        index_w = hbdb.db2df(sql, db='alluser').rename(columns={'cfgdm':'zqdm'})
        index_w=pd.merge(index_w,stock_zjhind_map[['zqdm','yjxymc']]
                             ,how='left',on='zqdm').rename(columns={'yjxymc':'zjh_industry'})
        index_w=pd.merge(index_w,stock_swind_map[['zqdm','yjxymc']]
                             ,how='left',on='zqdm')


        #distinguish hk stock
        current_hld['if_hk']=[len(x) for x in current_hld['zqdm']]
        last_hld['if_hk']=[len(x) for x in last_hld['zqdm']]


        ind2thememap=self.get_theme_map()
        ind2thememap.loc[ind2thememap['industry_name']=='医药生物','theme']='医药生物'

        current_hld=\
            pd.merge(current_hld,ind2thememap,how='left'
                     ,left_on='yjxymc',right_on='industry_name').drop('industry_name',axis=1)
        last_hld=\
            pd.merge(last_hld,ind2thememap,how='left',
                     left_on='yjxymc',right_on='industry_name').drop('industry_name',axis=1)

        index_w=\
            pd.merge(index_w,ind2thememap,how='left',
                     left_on='yjxymc',right_on='industry_name').drop('industry_name',axis=1)

        #divide the 制造业 to 5+1 theme
        current_hld.loc[current_hld['zjh_industry']=='制造业','zjh_industry']=\
            current_hld[current_hld['zjh_industry']=='制造业']['theme']
        last_hld.loc[last_hld['zjh_industry']=='制造业','zjh_industry']=\
            last_hld[last_hld['zjh_industry']=='制造业']['theme']
        index_w.loc[index_w['zjh_industry']=='制造业','zjh_industry']=\
            index_w[index_w['zjh_industry']=='制造业']['theme']

        last_hld['rank'] = \
                last_hld.groupby(['jjdm','jsrq'])['zjbl'].rank(method='min',ascending=False)
        last_hld_key=last_hld[last_hld['rank']<=10]

        trade_date_2=util._shift_date(asofdate)
        stock_ret=\
            self.get_stock_price_mv(date_list=[trade_date_2]
                                    ,zqdm_list=current_hld['zqdm'].unique().tolist()
                                               +last_hld['zqdm'].unique().tolist())
        # stock_ret['ret']=\
        #     stock_ret[trade_date_2]/stock_ret[trade_date_1]-1

        bond_ret['nav'] = (bond_ret['CBA00301'] / 100 + 1).cumprod()
        bond_ret['asofdate_nav'] = bond_ret[bond_ret['jyrq'] == int(trade_date_2)]['nav'].iloc[0]
        bond_ret['nav'] = bond_ret['nav'].shift(1).fillna(1)



        outputdf=[]
        err_c=0
        #008861 domain error  003889,004359 Rank(A) < p or Rank([P; A; G]) < n 003993,004098 '制造业'
        for jjdm in jjdm_list:
            # print(jjdm) 740001
            try:
                first_holding=[]

                knowing_weight=current_hld[(current_hld['jsrq']==current_hld['jsrq'].max())
                                           &(current_hld['jjdm']==jjdm)]
                max_stock_weight=knowing_weight['zjbl'].min()

                #get the overlaped holding
                overlap_hld=self.get_overlap_hld(jjdm,jjdm_list,last_date,asofdate,last_hld,
                            current_hld,knowing_weight,max_stock_weight)

                #get the initial industry constrains
                company_jj_list = \
                    jj_company_info[
                        jj_company_info['glrm'] == jj_company_info[jj_company_info['jjdm'] == jjdm]['glrm'].iloc[0]][
                        'jjdm'].tolist()



                temp_asset_allocation=fund_jjjzc[fund_jjjzc['jjdm']==jjdm]



                #update the constrains by published key holding
                adjusted_weight=\
                    (current_hld[(current_hld['jjdm']==jjdm)
                                 &(current_hld['if_hk']==6)].groupby('zjh_industry')['zjbl'].sum()).to_frame('adjusted_zjbl')
                adjusted_weight.loc['合计'] = adjusted_weight['adjusted_zjbl'].sum()

                industry_constrains=\
                    self.get_the_initial_constrains(jj_zjh_industry_data,jjdm,last_hld_key,last_hld,current_hld,company_jj_list,ind2thememap,adjusted_weight)
                hk_weight=\
                    temp_asset_allocation['gptzzjb'].iloc[0]/100-industry_constrains.loc['合计'].iloc[0]

                industry_constrains=pd.merge(industry_constrains,adjusted_weight
                                             ,how='outer',on='zjh_industry').fillna(0)
                industry_constrains['zjbl']=industry_constrains['zjbl']-industry_constrains['adjusted_zjbl']

                first_holding.append(current_hld[current_hld['jjdm']==jjdm][['zjbl','zqdm','zjh_industry','yjxymc']])

                #insert the manager related holding and updated the industry constrains
                overlap_hld=overlap_hld.sort_values('zjbl', ascending=False)
                first_holding,industry_constrains=\
                    self.insert_zq_with_constrains(industry_constrains, overlap_hld, first_holding,max_stock_weight)


                #insert last hold
                temp_last_hld=last_hld[(last_hld['jjdm']==jjdm)
                                       &(~last_hld['zqdm'].isin(pd.concat(first_holding,axis=0)['zqdm'].unique().tolist()))
                                       &(last_hld['zjh_industry'].isin(industry_constrains[industry_constrains['zjbl']>0].index.to_list()))]

                #merge the stock return and recalculate the zjbl
                temp_last_hld=pd.merge(temp_last_hld,stock_ret[['zqdm','spjg']],on='zqdm',how='left')
                temp_last_hld['jjjzc']=fund_jjjzc[fund_jjjzc['jjdm']==jjdm]['jjjzc'].iloc[0]
                temp_last_hld.loc[(temp_last_hld['spjg'].notnull()&(temp_last_hld['ccsl'].notnull())),'zjbl']=\
                    temp_last_hld.loc[(temp_last_hld['spjg'].notnull()&(temp_last_hld['ccsl'].notnull()))]['spjg']*temp_last_hld.loc[(temp_last_hld['spjg'].notnull()&(temp_last_hld['ccsl'].notnull()))]['ccsl']/temp_last_hld.loc[(temp_last_hld['spjg'].notnull()&(temp_last_hld['ccsl'].notnull()))]['jjjzc']

                temp_last_hld.sort_values('zjbl',ascending=False,inplace=True)
                temp_last_hld.loc[temp_last_hld['zjbl']>max_stock_weight,'zjbl']=max_stock_weight

                first_holding,industry_constrains=\
                    self.insert_zq_with_constrains(industry_constrains, temp_last_hld[temp_last_hld['if_hk']==6], first_holding,max_stock_weight)
                first_holding=pd.concat(first_holding,axis=0)

                industry_constrains_copy=industry_constrains.copy()
                not_filled_industry_list=\
                    industry_constrains[(industry_constrains['zjbl']>0)&(industry_constrains.index!='合计')].sort_values('zjbl',ascending=False).index.tolist()

                if(len(not_filled_industry_list)>0):

                    regression_holding = []
                    totalnum=0
                    # company holding

                    company_jj_list.remove(jjdm)
                    company_holding=current_hld[(current_hld['jjdm'].isin(company_jj_list))
                                                &(~current_hld['zqdm'].isin(first_holding['zqdm'].tolist()))
                                                &(current_hld['zjh_industry'].isin(not_filled_industry_list))]
                    company_holding=pd.merge(company_holding.groupby('zqdm')[['zjbl']].mean(),company_holding[['zqdm','zjh_industry','yjxymc','if_hk']]
                                             ,how='left',on='zqdm')[['zqdm','zjbl','zjh_industry','yjxymc','if_hk']].drop_duplicates('zqdm')

                    company_holding=pd.merge(company_holding,stock_ret[['zqdm','zjsz']],
                                             on='zqdm',how='left')
                    company_holding=company_holding[company_holding['zjsz'].notnull()]
                    company_holding.sort_values(['zjsz','zjh_industry'],ascending=False,inplace=True)

                    company_holding, totalnum, not_filled_industry_list,industry_constrains, regression_holding=\
                        self.insert_zq_for_regression_pool(company_holding[company_holding['if_hk']==6],totalnum,not_filled_industry_list,
                                          industry_constrains,regression_holding,max_stock_weight)


                    #get the all mutual holding if necessary
                    not_filled_industry_list = \
                        industry_constrains[
                            (industry_constrains['zjbl'] > 0) & (industry_constrains.index != '合计')].sort_values(
                            'zjbl', ascending=False).index.tolist()
                    if (len(not_filled_industry_list) > 0):
                        if(len(regression_holding)>0):
                            market_holding = current_hld[(~current_hld['zqdm'].isin(pd.concat(regression_holding)['zqdm'].tolist()))
                                                          & (~current_hld['zqdm'].isin(first_holding['zqdm'].tolist()))
                                                          & (current_hld['zjh_industry'].isin(not_filled_industry_list))]
                        else:
                            market_holding = current_hld[ (~current_hld['zqdm'].isin(first_holding['zqdm'].tolist()))
                                                          & (current_hld['zjh_industry'].isin(not_filled_industry_list))]
                        market_holding = pd.merge(market_holding.groupby('zqdm')[['zjbl']].mean(),
                                                   market_holding[['zqdm','zjh_industry','yjxymc','if_hk']]
                                                   , how='left', on='zqdm')[
                            ['zqdm', 'zjbl', 'zjh_industry', 'yjxymc','if_hk']].drop_duplicates('zqdm')

                        market_holding = pd.merge(market_holding, stock_ret[['zqdm', 'zjsz']],
                                                   on='zqdm', how='left')
                        market_holding.sort_values(['zjsz', 'zjh_industry'], ascending=False, inplace=True)
                        market_holding = market_holding[market_holding['zjsz'].notnull()]

                        market_holding, totalnum, not_filled_industry_list, industry_constrains, regression_holding = \
                            self.insert_zq_for_regression_pool(market_holding[market_holding['if_hk']==6], totalnum, not_filled_industry_list,
                                                               industry_constrains, regression_holding,max_stock_weight)

                        not_filled_industry_list = \
                            industry_constrains[
                                (industry_constrains['zjbl'] > 0) & (industry_constrains.index != '合计')].sort_values(
                                'zjbl', ascending=False).index.tolist()
                        #add ZZ800 stocks if necessary
                        if(len(not_filled_industry_list) > 0):

                            if (len(regression_holding) > 0):
                                index_holding = index_w[
                                    (~index_w['zqdm'].isin(pd.concat(regression_holding)['zqdm'].tolist()))
                                    & (~index_w['zqdm'].isin(first_holding['zqdm'].tolist()))
                                    & (index_w['zjh_industry'].isin(not_filled_industry_list))]
                            else:
                                index_holding = index_w[(~index_w['zqdm'].isin(first_holding['zqdm'].tolist()))
                                                             & (index_w['zjh_industry'].isin(
                                    not_filled_industry_list))]
                            index_holding.rename(columns={'qz':'zjbl'},inplace=True)
                            index_holding = pd.merge(index_holding.groupby('zqdm')[['zjbl']].mean(),
                                                      index_holding[['zqdm', 'zjh_industry', 'yjxymc']]
                                                      , how='left', on='zqdm')[
                                ['zqdm', 'zjbl', 'zjh_industry', 'yjxymc']].drop_duplicates('zqdm')

                            index_holding = pd.merge(index_holding, stock_ret[['zqdm', 'zjsz']],
                                                      on='zqdm', how='left')
                            index_holding.sort_values(['zjsz', 'zjh_industry'], ascending=False, inplace=True)
                            index_holding = index_holding[index_holding['zjsz'].notnull()]

                            index_holding, totalnum, not_filled_industry_list, industry_constrains, regression_holding = \
                                self.insert_zq_for_regression_pool(index_holding,
                                                                   totalnum, not_filled_industry_list,
                                                                   industry_constrains, regression_holding,
                                                                   max_stock_weight)

                        # check if the solution is possible for max stock weight
                        solution_check = pd.merge(industry_constrains_copy
                                                  , pd.concat(regression_holding,axis=0).groupby('zjh_industry')[
                                                      'zqdm'].count() * max_stock_weight
                                                  , how='left', on='zjh_industry')
                        not_filled_industry_list = solution_check[solution_check['zjbl'] >= solution_check['zqdm']].index.tolist()
                        # add ZZ800 stocks if necessary
                        if (len(not_filled_industry_list) > 0):

                            if (len(regression_holding) > 0):
                                index_holding = index_w[
                                    (~index_w['zqdm'].isin(pd.concat(regression_holding)['zqdm'].tolist()))
                                    & (~index_w['zqdm'].isin(first_holding['zqdm'].tolist()))
                                    & (index_w['zjh_industry'].isin(not_filled_industry_list))]
                            else:
                                index_holding = index_w[(~index_w['zqdm'].isin(first_holding['zqdm'].tolist()))
                                                        & (index_w['zjh_industry'].isin(
                                    not_filled_industry_list))]
                            index_holding.rename(columns={'qz': 'zjbl'}, inplace=True)
                            index_holding = pd.merge(index_holding.groupby('zqdm')[['zjbl']].mean(),
                                                     index_holding[['zqdm', 'zjh_industry', 'yjxymc']]
                                                     , how='left', on='zqdm')[
                                ['zqdm', 'zjbl', 'zjh_industry', 'yjxymc']].drop_duplicates('zqdm')

                            index_holding = pd.merge(index_holding, stock_ret[['zqdm', 'zjsz']],
                                                     on='zqdm', how='left')
                            index_holding.sort_values(['zjsz', 'zjh_industry'], ascending=False, inplace=True)
                            index_holding = index_holding[index_holding['zjsz'].notnull()]

                            index_holding, totalnum, not_filled_industry_list, industry_constrains, regression_holding = \
                                self.insert_zq_for_regression_pool(index_holding,
                                                                   0, not_filled_industry_list,
                                                                   industry_constrains, regression_holding,
                                                                   max_stock_weight)

                    regression_holding=pd.concat(regression_holding,axis=0)
                    no_regression_holding=\
                        regression_holding[regression_holding['zjh_industry'].isin(regression_holding.groupby('zjh_industry')['zqdm'].count()[regression_holding.groupby('zjh_industry')['zqdm'].count()==1].index)]
                    regression_holding=\
                        regression_holding[~regression_holding['zjh_industry'].isin(regression_holding.groupby('zjh_industry')['zqdm'].count()[regression_holding.groupby('zjh_industry')['zqdm'].count()==1].index)]
                    first_holding=pd.concat([first_holding,no_regression_holding[['zqdm','zjbl','yjxymc']]],axis=0)
                    industry_constrains_copy=\
                        industry_constrains_copy.loc[regression_holding['zjh_industry'].unique().tolist()]



                    #get the hk holding
                    if(len(knowing_weight[knowing_weight['if_hk']==5])>0):
                        unkonw_hk_w=\
                            hk_weight-knowing_weight[knowing_weight['if_hk']==5]['zjbl'].sum()
                    else:
                        unkonw_hk_w=\
                            hk_weight

                    if(unkonw_hk_w>0):
                        last_hk_hld=temp_last_hld[temp_last_hld['if_hk'] == 5]
                        last_hk_hld['zjbl']=last_hk_hld['zjbl']/last_hk_hld['zjbl'].sum()*unkonw_hk_w
                    else:
                        last_hk_hld=pd.DataFrame()

                    first_holding=pd.concat([first_holding,last_hk_hld],axis=0)

                    if(len(regression_holding)>0):
                        temp_regress_data=\
                            return_data[return_data['zqdm'].isin(list(set(first_holding['zqdm'].tolist()+
                                                                          regression_holding['zqdm'].tolist())))]
                        temp_fund_return=jj_ret_data[jj_ret_data['jjdm']==jjdm]


                        #adjust the zq weight by stock ret and fund ret
                        temp_regress_data['nav'] = temp_regress_data['zdfd'] / 100 + 1
                        temp_regress_data['nav']=temp_regress_data.groupby('zqdm')['nav'].cumprod()
                        temp_regress_data=pd.merge(temp_regress_data,
                                                   temp_regress_data[temp_regress_data['jyrq']==int(trade_date_2)][['nav','zqdm']].rename(columns={'nav':'asofdate_nav'})
                                                   ,how='left',on='zqdm')
                        temp_regress_data['nav']=temp_regress_data.groupby('zqdm')['nav'].shift(1).fillna(1)
                        temp_regress_data['cum_ret']=temp_regress_data['nav']/temp_regress_data['asofdate_nav']


                        temp_fund_return['nav']=(temp_fund_return['hbdr']/100+1).cumprod()
                        temp_fund_return['asofdate_nav']=temp_fund_return[temp_fund_return['jzrq']==int(trade_date_2)]['nav'].iloc[0]
                        temp_fund_return['nav'] = temp_fund_return['nav'].shift(1).fillna(1)
                        temp_fund_return['cum_ret']=temp_fund_return['nav']/temp_fund_return['asofdate_nav']


                        bond_ret['zjbl']=temp_asset_allocation['zqzszzjb'].iloc[0]/100
                        bond_ret['cum_ret'] = bond_ret['nav'] / bond_ret['asofdate_nav']
                        bond_ret=pd.merge(bond_ret,temp_fund_return[['jzrq','cum_ret']],how='left'
                                                ,left_on='jyrq',right_on='jzrq')
                        bond_ret['zjbl']=bond_ret['zjbl']*bond_ret['cum_ret_x']/bond_ret['cum_ret_y']


                        first_pool_ret=pd.merge(temp_regress_data,first_holding[['zqdm','zjbl']],on='zqdm',how='right')
                        first_pool_ret=pd.merge(first_pool_ret,temp_fund_return[['jzrq','cum_ret']],how='left'
                                                ,left_on='jyrq',right_on='jzrq')
                        first_pool_ret['zjbl']=first_pool_ret['zjbl']*first_pool_ret['cum_ret_x']/first_pool_ret['cum_ret_y']
                        first_pool_ret['zdfd']=first_pool_ret['zdfd']*first_pool_ret['zjbl']
                        first_pool_ret=first_pool_ret.groupby('jyrq')[['zdfd']].sum()


                        #calculate the weight by ols
                        regress_pool_ret=pd.merge(regression_holding[['zqdm','zjbl']],temp_regress_data,
                                                  on='zqdm',how='left')
                        regress_pool_ret=pd.merge(regress_pool_ret,temp_fund_return,how='left',left_on='jyrq',right_on='jzrq')
                        regress_pool_ret['zdfd']=\
                            regress_pool_ret['zdfd']*regress_pool_ret['cum_ret_x']/regress_pool_ret['cum_ret_y']
                        regress_pool_ret=regress_pool_ret.pivot_table('zdfd','jyrq','zqdm')


                        #remove the bond return
                        temp_fund_return=pd.merge(temp_fund_return,bond_ret[['jyrq','CBA00301','zjbl']],
                                                  left_on='jzrq',right_on='jyrq',how='left')
                        temp_fund_return['hbdr']=temp_fund_return['hbdr']-temp_fund_return['CBA00301']*temp_fund_return['zjbl']
                        bond_ret.drop(['zjbl','cum_ret_x','cum_ret_y','jzrq'],axis=1,inplace=True)

                        #remove the first pool return

                        temp_fund_return=pd.merge(temp_fund_return,first_pool_ret,
                                                  left_on='jzrq',right_on='jyrq',how='left')
                        temp_fund_return['hbdr']=temp_fund_return['hbdr']-temp_fund_return['zdfd']




                        #get the solvable stock weight constrains
                        regression_holding=pd.merge(regression_holding,industry_constrains_copy['zjbl'].to_frame('upbond'),
                                                    how='left',on='zjh_industry')
                        regression_holding['zjbl']=[np.min([x,max_stock_weight]) for x in  regression_holding['zjbl']]


                        result,r_sqr,adj_r_sqr=\
                            util.my_general_linear_model_func_holding_companzation(regress_pool_ret.values,
                                                                                   temp_fund_return['hbdr'].values,
                                                                                   max_stock_weight,pd.get_dummies(regression_holding.sort_values('zqdm')[['zjh_industry']]).sort_index().T,
                                                                                   (industry_constrains_copy[(industry_constrains_copy.index!='合计')&(industry_constrains_copy['zjbl']>0)].sort_index())['zjbl'].values
                                                                                   ,if_wls=False)
                        # print(r_sqr)
                        regression_holding=regression_holding.sort_values('zqdm')
                        regression_holding['regression_zjbl']=result

                        final_holding=pd.concat([first_holding[['zqdm','zjbl','yjxymc']],regression_holding[['zqdm','zjbl','yjxymc']]],axis=0)
                    else:
                        final_holding = first_holding[['zqdm', 'zjbl', 'yjxymc']]

                else:
                    final_holding=first_holding[['zqdm','zjbl','yjxymc']]

                final_holding['jjdm'] = jjdm

                outputdf.append(final_holding)

            except Exception as e:
                print(jjdm)
                print(e)
                err_c+=1
                continue
        print('total error number is {}'.format(err_c))
        pd.concat(outputdf,axis=0).drop_duplicates(['jjdm','zqdm']).fillna(0).to_excel('补全持仓数据_{}.xlsx'.format(asofdate))

    @staticmethod
    def save_quarter_data_2_db(path,add=True):

        import os
        file_list = []
        # path = r"E:\GitFolder\docs\公募基金行业动态模拟\持仓数据补全\年报半年报补全\\"
        for i, j, k in os.walk(path):
            if (len(file_list) == 0):
                file_list = k

        if(add):
            file_list=file_list[-1:]

        for file in file_list:
            asofdate = file.split('_')[1][0:8]
            hld = \
                pd.read_excel(path+file).drop('Unnamed: 0', axis=1)
            hld['zqdm'] = [("000000" + str(x))[-6:] for x in hld['zqdm']]
            hld['jjdm'] = [("000000" + str(x))[-6:] for x in hld['jjdm']]
            localdb.execute("delete from artificial_quartly_full_hld where jsrq='{}'".format(asofdate))
            hld['jsrq']=asofdate
            hld.to_sql('artificial_quartly_full_hld',index=False,if_exists='append',con=localdb)

    @staticmethod
    def mimic_hlding_accuracy_check():

        import os
        file_list = []
        path = r"E:\GitFolder\docs\公募基金行业动态模拟\持仓数据补全\年报半年报补全\\"
        for i, j, k in os.walk(path):
            if (len(file_list) == 0):
                file_list = k
        real_date = []
        artificial_data = []
        overlap_data = []

        for file in file_list:
            asofdate = file.split('_')[1][0:8]
            hld = \
                pd.read_excel(
                    r"E:\GitFolder\docs\公募基金行业动态模拟\持仓数据补全\年报半年报补全\{0}".format(file)).drop(
                    'Unnamed: 0', axis=1)
            hld['zqdm'] = [("000000" + str(x))[-6:] for x in hld['zqdm']]
            hld['jjdm'] = [("000000" + str(x))[-6:] for x in hld['jjdm']]
            hld['jsrq'] = asofdate
            jjdm_list = hld['jjdm'].unique().tolist()

            sql = "select jjdm,flmc,zzjbl,jsrq from st_fund.t_st_gm_jjhyzhyszb where jjdm in ({0}) and hyhfbz=2 and jsrq>='{1}' and jsrq<='{2}' and zclb=2" \
                .format(util.list_sql_condition(jjdm_list), asofdate[0:6] + '01', asofdate[0:6] + '31')
            hyfb = hbdb.db2df(sql, db='funduser')

            hld = hld.groupby(['jjdm', 'yjxymc'])['zjbl'].sum().reset_index()

            industry_overlap = pd.merge(hyfb, hld, how='left', left_on=['jjdm', 'flmc'], right_on=['jjdm', 'yjxymc'])
            industry_overlap['zzjbl'] = industry_overlap['zzjbl'] / 100
            industry_overlap['overlap'] = industry_overlap[['zzjbl', 'zjbl']].min(axis=1)
            industry_overlap = industry_overlap.groupby('jjdm')[['overlap']].sum()
            industry_overlap = pd.merge(industry_overlap,
                                        (hyfb.groupby('jjdm')['zzjbl'].sum() / 100).to_frame('total_w')
                                        , how='left', on='jjdm')
            industry_overlap['overlap'] = industry_overlap['overlap'] / industry_overlap['total_w']

            hyfb = hyfb.groupby('flmc')['zzjbl'].sum() / len(hyfb['jjdm'].unique()) / 100
            hld = hld.groupby('yjxymc')['zjbl'].sum() / len(hld['jjdm'].unique())

            real_date.append(hyfb.to_frame(asofdate))
            artificial_data.append(hld.to_frame(asofdate))
            overlap_data.append(industry_overlap['overlap'].to_frame(asofdate))

        real_date = pd.concat(real_date, axis=1)
        artificial_data = pd.concat(artificial_data, axis=1)
        overlap_data = pd.concat(overlap_data, axis=1)

        real_date.to_excel('实际值.xlsx')
        artificial_data.to_excel('拟合值.xlsx')
        overlap_data.to_excel('个基行业重合度.xlsx')

    @staticmethod
    def plot_industry_diviation():

        plot = functionality.Plot(1200, 600)
        realdata = \
            pd.read_excel(r"E:\GitFolder\docs\公募基金行业动态模拟\补全算法结果汇总.xlsx",
                          sheet_name='实际值').set_index('日期')
        olsdata = \
            pd.read_excel(r"E:\GitFolder\docs\公募基金行业动态模拟\补全算法结果汇总.xlsx",
                          sheet_name='补全值').set_index('日期')
        #
        realdata['total'] = realdata.sum(axis=1)
        olsdata['total'] = olsdata.sum(axis=1)

        for col in realdata.columns.tolist():
            tempdata = 100 * pd.merge(realdata[col].to_frame('实际仓位')
                                      , olsdata[col].to_frame('回归仓位'), how='left', left_index=True,
                                      right_index=True)
            tempdata.index = tempdata.index.astype(str)
            plot.plotly_line_style(tempdata.sort_index(), col + '仓位时序%', fix_range=[0, 20],
                                   save_local_file=r"E:\GitFolder\docs\公募基金行业动态模拟\\")

        # for col in realdata.columns.tolist()[0:-1]:
        #     tempdata=pd.merge((realdata[col]/realdata['total']*100).to_frame('实际仓位')
        #                                     ,(olsdata[col]/olsdata['total']*100).to_frame('回归仓位'),how='left',left_index=True,right_index=True)
        #     tempdata.index = tempdata.index.astype(str)
        #     plot.plotly_line_style(tempdata.sort_index(),col+'仓位时序%',fix_range=[0,20],save_local_file= r"E:\GitFolder\docs\公募基金行业动态模拟\\" )

class Brinson_ability:

    def __init__(self):
        self.localengine=db_engine.PrvFunDB().engine
        self.hbdb=db_engine.HBDB()
        self.today=str(datetime.datetime.today().date())

    def rank_perc(self,ret_df):

        ret_col=ret_df.columns
        ret_df[ret_col] = ret_df[ret_col].rank(ascending=False)
        for col in ret_col:
            ret_df[col] = ret_df[col] / ret_df[col].max()

        return ret_df

    def get_brinson_data(self,asofdate):

        sql="select distinct tjrq from st_fund.r_st_hold_excess_attr_df where tjrq>='{0}' and tjrq<='{1}' "\
            .format(str(int(asofdate[0:4])-7)+'0101',asofdate)
        tjrq_list=self.hbdb.db2df(sql,db='funduser').sort_values('tjrq',ascending=False)['tjrq'].tolist()
        tjrq_list.sort()

        fin_df=pd.DataFrame(data=util.get_mutual_stock_funds(tjrq_list[-1]),columns=['jjdm'])

        ret_col = ['asset_allo', 'sector_allo', 'equity_selection', 'trading']
        for tjrq in tjrq_list:
            sql="""select jjdm,asset_allo,sector_allo,equity_selection,trading 
            from st_fund.r_st_hold_excess_attr_df where tjrq='{0}'""".format(tjrq)
            ret_df=self.hbdb.db2df(sql,db='funduser')

            for col in ret_col:

                ret_df.rename(columns={col: col + "_" + tjrq}, inplace=True)

            fin_df=pd.merge(fin_df,ret_df,how='left',on='jjdm')

        return  fin_df

    def brinson_rank(self,fin_df,threshold):

        outputdf = pd.DataFrame()
        outputdf['jjdm'] = fin_df.columns.tolist()

        for i in range(4):
            step = int(len(fin_df) / 4)
            tempdf = fin_df.iloc[i * step:(i + 1) * step]
            inputdf = pd.DataFrame()
            inputdf['jjdm'] = tempdf.columns.tolist()

            for j in range(1, 13):
                inputdf['{}month_ave_rank'.format(6 * j)] = self.rank_perc(tempdf.rolling(j).sum().T).T.mean().values

            short_term = inputdf.columns[1:7]
            long_term = inputdf.columns[7:13]

            new_col = 'short_term_{}'.format(tempdf.index[0].split('_')[0])
            inputdf[new_col] = 0
            inputdf.loc[(inputdf[short_term] <= threshold).sum(axis=1) >= 1, new_col] = 1

            new_col2 = 'long_term_{}'.format(tempdf.index[0].split('_')[0])
            inputdf[new_col2] = 0
            inputdf.loc[(inputdf[long_term] <= threshold).sum(axis=1) >= 1, new_col2] = 1

            outputdf = pd.merge(outputdf, inputdf[['jjdm', new_col, new_col2]], how='left', on='jjdm')

            return outputdf

    def target_fun_brinson(self,outputdf,iteration):

        target = outputdf[['short_term_trading', 'long_term_trading', 'short_term_sector',
                         'long_term_sector', 'short_term_equity', 'long_term_equity',
                         'short_term_asset', 'long_term_asset']].sum(axis=1)

        print('iteration {}'.format(iteration))
        print("ratio of multi label is {0}, ratio of null label is {1}".format(len(target[target > 1]) / len(target),
                                                                               len(target[target == 0]) / len(target)))
        print('sum of two ratio is {}'.format(len(target[target > 1]) / len(target) + len(target[target == 0]) / len(target)))

    def classify_threshold(self,iteration_num=100):

        fin_df=self.get_brinson_data()

        fin_df=fin_df.T.sort_index(ascending=False)
        fin_df.columns=fin_df.loc['jjdm']
        fin_df.drop('jjdm',axis=0,inplace=True)


        # for iteration in range(0,iteration_num):
        #
        #     threshold=0.01*(iteration+1)
        #
        #     outputdf=self.brinson_rank(fin_df,threshold)
        #
        #     self.target_fun_brinson(outputdf, iteration)

        inputdf=self.brinson_rank(fin_df,0.1)

        print('Done')

    def classify_socring(self,asofdate):

        fin_df=self.get_brinson_data(asofdate)

        asofdate=fin_df.columns[-1].split('_')[-1]

        fin_df=fin_df.T.sort_index()
        fin_df.columns=fin_df.loc['jjdm']
        fin_df.drop('jjdm',axis=0,inplace=True)

        outputdf = pd.DataFrame()
        outputdf['jjdm'] = fin_df.columns.tolist()

        for i in range(4):
            step = int(len(fin_df) / 4)
            tempdf = fin_df.iloc[i * step:(i + 1) * step]
            inputdf = pd.DataFrame()
            inputdf['jjdm'] = tempdf.columns.tolist()


            for j in [6,12]:
                inputdf['{}month_ave_rank'.format(6 * j)] = self.rank_perc(tempdf.rolling(j).sum().T).T.mean().values
            short_term = inputdf.columns[1]
            long_term = inputdf.columns[2]

            # for j in range(1, 13):
            #     inputdf['{}month_ave_rank'.format(6 * j)] = self.rank_perc(tempdf.rolling(j).sum().T).T.mean().values
            #
            # short_term = inputdf.columns[1:7]
            # long_term = inputdf.columns[7:13]

            inputdf=inputdf[inputdf.mean(axis=1).notnull()]


            # new_col = 'short_term_{}'.format(tempdf.index[0].split('_')[0])
            # inputdf[new_col] = 10-(inputdf[short_term].mean(axis=1)*10).astype(int)
            #
            # new_col2 = 'long_term_{}'.format(tempdf.index[0].split('_')[0])
            # inputdf[new_col2] =10- (inputdf[long_term].mean(axis=1)*10).fillna(0).astype(int)


            new_col = 'short_term_{}'.format(tempdf.index[0].split('_')[0])
            inputdf[new_col] = 10-(inputdf[short_term]*10).astype(int)

            new_col2 = 'long_term_{}'.format(tempdf.index[0].split('_')[0])
            inputdf[new_col2] =10- (inputdf[long_term]*10).fillna(0).astype(int)

            outputdf = pd.merge(outputdf, inputdf[['jjdm', new_col, new_col2]], how='left', on='jjdm')

        outputdf['asofdate']=asofdate

        #check if data already exist
        sql='select distinct asofdate from brinson_score'
        date_list=pd.read_sql(sql,con=self.localengine)['asofdate'].tolist()
        if(asofdate in date_list):
            sql="delete from brinson_score where asofdate='{}'".format(asofdate)
            self.localengine.execute(sql)


        #check if data already exist
        sql="delete from brinson_score where asofdate='{0}'".format(asofdate)
        localdb.execute(sql)

        outputdf.to_sql('brinson_score',con=self.localengine,index=False,if_exists='append')

    def brinson_score_pic(self,jjdm,asofdate):

        sql="select * from brinson_score where jjdm='{0}' and asofdate='{1}'".format(jjdm,asofdate)
        scoredf=pd.read_sql(sql,con=self.localengine)
        plot=functionality.Plot(fig_width=1000,fig_height=600)

        new_name=['jjdm','交易能力_短期','交易能力_长期','行业配置能力_短期',
                  '行业配置能力_长期','选股能力_短期','选股能力_长期','大类资产配置能力_短期',
                  '大类资产配置能力_长期','asofdate']
        scoredf.columns=new_name
        col=['交易能力_短期','交易能力_长期','行业配置能力_短期',
                  '行业配置能力_长期','选股能力_短期','选股能力_长期','大类资产配置能力_短期',
                  '大类资产配置能力_长期']

        plot.ploty_polar(scoredf[col],'Brinson能力图')

    @staticmethod
    def factorlize_brinson(factor_name):

        sql="select jjdm,{0},asofdate from brinson_score".format(factor_name)
        raw_df=pd.read_sql(sql,con=localdb)
        raw_df.rename(columns={'asofdate':'date'},inplace=True)

        return  raw_df

class Barra_analysis:

    def __init__(self):
        self.localengine=db_engine.PrvFunDB().engine
        self.hbdb=db_engine.HBDB()
        self.barra_col=['size','beta','momentum','resvol','btop','sizenl','liquidity','earnyield','growth','leverage']
        self.indus_col=['aerodef','agriforest','auto','bank','builddeco','chem','conmat','commetrade','computer','conglomerates','eleceqp','electronics',
        'foodbever','health','houseapp','ironsteel','leiservice','lightindus','machiequip','media','mining','nonbankfinan','nonfermetal',
        'realestate','telecom','textile','transportation','utilities']
        chinese_name=['国防军工','农林牧渔','汽车','银行','建筑装饰','化工','建筑材料','商业贸易','计算机','综合','电气设备',
                      '电子','食品饮料','医药生物','家用电器','钢铁','休闲服务','轻工制造','机械设备','传媒','采掘','非银金融',
                      '有色金属','房地产','通信','纺织服装','交通运输','公用事业']
        self.industry_name_map=dict(zip(chinese_name,self.indus_col))

        self.industry_name_map_e2c = dict(zip(self.indus_col,chinese_name))

        self.style_trans_map=dict(zip(self.barra_col,['市值','市场','动量','波动率','价值','非线性市值','流动性','盈利','成长','杠杆',]))

        self.ability_trans=dict(zip(['stock_alpha_ret_adj', 'trading_ret', 'industry_ret_adj',
       'unexplained_ret', 'barra_ret_adj'],['股票配置','交易','行业配置','不可解释','风格配置']))

    def read_barra_fromdb(self,date_sql_con,tickerlist):

        # date_list=[''.join(x.split('-')) for x in date_list.astype(str)]
        # date_con="'"+"','".join(date_list)+"'"
        ticker_con="'"+"','".join(tickerlist)+"'"

        sql="""
        select ticker,trade_date,size,beta,momentum,resvol,btop,sizenl,liquidity,earnyield,growth,leverage,
        aerodef,agriforest,auto,bank,builddeco,chem,conmat,commetrade,computer,conglomerates,eleceqp,electronics,
        foodbever,health,houseapp,ironsteel,leiservice,lightindus,machiequip,media,mining,nonbankfinan,nonfermetal,
        realestate,telecom,textile,transportation,utilities 
        from st_ashare.r_st_barra_style_factor where trade_date in ({0}) and ticker in ({1})
        """.format(date_sql_con,ticker_con)
        expdf=self.hbdb.db2df(sql,db='alluser')

        fac_ret_df=pd.DataFrame()
        date_list=date_sql_con.split(',')
        date_list.sort()
        new_date=date_list[-1].replace("'","")
        new_date = datetime.datetime.strptime(new_date, '%Y%m%d')
        new_date = (new_date +datetime.timedelta(days=30)).strftime('%Y%m%d')
        date_list.append(new_date)
        for i in range(len(date_list)-1):
            t0=date_list[i]
            t1=date_list[i+1]
            sql="select factor_name,factor_ret,trade_date from st_ashare.r_st_barra_factor_return where trade_date>={0} and trade_date<{1} "\
                .format(t0,t1)
            temp=self.hbdb.db2df(sql,db='alluser')
            temp['factor_ret']=temp['factor_ret']+1
            temp=temp.groupby('factor_name').prod()
            temp['factor_ret'] = temp['factor_ret'] -1
            temp.reset_index(drop=False,inplace=True)
            temp['trade_date']=t0.replace("'","")
            fac_ret_df=pd.concat([fac_ret_df,temp],axis=0)


        return expdf,fac_ret_df

    def read_anon_fromdb(self,date_list,tickerlist):

        # date_list=[''.join(x.split('-')) for x in date_list.astype(str)]
        ticker_con="'"+"','".join(tickerlist)+"'"
        date_list.sort()
        outputdf=pd.DataFrame()
        for i in range(len(date_list)-1):
            t0=date_list[i]
            t1=date_list[i+1]
            sql=""" select ticker,trade_date,s_ret from st_ashare.r_st_barra_specific_return where ticker in ({0})
            and trade_date >='{1}' and trade_date<'{2}'
            """.format(ticker_con,t0,t1)

            anon_ret=self.hbdb.db2df(sql,db='alluser')
            anon_ret['s_ret']=1+anon_ret['s_ret']
            temp=anon_ret.groupby('ticker').prod()
            temp['s_ret']=temp['s_ret']-1
            temp['trade_date']=t0
            temp.reset_index(drop=False,inplace=True)
            outputdf=pd.concat([outputdf,temp],axis=0)

        return outputdf

    def read_hld_fromdb(self,start_date,end_date,jjdm):

        sql="""select jsrq,zqdm,zjbl from st_fund.t_st_gm_gpzh where jjdm='{0}' and jsrq>='{1}' and jsrq<='{2}'
        """.format(jjdm,start_date,end_date)
        hld=self.hbdb.db2df(sql,db='funduser')
        hld['jsrq']=hld['jsrq'].astype(str)
        return hld

    def smooth_hld(self,hld,date_list_orgi,weight_col,date_col,code_col):

        date_list=date_list_orgi.copy()
        smoothed_hld=pd.DataFrame()
        ext_zqdm=[]
        ext_date=[]
        ext_zjbl=[]

        for i in range(len(date_list)-1):
            q0=date_list[i]
            q1=date_list[i+1]

            sql = """
            select distinct(trade_date)
            from st_ashare.r_st_barra_style_factor where trade_date>'{0}' and trade_date<'{1}'
            """.format(q0, q1)


            ext_date_list = self.hbdb.db2df(sql, db='alluser')
            ext_date_list['yeatmonth'] = [x[0:6] for x in ext_date_list['trade_date']]


            ext_date_list.drop(ext_date_list[ext_date_list['yeatmonth']==q1[0:6]].index,axis=0,inplace=True)

            ext_date_list=ext_date_list.drop_duplicates('yeatmonth', keep='last')['trade_date'].to_list()

            tempdf=pd.merge(hld[hld[date_col]==q0].drop_duplicates([code_col],keep='first')
                            ,hld[hld[date_col]==q1].drop_duplicates([code_col],keep='first'),
                            how='outer',on=code_col).fillna(0)
            tempdf['shift_rate']=(tempdf[weight_col+'_y']-tempdf[weight_col+'_x'])/(len(ext_date_list)+1)
            zqdm=tempdf[code_col].unique().tolist()
            zq_amt=len(zqdm)
            ini_zjbl=tempdf[weight_col+'_x'].tolist()

            for j  in range(len(ext_date_list)):
                ext_date+=[ext_date_list[j]]*zq_amt
                ext_zjbl+=(np.array(ini_zjbl)+np.array((tempdf['shift_rate']*(j+1)).tolist())).tolist()
                ext_zqdm+=zqdm

        smoothed_hld[weight_col]=ext_zjbl
        smoothed_hld[date_col] = ext_date
        smoothed_hld[code_col] = ext_zqdm

        hld=pd.concat([hld,smoothed_hld],axis=0)
        return hld

    def read_hld_ind_fromdb(self,start_date,end_date,jjdm):

        sql = """select jsrq,fldm,zzjbl from st_fund.t_st_gm_gpzhhytj where jjdm='{0}' and jsrq>='{1}' and jsrq<='{2}' and hyhfbz='2'
        """.format(jjdm, start_date, end_date)
        hld = self.hbdb.db2df(sql, db='funduser')
        hld['jsrq'] = hld['jsrq'].astype(str)

        sql="select fldm,flmc from st_market.t_st_zs_hyzsdmdyb where hyhfbz='2'"
        industry_map=self.hbdb.db2df(sql,db='alluser')

        hld=pd.merge(hld,industry_map,how='left',on='fldm')
        hld.drop(hld[hld['flmc'].isnull()].index,axis=0,inplace=True)
        hld['flmc']=[ self.industry_name_map[x] for x in hld['flmc']]

        hld.loc[hld['zzjbl']==99999,'zzjbl']=0
        hld['zzjbl']=hld['zzjbl']/100

        return hld

    def read_hld_ind_fromstock(self,hld,tickerlist,hfbz=24):

        ticker_con="'"+"','".join(tickerlist)+"'"

        sql="select a.zqdm,b.yjxymc,b.xxfbrq from st_ashare.t_st_ag_zqzb a left join st_ashare.t_st_ag_gshyhfb b on a.gsdm=b.gsdm where a.zqdm in ({0}) and b.xyhfbz={1} "\
            .format(ticker_con,hfbz)
        ind_map=self.hbdb.db2df(sql,db='alluser')
        ind_map.sort_values(['zqdm','xxfbrq'],inplace=True)
        temp=ind_map['zqdm']
        temp.drop_duplicates(keep='last', inplace=True)
        ind_map=ind_map.loc[temp.index][['zqdm','yjxymc']]

        ind_hld=pd.merge(hld,ind_map,how='left',on='zqdm')

        ind_hld=ind_hld.groupby(['jsrq', 'yjxymc'], as_index=False).sum()
        ind_hld.rename(columns={'yjxymc': 'flmc', 'zjbl': 'zzjbl'}, inplace=True)
        ind_hld['fldm']=''
        ind_hld['flmc']=[self.industry_name_map[x] for x in ind_hld['flmc']]
        ind_hld['zzjbl']=ind_hld['zzjbl']/100

        return ind_hld[['fldm','zzjbl', 'jsrq','flmc']]

    def weight_times_exp(self,fund_exp,col_list):

        for col in col_list:
            fund_exp[col]=fund_exp[col]*fund_exp['zjbl']

        return  fund_exp

    def _shift_date(self,date):
        trade_dt = datetime.datetime.strptime(date, '%Y%m%d')
        pre_date = (trade_dt -datetime.timedelta(days=30)).strftime('%Y%m%d')

        sql_script = "SELECT JYRQ, SFJJ, SFYM FROM funddb.JYRL WHERE JYRQ >= {} and JYRQ <= {}".format(
            pre_date,date)
        df=self.hbdb.db2df(sql_script,db='readonly')
        df=df.rename(
            columns={"JYRQ": 'calendarDate', "SFJJ": 'isOpen',
                      "SFYM": "isMonthEnd"}).sort_values(by='calendarDate')
        df['isOpen'] = df['isOpen'].astype(int).replace({0: 1, 1: 0})
        df['isMonthEnd'] = df['isMonthEnd'].fillna(0).astype(int)

        trading_day_list = df[df['isOpen'] == 1]['calendarDate'].tolist()

        return trading_day_list[-1]

    def stock_price(self,date_sql_con,tickerlist):

        # date_list=[''.join(x.split('-')) for x in date_list.astype(str)]
        ticker_con="'"+"','".join(tickerlist)+"'"

        sql="""
        select zqmd ZQDM,jyrq JYRQ,drjj DRJJ from st_ashare.t_st_ag_gpjy where zqdn in ({0}) and jyrq in ({1})
         """.format(ticker_con,date_sql_con)

        stock_price=self.hbdb.db2df(sql,db='alluser')

        jyrq_list=stock_price['JYRQ'].unique().tolist()
        jyrq_list.sort()
        right_df=pd.DataFrame()
        for i in range(0,len(jyrq_list)-1):
            tempdf=pd.merge(stock_price[stock_price['JYRQ']==jyrq_list[i]][['ZQDM','JYRQ','DRJJ']]
                            ,stock_price[stock_price['JYRQ']==jyrq_list[i+1]][['ZQDM','DRJJ']]
                            ,how='inner',on='ZQDM')
            tempdf['hld_ret']=tempdf['DRJJ_y']/tempdf['DRJJ_x']-1
            right_df=pd.concat([right_df,tempdf[['ZQDM','JYRQ','hld_ret']]])

        #stock_price['hld_ret']=stock_price['SPJG']/stock_price['QSPJ']-1
        stock_price=pd.merge(stock_price,right_df,how='left',on=['ZQDM','JYRQ'])

        return stock_price

    @staticmethod
    def hld_compenzation(hlddf,fund_allocation):

        q_date=hlddf.loc[[(x[4:6] == '03') | (x[4:6] == '09') for x in hlddf['jsrq']]]['jsrq'].unique().tolist()
        a_date=hlddf.loc[[(x[4:6] == '06') | (x[4:6] == '12') for x in hlddf['jsrq']]]['jsrq'].unique().tolist()
        q_list=hlddf['jsrq'].unique().tolist()
        q_list.sort()

        hld_H=pd.DataFrame()
        hld_L = pd.DataFrame()
        #get heavy hld for annual and half_annual report
        for date in a_date:
            hld_H=pd.concat([hld_H,hlddf[hlddf['jsrq']==date].sort_values('zjbl')[-10:].reset_index(drop=True)],axis=0)
            hld_L=pd.concat([hld_L,hlddf[hlddf['jsrq']==date].sort_values('zjbl')[0:-10].reset_index(drop=True)],axis=0)
        for date in q_date:
            hld_H=pd.concat([hld_H,hlddf[hlddf['jsrq']==date]],axis=0)


        for i in range(len(q_list)):
            t1=q_list[i]
            if((i>0) and (t1[4:6] == '03') or  (t1[4:6] == '09')):
                t0=q_list[i-1]
            else:
                continue
            #calculate the no hevay hld for quarter report data by the mean of two annaul data if next annaul report exists
            if(i!=len(q_list)-1):
                t2=q_list[i+1]
                temp=pd.merge(hlddf[hlddf['jsrq']==t0].sort_values('zjbl')[0:-10],
                              hlddf[hlddf['jsrq']==t2].sort_values('zjbl')[0:-10],
                              how='outer',on='zqdm').fillna(0)
                temp.set_index('zqdm',inplace=True)
                if(len(temp)==0):
                    continue
                drop_list=list(set(temp.index).intersection( set(hlddf[hlddf['jsrq']==t1]['zqdm'])))
                temp.drop(drop_list,axis=0,inplace=True)
                temp['zjbl']=(temp['zjbl_x']+temp['zjbl_y'])/2
                temp['zjbl']=temp['zjbl']*((fund_allocation[fund_allocation['jsrq'] == t1]['gptzzjb']*100-hld_H[hld_H['jsrq']==t1]['zjbl'].sum()).values[0]/temp['zjbl'].sum())
                temp['jsrq']=t1
                temp.reset_index(drop=False,inplace=True)
                hld_L=pd.concat([hld_L,temp[['zjbl','jsrq','zqdm']]],axis=0)

            else:
                temp=hlddf[hlddf['jsrq']==t0].sort_values('zjbl')[0:-10]
                temp['zjbl']=temp['zjbl']/temp['zjbl'].sum()
                temp['zjbl']=temp['zjbl']*(fund_allocation[fund_allocation['jsrq'] == t1]['gptzzjb']*100-hld_H[hld_H['jsrq']==t1]['zjbl'].sum()).values[0]
                temp['jsrq']=t1
                temp.reset_index(drop=False,inplace=True)
                hld_L=pd.concat([hld_L,temp[['zjbl','jsrq','zqdm']]],axis=0)
        return pd.concat([hld_H,hld_L],axis=0).sort_values('jsrq').reset_index(drop=True)

    def save_barra_ret2db(self,jjdm,start_date,end_date,add=False,hld_compenzation=False):

        #read holding info
        hld=self.read_hld_fromdb(start_date,end_date,jjdm)
        #remove HK stock
        tickerlist=hld['zqdm'][~hld['zqdm'].dropna().str.contains('H')].unique()
        #shift the report date to trading date
        org_date_list=hld['jsrq'].unique().tolist()
        date_list = [self._shift_date(x) for x in org_date_list]
        date_map=dict(zip(org_date_list,date_list))
        changed_date=set(org_date_list).difference(set(date_list))

        #get fund asset allocation info
        fund_allocation = self.fund_asset_allocation(jjdm, org_date_list)

        #hld compenzation if necessary
        if(hld_compenzation):
            hld = self.hld_compenzation(hld,fund_allocation)
            table_sur='barra_style_hldcom_'
            hld_industry = self.read_hld_ind_fromstock(hld,tickerlist)
        else:
            table_sur='barra_style_'
            hld_industry = self.read_hld_ind_fromdb(start_date, end_date, jjdm)

        #transfor report date to trading date
        for date in changed_date:
            hld.loc[hld['jsrq']==date,'jsrq']=date_map[date]
            hld_industry.loc[hld_industry['jsrq'] == date, 'jsrq'] = date_map[date]
            fund_allocation.loc[fund_allocation['jsrq'] == date, 'jsrq'] = date_map[date]

        #hld smoothing
        hld=self.smooth_hld(hld,date_list,weight_col='zjbl',date_col='jsrq',code_col='zqdm')
        hld_industry=self.smooth_hld(hld_industry[['zzjbl','jsrq','flmc']],date_list,weight_col='zzjbl',date_col='jsrq',code_col='flmc')
        fund_allocation = self.smooth_hld(fund_allocation, date_list, weight_col='gptzzjb', date_col='jsrq',
                                          code_col='jjdm')
        date_sql_con="'"+"','".join(hld['jsrq'].unique().tolist())+"'"

        #read barra exposure and return info
        expdf, fac_ret_df=self.read_barra_fromdb(date_sql_con,tickerlist)
        #read the stock price for each
        stock_df = self.stock_price(date_sql_con, tickerlist)
        #read the special return for each stock
        anno_df=self.read_anon_fromdb(hld['jsrq'].unique().tolist(),tickerlist)

        fund_exp=pd.merge(hld,expdf[['ticker','trade_date']+self.barra_col],
                          how='inner',left_on=['zqdm','jsrq'],
                          right_on=['ticker','trade_date']).drop(['ticker', 'trade_date'],axis=1)

        fund_exp=pd.merge(fund_exp, stock_df[['ZQDM', 'JYRQ', 'hld_ret']], how='inner', left_on=['zqdm', 'jsrq'],
                 right_on=['ZQDM', 'JYRQ']).drop(['ZQDM','JYRQ'],axis=1)

        fund_exp=pd.merge(fund_exp, anno_df, how='left', left_on=['zqdm', 'jsrq'],
                 right_on=['ticker', 'trade_date']).drop(['ticker', 'trade_date'],axis=1)

        fund_exp=self.weight_times_exp(fund_exp,self.barra_col+['hld_ret','s_ret'])

        fund_exp.drop(['zqdm'],axis=1,inplace=True)

        fund_exp=fund_exp.groupby(by='jsrq').sum()/100

        hld_ret=fund_exp[['zjbl','hld_ret']]
        s_ret=fund_exp[['zjbl','s_ret']]

        fund_exp.drop(['hld_ret','s_ret'],axis=1,inplace=True)
        fund_exp=fund_exp.T

        indus_exp = pd.DataFrame()
        indus_exp['industry'] = self.indus_col

        for date in hld_industry['jsrq'].unique():
            indus_exp=pd.merge(indus_exp,hld_industry[hld_industry['jsrq']==date][['zzjbl','flmc','jsrq']]
                               ,how='left',left_on='industry',right_on='flmc').drop(['flmc','jsrq'],axis=1).fillna(0)
            indus_exp.rename(columns={'zzjbl':date},inplace=True)

        for date in fac_ret_df['trade_date'].unique():

            tempdf=fac_ret_df[fac_ret_df['trade_date']==date][['factor_ret','factor_name']].T
            tempdf.columns = [x.lower() for x in  tempdf.loc['factor_name']]

            # indus_exp=pd.merge(indus_exp,hld_industry[hld_industry['jsrq']==date][['zzjbl','flmc','jsrq']]
            #                    ,how='left',left_on='industry',right_on='flmc').drop(['flmc','jsrq'],axis=1).fillna(0)
            # indus_exp.rename(columns={'zzjbl':date},inplace=True)
            fund_exp[date+'_ret']=fund_exp[date].values*np.append([1],tempdf[self.barra_col].loc['factor_ret'].values)
            indus_exp[date+'_ret']=indus_exp[date].values*tempdf[self.indus_col].loc['factor_ret'].values

        fund_exp=fund_exp.T
        indus_exp.set_index(['industry'], inplace=True)
        indus_exp=indus_exp.T

        fund_exp['total_bar']=fund_exp[self.barra_col].sum(axis=1)
        indus_exp['total_ind'] = indus_exp[self.indus_col].sum(axis=1)

        fund_exp['index']=fund_exp.index
        indus_exp['index'] = indus_exp.index
        fund_exp['jjrq']=[x.split('_')[0] for x in fund_exp['index']]
        indus_exp['jjrq'] = [x.split('_')[0] for x in indus_exp['index']]
        hld_ret['jjrq'] = hld_ret.index
        s_ret['jjrq'] = s_ret.index
        for df in [fund_exp,indus_exp,hld_ret,s_ret]:
            df['jjdm']=jjdm

        fund_allocation=pd.merge(s_ret['jjrq'],fund_allocation,how='left',left_on='jjrq',
                                 right_on='jsrq').drop('jjrq',axis=1)

        if(not add):
            sql="select distinct jjrq from {1}hld_ret where jjdm='{0}'".format(jjdm,table_sur)
            date_list=pd.read_sql(sql,con=self.localengine)['jjrq']
            common_date=list(set(date_list).intersection(set(fund_allocation['jsrq'] )))
            date_con="'"+"','".join(common_date)+"'"

            sql="delete from {2}fund_exp where jjdm='{0}' and jjrq in ({1})".format(jjdm,date_con,table_sur)
            self.localengine.execute(sql)
            sql="delete from {2}indus_exp where jjdm='{0}' and jjrq in ({1})".format(jjdm,date_con,table_sur)
            self.localengine.execute(sql)
            sql="delete from {2}hld_ret where jjdm='{0}' and jjrq in ({1})".format(jjdm,date_con,table_sur)
            self.localengine.execute(sql)
            sql="delete from {2}s_ret where jjdm='{0}' and jjrq in ({1})".format(jjdm,date_con,table_sur)
            self.localengine.execute(sql)
            sql = "delete from {2}fund_allocation where jjdm='{0}' and jsrq in ({1})".format(jjdm, date_con,table_sur)
            self.localengine.execute(sql)

        fund_exp.to_sql(table_sur+'fund_exp',con=self.localengine,index=False,if_exists='append')
        indus_exp.to_sql(table_sur+'indus_exp', con=self.localengine,index=False,if_exists='append')
        hld_ret.to_sql(table_sur+'hld_ret', con=self.localengine,index=False,if_exists='append')
        s_ret.to_sql(table_sur+'s_ret', con=self.localengine,index=False,if_exists='append')
        fund_allocation.to_sql(table_sur+'fund_allocation', con=self.localengine,index=False,if_exists='append')

        #print('{0} data for {1} to {2} has been saved in local db'.format(jjdm,start_date,end_date))

    def read_barra_retfromdb(self,jjdm,start_date,end_date,hld_com):

        if(hld_com):
            surname='barra_style_hldcom_'
        else:
            surname='barra_style_'

        sql="select * from {3}fund_exp where jjdm='{0}' and jjrq>='{1}' and jjrq<='{2}'"\
            .format(jjdm,start_date,end_date,surname)
        fund_exp=pd.read_sql(sql,con=self.localengine).drop(['jjdm','jjrq'],axis=1)
        fund_exp.set_index('index',drop=True,inplace=True)

        sql="select * from {3}indus_exp where jjdm='{0}' and jjrq>='{1}' and jjrq<='{2}'"\
            .format(jjdm,start_date,end_date,surname)
        indus_exp=pd.read_sql(sql,con=self.localengine).drop(['jjdm','jjrq'],axis=1)
        indus_exp.set_index('index', drop=True,inplace=True)

        sql="select * from {3}hld_ret where jjdm='{0}' and jjrq>='{1}' and jjrq<='{2}'"\
            .format(jjdm,start_date,end_date,surname)
        hld_ret=pd.read_sql(sql,con=self.localengine).drop(['jjdm'],axis=1)
        hld_ret.set_index('jjrq', drop=True,inplace=True)

        sql="select * from {3}s_ret where jjdm='{0}' and jjrq>='{1}' and jjrq<='{2}'"\
            .format(jjdm,start_date,end_date,surname)
        s_ret=pd.read_sql(sql,con=self.localengine).drop(['jjdm'],axis=1)
        s_ret.set_index('jjrq', drop=True,inplace=True)

        sql="select * from {3}fund_allocation where jjdm='{0}' and jsrq>='{1}' and jsrq<='{2}'"\
            .format(jjdm,start_date,end_date,surname)
        fund_allocation=pd.read_sql(sql,con=self.localengine).drop(['jjdm'],axis=1)

        sql="""select jsrq from st_fund.t_st_gm_gpzh where jjdm='{0}' and jsrq>='{1}' and jsrq<='{2}'
        """.format(jjdm,start_date,end_date)
        hld=self.hbdb.db2df(sql,db='funduser')
        hld['jsrq']=hld['jsrq'].astype(str)

        date_list=hld['jsrq'].unique().tolist()

        return fund_exp, indus_exp, hld_ret, s_ret, date_list,fund_allocation

    def fund_nv(self,jjdm,date_list):

        date_con="'"+"','".join(date_list)+"'"

        sql="""
        select jzrq,zbnp from st_fund.t_st_gm_rqjhb where jjdm='{0}' and zblb='2101'
        and jzrq in ({1})
        """.format(jjdm,date_con)

        fundnv=self.hbdb.db2df(sql,db='funduser')
        fundnv.rename(columns={'zbnp':'hbdr'},inplace=True)
        fundnv['jzrq']=fundnv['jzrq'].astype(str)
        fundnv['hbdr']=fundnv['hbdr']/100

        return fundnv

    def fund_asset_allocation(self,jjdm,date_list):

        sql="select jjdm,jsrq,jjzzc,gptzzjb from st_fund.t_st_gm_zcpz where jjdm='{2}' and jsrq>='{0}' and jsrq<='{1}'"\
            .format(date_list[0],date_list[-1],jjdm)
        fund_allocation=self.hbdb.db2df(sql,db='funduser')
        fund_allocation['gptzzjb']=fund_allocation['gptzzjb']/100
        fund_allocation['jsrq']=fund_allocation['jsrq'].astype(str)
        return fund_allocation

    def ret_div(self,jjdm,start_date,end_date,hld_com):

        fund_exp,indus_exp,hld_ret,s_ret,date_list,fund_allocation=self.read_barra_retfromdb(jjdm,start_date,end_date,hld_com)

        fundnv=self.fund_nv(jjdm,hld_ret.index.tolist())
        hld_ret['jzrq']=hld_ret.index
        hld_ret=pd.merge(hld_ret,fundnv,how='left',on='jzrq')

        barra_ret=fund_exp.loc[[x+'_ret' for x in hld_ret['jzrq'][0:-1]]][self.barra_col+['total_bar']].reset_index(drop=True)
        barra_exp=fund_exp.loc[hld_ret['jzrq']][self.barra_col+['total_bar']].reset_index(drop=True)
        barra_exp.columns=[x+'_exp' for x in barra_exp.columns]

        ind_ret = indus_exp.loc[[x + '_ret' for x in hld_ret['jzrq'][0:-1]]].reset_index(
            drop=True)
        ind_exp = indus_exp.loc[hld_ret['jzrq']].reset_index(drop=True)
        ind_exp.columns = [x + '_exp' for x in ind_exp.columns]

        s_ret=s_ret['s_ret'].reset_index(drop=True)
        ouputdf=pd.concat([hld_ret,barra_ret,barra_exp,ind_ret,ind_exp,s_ret],axis=1)

        columns=['zjbl', 'hld_ret', 'jzrq', 'hbdr', 'total_bar', 'total_bar_exp', 's_ret','total_ind']

        new_names=['published_stock_weight','hld_based_ret','date','nv_ret','barra_ret','barra_exp','stock_alpha_ret','industry_ret']

        ouputdf.rename(columns=dict(zip(columns,new_names)),inplace=True)

        ouputdf=pd.merge(ouputdf,fund_allocation,how='left',left_on='date',right_on='jsrq').drop('jsrq',axis=1)

        for col in self.barra_col+self.indus_col:
            ouputdf[col+"_adj"]=ouputdf[col]/ouputdf['published_stock_weight']*ouputdf['gptzzjb']
            ouputdf[col + "_exp_adj"] = ouputdf[col+"_exp"] / ouputdf['published_stock_weight'] * ouputdf['gptzzjb']

        ouputdf.set_index('date',drop=True,inplace=True)

        return  ouputdf,date_list

    def date_trans(self,date_list,inputlist):

        missing_date=set(inputlist).difference(set(date_list))
        available_list=list(set(inputlist).difference(set(missing_date)))
        new_list = []
        if(len(missing_date)>0):
            for date in missing_date:
                diff=abs(date_list.astype(int)-int(date)).min()
                new_list.append(date_list[abs(date_list.astype(int)-int(date))==diff][0])
        available_list+=new_list
        available_list.sort()
        return  available_list

    def cul_ret(self,weight,ret):

        cul_ret=1
        for i in range(len(weight)):
            cul_ret*=weight[i]*(ret[i]+1)

        return cul_ret

    def style_change_detect_engine(self,q_df,diff1,diff2,q_list,col_list,t1,t2):

        style_change=[]

        for col in col_list:

            potential_date=diff2[diff2[col]<=-1*t1].index.to_list()
            last_added_date=q_list[-1]
            for date in potential_date:
                if(diff1.loc[q_df.index[q_df.index<=date][-3]][col]<=-1*t2):
                    added_date=q_df.index[q_df.index<=date][-3]
                elif(diff1.loc[q_df.index[q_df.index<=date][-2]][col]<=-1*t2):
                    added_date=q_df.index[q_df.index<=date][-2]
                elif(diff1.loc[q_df.index[q_df.index<=date][-1]][col]<=-1*t2):
                    added_date = q_df.index[q_df.index <= date][-1]
                else:
                    added_date = q_df.index[q_df.index <= date][-3]

                if((q_list.index(added_date)-q_list.index(last_added_date)<=2
                        and q_list.index(added_date)-q_list.index(last_added_date)>0) or added_date==q_list[-1]):
                    continue
                else:
                    style_change.append(added_date + "@" + col)
                    last_added_date = added_date

            potential_date = diff2[diff2[col] >= t1].index.to_list()
            last_added_date = q_list[-1]
            for date in potential_date:
                if (diff1.loc[q_df.index[q_df.index <= date][-3]][col] >= t2):
                    added_date = q_df.index[q_df.index <= date][-3]
                elif (diff1.loc[q_df.index[q_df.index <= date][-2]][col] >= t2):
                    added_date = q_df.index[q_df.index <= date][-2]
                elif (diff1.loc[q_df.index[q_df.index <= date][-1]][col] >= t2):
                    added_date = q_df.index[q_df.index <= date][-1]
                else:
                    added_date = q_df.index[q_df.index <= date][-3]

                if (q_list.index(added_date) - q_list.index(last_added_date) <= 2
                        and q_list.index(added_date) - q_list.index(last_added_date) > 0):
                    continue
                else:
                    style_change.append(added_date + "@" + col)
                    last_added_date = added_date

        return style_change

    def style_change_detect_engine2(self, q_df, diff1, col_list, t1, t2):

        style_change=[]
        t3=t2/2

        for col in col_list:

            tempdf=pd.merge(q_df[col],diff1[col],how='left',on='date')
            tempdf['style']=''
            style_num=0
            tempdf['style'].iloc[0:2] = style_num

            for i in range(2,len(tempdf)-1):
                if(tempdf[col+'_y'].iloc[i]>t1 and tempdf[col+'_y'].iloc[i+1]>-1*t3 ):
                    style_num+=1
                    added_date = tempdf.index[i]
                    style_change.append(added_date + "@" + col)
                elif(tempdf[col+'_x'].iloc[i]-tempdf[tempdf['style']==style_num][col+'_x'][0]>t1 and
                     tempdf[col+'_y'].iloc[i]>t2 and tempdf[col+'_y'].iloc[i+1]>-1*t3):
                    style_num += 1
                    added_date=tempdf.index[i]
                    style_change.append(added_date + "@" + col)
                elif(tempdf[col+'_y'].iloc[i]<-1*t1 and tempdf[col+'_y'].iloc[i+1]<t3 ):
                    style_num += 1
                    added_date = tempdf.index[i]
                    style_change.append(added_date + "@" + col)
                elif (tempdf[col + '_x'].iloc[i] - tempdf[tempdf['style'] == style_num][col + '_x'][0] < -1*t1 and
                      tempdf[col + '_y'].iloc[i] < -1*t2 and tempdf[col + '_y'].iloc[i + 1] <  t3):
                    style_num += 1
                    added_date = tempdf.index[i]
                    style_change.append(added_date + "@" + col)

                tempdf['style'].iloc[i] = style_num

        return style_change

    def style_change_detect(self,df,q_list,col_list,t1,t2):

        q_list.sort()
        q_df = df.loc[q_list]
        diff1=q_df.diff(1)
        # diff2=q_df.rolling(3).mean().diff(2)
        # diff4 = q_df.rolling(3).mean().diff(4)

        # style_change_short=self.style_change_detect_engine(q_df,diff1,diff2,q_list,col_list,t1,t2)
        # style_change_long=self.style_change_detect_engine(q_df,diff1,diff4,q_list,col_list,t1,t2)
        # style_change=style_change_short+style_change_long

        style_change = self.style_change_detect_engine2(q_df, diff1, col_list, t1, t2)

        return list(set(style_change)),np.array(q_list)

    def shifting_expression(self,change_ret,name,jjdm,style='Total'):

        change_winning_pro = sum(change_ret[2]) / len(change_ret)
        left_ratio = sum(change_ret[0]) / len(change_ret)
        right_ratio = 1-left_ratio
        one_q_ret = change_ret[3].mean()
        hid_q_ret = change_ret[4].mean()

        return  np.array([style.split('_')[0],len(change_ret),change_winning_pro,one_q_ret,hid_q_ret,left_ratio,right_ratio])

    def style_change_ret(self,df,q_list,col_list,t1,t2):

        style_change,q_list = self.style_change_detect(df,q_list,col_list,t1,t2)
        change_count = len(style_change)
        style_changedf=pd.DataFrame()
        style_changedf['date']=[x.split('@')[0] for x in style_change]
        style_changedf['style']=[x.split('@')[1] for x in style_change]
        style_changedf.sort_values('date',inplace=True,ascending=False)
        style_chang_extret=dict(zip(style_change,style_change))

        if(len(df.columns)>20):
            def get_factor_return(q_list, first_change_date, style):

                sql="select fldm,flmc,zsdm from st_market.t_st_zs_hyzsdmdyb where hyhfbz='2' and fljb='1' "
                industry_index_code=hbdb.db2df(sql,db='alluser')
                industry_index_code['name_eng']=[self.industry_name_map[x] for x in industry_index_code['flmc']]

                sql="select zqdm,jyrq,spjg from st_market.t_st_zs_hqql where zqdm='{0}' and jyrq>='{1}' and  jyrq<='{2}'  "\
                    .format(industry_index_code[industry_index_code['name_eng']==style.split('_')[0]]['zsdm'].iloc[0],
                            q_list[q_list < first_change_date][-2],q_list[-1])
                fac_ret_df=hbdb.db2df(sql, db='alluser')
                fac_ret_df['jyrq']=fac_ret_df['jyrq'].astype(str)
                fac_ret_df.set_index('jyrq', drop=True, inplace=True)

                fac_ret_df['price'] = fac_ret_df['spjg']

                return fac_ret_df
            def q_ret(fac_ret_df,q0,q1,time_length=1):
                res=np.power(fac_ret_df.loc[q1]['price']/fac_ret_df.loc[q0]['price'],1/time_length)-1
                return  res
        else:
            def get_factor_return(q_list,first_change_date,style):
                sql = "select factor_ret,trade_date from st_ashare.r_st_barra_factor_return where trade_date>='{0}' and UPPER(factor_name)='{1}' and trade_date<='{2}'" \
                    .format(q_list[q_list<first_change_date][-2], style.split('_')[0].upper(),q_list[-1])
                fac_ret_df = self.hbdb.db2df(sql, db='alluser')
                fac_ret_df.set_index('trade_date', drop=True, inplace=True)
                fac_ret_df['factor_ret_adj'] = fac_ret_df['factor_ret'] + 1
                fac_ret_df['price']=fac_ret_df.rolling(len(fac_ret_df), 1)['factor_ret_adj'].apply(np.prod, raw=True)

                return  fac_ret_df
            def q_ret(fac_ret_df,q0,q1,time_length=1):
                ret=np.power(fac_ret_df['factor_ret_adj'].loc[q0:q1].prod(),
                                         1/time_length)-1
                return  ret

        if(change_count>0):
            for style in style_changedf['style']:

                changedf=style_changedf[style_changedf['style']==style]
                changedf=changedf.sort_values('date')
                first_change_date=changedf['date'].values[0]
                fac_ret_df=get_factor_return(q_list,first_change_date,style)


                for i in range(len(changedf)):
                    date=changedf.iloc[i]['date']

                    observer_term=np.append(q_list[q_list<date][-2:],q_list[(q_list>=date)][0:2])

                    new_exp=df[style].loc[observer_term[2]]
                    old_exp=df[style].loc[observer_term[1]]

                    q0=observer_term[0]
                    q1=observer_term[1]
                    old_ret=q_ret(fac_ret_df,q0,q1)


                    q0=observer_term[1]
                    q1=observer_term[2]
                    current_ret=q_ret(fac_ret_df,q0,q1)
                    if_left=fac_ret_df['price'].loc[q0:q1].mean()>fac_ret_df['price'].loc[q1]

                    q0=observer_term[2]
                    q1=observer_term[3]
                    next_ret=q_ret(fac_ret_df,q0,q1)


                    if (i != len(changedf) - 1):
                        q1 = changedf.iloc[i + 1]['date']
                        q2 = q1
                    else:
                        q1 = q_list[-1]
                        q2=fac_ret_df.index[-1]

                    change_date=date
                    time_length = q_list.tolist().index(q1) - q_list.tolist().index(change_date)
                    holding_ret=q_ret(fac_ret_df,q0,q2,time_length=time_length)

                    if_win_next=(new_exp>old_exp)&(next_ret>current_ret)
                    if_win_hld=(new_exp>old_exp)&(holding_ret>current_ret)

                    shift_retur_next= (new_exp-old_exp)*(next_ret-current_ret)
                    shift_retur_hld = (new_exp - old_exp) * (holding_ret - current_ret)

                    style_chang_extret[date+"@"+style]=[if_left,if_win_next,if_win_hld,shift_retur_next,shift_retur_hld]

        return style_chang_extret

    def style_shifting_analysis(self,df,q_list,col_list,t1,t2,name,jjdm):

        # col_list=[x+"_exp_adj" for x in col]
        change_ret=self.style_change_ret(df,q_list,col_list,t1=t1,t2=t2)
        change_ret = pd.DataFrame.from_dict(change_ret).T
        change_ret['style'] = list([x.split('@')[1] for x in change_ret.index])
        change_ret['date'] = list([x.split('@')[0] for x in change_ret.index])

        data=[]

        if(len(change_ret)>0):
            data.append(self.shifting_expression(change_ret,name,jjdm))
            for style in change_ret['style'].unique():
                tempdf=change_ret[change_ret['style']==style]
                data.append(self.shifting_expression(tempdf,name,jjdm,style))

        shift_df = pd.DataFrame(data=data,columns=['风格类型','切换次数','胜率','下季平均收益','持有平均收益','左侧比率','右侧比例'])

        for col in ['胜率','下季平均收益','持有平均收益','左侧比率','右侧比例']:
            shift_df[col] = shift_df[col].astype(float).map("{:.2%}".format)

        return  shift_df

    def style_label_engine(self,desc,style_stable_list,exp1,exp2,exp3,map_dict):

        style_lable=[]

        for style in style_stable_list:
            if(abs(desc[style]['mean'])>=exp2 and abs(desc[style]['mean'])<exp1):
                label="稳定偏好{}".format("较@"+map_dict[style.split('_')[0]])
            elif(abs(desc[style]['mean'])>=exp1):
                label="稳定偏好{}".format("@"+map_dict[style.split('_')[0]])
            elif(abs(desc[style]['mean'])<=exp3):
                label = "规避{}暴露".format(map_dict[style.split('_')[0]])
            else:
                continue
            if(desc[style]['mean'])<0:
                label=label.replace('@','低')
            else:
                label=label.replace('@','高')
            style_lable.append(label)

        return style_lable

    def style_label_generator(self,df,style_shift_df,ind_shift_df,average_a_w,hld_com):

        style_noshift_col=list(set(self.barra_col).difference(set(style_shift_df.iloc[1:]['风格类型'])))
        ind_noshift_col=list(set(self.indus_col).difference(set(ind_shift_df.iloc[1:]['风格类型'])))

        if(len(style_noshift_col)>0):
            if (hld_com):
                desc=df[[x+"_exp" for x in style_noshift_col]].describe()
            else:
                desc=df[[x+"_exp_adj" for x in style_noshift_col]].describe()

            style_stable_list=desc.columns[((desc.loc['max'] - desc.loc['min']) < 0.5*average_a_w).values].tolist()
            style_lable = self.style_label_engine(desc, style_stable_list,0.75*average_a_w,0.5*average_a_w,0.25*average_a_w,self.style_trans_map)
        else:
            style_lable=[]


        if(len(ind_noshift_col)>0):
            if (hld_com):
                desc=df[[x+"_exp" for x in ind_noshift_col]].describe()
            else:
                desc=df[[x+"_exp_adj" for x in ind_noshift_col]].describe()

            ind_stable_list=desc.columns[((desc.loc['max'] - desc.loc['min']) < 0.1*average_a_w).values].tolist()
            ind_lable = self.style_label_engine(desc, ind_stable_list,0.2*average_a_w,0.1*average_a_w,0.05*average_a_w,self.industry_name_map_e2c)
        else:
            ind_lable=[]

        return style_lable+ind_lable

    def ret_analysis(self,df,a_list,hld_com):

        ret_col_list = ['hld_based_ret', 'barra_ret', 'stock_alpha_ret', 'industry_ret']

        if(hld_com):
            for col in ret_col_list:
                df[col + '_adj'] = np.append([np.nan], df[col][0:-1])
        else:
            for col in ret_col_list:
                df[col+'_adj']=df[col]/df['published_stock_weight']*df['gptzzjb']
                df[col+'_adj'] = np.append([np.nan], df[col+'_adj'][0:-1])

        df = df[[x + '_adj' for x in ret_col_list] + ['nv_ret']]

        df['unexplained_ret'] = df['hld_based_ret_adj'] - (
                    df['barra_ret_adj'] + df['industry_ret_adj'] + df['stock_alpha_ret_adj'])
        df['trading_ret'] =df['nv_ret']- df['hld_based_ret_adj']

        ability_label = []
        for col in ['barra_ret_adj','industry_ret_adj','stock_alpha_ret_adj','unexplained_ret']:
            temp=(df[col]/df['hld_based_ret_adj']).describe()
            # print(col)
            # print(temp['50%'])
            # print(temp['std'])
            if(abs(temp['50%'])>0.35):
                if(temp.std()/temp.mean()<=1):
                    ext = '稳定'
                else:
                    ext = ''
                if(temp['50%']>0):
                    ext2='良好的'
                else:
                    ext2 = '糟糕的'
                ability_label.append(ext+ext2 + self.ability_trans[col] + "能力")

        temp=(df['trading_ret']/df['nv_ret']).describe()

        if(abs(temp['50%'])>0.5):
            if(temp.std()/temp.mean()<=1):
                ext = '稳定'
            else:
                ext = ''
            if(temp['50%']>0):
                ext2='良好的'
            else:
                ext2 = '糟糕的'
            ability_label.append(ext+ext2 + self.ability_trans[col] + "能力")

        return ability_label

    def exp_analysis(self,df,q_list,jjdm,average_a_w,hld_com):

        if(hld_com):
            style_shift_df = self.style_shifting_analysis(
                df[[x + "_exp" for x in self.barra_col] + [x for x in self.barra_col]].astype(float),
                q_list,[x + "_exp" for x in self.barra_col],
                t1=0.5 * average_a_w, t2=0.2 * average_a_w, name='barra style', jjdm=jjdm)

            ind_shift_df = self.style_shifting_analysis(
                df[[x + "_exp" for x in self.indus_col] + [x  for x in self.indus_col]].astype(float),
                q_list,[x + "_exp" for x in self.indus_col],
                t1=0.1 * average_a_w, t2=0.075 * average_a_w, name='industry', jjdm=jjdm)

        else:

            style_shift_df=self.style_shifting_analysis(
                df[[x+"_exp_adj" for x in self.barra_col]+[x+"_adj" for x in self.barra_col]].astype(float)
                ,q_list,[x+"_exp_adj" for x in self.barra_col],t1=0.3*average_a_w,
                t2=0.15*average_a_w,name='barra style',jjdm=jjdm)

            ind_shift_df=self.style_shifting_analysis(
                df[[x + "_exp_adj" for x in self.indus_col]+[x+"_adj" for x in self.indus_col]].astype(float),
                q_list,[x+"_exp_adj" for x in self.indus_col], t1=0.1*average_a_w,
                t2=0.075*average_a_w, name='industry',jjdm=jjdm)

        style_lable = self.style_label_generator(df,style_shift_df,ind_shift_df,average_a_w,hld_com)

        return  style_shift_df,ind_shift_df,style_lable

    def centralization_level(self,df,num1=3,num2=5):

        outputdf=pd.DataFrame(index=df.index,columns=['c_level'])

        for i in range(len(df)):
            outputdf.iloc[i]['c_level']=(df.iloc[i].sort_values()[-1*num1:].sum()+df.iloc[i].sort_values()[-1*num2:].sum())/2/df.iloc[i].sum()

        return outputdf.mean()[0]

    @staticmethod
    def ind_shift_rate(indf):
        indf.sort_index(inplace=True)
        indus_col=indf.columns.tolist()
        indus_col.remove('jjzzc')
        for col in indus_col:
            indf[col+'_mkt']=indf[col]*indf['jjzzc']
        diff=indf[[x+'_mkt' for x in indus_col]].diff(1)
        diff['jjzzc']=indf[[x+'_mkt' for x in indus_col]].sum(axis=1)
        diff['jjzzc']=diff['jjzzc'].rolling(2).mean()
        shift_ratio=diff[[x+'_mkt' for x in indus_col]].abs().sum(axis=1)/2/diff['jjzzc']
        return shift_ratio.describe()

    def ind_analysis(self,df,hld_com):

        q_date=df.loc[[(x[4:6] == '03') | (x[4:6] == '09') for x in df.index]].index
        a_date=df.loc[[(x[4:6] == '06') | (x[4:6] == '12') for x in df.index]].index
        q_list=q_date.to_list()+a_date.to_list()

        if(not hld_com):
            #calculate the ratio between quarter report stock weigth and annual report stock weight
            average_q_w=(df.loc[q_date]['published_stock_weight']).mean()
            average_a_w=(df.loc[a_date]['published_stock_weight']).mean()
            shift_confidence=average_q_w/average_a_w

            # calculate the average industry exp num
            inddf = df[[x + '_exp_adj' for x in self.indus_col]].loc[q_list]
            average_ind_num = (inddf.loc[a_date] > 0).sum(axis=1).mean()
            adj_average_ind_num = ((inddf > 0).sum(axis=1) * df.loc[q_list][
                'published_stock_weight']).mean() / average_a_w

            # calculate the industry holding centralization_level
            average_ind_cen_level = self.centralization_level(inddf.loc[a_date])

            # calculate the industry holding shift ratio
            shift_ratio = self.ind_shift_rate(df[[x + '_exp' for x in self.indus_col] + ['jjzzc']].loc[a_date])

            # the 50,75,25 for c is 0.0.617,0.712,0.0.55
            # the 50,75,25 for r is 0.288,0.343,0.235
            if (average_ind_cen_level > 0.617 and shift_ratio['mean'] > 0.288):
                ind_label = '行业博弈型'
            elif (average_ind_cen_level > 0.617 and shift_ratio['mean'] < 0.288):
                ind_label = '行业专注型'
            elif (average_ind_cen_level < 0.617 and shift_ratio['mean'] > 0.288):
                ind_label = '行业轮动型'
            elif (average_ind_cen_level < 0.617 and shift_ratio['mean'] < 0.288):
                ind_label = '行业配置型'
            else:
                ind_label = ''

            a_date=a_date.tolist()

        else:
            shift_confidence=1
            inddf = df[[x + '_exp' for x in self.indus_col]]

            average_q_w = (df.loc[q_date]['published_stock_weight']).mean()
            average_a_w = (df.loc[a_date]['published_stock_weight']).mean()

            # calculate the average industry exp num
            average_ind_num = (inddf.loc[q_list] > 0).sum(axis=1).mean()

            # calculate the industry holding centralization_level
            average_ind_cen_level = self.centralization_level(inddf)

            # calculate the industry holding shift ratio
            shift_ratio = self.ind_shift_rate(df[[x + '_exp' for x in self.indus_col] + ['jjzzc']].loc[q_list])
            #the 50,75,25 for c is 0.0.63,0.72,0.56
            #the 50,75,25 for r is 0.43,0.51,0.34
            if(average_ind_cen_level>0.63 and shift_ratio['mean']>0.43):
                ind_label='行业博弈型'
            elif (average_ind_cen_level > 0.63 and shift_ratio['mean'] < 0.43):
                ind_label = '行业专注型'
            elif (average_ind_cen_level < 0.63 and shift_ratio['mean'] > 0.43):
                ind_label = '行业轮动型'
            elif (average_ind_cen_level <0.63 and shift_ratio['mean'] < 0.43):
                ind_label = '行业配置型'
            else:
                ind_label=''

            a_date=q_list

        # print(ind_label)

        return ind_label,q_list,average_a_w,average_ind_cen_level,shift_ratio['mean'],shift_confidence,a_date

    def classify(self,jjdm,start_date,end_date,hld_com=False):

        df,q_list=self.ret_div(jjdm,start_date,end_date,hld_com)

        ind_label,q_list,average_a_w,average_ind_cen_level,\
        shift_ratio,shift_confidence,a_list=self.ind_analysis(df,hld_com)

        # q_date=df.loc[[(x[4:6] == '03') | (x[4:6] == '09') for x in df.index]].index
        # a_date=df.loc[[(x[4:6] == '06') | (x[4:6] == '12') for x in df.index]].index
        # q_list=q_date.to_list()+a_date.to_list()
        # average_a_w=df.loc[a_date]['published_stock_weight'].mean()
        style_shift_df,ind_shift_df,style_lable=self.exp_analysis(df,q_list,jjdm,average_a_w,hld_com)

        ability_label=self.ret_analysis(df,q_list,hld_com)

        if(hld_com):
            df=df[[x + "_exp" for x in self.barra_col]+[x + "_exp" for x in self.indus_col]]
        else:
            df = df[[x + "_exp_adj" for x in self.barra_col] + [x + "_exp_adj" for x in self.indus_col]]

        return df,style_shift_df,ind_shift_df,style_lable,average_ind_cen_level,shift_ratio,shift_confidence,average_a_w,ind_label,ability_label

    def data_preparation(self,hld_compenzation=False):

        jjdm_list=util.get_mutual_stock_funds('20211231')
        #'001291'
        # jjdm_list=jjdm_list.iloc[508:]
        for jjdm in jjdm_list:

            sql = """select min(jsrq) from st_fund.t_st_gm_gpzh where jjdm='{0}' and jsrq>=20150101
            """.format(jjdm)
            jsrq = str(self.hbdb.db2df(sql, db='funduser')['min(jsrq)'][0])
            #['2016','2017','2018','2019','2020','2021']
            for year in ['2018','2019','2020','2021']:
                if(year<jsrq[0:4]):
                    continue
                elif(year==jsrq[0:4]):
                    start_date=jsrq
                else:
                    start_date = str(int(year)-1) + "1231"

                end_date=year+"1231"
                try:
                    self.save_barra_ret2db(jjdm=jjdm,start_date=start_date,end_date=end_date,
                                           add=False,hld_compenzation=hld_compenzation)
                except Exception as e :
                    print(e)
                    print("{} failed at start date {} and end date{}".format(jjdm,start_date,end_date))

    def new_joinner_old(self,jjdm,start_date,end_date):

        ##get holding info for give jjdm
        sql="""select jsrq,zqdm,zjbl,zqmc from st_fund.t_st_gm_gpzh where jjdm='{0}' and jsrq<='{1}'  
        """.format(jjdm,end_date)
        hld=self.hbdb.db2df(sql,db='funduser')
        hld['jsrq']=hld['jsrq'].astype(str)

        #get the history ticker list based on start date
        history_ticker=hld[hld['jsrq']<start_date]['zqdm'].unique().tolist()
        #take only the holding after the start date
        hld=hld[(hld['jsrq']>=start_date)&(hld['zjbl']>0)].reset_index(drop=True)
        date_list=hld['jsrq'].unique().tolist()

        #get the date map between report date and the trade date
        new_date_list=[self._shift_date(x) for x in hld['jsrq'].unique()]
        date_map=dict(zip(hld['jsrq'].unique().tolist(),new_date_list))

        #take holding without the latest date since we need atleast one more quarter to calcualte the new joinner ret
        hld=hld[hld['jsrq']<end_date]


        hld['HK']=[len(x) for x in hld['zqdm']]
        hld=hld[hld['HK']==6]

        new_joinner_list=[]
        ret_list=[]
        q_list=[]
        adding_date=[]

        #for each item in the holding,check if it is a new joinner
        for i in range(len(hld)):
            if(len(new_joinner_list)>0):
                if(len(new_joinner_list)!=len(ret_list)):
                    print(i-1)
                    raise Exception
            zqdm=hld.iloc[i]['zqdm']
            zqmc=hld.iloc[i]['zqmc']
            if(zqdm not in history_ticker):
                #if new joinner, add it to new joinner list and history list
                history_ticker.append(zqdm)
                new_joinner_list.append(zqdm)

                # get the next report date
                t0 = hld.iloc[i]['jsrq']
                date_ind=date_list.index(t0)
                t0=date_map[hld.iloc[i]['jsrq']]
                adding_date.append(t0)
                t1=date_map[date_list[date_ind+1]]
                q_list.append('t1')
                date_sql_con="and JYRQ in ({})".format("'"+t0+"','"+t1+"'"+"@")

                # get the report date after the next report date if possible
                if(date_ind<len(date_list)-3):
                    t2=date_map[date_list[date_ind+2]]
                    t3=date_map[date_list[date_ind+3]]
                    date_sql_con=date_sql_con.replace("@",",'{0}','{1}'".format(t2,t3))
                    new_joinner_list.append(zqdm)
                    new_joinner_list.append(zqdm)
                    q_list.append('t2')
                    q_list.append('t3')
                    adding_date.append(t0)
                    adding_date.append(t0)

                elif(date_ind<len(date_list)-2):
                    t2=date_map[date_list[date_ind+2]]
                    date_sql_con=date_sql_con.replace("@",",'"+t2+"'")
                    new_joinner_list.append(zqdm)
                    q_list.append('t2')
                    adding_date.append(t0)
                else:
                    date_sql_con = date_sql_con.replace("@", "")

                #get ticker price for given date
                sql = """
                select zqdm ZQDM,jyrq JYRQ,drjj DRJJ,scdm SCDM from st_ashare.t_st_ag_gpjy where zqdm ='{0}' {1}
                 """.format(zqdm, date_sql_con)
                quarter_price = self.hbdb.db2df(sql, db='alluser')

                # get benchmark price for given date
                sql="select zqdm,spjg,jyrq from st_market.t_st_zs_hq where  zqdm='000002' {0} "\
                    .format(date_sql_con)
                benchmakr_ret=self.hbdb.db2df(sql,db='alluser')

                # continue_flag=False
                if(len(quarter_price)!=len(benchmakr_ret)):
                    sql = "select min(jyrq) as jyrq from  st_ashare.t_st_ag_gpjy where zqdm ='{0}' and zqmc='{1}'".format(zqdm,zqmc)
                    min_jyrq =self.hbdb.db2df(sql, db='readonly')['JYRQ'][0]
                    if(min_jyrq>t0):
                        sql = """
                        select zqdm ZQDM,jyrq JYRQ,drjj DRJJ,scdm SCDM from st_ashare.t_st_ag_gpjy where zqdm ='{0}' {1}
                         """.format(zqdm, date_sql_con)
                        sql=sql.replace(t0,min_jyrq)
                        quarter_price = self.hbdb.db2df(sql, db='readonly')
                #     else:
                #         continue_flag=True
                #
                # if(continue_flag):
                #     continue

                for i in range(1,len(quarter_price)):
                    ret_list.append( (quarter_price.iloc[i]['DRJJ'] /quarter_price.iloc[0]['DRJJ']-1)-
                                     (benchmakr_ret.iloc[i]['spjg'] /benchmakr_ret.iloc[0]['spjg']-1))

        retdf=pd.DataFrame()
        retdf['zqdm']=new_joinner_list
        retdf['qt']=q_list
        retdf['ret']=ret_list
        retdf['added_date']=adding_date

        # outputdf=pd.DataFrame(columns=['收益时序','胜率','平均超额收益'])
        # outputdf['收益时序']=['1个季度后','2个季度后','3个季度后']
        # outputdf['胜率']=(retdf[retdf['ret']>0]).groupby('qt').count()['zqdm'].values/retdf.groupby('qt').count()['zqdm'].values
        # outputdf['平均超额收益']=retdf.groupby('qt').mean()['ret'].values
        # outputdf['超额收益中位数']=retdf.groupby('qt').median()['ret'].values
        # outputdf['最大超额收益'] = retdf.groupby('qt').max()['ret'].values
        # outputdf['最小超额收益'] = retdf.groupby('qt').min()['ret'].values
        # for col in ['胜率','平均超额收益','超额收益中位数','最大超额收益','最小超额收益']:
        #     outputdf[col] = outputdf[col].astype(float).map("{:.2%}".format)
        #
        # return  outputdf

        return retdf

    def new_joinner(self,jjdm):

        ##get holding info for give jjdm no older than 20151231
        sql="""select jsrq,zqdm,zjbl,zqmc from st_fund.t_st_gm_gpzh where jjdm='{0}' and jsrq>='20151231'  
        """.format(jjdm)
        hld=self.hbdb.db2df(sql,db='funduser')
        hld['jsrq']=hld['jsrq'].astype(str)
        end_date=hld['jsrq'].unique()[-1]
        start_date=hld['jsrq'].unique()[1]


        #get the history ticker list based on start date
        history_ticker=hld[hld['jsrq']<start_date]['zqdm'].unique().tolist()
        #take only the holding after the start date
        hld=hld[(hld['jsrq']>=start_date)&(hld['zjbl']>0)].reset_index(drop=True)
        date_list=hld['jsrq'].unique().tolist()

        #get the date map between report date and the trade date
        new_date_list=[self._shift_date(x) for x in hld['jsrq'].unique()]
        date_map=dict(zip(hld['jsrq'].unique().tolist(),new_date_list))

        #take holding without the latest date since we need atleast one more quarter to calcualte the new joinner ret
        hld=hld[hld['jsrq']<end_date]


        hld['HK']=[len(x) for x in hld['zqdm']]
        hld=hld[hld['HK']==6]

        new_joinner_list=[]
        ret_list=[]
        q_list=[]
        adding_date=[]

        #for each item in the holding,check if it is a new joinner
        for i in range(len(hld)):
            # if(len(new_joinner_list)>0):
            #     if(len(new_joinner_list)!=len(ret_list)):
            #         print(i-1)
            #         raise Exception
            zqdm=hld.iloc[i]['zqdm']
            zqmc=hld.iloc[i]['zqmc']
            if(zqdm not in history_ticker):
                #if new joinner, add it to new joinner list and history list
                history_ticker.append(zqdm)
                # new_joinner_list.append(zqdm)

                # get the next report date
                t0 = hld.iloc[i]['jsrq']
                date_ind=date_list.index(t0)
                t0=date_map[hld.iloc[i]['jsrq']]
                # adding_date.append(t0)
                t1=date_map[date_list[date_ind+1]]
                # q_list.append('t1')
                date_sql_con="and JYRQ in ({})".format("'"+t0+"','"+t1+"'"+"@")

                # get the report date after the next report date if possible
                if(date_ind<len(date_list)-3):
                    t2=date_map[date_list[date_ind+2]]
                    t3=date_map[date_list[date_ind+3]]
                    date_sql_con=date_sql_con.replace("@",",'{0}','{1}'".format(t2,t3))


                elif(date_ind<len(date_list)-2):
                    t2=date_map[date_list[date_ind+2]]
                    date_sql_con=date_sql_con.replace("@",",'"+t2+"'")

                else:
                    date_sql_con = date_sql_con.replace("@", "")

                #get ticker price for given date
                sql = """
                select zqdm ZQDM,jyrq JYRQ,drjj DRJJ,SCDM from st_ashare.t_st_ag_gpjy where zqdm ='{0}' and drjj is not null  {1}
                 """.format(zqdm, date_sql_con)
                quarter_price = self.hbdb.db2df(sql, db='alluser')

                # get benchmark price for given date
                sql="select zqdm,spjg,jyrq from st_market.t_st_zs_hq where  zqdm='000002' {0} "\
                    .format(date_sql_con)
                benchmakr_ret=self.hbdb.db2df(sql,db='alluser')
                benchmakr_ret['jyrq']=benchmakr_ret['jyrq'].astype(str)
                benchmakr_ret['ind']=benchmakr_ret.index
                if(len(quarter_price)>0):
                    if(quarter_price['JYRQ'].min()>t0):
                        sql = "select min(jyrq) as jyrq from  st_ashare.t_st_ag_gpjy where zqdm ='{0}' and zqmc='{1}' and jyrq>'{2}' and drjj is not null ".format(zqdm,zqmc,t0)
                        min_jyrq =self.hbdb.db2df(sql, db='alluser')['JYRQ'][0]
                        if(min_jyrq>t0 and min_jyrq<t1):
                            sql = """
                            select zqdm ZQDM,jyrq JYRQ,drjj DRJJ,scdm SCDM from st_ashare.t_st_ag_gpjy where zqdm ='{0}' and drjj is not null {1}
                             """.format(zqdm, date_sql_con)
                            sql=sql.replace(t0,min_jyrq)
                            quarter_price = self.hbdb.db2df(sql, db='alluser')

                    if(quarter_price['JYRQ'].min()==t0):

                        tempdf=pd.merge(quarter_price,benchmakr_ret,how='left',left_on='JYRQ',right_on='jyrq')
                        for i in range(1,len(tempdf)):
                            new_joinner_list.append(zqdm)
                            adding_date.append(t0)
                            q_list.append("t"+str(tempdf['ind'][i]))
                            ret_list.append( (quarter_price.iloc[i]['DRJJ'] /quarter_price.iloc[0]['DRJJ']-1)-
                                             (benchmakr_ret.iloc[i]['spjg'] /benchmakr_ret.iloc[0]['spjg']-1))

        retdf=pd.DataFrame()
        retdf['zqdm']=new_joinner_list
        retdf['qt']=q_list
        retdf['ret']=ret_list
        retdf['added_date']=adding_date

        return retdf

    def save_new_joinner_date2localdb(self):


        jjdm_list=util.get_mutual_stock_funds('20211231')

        erro_df=pd.DataFrame()
        error_list=[]

        localdb.execute("delete from new_joinner_ret")

        for i in range(0,len(jjdm_list)):
            try:
                retdf=self.new_joinner(jjdm_list[i])
                retdf['jjdm']=jjdm_list[i]
                retdf.to_sql('new_joinner_ret',index=False,if_exists='append',con=self.localengine)
                print("{0} done ".format(jjdm_list[i]))
            except Exception as e :
                error_list.append(jjdm_list[i]+"@"+str(e))
                continue
        erro_df['error']=error_list
        erro_df.to_csv(r"E:\新股错误数据.csv")
        print('Done')

    def change_analysis(self,jjdm,start_date,end_date,hld_com=True):

        df,q_list=self.ret_div(jjdm,start_date,end_date,hld_com)
        q_list=df.loc[[(x[4:6] == '03') | (x[4:6] == '09')|(x[4:6] == '06')
                              | (x[4:6] == '12') for x in df.index]].index.tolist()
        q_list.sort()
        df=df.loc[q_list][[x+"_exp" for x in self.indus_col]]

        diff = df.diff(1, axis=0)
        diff['total_w'] = df.sum(axis=1)
        change_ret = diff.copy()
        change_ret_nextq = diff.copy()
        sql = "select flmc,zsdm from st_market.t_st_zs_hyzsdmdyb where hyhfbz='2'"
        zqdm_list = self.hbdb.db2df(sql, db='alluser')

        for col in self.indus_col:
            # print(col)
            zqdm = zqdm_list[zqdm_list['flmc'] == self.industry_name_map_e2c[col]]['zsdm'].tolist()[0]
            for i in range(1, len(diff) - 1):
                #print(i)
                t0 = diff.index[i - 1]
                t1 = diff.index[i]
                t2 = diff.index[i + 1]
                date_con = "'{0}','{1}','{2}'".format(t0, t1,t2)
                sql = """select zqdm,spjg,jyrq from  st_market.t_st_zs_hqql where jyrq in ({0}) and (zqdm='{1}' or zqdm='000002')
                """.format(date_con, zqdm)
                index_price = self.hbdb.db2df(sql, db='alluser')
                index_price['ret'] = index_price['spjg'].pct_change()
                index_price['jyrq']=index_price['jyrq'].astype(str)
                index_price.set_index('jyrq', drop=True, inplace=True)

                change_ret.loc[t1, col+"_exp"] = \
                    (index_price[index_price['zqdm']==zqdm].loc[t1]['ret']
                                                  - index_price[index_price['zqdm']=='000002'].loc[t1]['ret']) \
                    * diff.loc[t1, col+"_exp"] / diff.loc[t1, "total_w"]
                if(t2 in index_price[index_price['zqdm']==zqdm].index):
                    change_ret_nextq.loc[t1, col+"_exp"] = \
                        (index_price[index_price['zqdm']==zqdm].loc[t2]['ret']
                                                      - index_price[index_price['zqdm']=='000002'].loc[t2]['ret']) \
                        * diff.loc[t1, col+"_exp"] / diff.loc[t1, "total_w"]
                else:
                    change_ret_nextq.loc[t1, col + "_exp"]=np.nan

        change_ret=change_ret.loc[change_ret.index[1:-1]].drop('total_w',axis=1)
        change_ret_nextq = change_ret_nextq.loc[change_ret_nextq.index[1:-1]].drop('total_w',axis=1)

        industry_based_ret=pd.concat([change_ret.sum(axis=0),change_ret_nextq.sum(axis=0)],axis=1)
        term_based_ret=pd.concat([change_ret.sum(axis=1),change_ret_nextq.sum(axis=1)],axis=1)
        industry_based_ret.columns=['当季','下季']
        term_based_ret.columns = ['当季', '下季']

        for col in industry_based_ret.columns:
            industry_based_ret[col] = industry_based_ret[col].astype(float).map("{:.2%}".format)
        for col in term_based_ret.columns:
            term_based_ret[col] = term_based_ret[col].astype(float).map("{:.2%}".format)

        industry_based_ret.sort_values('当季',ascending=False,inplace=True)

        return change_ret,change_ret_nextq,industry_based_ret,term_based_ret

    def change_analysis_givendf(self,df):

        q_list=df.loc[[(x[4:6] == '03') | (x[4:6] == '09')|(x[4:6] == '06')
                              | (x[4:6] == '12') for x in df.index]].index.tolist()
        q_list.sort()
        df=df.loc[q_list][[x+"_exp" for x in self.indus_col]]

        diff = df.diff(1, axis=0)
        diff['total_w'] = df.sum(axis=1)
        change_ret = diff.copy()
        change_ret_nextq = diff.copy()
        sql = "select flmc,zsdm from st_market.t_st_zs_hyzsdmdyb where hyhfbz='2'"
        zqdm_list = self.hbdb.db2df(sql, db='alluser')

        for col in self.indus_col:
            # print(col)
            zqdm = zqdm_list[zqdm_list['flmc'] == self.industry_name_map_e2c[col]]['zsdm'].tolist()[0]
            for i in range(1, len(diff) - 1):
                #print(i)
                t0 = diff.index[i - 1]
                t1 = diff.index[i]
                t2 = diff.index[i + 1]
                date_con = "'{0}','{1}','{2}'".format(t0, t1,t2)
                sql = """select zqdm,spjg,jyrq from  st_market.t_st_zs_hqql where jyrq in ({0}) and (zqdm='{1}' or zqdm='000002')
                """.format(date_con, zqdm)
                index_price = self.hbdb.db2df(sql, db='alluser')
                index_price['ret'] = index_price['spjg'].pct_change()
                index_price['jyrq']=index_price['jyrq'].astype(str)
                index_price.set_index('jyrq', drop=True, inplace=True)

                change_ret.loc[t1, col+"_exp"] = \
                    (index_price[index_price['zqdm']==zqdm].loc[t1]['ret']
                                                  - index_price[index_price['zqdm']=='000002'].loc[t1]['ret']) \
                    * diff.loc[t1, col+"_exp"] / diff.loc[t1, "total_w"]
                if(t2 in index_price[index_price['zqdm']==zqdm].index):
                    change_ret_nextq.loc[t1, col+"_exp"] = \
                        (index_price[index_price['zqdm']==zqdm].loc[t2]['ret']
                                                      - index_price[index_price['zqdm']=='000002'].loc[t2]['ret']) \
                        * diff.loc[t1, col+"_exp"] / diff.loc[t1, "total_w"]
                else:
                    change_ret_nextq.loc[t1, col + "_exp"]=np.nan

        change_ret=change_ret.loc[change_ret.index[1:-1]].drop('total_w',axis=1)
        change_ret_nextq = change_ret_nextq.loc[change_ret_nextq.index[1:-1]].drop('total_w',axis=1)

        industry_based_ret=pd.concat([change_ret.sum(axis=0),change_ret_nextq.sum(axis=0)],axis=1)
        term_based_ret=pd.concat([change_ret.sum(axis=1),change_ret_nextq.sum(axis=1)],axis=1)
        industry_based_ret.columns=['当季','下季']
        term_based_ret.columns = ['当季', '下季']

        for col in industry_based_ret.columns:
            industry_based_ret[col] = industry_based_ret[col].astype(float).map("{:.2%}".format)
        for col in term_based_ret.columns:
            term_based_ret[col] = term_based_ret[col].astype(float).map("{:.2%}".format)

        industry_based_ret.sort_values('当季',ascending=False,inplace=True)

        return change_ret,change_ret_nextq,industry_based_ret,term_based_ret

    @staticmethod
    def factorlize_new_joinner(factor_name):

        sql="select jjdm,added_date,avg(ret) as {0} from new_joinner_ret  where qt='t1' GROUP BY jjdm,added_date "\
            .format(factor_name)

        raw_df=pd.read_sql(sql,con=localdb)
        date_list=raw_df['added_date'].unique()
        date_list.sort()
        first_date=date_list[0]
        raw_df.rename(columns={'added_date':'date'},inplace=True)
        raw_df[factor_name]=[np.nan] + raw_df[factor_name][0:-1].tolist()

        raw_df=raw_df[raw_df['date']!=first_date]
        #take the last 3years mean t_ret as factor
        raw_df['new_join_'+factor_name] = raw_df.groupby(by='jjdm',as_index=False)[factor_name].rolling(12, 1).mean().values

        return raw_df

class Stock_trade_timing:

    @staticmethod
    def data_factory(ticker,threshold=5,time_length=3):

        asofdate=datetime.datetime.today().strftime('%Y%m%d')
        start_date=str(int(asofdate[0:4])-time_length)+asofdate[4:]

        jjdm_list=util.get_mutual_stock_funds('20220630')
        jjdm_con=util.list_sql_condition(jjdm_list)

        sql="select distinct(jsrq) from st_fund.t_st_gm_jjcgbd where jsrq>={}".format(start_date)
        hld_reprot_date_list=hbdb.db2df(sql,db='funduser').sort_values('jsrq')['jsrq'].astype(str).tolist()

        #get the stock that become zc
        sql="""select jjdm,jsrq from st_fund.t_st_gm_jjcgbd where zqdm='{0}' 
        and zclb='1' and jjdm in ({1}) and jsrq>='{2}'
        """.format(ticker,jjdm_con,start_date)
        hld_df=hbdb.db2df(sql,db='funduser')
        hld_df['jsrq']=hld_df['jsrq'].astype(str)


        #get the stock zgbl
        jjdm_con_new=util.list_sql_condition(hld_df['jjdm'].unique().tolist())
        sql="select jjdm,jsrq,zgbl from st_fund.t_st_gm_gpzh where zqdm='{2}' and jjdm in ({0}) and jsrq in ({1}) "\
            .format(jjdm_con_new,
                    util.list_sql_condition(hld_df['jsrq'].unique().tolist()),
                    ticker)
        zgbl=hbdb.db2df(sql,db='funduser')
        zgbl['jsrq'] = zgbl['jsrq'].astype(str)
        hld_df=pd.merge(hld_df,zgbl,how='left',on=['jjdm','jsrq'])
        hld_df=hld_df[hld_df['zgbl']>=threshold]


        hld_df['lastdate'] = [hld_reprot_date_list[hld_reprot_date_list.index(x) - 1] for x in hld_df['jsrq']]
        hld_df.loc[hld_df['jsrq']<hld_reprot_date_list[-1],'nextdate'] = [hld_reprot_date_list[hld_reprot_date_list.index(x) + 1]
                              for x in hld_df[hld_df['jsrq']<hld_reprot_date_list[-1]]['jsrq']]

        hld_df = pd.merge(hld_df, hld_df[['jjdm', 'jsrq']], how='left',
                          left_on=['jjdm','lastdate'],right_on=['jjdm','jsrq'])

        hld_df = pd.merge(hld_df, hld_df[['jjdm', 'jsrq_x']], how='left',
                          left_on=['jjdm','nextdate'],right_on=['jjdm','jsrq_x'])


        #map the jjdm to jjjl
        sql="select jjdm,ryxm,rzrq,lrrq from st_fund.t_st_gm_jjjl where jjdm in ({0})"\
            .format(jjdm_con_new)
        jjjl=hbdb.db2df(sql,db='funduser')
        jjjl['rzrq']=jjjl['rzrq'].astype(str)
        jjjl['lrrq'] = jjjl['lrrq'].astype(str)

        hld_df=pd.merge(hld_df,jjjl,how='left',on='jjdm')

        #map the jjdm with jjjc
        sql="select jjdm,jjjc from st_fund.t_st_gm_jjxx  "
        jjjc=hbdb.db2df(sql,db='funduser')
        hld_df=pd.merge(hld_df,jjjc,how='left',on='jjdm')
        hld_df['ryxm']=hld_df['ryxm']+'_'+hld_df['jjjc']

        #map the jjdm to jjgs
        sql="select a.jjdm,b.jgjc from st_main.t_st_gg_jjxx a left join st_main.t_st_gg_jgxx b on a.glrm=b.jgdm where a.jjdm in ({0})"\
            .format(jjdm_con_new)
        jjgs=hbdb.db2df(sql,db='alluser')
        hld_df=pd.merge(hld_df,jjgs,how='left',on='jjdm')
        hld_df['ryxm']=hld_df['ryxm']+'_'+hld_df['jgjc']

        hld_df1=hld_df[hld_df['jsrq_y'].isnull()][['ryxm','jsrq_x_x','zgbl']].rename(columns={'jsrq_x_x':'jsrq'})
        hld_df2=hld_df[(hld_df['nextdate'].notnull())
                       &(hld_df['jsrq_x_y'].isnull())][['ryxm','nextdate','zgbl']].rename(columns={'nextdate':'jsrq'})
        hld_df.drop_duplicates(['jsrq_x_x','zgbl','jjjc'],inplace=True)
        hld_df1_gs=hld_df[hld_df['jsrq_y'].isnull()][['jgjc','jsrq_x_x','zgbl']]\
            .rename(columns={'jsrq_x_x':'jsrq'})\
            .groupby(['jgjc','jsrq']).mean().reset_index()
        hld_df2_gs=hld_df[(hld_df['nextdate'].notnull())
                       &(hld_df['jsrq_x_y'].isnull())][['jgjc','nextdate','zgbl']]\
            .rename(columns={'nextdate':'jsrq'})\
            .groupby(['jgjc','jsrq']).mean().reset_index()
        del hld_df

        hld_df1=hld_df1.sort_values(['jsrq','zgbl']).groupby(['jsrq', 'ryxm'], as_index=False).mean()
        hld_df2 = hld_df2.sort_values(['jsrq','zgbl']).groupby(['jsrq', 'ryxm'], as_index=False).mean()

        hld_df1 = hld_reportdate2trade_date(hld_df1,date_col='jsrq')
        hld_df2 = hld_reportdate2trade_date(hld_df2, date_col='jsrq')
        hld_df1_gs = hld_reportdate2trade_date(hld_df1_gs,date_col='jsrq')
        hld_df2_gs = hld_reportdate2trade_date(hld_df2_gs, date_col='jsrq')

        hld_df1['jjdm_new'] =hld_df1['ryxm']+ [": "+str(x)[0:4] + "<br />" for x in hld_df1['zgbl']]
        hld_df2['jjdm_new'] =hld_df2['ryxm']+ [": "+str(x)[0:4]  + "<br />" for x in hld_df2['zgbl']]
        hld_df1_gs['jjdm_new'] =hld_df1_gs['jgjc']+ [": "+str(x)[0:4]  + "<br />" for x in hld_df1_gs['zgbl']]
        hld_df2_gs['jjdm_new'] =hld_df2_gs['jgjc']+ [": "+str(x)[0:4]  + "<br />" for x in hld_df2_gs['zgbl']]

        #rank by zgbl
        hld_df1=pd.concat([hld_df1,
                           hld_df1.groupby('jsrq', as_index=False).rank(ascending=False,method='min').rename(columns={'zgbl': 'rank'})],
                          axis=1)

        hld_df2=pd.concat([hld_df2,
                           hld_df2.groupby('jsrq', as_index=False).rank(method='min').rename(columns={'zgbl': 'rank'})],
                          axis=1)

        hld_df1_gs=pd.concat([hld_df1_gs,
                           hld_df1_gs.groupby('jsrq', as_index=False).rank(ascending=False,method='min').rename(columns={'zgbl': 'rank'})],
                          axis=1)

        hld_df2_gs=pd.concat([hld_df2_gs,
                           hld_df2_gs.groupby('jsrq', as_index=False).rank(method='min').rename(columns={'zgbl': 'rank'})],
                          axis=1)

        #take only the top 20 for buy and last 20 for sell


        hld_df_pic_1=hld_df1[hld_df1['rank']<=20].groupby('jsrq')['jjdm_new'].sum().to_frame('jjdm')
        hld_df_pic_2 = hld_df2[hld_df2['rank'] <= 20].groupby('jsrq')['jjdm_new'].sum().to_frame('jjdm')
        hld_df_gs_pic_1=hld_df1_gs[hld_df1_gs['rank']<=20].groupby('jsrq')['jjdm_new'].sum().to_frame('jjdm')
        hld_df_gs_pic_2 = hld_df2_gs[hld_df2_gs['rank'] <= 20].groupby('jsrq')['jjdm_new'].sum().to_frame('jjdm')


        #get the stock price data
        sql = """
        select jyrq JYRQ,spjg SPJG from st_ashare.t_st_ag_gpjy where zqdm='{0}' and drjj is not null and jyrq>='{1}'
         """.format(ticker,start_date)
        price_df=hbdb.db2df(sql,db='alluser')
        price_df.sort_values('JYRQ',inplace=True)

        hld_df_pic_1=pd.merge(price_df,hld_df_pic_1,how='left',left_on='JYRQ',right_index=True).drop(['ROW_ID'],axis=1)
        hld_df_pic_1.set_index('JYRQ',drop=True,inplace=True)

        hld_df_pic_2=pd.merge(price_df,hld_df_pic_2,how='left',left_on='JYRQ',right_index=True).drop(['ROW_ID'],axis=1)
        hld_df_pic_2.set_index('JYRQ',drop=True,inplace=True)

        hld_df_gs_pic_1=pd.merge(price_df,hld_df_gs_pic_1,how='left',left_on='JYRQ',right_index=True).drop(['ROW_ID'],axis=1)
        hld_df_gs_pic_1.set_index('JYRQ',drop=True,inplace=True)

        hld_df_gs_pic_2=pd.merge(price_df,hld_df_gs_pic_2,how='left',left_on='JYRQ',right_index=True).drop(['ROW_ID'],axis=1)
        hld_df_gs_pic_2.set_index('JYRQ',drop=True,inplace=True)

        return hld_df1.drop(['jjdm_new','rank'],axis=1),hld_df2.drop(['jjdm_new','rank'],axis=1),\
               hld_df1_gs.drop(['jjdm_new','rank'],axis=1),hld_df2_gs.drop(['jjdm_new','rank'],axis=1),\
               hld_df_pic_1,hld_df_pic_2,hld_df_gs_pic_1,hld_df_gs_pic_2

if __name__ == '__main__':




    # gh = General_holding()
    # stock_swind_map \
    #     = gh.get_ind_map(2)
    #
    # sql = """select jjdm,jsrq,zqdm,zjbl from st_fund.t_st_gm_gpzh where jjdm in ({0}) and jsrq>='{1}' and jsrq<='{2}'
    # """.format(util.list_sql_condition(['000612','006511']), '20190601', '20221231')
    # hld = hbdb.db2df(sql, db='funduser')
    # dir = r"E:\GitFolder\docs\公募基金行业动态模拟"
    # jsrq_list=\
    #     hld['jsrq'].unique().tolist()
    #
    # for jsrq in jsrq_list:
    #     try:
    #         file_name = "\补全持仓数据_{}.xlsx".format(jsrq)
    #         craft_data=pd.read_excel(dir+file_name)
    #         craft_data['jjdm']=[("000000"+str(x))[-6:] for x in craft_data['jjdm']]
    #         craft_data=craft_data[craft_data['jjdm'].isin(['000612','006511'])]
    #         craft_data['jsrq']=jsrq
    #         craft_data['zqdm']=[("000000"+str(x))[-6:] for x in craft_data['zqdm']]
    #     except Exception as e :
    #         print(e)
    #         continue
    #
    #     hld=hld[~((hld['jsrq']==jsrq)&(hld['jjdm'].isin(craft_data['jjdm'].unique().tolist())))]
    #     hld=pd.concat([hld,craft_data[['zjbl','jjdm','jsrq','zqdm']]],axis=0)
    #
    # hld = hld.sort_values(['jsrq', 'jjdm'])
    # hld=pd.merge(hld,stock_swind_map,how='left',on='zqdm')
    # hld.to_excel('target_hld.xlsx')


    # ba=Barra_analysis()
    # ba.save_new_joinner_date2localdb()


    # ratio_his=pd.read_excel('ratio_his.xlsx')
    # # save the cen and shift ratio into local db
    # sql="delete from hbs_cen_shift_ratio_his_industry{0} where jsrq>='{1}' and jsrq<='{2}'"\
    #     .format(str(2+1),ratio_his.index.min(),ratio_his.index.max())
    # localdb.execute(sql)
    # ratio_his.to_sql('hbs_cen_shift_ratio_his_industry{0}'.format(str(2+1)), con=localdb,
    #                                           if_exists='append', index=False)
    # industry_hld_list=[pd.read_excel(r)]

    # for i in range(2):
    # # #check if data already exist
    # sql="delete from hbs_industry_class{2}_exp where jsrq>='{0}' and jsrq<='{1}'"\
    #     .format(industry_hld_list[i]['jsrq'].min(),industry_hld_list[i]['jsrq'].max(),i+1)
    # localdb.execute(sql)
    # industry_hld_list[i].to_excel('hbs_industry_class{0}_exp.xlsx'.format(i + 1))

    #

    gh=General_holding()
    # gh.update_fund_holding_local_file('20230331','20230630')
    #index_industry_distribution()
    # gh.save_quarter_data_2_db( r"E:\GitFolder\docs\公募基金行业动态模拟\持仓数据补全\\")
    asofdate='20230930'
    #if it is September then the from local db parameter is False else this parameter is True
    # gh.key_holding_expantation(util.get_stock_funds_pool(str(2023) + '0930', time_length=0.5)[0:10],
    #                            str(2023) + '0930', str(2023) + '0630', str(2023) + '0901',
    #                            str(2023) + '1031', False)

    # data=pd.read_excel(r"E:\GitFolder\hbshare\fe\mutual_analysis\补全持仓数据_20230930.xlsx")
    # data['zqdm']=[("000000"+str(x))[-6:] for x in data['zqdm']]
    # data['jjdm']=[("000000"+str(x))[-6:] for x in data['jjdm']]
    # data['jsrq'] = '20230930'
    # data.drop_duplicates(['jjdm','zqdm'],inplace=True)
    # data.drop('Unnamed: 0', axis=1).to_sql('artificial_quartly_full_hld',con=localdb,if_exists='append',index=False)
    # for i in range(8,9):
        # print(i)
        # gh.key_holding_expantation(util.get_stock_funds_pool(str(2022-i)+'0930',time_length=0.5) ,str(2022-i)+'0930',str(2022-i)+'0630',str(2022-i)+'0901',str(2022-i)+'1031')
        # gh.key_holding_expantation(util.get_stock_funds_pool(str(2022-i)+'0331',time_length=0.5), str(2022-i)+'0331', str(2021-i)+'1231', str(2022-i)+'0301', str(2022-i)+'0430')

    # for i in range(9):
    #     print(i)
    #     gh.key_holding_expantation(util.get_stock_funds_pool(str(2022-i)+'1231',time_length=0.5) ,str(2022-i)+'1231',str(2022-i)+'0930',str(2022-i)+'1201',str(2023-i)+'0131',True)
    #     gh.key_holding_expantation(util.get_stock_funds_pool(str(2022-i)+'0630',time_length=0.5), str(2022-i)+'0630', str(2022-i)+'0331', str(2022-i)+'0601', str(2022-i)+'0731',True)



    # gh.save_style_indexhistory2db()
    # gh.save_size_indexhistory2db()
    # gh.save_industry_financial_stats2db(start_date='20130630',end_date='20141231')
    #jjdm_list=util.get_potient_mutual_stock_funds(asofdate)

    jjdm_list = util.get_all_mutual_stock_funds(asofdate)
    #jjdm_list=util.get_stock_funds_pool('20220331',time_length=0.5)
    # jjdm_list=util.get_885001_funds('20221230',onlyA=False)
    # jjdm_list=util.get_stock_funds_pool('20220630',2)
    #jjdm_list=['005827','005241','010409','008901','006179','519915','001832','010454','005004','519714','004868','519710','090016','519019']
    # jjdm_list=util.get_885001_funds('20220831')
    #jjdm_list=['012159']
    # temphld = gh.read_hld_fromdb('20180101', '20220630', '519133', False)
    # hld, new_jjdm_list = gh.fund_holding_date_manufacture(jjdm_list,
    #                                                         '20180101', '20220630',
    #                                                         if_zstockbl=False, if_hldcom=True, keyholdonly=False)
    # #
    # hld = hld[hld['zqdm'].isin(['600885'])]
    # hld['mv'] = hld['jjzzc'] * hld['zjbl']/100
    # hld=pd.merge(hld.groupby(['zqdm','jsrq']).count()['jjdm'].to_frame('count')
    #                  ,hld.groupby(['zqdm','jsrq'])['mv'].sum().to_frame('mv'),how='left',on=['zqdm','jsrq'])
    # hld.to_excel('公募持仓信息.xlsx')
    #
    # print('done')



    trunk_size=1000
    # # #
    # # sql="delete from hbs_hld_sl_history where asofdate='{}' ".format(asofdate)
    # # localdb.execute(sql)
    # # #
    # for i in range(3):
    #     #check if data already exist
    #     sql="delete from hbs_industry_class{2}_exp where jsrq>='{0}' and jsrq<='{1}'"\
    #         .format('20100630','20141231',i+1)
    #     localdb.execute(sql)
    # # #
    # # # jjdm_list=['012476']
    # #
    # for i in range(0,int(np.floor(len(jjdm_list)/trunk_size)+1)):
    #     print(i)
    #     temp_jjdm_list=jjdm_list[i*trunk_size:(i+1)*trunk_size]
    #     #
    #     # hls_sl_history=gh.adjusted_hldquant(temp_jjdm_list, '20151231', '20220831')
    #     # hls_sl_history.to_excel('hsl_sl_20220603_{}.xlsx'.format(i),index=False)
    #     # hls_sl_history.to_sql('hbs_hld_sl_history', con=localdb, index=False, if_exists='append')
    #
    #     industry_hld_list=\
    #         gh.save_industry_exp2db(temp_jjdm_list,start_date='20230901',end_date='20230930')
    #
    #     for j in range(0,len(industry_hld_list)):
    #
    #         industry_hld_list[j].to_sql('mimic_hbs_industry_class{0}_exp'.format(j + 1),
    #                                                                 index=False,
    #                                     if_exists='append', con=localdb)
    #
    #     print('{} done'.format(i))

    # for j in range(3):
    #
    #     data=pd.read_sql("select * from hbs_industry_class{0}_exp_key_only where jsrq='20220930' ".format(j + 1)
    #                      ,con=localdb)
    #     if(j==0):
    #         col='yjxymc'
    #     elif(j==1):
    #         col='ejxymc'
    #     else:
    #         col='sjxymc'
    #     localdb.execute("delete from hbs_industry_class{0}_exp where jsrq='20220930'".format(j + 1))
    #     data.drop_duplicates(['jjdm',col]
    #                          ,keep='last').to_sql('hbs_industry_class{0}_exp'.format(j + 1),
    #                                 index=False,
    #                                 if_exists='append', con=localdb)
    #
    #     print('{} done'.format(j))



    # for i in range(0,int(np.floor(len(jjdm_list)/trunk_size)+1)):
    #     print(i)
    #
    #     hls_sl_history=pd.read_excel('hsl_sl_20220603_{}.xlsx'.format(i))
    #     hls_sl_history['jjdm']=[("000000"+str(x))[-6:] for x in hls_sl_history['jjdm'].tolist()]
    #     hls_sl_history.to_sql('hbs_hld_sl_history', con=localdb, index=False, if_exists='append')


    # sql='select * from stock_style_lable'
    # stock_lable=pd.read_sql(sql,con=localdb).drop_duplicates(['jsrq','zqdm'])
    #
    # sql='select * from stock_style_lable_new'
    # stock_lable_new=pd.read_sql(sql,con=localdb).drop_duplicates(['jsrq','zqdm'])
    # test = pd.merge(stock_lable, stock_lable_new, how='outer', on=['jsrq', 'zqdm'])
    # output_df=pd.DataFrame()
    # for col in ['style_type_x', 'size_type_x', 'style_type_y',
    #    'size_type_y']:
    #     output_df=pd.concat([output_df,
    #                          test.groupby(['jsrq',col]).count()[['zqdm']].reset_index()],axis=1)

    # jjdm_list = util.get_mutual_stock_funds('20220630')
    # jjdm_list = util.get_885001_funds('20220630')


    # gh.save_style_exp2db(jjdm_list,start_date='20230901'
    #                       ,end_date='20230930',if_885001=False)
    # table_name='mimic_'
    # style_hld=pd.read_excel(table_name+'style_hld.xlsx')
    # size_hld=pd.read_excel(table_name+'size_hld.xlsx')
    # lable_hld=pd.read_excel(table_name+'label_hld.xlsx')
    # style_hld['jjdm']=[("000000"+str(x))[-6:] for x in style_hld['jjdm']]
    # size_hld['jjdm'] = [("000000" + str(x))[-6:] for x in size_hld['jjdm']]
    # lable_hld['jjdm'] = [("000000" + str(x))[-6:] for x in lable_hld['jjdm']]
    # localdb.execute("delete from {1}hbs_style_exp where jsrq in ({0}) "
    #                 .format(util.list_sql_condition(style_hld['jsrq'].astype(str).unique().tolist()),table_name))
    # localdb.execute("delete from {1}hbs_size_exp where jsrq in ({0})  "
    #                 .format(util.list_sql_condition(size_hld['jsrq'].astype(str).unique().tolist()),table_name))
    # localdb.execute("delete from {1}hbs_9_lables_exp where jsrq in ({0})  "
    #                 .format(util.list_sql_condition(lable_hld['jsrq'].astype(str).unique().tolist()),table_name))
    # style_hld.to_sql(table_name + 'hbs_style_exp', index=False, if_exists='append', con=localdb)
    # size_hld.to_sql(table_name + 'hbs_size_exp', index=False, if_exists='append', con=localdb)
    # lable_hld.to_sql(table_name + 'hbs_9_lables_exp', index=False, if_exists='append', con=localdb)

    # jjdm_list = util.get_885001_funds('20220831')
    # gh.save_style_exp2db(jjdm_list,start_date='20151231'
    #                      ,end_date='20220630',if_885001=True)
    # jjdm_list=['540007','530003','519752']
    # jjdm_list=util.get_mutual_stock_funds('20210630')
    # jjdm_list.sort()
    #
    jjdm_list = util.get_stock_funds_pool('20230630')
    # gh.get_hld_property("20200601", "20230630", add=False)
    # gh.get_hld_property("20200101", "20221231", add=False)
    # gh.get_hld_property("20190701", "20220630", add=False)
    # gh.get_hld_property("20190101", "20211231", add=False)
    # gh.get_hld_property("20180701", "20210630", add=False)
    # gh.get_hld_property("20180101", "20201231", add=False)
    # gh.get_hld_property("20170701", "20200630", add=False)
    # gh.get_hld_property("20170101", "20191231", add=False)
    # gh.get_hld_property("20160701", "20190630", add=False)
    # gh.get_hld_property("20160101", "20181231", add=False)
    # gh.get_hld_property("20150701", "20180630", add=False)
    # gh.get_hld_property("20150101", "20171231", add=False)
    # gh.get_hld_property("20140701", "20170630", add=False)
    # gh.get_hld_property("20140101", "20161231", add=False)
    # gh.get_hld_property("20130701", "20160630", add=False)
    # gh.get_hld_property("20130101", "20151231", add=False)
    # gh.get_hld_property("20120701", "20150630", add=False)
    # gh.get_hld_property("20120101", "20141231", add=False)
    # gh.get_hld_property("20110701", "20140630", add=False)
    # gh.get_hld_property("20110101", "20131231", add=False)
    # gh.get_hld_property("20100701", "20130630", add=False)


    # gh.save_holding_trading_2db(jjdm_list, '20100701', '20230630')
    # gh.get_holding_trading_analysis('20230630')
    # gh.get_holding_trading_analysis('20180629')
    # gh.get_holding_trading_analysis('20171229')
    # gh.get_holding_trading_analysis('20170630')
    # gh.get_holding_trading_analysis('20161230')
    # gh.get_holding_trading_analysis('20160630')
    # gh.get_holding_trading_analysis('20151231')
    # gh.get_holding_trading_analysis('20150630')
    # gh.get_holding_trading_analysis('20141231')
    # gh.get_holding_trading_analysis('20140630')
    # gh.get_holding_trading_analysis('20131231')
    # gh.get_holding_trading_analysis('20130628')





    # gh.ticker_contribution(jjdm_list, '20200601', '20230630')

    # gh.save_prv_style_exp2db(start_date='20191231',end_date='20230331')


    #
    # last_quarter = (datetime.datetime.strptime('20190304', '%Y%m%d') - datetime.timedelta(days=93)) \
    #     .strftime('%Y%m%d')
    # get the cleaning holding data
    # hld, new_jjdm_list = gh.fund_holding_date_manufacture(jjdm_list, last_quarter, '20220304')
    # hld.reset_index(drop=False,inplace=True)
    # hld.drop_duplicates(inplace=True)
    # hld.to_excel('hbs_raw_data.xlsx',encoding='gbk')
    #
    # hld.to_sql('hbs_raw_data',index=False,if_exists='append',con=localdb)


    #
    #ia=Industry_analysis()
    sa=Style_analysis()
    fre='Q'
    if_prv=False

    import warnings
    warnings.filterwarnings('ignore')
    asofdate='20230630'




    # print(asofdate)
    #ia.save_industry_property2localdb(asofdate=asofdate,time_length=3,if_prv=if_prv,fre=fre)
    #ia.save_industry_shift_property2localdb(asofdate=asofdate, time_length=3,if_prv=if_prv)


    # asofdate='20230831'

    # ia.save_industry_property2localdb(asofdate=asofdate,time_length=3,if_prv=if_prv,fre=fre)
    # ia.save_industry_shift_property2localdb(asofdate=asofdate, time_length=3,if_prv=if_prv)

    #sa.save_style_property2db(asofdate=asofdate, time_length=3,if_prv=if_prv,fre=fre)
    # sa.style_shift_analysis(asofdate=asofdate, time_length=3,if_prv=if_prv)



    #
    # industry_shift_table = 'hbs_industry_shift_property_new'
    # theme_shift_table = 'hbs_theme_shift_property_new'
    # collect_df=pd.read_excel(r"E:\GitFolder\hbshare\fe\mutual_analysis\industry_shit.xlsx")
    # collect_df['jjdm'] = '00000' + collect_df['jjdm'].astype(str)
    # collect_df['jjdm'] = collect_df['jjdm'].str[-6:]
    # collect_df_theme = pd.read_excel(r"E:\GitFolder\hbshare\fe\mutual_analysis\theme_shit.xlsx")
    # collect_df_theme['jjdm'] = '00000' + collect_df_theme['jjdm'].astype(str)
    # collect_df_theme['jjdm'] = collect_df_theme['jjdm'].str[-6:]
    # #
    # sql="delete from {1} where asofdate='{0}'".format(collect_df['asofdate'].iloc[0],industry_shift_table)
    # localdb.execute(sql)
    # collect_df.to_sql(industry_shift_table, index=False, if_exists='append', con=localdb)
    # sql="delete from {1} where asofdate='{0}'".format(collect_df_theme['asofdate'].iloc[0],theme_shift_table)
    # localdb.execute(sql)
    # collect_df_theme.to_sql(theme_shift_table, index=False, if_exists='append', con=localdb)


    #
    #
    # if (if_prv):
    #     if(fre=='M'):
    #         fre_table='_monthly'
    #     else:
    #         fre_table=''
    #     cen_shift_his_table = 'hbs_prv_cen_shift_ratio_his_industry{}'.format(fre_table)
    #     ind_porperty_table = 'hbs_prv_industry_property{}'.format(fre_table)
    #     theme_exp_his_table = 'hbs_prv_theme_exp{}'.format(fre_table)
    #
    # else:
    #     cen_shift_his_table = 'hbs_cen_shift_ratio_his_industry'
    #     ind_porperty_table = 'hbs_industry_property'
    #     theme_exp_his_table = 'hbs_theme_exp'
    #
    #
    # for i in range(3):
    #     sql = "delete from {2}_{1}_industry_level where asofdate='{0}'".format(asofdate, i + 1,ind_porperty_table)
    #     localdb.execute(sql)
    #     df = pd.read_csv("collectdf{0}.csv".format(i+1),encoding='gbk')
    #
    #     df['jjdm'] = '00000' + df['jjdm'].astype(str)
    #     df['jjdm'] = df['jjdm'].str[-6:]
    #     trunk_size = 1000
    #     for j in range(0, int(np.floor(len(df) / trunk_size) + 1)):
    #         df.iloc[j*trunk_size:(j+1)*trunk_size].to_sql('{1}_{0}_industry_level'.format(i + 1,ind_porperty_table), index=False, if_exists='append',
    #                            con=localdb)
    #
    #     #save the cen and shift ratio into local db
    #     ratio_his=pd.read_excel('ratio_his_{0}.xlsx'.format(str(i+1)))
    #     sql = "delete from {3}{0} where jsrq>='{1}' and jsrq<='{2}'" \
    #         .format(str(i + 1), ratio_his['jsrq'].min(), ratio_his['jsrq'].max(), cen_shift_his_table)
    #     localdb.execute(sql)
    #     ratio_his.to_sql('{1}{0}'.format(str(i + 1),cen_shift_his_table), con=localdb,
    #                                              if_exists='append', index=False)
    #
    # collect_df=pd.read_csv('collectdf.csv',encoding='gbk')
    #
    # collect_df['jjdm'] = '00000' + collect_df['jjdm'].astype(str)
    # collect_df['jjdm'] = collect_df['jjdm'].str[-6:]
    # sql = "delete from {1}_new where asofdate='{0}'".format(asofdate,ind_porperty_table)
    # localdb.execute(sql)
    # collect_df.to_sql('{0}_new'.format(ind_porperty_table), index=False, if_exists='append', con=localdb)
    #
    # theme_exp_his=pd.read_excel('theme_exp.xlsx')
    # theme_exp_his['jjdm']=[("000000"+str(x))[-6:] for x in theme_exp_his['jjdm']]
    # sql = "delete from {2} where jsrq>='{0}' and jsrq<='{1}'" \
    #     .format( theme_exp_his['jsrq'].min(), theme_exp_his['jsrq'].max(),theme_exp_his_table)
    # localdb.execute(sql)
    # theme_exp_his.to_sql(theme_exp_his_table, con=localdb,
    #                                               if_exists='append', index=False)


    #
    # change_ret, change_ret_nextq, \
    # industry_based_ret, term_based_ret = fc.change_analysis('000167', '20151231', '20211231')
    # ba.data_preparation(hld_compenzation=True)
    # ba.save_new_joinner_date2localdb()


    #
    # br = Brinson_ability()
    # sql = "select distinct tjrq from st_fund.r_st_hold_excess_attr_df where tjrq>'20171229' "
    # tjrq_list=hbdb.db2df(sql,'funduser')['tjrq'].tolist()
    # tjrq_list=['20211231']
    # for tjrq in tjrq_list:
    #     br.classify_socring(tjrq)

    #plot the pic of fund trading point per stock
    # #
    # stt=Stock_trade_timing()
    # ticker = '600309'
    # threshold=3
    # buydf, selldf,buydfgs, selldfgs, buypicdf, sellpicdf,buypicdfgs, sellpicdfgs  = stt.data_factory(ticker,threshold)
    #
    # target_jsrq_list = buydf[buydf['ryxm'].str.contains('国富')]['jsrq'].unique().tolist()
    # print("目标买入时点："+util.list_sql_condition(target_jsrq_list))
    #
    # plot = functionality.Plot(1200, 600)
    # plot.plotly_line_with_annotation(buypicdf, data_col=['SPJG'], anno_col=['jjdm'], title_text='基金买入时序图_by基金经理')
    # plot.plotly_line_with_annotation(sellpicdf, data_col=['SPJG'], anno_col=['jjdm'], title_text='基金卖出时序图_by基金经理')
    # plot.plotly_line_with_annotation(buypicdfgs, data_col=['SPJG'], anno_col=['jjdm'], title_text='基金买入时序图_by基金公司')
    # plot.plotly_line_with_annotation(sellpicdfgs, data_col=['SPJG'], anno_col=['jjdm'], title_text='基金卖出时序图_by基金公司')
    #
    # plot = functionality.Plot(500, 200)
    # plot.plotly_table(buydf.rename(columns={'jsrq': '进入时点'}), 500, 'buy')
    # plot.plotly_table(selldf.rename(columns={'jsrq': '离开时点'}), 500, 'sell')
    # plot.plotly_table(buydfgs.rename(columns={'jsrq': '进入时点'}), 500, 'buy')
    # plot.plotly_table(selldfgs.rename(columns={'jsrq': '离开时点'}), 500, 'sell')

    # df=pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\Cache\File\2022-05\无标题.xlsx")
    #
    #
    # df['date'] = [datetime.datetime.strptime(str(x), '%Y%m%d') for x in df['trade_date']]
    # max_date=(df.groupby('jjdm').max()['trade_date']).reset_index().rename(columns={'trade_date':'max'})
    # min_date = (df.groupby('jjdm').min()['trade_date']).reset_index().rename(columns={'trade_date':'min'})
    # df.drop_duplicates(['jjdm','trade_date'],inplace=True)
    # df['fre']=df['date']-df['date'].shift(1)
    # df['fre']=df['fre'].fillna('0 days')
    # df['fre']=[int(str(x).split(' days')[0]) for x in df['fre']]
    # df.drop_duplicates(['jjdm'], inplace=True,keep='last')
    # df=pd.merge(df,max_date,how='left',on='jjdm')
    # df = pd.merge(df, min_date, how='left', on='jjdm')
    # df=pd.merge(df,prv_info,how='left',on='jjdm')
    # df[['jjdm','jjjc','fre','max','min']].to_excel('AMS_summary.xlsx')
    #
    # print('')