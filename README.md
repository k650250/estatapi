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
|2021-06-27|予め`estatapi.appId`にアプリケーションIDを指定しておけば、`StatsData`等の第2引数を省略することができるようにした。|
|2021-07-01|1. 第2引数の値<br />2. ホームディレクトリの「.estatapi」ディレクトリの「appId」ファイルの値<br />3. 環境変数「ESTATAPI_APP_ID」の値<br />の優先度でアプリケーションIDを読み込むようにした。<br />ホームディレクトリのに関しては、`estatapi.set_appId`関数を介して設定が可能。|
