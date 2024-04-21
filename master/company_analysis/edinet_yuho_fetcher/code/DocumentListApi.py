import json
import datetime
import urllib.request
import urllib.error
from tqdm import tqdm

class DocumentListApi:
    """
    書類一覧APIに相当するクラス
    """

    def __init__(self, api_key) -> None:
        self.endpoint = "https://api.edinet-fsa.go.jp/api/v2/documents.json"
        self.api_key = api_key

    def get_document_indice_filername(self, edinet_code: list, this_date: datetime, date_to: datetime):
        # edinet_code_dictを空の辞書として初期化
        edinet_code_dict = {}
        edinet_code_dict = {key: val for key, val in zip(edinet_code, [{"filerName":'',"docID":[]} for _ in range(len(edinet_code))])}
        date_l = self._get_datelist(this_date, date_to)
        for s_date in tqdm(date_l):
            for edinet_code in edinet_code_dict.keys():
                doc_meta = self._get_doc_metadata(edinet_code, s_date)
                if doc_meta == None:
                    continue
                edinet_code_dict[edinet_code]["docID"].append(doc_meta["docID"])
                edinet_code_dict[edinet_code]["filerNamefilerName"] = doc_meta["filerName"]
        
        return edinet_code_dict

    def _get_doc_metadata(self, edinet_code, date):
        url = f'{self.endpoint}?date={date}&type={2}&Subscription-Key={self.api_key}'
        # res = utils.get_with_sleep(url)
        try:
            with urllib.request.urlopen(url) as res:
                j_res = json.loads(res.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code != 200:
                print(e.reason)
            else:
                raise e
        docs = j_res["results"]
        f_docs = [doc for doc in docs if doc["edinetCode"] == edinet_code and "有価証券報告書" in doc["docDescription"]]
        if len(f_docs) <= 0:
            # print("no data was found.")
            return None

        # print(f"{len(f_docs)} document was found.")
        return f_docs[0]
    
    def _get_datelist(self,this_date, date_to):
        
        date_l = []
        while this_date <= date_to:
            this_date += datetime.timedelta(days=1)
            date_l.append(this_date.strftime("%Y-%m-%d"))
        return date_l
    

    