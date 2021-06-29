# -*- coding: utf-8; -*-

import gzip
import urllib.request
import json
import pandas

appId = str(None)

class StatsData:
    """\
    このサービスは、政府統計総合窓口(e-Stat)のAPI機能を使用していますが、サービスの内容は国によって保証されたものではありません。
    
    e-Stat-APIを介して統計データを取得し、これを保持する。

    Parameters
    ----------
    url : str
        APIのURLを指定する。
    appId : str
        APIのアプリケーションIDを指定する。
    data : dict, default None
        取得済みデータを指定する。
        未指定 (`None`) の場合、APIにより統計データを取得し、
        これを当該個体 (instance) の `data` プロパティに登録する。

    Examples
    --------
    個体生成から、取得したデータの代入迄を一気通貫で行う。

    >>> data = StatsData('url', 'appId').data

    上記を最大3段階の手続きに分割できる。

    >>> obj = StatsData('url', 'appId', data={})  # 1. 個体生成
    >>> obj.load()                          # 2. APIにより統計データを取得
    >>> data = obj.data                     # 3. 取得した統計データの代入
    """

    def __init__(self, url: str, appId: str=None, data: dict=None):
        self.url = url
        self.appId = appId
        if appId is None:
            self.appId = globals()['appId']
        self.data = data
        if data is None:
            self.load()

    def load(self):
        """\
        e-Stat-APIにより統計データを取得し、
        これを当該個体の `data` プロパティに登録する。
        """
        url = self.url
        url = url.replace('http:', 'https:')
        url = url.replace('appId=', 'appId=' + self.appId)
        if not '/app/json/' in url:
            url = url.replace('/app/', '/app/json/')

        request = urllib.request.Request(url, headers={'Accept-Encoding': 'gzip'}) 

        with urllib.request.urlopen(request) as r:
            gzipFile = gzip.GzipFile(fileobj=r) 
            self.data = json.loads(gzipFile.read().decode('utf8'))

class StatsDataForPandas(StatsData):
    """\
    このサービスは、政府統計総合窓口(e-Stat)のAPI機能を使用していますが、サービスの内容は国によって保証されたものではありません。
    
    e-Stat-APIを介して統計データを取得し、これを保持する。
    当該個体 (instance) の `to_df` メソッドで`DataFrame`に変換できる。

    Parameters
    ----------
    url : str
        APIのURLを指定する。
    appId : str
        APIのアプリケーションIDを指定する。
    data : dict, default None
        取得済みデータを指定する。
        未指定 (`None`) の場合、APIにより統計データを取得し、
        これを当該個体の `data` プロパティに登録する。
    names : dict, default None
        置換辞書を指定する。
        未指定 (`None`) の場合、当該個体の `data` プロパティの値を元に
        置換辞書を生成し、これを当該個体の `names` プロパティに登録する。

    Examples
    --------
    個体生成から、置換済DataFrameの取得迄を一気通貫で行う。

    >>> df = StatsDataForPandas('url', 'appId').to_df()

    上記を最大6段階の手続きに分割できる。

    >>> obj = StatsDataForPandas('url', 'appId', data={}, names={})  # 1. 個体生成
    >>> obj.load()                          # 2. APIにより統計データを取得
    >>> obj.make_names()                    # 3. 置換辞書を生成
    >>> df1 = obj.to_df(names={})           # 4. 未置換DataFrameを取得
    >>> df2 = obj.code2name(df1)            # 5. code形式からname形式にデータ値置換
    >>> df3 = obj.id2name(df2)              # 6. id形式からname形式に列名置換

    code/id形式及びname形式を混在させる。

    >>> import numpy as np
    >>> import pandas as pd
    >>> obj = StatsDataForPandas('url', 'appId')
    >>> df_vcode = obj.to_df(names={})      # 未置換DataFrameを取得
    >>> df_vname = obj.to_df()              # 置換済DataFrameを取得
    >>> columns = np.empty(len(df_vcode.columns)*2, dtype=np.object)
    >>> columns[0::2] = df_vcode.columns
    >>> columns[1::2] = df_vname.columns
    >>> columns = pd.Series(columns).drop_duplicates()
    >>> df = pd.merge(df_vcode, df_vname).loc[:, columns]
    """

    def __init__(self, url: str, appId: str=None, data: dict=None, names: dict=None):
        super().__init__(url, appId, data)
        self.names = names
        if names is None:
            self.make_names()

    def make_names(self):
        """\
        当該個体の `data` プロパティの値を元に置換辞書 (`names`) を生成し、
        これを同個体の `names` プロパティに登録する。
        但し、同個体の `data` プロパティの値が空 (`{}`) の場合、処理を行わない。
        """
        if not self.data:
            return
        self.names = dict(id=dict(), code=dict())
        for obj in self.data['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ']:
            obj_id = '@' + obj['@id']
            if isinstance(obj['CLASS'], dict):
                self.names['id'][obj_id] = obj['@name']
                self.names['code'][obj_id] = {obj['CLASS']['@code']: obj['CLASS']['@name']}
            else: # list
                self.names['id'][obj_id] = obj['@name']
                self.names['code'][obj_id] = dict()
                for cat in obj['CLASS']:
                    self.names['code'][obj_id][cat['@code']] = cat['@name']

    def to_df(self, names: dict=None) -> pandas.core.frame.DataFrame:
        """\
        当該個体の `data` プロパティの値を元に、`DataFrame`を生成する。
        その際、指定された置換辞書 (`names`) の値を元に、
        `DataFrame`のデータ値及び列名をcode/id形式からname形式に置換する。

        Parameters
        ----------
        names : dict, default None
            `DataFrame`の各値及び列名を変換する際に使用する置換辞書を指定する。
            置換辞書が未指定 (`None`) の場合、当該個体の `names` プロパティの値を使用する。
            置換辞書が空 (`{}`) の場合、`DataFrame`のデータ値及び列名を置換しない。

        Returns
        -------
        pd.DataFrame
            `DataFrame`が返却される。
        """
        df = pandas.json_normalize(self.data['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE'])
        self.code2name(df, names, inplace=True)
        self.id2name(df, names, inplace=True)
        return df

    def code2name(self, df: pandas.core.frame.DataFrame, names: dict=None, inplace: bool=False) -> pandas.core.frame.DataFrame:
        """\
        指定された置換辞書 (`names`) の `code` キーの値を元に、
        `DataFrame`のデータ値をcode形式からname形式に置換する。
        但し、`DataFrame`の列名がid形式でなければならない。

        Parameters
        ----------
        df : pd.DataFrame
            置換対象`DataFrame`指定する。
        names : dict, default None
            置換辞書を指定する。
            置換辞書が未指定 (`None`) の場合、当該個体の `names` プロパティの値を使用する。
            置換辞書が空 (`{}`) の場合、`DataFrame`のデータ値を置換しない。
        inplace : bool, default False
            `False`（default）の場合、置換対象`DataFrame`（引数`df`の値）は変更されず、
            新しい`DataFrame`が返却される。
            `True`の場合、置換対象`DataFrame`が変更される。

        Returns
        -------
        pd.DataFrame or None
            引数`inplace`の値が`False`、かつ置換辞書が有効な値である場合、
            `DataFrame`が返却される。
        """
        if names is None:
            names = self.names
        if 'code' in names:
            return df.replace(names['code'], inplace=inplace)

    def id2name(self, df: pandas.core.frame.DataFrame, names: dict=None, inplace: bool=False) -> pandas.core.frame.DataFrame:
        """\
        指定された置換辞書 (`names`) の `id` キーの値を元に、
        `DataFrame`の列名をid形式からname形式に置換する。

        Parameters
        ----------
        df : pd.DataFrame
            置換対象`DataFrame`を指定する。
        names : dict, default None
            置換辞書を指定する。
            置換辞書が未指定 (`None`) の場合、当該個体の `names` プロパティの値を使用する。
            置換辞書が空 (`{}`) の場合、`DataFrame`の列名を置換しない。
        inplace : bool, default False
            `False`（default）の場合、置換対象`DataFrame`（引数`df`の値）は変更されず、
            新しい`DataFrame`が返却される。
            `True`の場合、置換対象`DataFrame`が変更される。

        Returns
        -------
        pd.DataFrame or None
            引数`inplace`の値が`False`、かつ置換辞書が有効な値である場合、
            `DataFrame`が返却される。
        """
        if names is None:
            names = self.names
        if 'id' in names:
            return df.rename(columns=names['id'], inplace=inplace)
