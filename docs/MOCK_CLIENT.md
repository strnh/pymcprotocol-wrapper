# MockClient 仕様 (開発者向け)

このドキュメントはテスト用の `MockClient` の振る舞いと設定についてまとめたものです。

## アドレス形式
- 文字列で、先頭に大文字 `D`、続けて1つ以上の桁 (`0-9`)。例: `D0`, `D100`, `D9999`。
- 検証は `src/pymcprotocol_wrapper/utils.py` の `validate_address()` が行います（正規表現 `^D\d+$`）。

- ## アドレス空間 / 存在性
- `MockClient` は 3バイト（24-bit）デバイス番号のアドレス空間を想定します。数値部は `0` から `16777215` (`0xFFFFFF`) まで扱えます。
- 書き込み (`write_data`) と読み込み (`read_data`) は、その数値部が 24-bit 範囲内なら許可されます。
- 範囲外（負数や 65535 を超える値）は無視され、ログに記録されます。

## 読み書きの振る舞い
- `write_data(address, value)`:
  - `validate_address` に通らない場合は何も行わずデバッグログに記録します。
  - 数値部が 16-bit 範囲内であれば内部ストアに値を保存します。

- `read_data(address)`:
  - `validate_address` に通らない場合は `None` を返します（かつログ出力）。
  - 数値部が 16-bit 範囲外なら `None` を返します。
  - 存在すれば保存されている値を返します（存在しないアドレスは `None` を返します）。

## ロギング
- ログは `src/pymcprotocol_wrapper/utils.py` の `log_message()` を通して行われます。
- デフォルト実装は `logging.getLogger("pymcprotocol_wrapper").debug()` を呼び出します。アプリケーション側でログレベルやハンドラを設定してください。

## 接続状態について（現在の既定）
- 現状の `MockClient` は読み書き操作を `connect()` 状態に依存させていません（テストでの利便性のため）。
- 必要に応じて「接続必須モード」を有効化できます（下記参照）。

## `require_connection` フラグ（今回追加）
- `MockClient(require_connection: bool = False)` が導入されました。
- `require_connection=True` を渡すと、`read_data()` と `write_data()` は `connect()` を呼んでいない状態で呼び出すと `ConnectionError` を発生させます。
- デフォルトは `False` で後方互換性を保ちます。

移行手順:
- 既存テスト/コードを実機ライクにしたい場合、`MockClient(require_connection=True)` を生成し、`connect()` を呼ぶようにしてください（テストでは `setUp()` で `connect()` を呼ぶのが推奨）。

## ロギング設定の例
`pymcprotocol_wrapper` は内部で `logging.getLogger('pymcprotocol_wrapper')` を利用しています。簡単にコンソールにデバッグ出力を出したい場合、アプリケーションの起動時に次を呼んでください:

```python
from pymcprotocol_wrapper import configure_debug_console

configure_debug_console()  # 出力は DEBUG レベルでコンソールへ

# あるいは好みのレベルで
from pymcprotocol_wrapper import configure_logging
import logging

configure_logging(level=logging.INFO)
```

この設定により、`MockClient` や `Client` の内部で `log_message()` を呼んだ際にコンソールへログが出力されます。


## 「接続必須モード」導入案（要検討）
オプションとして `MockClient(require_connection: bool = False)` を追加し、`require_connection=True` のときは `connect()` を呼んでいない状態では `read_data`/`write_data` が例外を投げるか、何も行わない設計にできます。

導入時に検討すべき条件（後述の要約も参照）:
- 既存テストの更新（`setUp()` で `connect()` を呼ぶ必要あり）
- 接続失敗時の振る舞い（例外 vs 無視）
- ロギングとエラー種別（`ConnectionError` を投げることが自然か）

---
このファイルは `MockClient` の実装・テスト・利用方法を速やかに理解するための参照資料です。仕様変更を行った場合はここも併せて更新してください。
