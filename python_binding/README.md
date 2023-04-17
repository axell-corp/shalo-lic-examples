# SHALO LICENSING デコーダの Python binding

# 使い方

通常のライブラリと同様に `import` することで利用可能となる。
```python
import shalo_lic
```

# アセットファイルの復号

下記のように、アセットファイルを読み込み、
アプリキーを引数にしてアセットデータをデコードできる。
```python
# import io が必要
with open( "asset_data.bin", "rb" ) as f:
	ad = f.read()
ak = b"\xaa" * 32
r = shalo_lic.decrypt( ad, ak )
```

ライセンスが確認できない場合は例外が飛んでくるので、
`except` で受け取れる。
```python
try:
	r = shalo_lic.decrypt( d, ak )
except shalo_lic.core.ShaloLicInvalidLicenseException:
	print("ERROR: Invalid license.")
	sys.exit(1)
```

また、アプリキーが無効なプロダクトファイルで暗号化した場合は、
第二引数は省略可能。
```python
r = shalo_lic.decrypt( d )
```
