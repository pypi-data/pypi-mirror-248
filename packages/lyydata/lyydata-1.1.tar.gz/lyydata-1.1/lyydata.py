import os
import pandas as pd
import time
from pytdx.hq import TdxHq_API
import pandas as pd
import lyywmdf
from lyylog import log


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


def Get_df_1by1(code, server_ip, kline_n, db_last_date_int, debug=False):
    global today_time_hour
    try:

        print("# 初始化api连接,", code)
        #except Exception as e:
        #print("process_code_entry first error", e)
        global api_dict
        if server_ip not in api_dict.keys():
            api = TdxHq_API(multithread=False, heartbeat=False, auto_retry=True)
            api_dict[server_ip] = api
            api_dict[server_ip].connect(server_ip, 7709)
            # api = initialize_api(server_ip)
        # api = api_dict[server_ip]
        if debug:
            print("initserverip", server_ip)
        # 获得某个代码的wmdf

        wmdf = lyywmdf.wmdf(api_dict[server_ip], code, kline_n, server_ip=server_ip, debug=debug)
        if wmdf is None:

            raise Exception("wmdf is None")

        if debug:
            log("finish get wmdf")
        wmdf['code'] = code
        wmdf = df_add_notfull(wmdf, today_date_int)
        wmdf = wmdf.drop(wmdf.index[0]).reset_index(drop=True)
        print(wmdf)

        filtered_df = wmdf[wmdf['day'] > db_last_date_int]

        return filtered_df

    except Exception as e:
        log("process_code_entry error" + str(e))
        return pd.DataFrame()
    finally:
        pass
