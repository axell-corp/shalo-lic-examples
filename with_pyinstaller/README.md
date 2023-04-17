# pyinstaller で同梱される Python スクリプトを SHALO LICENSING で暗号化する

pyinstaller で実行可能ファイルに変換したものを SHALO LICENSING で暗号化しても、
スクリプト本体は暗号化対象領域外となります。

そのため、このサンプルではスクリプト本体を zip 形式で圧縮後、
SHALO LICENSING によりアセット暗号化を行い、それを実行する方法を紹介します。

なお、以下では Linux 環境を前提に説明しています。
Windows/macOS の場合は、デコーダライブラリのファイル名をそれぞれ
`shalod.dll`, `shalom.dll` や `libshalod.dylib`, `libshalom.dylib` と読み替えてください。

## 事前準備

1. Python 3 環境を用意する
2. pyinstaller を導入する
```sh
$ python3 -m pip install pyinstaller
```
3. SHALO LICENSING SDK を導入する
4. (Linux の場合) libusb を導入する

## スクリプトの圧縮と暗号化

1. 配布したい Python スクリプトの `__main__` が含まれるファイルを `__main__.py` というファイル名にします。
2. スクリプト一式を zip 形式で 1 つの `__main__.zip` ファイルに圧縮します。
3. 上記を SHALO LICENSING SDK に含まれるエンコーダによって暗号化します。
4. 暗号化済み zip ファイルは `__main__.bin` というファイル名にします。

## 暗号化スクリプトの起動スクリプトから実行する

下記のファイルを同一パスに配置します。
- 本ディレクトリの `bootcode.py`
- SHALO LICENSING SDK に同梱されている `libshalod.so`, `libshalom.so`
- 前章で作成した `__main__.bin`
- 本リポジトリにある Python binding の `shalo_lic` ディレクトリ以下一式

この状態で `bootcode.py` を実行すると、ライセンスチェックと復号後に実行されます。

## pyinstaller による実行ファイル化

pyinstaller によって `bootcode.py` を実行ファイルにします。
```sh
$ pyinstaller bootcode.py
```

これにより作成される実行ファイルと、下記のファイルを同一パスに配置します。
- SHALO LICENSING SDK に同梱されている `libshalod.so`, `libshalom.so`
- 前章で作成した `__main__.bin`

配布する場合は、上記のファイル一式を配布します。
