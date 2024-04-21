
import sys,os,re,json
import datetime
import time
import urllib.request
import urllib.error
from dotenv import load_dotenv
from datetime import timedelta
from tqdm import tqdm
from pathlib import Path

from DocumentListApi import DocumentListApi
from DocumentAcquisitionApi import DocumentAcquisitionApi

# Specify the path of the .env file to read
load_dotenv = ('../.env')

# get api key
# API_KEY = os.getenv('api_val')
API_KEY = '363e4ec24f444bf194e4db503c3b4879'
print(f'api:{API_KEY}')

def main():
    try:
        # Edinetコードの入力受付
        print("Enter edinet code. [Exxxxxx]")
        edinet_code = ['E00006','E01765']

        doc_indice = []
        filername = ""

        # year, month, day = map(int, input("Enter a date in the format 'YYYY M D': ").split())

        # dateオブジェクトを作成する
        this_date = datetime.date(2022, 3, 31)

        # ユーザーからの入力を受け取る
        # year, month, day = map(int, input("Enter a date in the format 'YYYY M D': ").split())

        # dateオブジェクトを作成する
        date_to = datetime.date(2023, 4, 1)

        doc_list_api = DocumentListApi(API_KEY)
        print("searching...")
        doc_dict = doc_list_api.get_document_indice_filername(edinet_code, this_date, date_to)
        print("searched.")
        for doc in doc_dict.keys():
            # 会社名とドキュメントidを取得
            doc_indice = doc_dict[doc]["docID"]
            filername = doc_dict[doc]['filerNamefilerName']
            
            # 文書番号一覧を取得
            data_dpath = os.path.join(Path(__name__).absolute().parent.parent, "data", filername)
            doc_indice_fpath = os.path.join(data_dpath, "doc_indice.txt")
            filername_fpath = os.path.join(data_dpath, "filername.txt")

            if len(doc_indice) <= 0:
                print("no data was found.")
                raise Exception()

                # フォルダを作成
            if os.path.exists(data_dpath) == False:
                os.mkdir(data_dpath)
                print(f"create directory: {data_dpath}")

                raw_dpath = os.path.join(data_dpath, "00_raw")
                os.mkdir(raw_dpath)
                print(f"create directory: {raw_dpath}")

                dst_dpath = os.path.join(data_dpath, "01_dst")
                os.mkdir(dst_dpath)
                print(f"create directory: {dst_dpath}")

                with open(filername_fpath, "w", encoding="utf8") as f:
                    f.write(filername)
                print(f"save file: {filername_fpath}")
                
                with open(doc_indice_fpath, "w", encoding="utf8") as f:
                    for doc_id in doc_indice:
                        f.write(f"{doc_id}\n")
                print(f"save file: {doc_indice_fpath}")

        # 文書を取得
        doc_acq_api = DocumentAcquisitionApi(API_KEY)
        data_type = 1#1:xbrl, 2:pdf, 5:csv
        ext = "pdf" if data_type == 2 else "zip"
        for doc_id in doc_indice:
            doc_fname = f"{doc_id}_{data_type}.{ext}"
            doc_fpath = os.path.join(data_dpath, "00_raw", doc_fname)
            doc_acq_api.download(doc_id, doc_fpath, data_type)

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()