import sys
import urllib.request
import urllib.error

class DocumentAcquisitionApi:
    """
    書類取得APIに相当するクラス
    """
    
    def __init__(self, api_key) -> None:
        self.endpoint = "https://api.edinet-fsa.go.jp/api/v2/documents/"
        self.api_key = api_key

    def download(self, doc_id, savepath, data_type=5):
        #data_type: 1:XBRL, 2:PDF, 3:代替書面・添付文書, 4:英文ファイル, 5:CSV
        url = f'{self.endpoint}/{doc_id}?&type={data_type}&Subscription-Key={self.api_key}'
        try:
            with urllib.request.urlopen(url) as res:
                content         =   res.read()
                with open(savepath, 'wb') as fp_out:
                    fp_out.write(content)
        
        except urllib.error.HTTPError as e:
            if e.code != 200:
                sys.stderr.write(e.reason+'\n')
            else:
                raise e


