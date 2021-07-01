# estatapi
**[政府統計の総合窓口（ｅ－Ｓｔａｔ）](https://www.e-stat.go.jp/)のAPI**を介して統計データを取得する為のPythonモジュールです。

|ファイル名|説明|
|:-|:-|
|estatapi.py|モジュール|
|sample_google.ipynb|モジュールの使用例（Google Colaboratory版）|

## 更新履歴

|日付|説明|
|:-|:-|
|2021-04-18|初版。|
|2021-06-27|予め`estatapi.appId`にアプリケーションIDを指定しておけば、`estatapi.StatsData`系列の第2引数を省略することができるようにした。|
|2021-07-01|<ol><li>`estatapi.StatsData`系列の第2引数の値</li><li>ホームディレクトリの「.estatapi」ディレクトリの「appId」ファイルの値</li><li>環境変数「ESTATAPI_APP_ID」の値</li></ol>の優先度でアプリケーションIDを読み込むようにした。<br />2に関しては、`estatapi.set_appId`関数を介して設定が可能。|
