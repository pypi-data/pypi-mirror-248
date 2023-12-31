import os
import pandas as pd
import time
from pytdx.hq import TdxHq_API
import pandas as pd
import lyywmdf
from lyylog import log
from datetime import datetime
from sqlalchemy import text
import lyytools
import lyycalendar
from tqdm import tqdm
import lyybinary
import lyystkcode
ins_lyycalendar = lyycalendar.lyycalendar_class()
import traceback
api_dict = {}
signal_id_dict={"昨日换手": 777, "昨日回头波": 776}  #,"涨停原因":888
column_mapping = {'时间': 'datetime', '代码': 'code', '名称': 'name', '开盘': 'open', '今开': 'open', '收盘': 'close', '最新价': 'close', '最高': 'high', '最低': 'low', '涨跌幅': 'change_rate', '涨跌额': 'change_amount', '成交量': 'vol', '成交额': 'amount', '振幅': 'amplitude', '换手率': 'turnover_rate'}
df_all_info = lyystkcode.get_all_codes_dict_em().rename(columns=column_mapping)
dict_all_code_guben = df_all_info.set_index('code')['流通股本亿'].to_dict()


def update_mysql_from_wmdf(df,engine=None,debug=False):
    debug=True
    if debug: print("enter update_mysql_from_wmdf")
    table_name = "stock_wmdf_test"
    # 从 MySQL 中读取数据
    if engine is None:
        import lyycfg
        if debug: print("engine is None, try to get from lyycfg")
        engine, conn, _ = lyycfg.con_aliyun_sqlalchemy()
    if debug: print(f"reading table from table:{table_name}")
    df_mysql = pd.read_sql(f'SELECT * FROM {table_name}', engine)

    if debug: print("# 获取每个 code 的 dayint 的最大值")
    
    max_dayint_dict = df_mysql.groupby('code')['dayint'].max().to_dict()
    print(max_dayint_dict)
    # 对 df 进行分组，然后筛选出 dayint 大于对应 code 的最大值的行
    def filter_rows(group):
        code = group.name
        return group[group['dayint'] > max_dayint_dict.get(code, -1)]
    
    if debug: print("筛选出 dayint 大于对应 code 的最大值的行")
    df_filtered = df.groupby('code').apply(filter_rows)
    ungrouped_df = df_filtered.reset_index(drop=True)

    if debug:("筛选成功，# 将结果写入到 MySQL 中")
    sql_columns = ["code",  "day",  "open",  "high",  "close",  "low",  "volume",  "up",  "tenhigh",  "chonggao",  "huitoubo",  "notfull",  "dayint"]
    df_towrite = ungrouped_df[sql_columns]
    print(df_towrite)
    df_towrite.to_sql(f'{table_name}', engine, if_exists='append',index=False)
    

def update_cg_series(df,debug=False):
    if len(df)<10000:
        print("dataframe<1000 line，check it")
    debug=True
    df_grouped = df.groupby("code")
    for code,group_rows in df_grouped:
        if debug: print("enter for code,group_rows in df_grouped")
        market = lyystkcode.get_market(code)
        tdx_signal_file = os.path.join(r"D:\SOFT\_Stock\Tdx_202311", rf"T0002\signals\signals_user_{999}", f"{market}_{code}.dat")
        db_last_date_int = lyybinary.get_lastdate_tdx_sinal(tdx_signal_file)
        if debug: print(f"try to filter: group_rows['dayint'] > {db_last_date_int}")
        filtered_rows = group_rows[group_rows['dayint'] > db_last_date_int]
        if debug:print(filtered_rows)
        data_dict = filtered_rows.set_index('dayint')['chonggao'].to_dict()

        if debug:print(tdx_signal_file,  db_last_date_int, "db_last_date_int type=", type(db_last_date_int))
        lyybinary.add_data_if_new_than_local(tdx_signal_file, data_dict, db_last_date_int, debug=debug)
        if debug:print("写入文件成功")
    

def update_signal_txt(df):
    grouped_df = df.groupby('code')
    # chonggao_dict = grouped_df['chonggao'].apply(lambda x: x.iloc[-1]).to_dict()
    # huitoubo_dict = grouped_df['huitoubo'].apply(lambda x: x.iloc[-1]).to_dict()
    
    df_reason = get_ztreason_df
    df_chonggao  =  grouped_df.apply(lambda  x:  pd.DataFrame([{'market':  lyystkcode.get_market(x['code']), 'code':  x['code'],'signal_id':  '666','text':'','number':  x['chonggao'].iloc[-1]}]))
    df_huitoubo = grouped_df.apply(lambda  x:  pd.DataFrame([{'market':  lyystkcode.get_market(x['code']), 'code':  x['code'],'signal_id':  '665','text':'','number':  x['chonggao'].iloc[-1]}]))
    # df = df[(df['signal_id'] != "665") & (df['signal_id'] != "666")]
    # df = pd.DataFrame(columns=['market', 'code', 'signal_id', 'text', 'number'], dtype=str)
    # df2 = pd.DataFrame(all_signals_lists, columns=['market', 'code', 'signal_id', 'number'], dtype=str)
    # df2['text'] = ""
    df_merged = pd.concat([df_chonggao, df_huitoubo,df_reason], axis=0, ignore_index=True)
    # df_merged = df_merged.dropna(subset=['code'])
    df_merged.reset_index(inplace=True, drop=True)
    # bool_series = df_merged['code'] != "0.000"
    # df_merged = df_merged[bool_series].dropna(subset=['code'])
    df_merged = df_merged.applymap(lambda x: x.encode('gbk', errors="ignore").decode('gbk') if isinstance(x, str) else x)
    path = r"D:\Soft\_Stock\Tdx_202311\T0002\signals\extern_user.txt"
    df_merged.to_csv(path, index=False, header=False, sep='|', encoding='gbk')


    pass


def get_ztreason_df():
    # 从数据库中读取股票代码
    engine, conn, session = lyycfg.con_aliyun_sqlalchemy()
    query = text("SELECT * as count FROM stock_jiucai WHERE  date > 20231001")
    query = """SELECT * FROM (SELECT *,ROW_NUMBER() OVER (PARTITION BY code ORDER BY date DESC) AS rn FROM stock_jiucai WHERE date >= DATE_SUB(CURDATE(), INTERVAL 20 DAY)) AS subquery WHERE rn = 1 """
    result = pd.read_sql(query, engine)
    # 获取数量
    result['code'] = result['code'].apply(lambda x: str(x).zfill(6))
    result['signal_id'] = "888"
    result['number'] = 0.000
    result['text'] = result.apply(lambda row: str(row['plate_name']) + '：' + str(row['reason']).replace("\n", ""), axis=1)
    result['market'] = result.code.apply(lambda x: lyystkcode.get_market(x))
    return_df = result[['market', 'code', 'signal_id', 'text', 'number']]
    print(return_df)
    return return_df

def 获取昨换手和回头波(item, debug=False):
    print("#查询计算相应股票代码对应的数据")
    code, server_ip = item
    api = lyywmdf.initialize_api(server_ip)
    code = str(code).zfill(6)
    market = lyystkcode.get_market(code)
    last_trade_day = ins_lyycalendar.最近完整收盘日(0)
    print("last_trade_day=", "------------------", last_trade_day)
    last_trade_day_str = str(last_trade_day)[:4] + "-" + str(last_trade_day)[4:6] + "-" + str(last_trade_day)[6:8]
    print("last_trade_day=", last_trade_day, 9, market, code)
    # df01 = api.to_df(api.get_security_bars(9, 0, "000001", 0, 1))
    # print("df01=", df01)
    K_number = 2 if datetime.now().hour < 9 else 1
    df = api.to_df(api.get_security_bars(9, market, code, 0, K_number))

    # from mootdx.quotes import Quotes

    # client = Quotes.factory(market='std')
    # df = client.bars(symbol=code, frequency=9, offset=10)
    print("dataframe=", df)
    data_dict = df.iloc[0].to_dict()

    print("r=", data_dict)

    # turn_dict = lyystkcode.get_bjs_liutongguben_dict()

    # 流通股本 = float(turn_dict[code])
    vol = data_dict['vol'] / pow(10, 6)

    # 流通市值 = round(流通股本 * data_dict['close'], 2)
    # print("流通股本=", 流通股本, "流通市值=", 流通市值)
    流通股本 = dict_all_code_guben[str(code)]
    换手 = round(vol / 流通股本, 2)

    turn_list = [market, code, 666, 换手]

    close = data_dict['close']
    print("close=", close)
    amount = data_dict['amount']

    high = data_dict['high']
    print("high=", high)

    huitoubo = (close - high) / high
    print("huitoubo=", huitoubo)
    huitoubo_list = [market, code, 665, round(huitoubo, 2)]
    debug = True
    if debug: print("turn_list=", turn_list, ",huitoubo_list=", huitoubo_list)
    return turn_list, huitoubo_list


def update_wmdf(wmdf, stkcode_list, server_list, last_date_dict, q=None, debug=False):
    df_list = [wmdf]
    code_server_dict = lyytools.assign(stkcode_list, server_list)
    print("code_server_dict=", code_server_dict)
    pbar = tqdm(range(100))
    for index, (code, server_ip) in enumerate(code_server_dict.items()):
        # print("code=", code, type(code))
        # print(last_date_dict.keys())
        # for i in (last_date_dict.keys()):
        #     print(i, type(i))
        if code in last_date_dict.keys():
            if debug: print("code in last_date_dict.keys()")
            db_last_date_int = last_date_dict[code]
            相差天数 = ins_lyycalendar.计算相隔天数_byIndex(db_last_date_int, ins_lyycalendar.最近完整收盘日())
            if debug: print("found 相差天数from dict", 相差天数)
        else:
            if debug: log(f"code={code} not in last_date_dict.keys()")
            db_last_date_int = ins_lyycalendar.tc_before_today(49)
            相差天数 = 49
        kline_n = min((相差天数 + 2) * 16,800)
        if 相差天数==0:#直接跳过返回。
            continue
        
        try:
            if debug: print("code=",code,",server_ip=", server_ip,",last_date=", db_last_date_int, "相差天数=",相差天数,"kline_n=", kline_n)
            df_single = get_and_format_wmdf_for_single_code(code, server_ip, db_last_date_int, kline_n, debug=False)  #(code, server_ip, kline_n, db_last_date_int, debug=False):
            print(df_single,"df_single")
        except Exception as e:
            traceback.print_exc()
        if debug: print("finish codd=", code)
        if len(df_single)>0:
            df_list.append(df_single)
        else:            #raise Exception("df_single is empty")
            if debug: log(f"{code}@{server_ip} df_single is empty")
        if index % 53 == 0:
            pbar.update(1)
        df_single.rename(columns={'day':  'dayint'},  inplace=True)
        df_single['day']=df_single['dayint'].apply(lambda x:str(x)[0:4]+"-"+str(x)[4:6]+"-"+str(x)[6:8])

    wmdf = pd.concat(df_list)
    print(wmdf)
    pbar.close()

    if q is not None:
        q.put(wmdf)
    else:
        return wmdf



def read_data_from_sql(table_name="stock_wmdf_test", conn=None, debug=True):
    if conn is None:
        import lyycfg
        engine, conn,_=lyycfg.con_aliyun_sqlalchemy()
    # 构建SQL查询语句
    sql_query = f"SELECT * FROM {table_name} "
    # 通过数据库连接执行SQL查询，并将结果存储到DataFrame
    df = pd.read_sql_query(sql_query, conn)
    return df

def get_wmdf_last_date(q=None):
    print("enter datacenter")
    old_df = lyytools.get_data_from_cache_or_func("stock_wmdf.pkl", 3600 * 8, read_data_from_sql, debug=True)
    # del old_df['dayint']
    # old_df['day']=old_df['day'].apply(lambda x:int(str(x).replace("-",""))).astype(int)
    # del old_df['id']
    # old_df.to_pickle("stock_wmdf.pkl")
    # print(old_df,"dfasfd")

    # time.sleep(3333)
    # if "dayint" not in old_df.columns:
    #     old_df['dayint']=old_df['day'].apply(lambda x:int(str(x).replace("-","")))
    #     old_df.to_pickle("stock_wmdf.pkl")
    print("try to ogg in get wmdf last date")
    grouped = old_df.groupby("code").agg({'dayint': 'max'})
    last_date_dict = grouped['dayint'].to_dict()
    print(last_date_dict)
    if q is not None:
        q.put((old_df, last_date_dict))
    else:
        return old_df,last_date_dict

def get_data_from_cache_or_func(cache_file_path, expiry_duration, next_func=None, debug=False):
    # 检查文件是否存在,expiry_duration=3600意味着1小时。
    if os.path.isfile(cache_file_path):
        if debug: print("file exists, check expiry duration")
        # 获取文件的最后修改时间
        last_modified_time = os.path.getmtime(cache_file_path)
        # 计算当前时间与最后修改时间的差值（秒）
        current_time = time.time()
        time_difference = current_time - last_modified_time
        if time_difference < expiry_duration:
            df = pd.read_pickle(cache_file_path)
            if debug: print(f"{cache_file_path} not expired, return it, =\n", df)
            return df
    #all else:
    if next_func is not None:
        return next_func()
    else:
        return None


def df_add_notfull(df, haveto_date):
    """
    添加一列notfull。先统一设置为15，然后如果下载到了今天的数据，今天却没收盘，则把今天（也就是最大值这天）的notfull为循环最初的小时。
    """
    now = datetime.now()
    today_date_int = now.year * 10000 + now.month * 100 + now.day
    # 先将'day'列转化为整数,方便匹配haveto_date
    df.loc[:, 'day'] = df['day'].apply(lambda x: int(str(x).replace("-", "")))
    df['notfull'] = 15
    # print("dfmax == today_date_int=<"+str(df["day"].max == today_date_int)+">", today_time_hour < 15, df["day"].max == today_date_int and today_time_hour < 15)
    if df["day"].max() == today_date_int and now.hour < 15:
        print("今天 没收盘，要重点标记一下。today_time_hour=", now.hour, "today_date_int=", today_date_int)
        df.loc[df['day'] == today_date_int, 'notfull'] = now.hour
    else:
        print("完美收盘无需牵挂", end="")
    return df


def get_and_format_wmdf_for_single_code(code, server_ip, db_last_date_int,kline_n,  debug=False):
    now = datetime.now()
    today_date_int = now.year * 10000 + now.month * 100 + now.day
    if debug:print("# 初始化api连接,", code)
    #except Exception as e:
    #print("process_code_entry first error", e)
    global api_dict
    if server_ip not in api_dict.keys():
        if debug: print("server_ip not in api_dict, connect it")
        api = TdxHq_API(multithread=False, heartbeat=False, auto_retry=True)
        api_dict[server_ip] = api
        api_dict[server_ip].connect(server_ip, 7709)
        # api = initialize_api(server_ip)
    else:
        api=api_dict[server_ip]
        if debug:print("tdx api already in dict.")
    # api = api_dict[server_ip]
    if debug:
        print("initserverip", server_ip)
    if debug: print("# 获得某个代码的wmdf")
    try:
        wmdf = lyywmdf.wmdf(api, code, kline_n,server_ip=server_ip, debug=debug)
    except Exception as e:
        traceback.print_exc()
    if wmdf is None:
        raise Exception("wmdf is None")
    wmdf['code'] = code
    wmdf = df_add_notfull(wmdf, today_date_int)
    wmdf = wmdf.drop(wmdf.index[0]).reset_index(drop=True)
    print(wmdf.columns)
    print(wmdf.tail(1))

    filtered_df = wmdf[wmdf['day'] > db_last_date_int]
    
    return filtered_df

    #except Exception as e:
    #     log("process_code_entry error" + str(e))
    #     return pd.DataFrame()
    # finally:
    #     pass


if __name__ == '__main__':
    import lyymysql
    import lyycfg,lyystkcode
    engine,conn,_ = lyycfg.con_aliyun_sqlalchemy()
    instance_lyymysql = lyymysql.lyymysql_class(engine)
    df = lyystkcode.get_all_codes_dict_em()
    stkcode_list = df['代码'].to_list()
    server_list = lyywmdf.perfact_new_fast_server_list(nextfuntion=instance_lyymysql.get_tdx_server_list)
    df_old, last_date_dict=get_wmdf_last_date()
    df=update_wmdf("",stkcode_list,server_list,last_date_dict)
    print(df)
    print("start lyydata")
