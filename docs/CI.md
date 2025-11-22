# CI / ローカル実行ガイド

このプロジェクトの CI とローカルでのテスト実行についてのサンプルと手順をまとめます。

## GitHub Actions (サンプル)
ファイル: `.github/workflows/ci.yml`

- Python 3.11 / 3.12 / 3.14 のマトリクスでテストを実行します。
- テストは `PYTHONPATH=src pytest -q` で実行されます（ソースを `src/` から参照するため）。

このワークフローは push や pull_request で自動的に走ります。

## ローカルでCI相当の実行
付属のスクリプト `scripts/ci_run.sh` を使うと、ローカルで CI と似た流れを再現できます。

使い方:
```bash
./scripts/ci_run.sh
```

スクリプトの動作:
- 仮想環境 `.venv` を作成（存在する場合は再利用）
- `requirements-dev.txt` があればそれをインストール、なければ `pytest` のみをインストール
- `PYTHONPATH=src pytest -q` を実行

## 直接コマンドで試す場合
- 仮想環境を使わずに素早く試す:
```bash
python3 -m pip install pytest
PYTHONPATH=src pytest -q
```

## 注意点
- テストは `src/` に配置されたパッケージを直接参照するよう設計されています。CI ワークフローやローカルスクリプトは `PYTHONPATH=src` を必ず指定します。
- 実行環境によっては Python のバージョンや利用可能なライブラリが異なるため、CI と同等の環境で検証する場合は `python-version` を合わせてください。
