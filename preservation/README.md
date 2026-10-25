# IDOS — Five Areas, Primary-Source Preservation Registry

## Purpose / 目的

Preserve rather than reduce. このディレクトリは思想を新しい演算・状態遷移・判定モデルに置換**しない**。原図の意味をコードで完全に再現したと主張しない。**原図（PNG）・一次監査原文を権威ある資料として保存し、コードは参照・同一性検証の仕組みだけに限定する。**

## Sources

1. **Original 183 diagrams:** `IDOS_183図_原図と非圧縮横断監査_保存一式.zip`（別の配布ファイル）に含まれる `原図183枚/` のPNG。アップロード元と同一ファイルであることを `metadata/original_183_images_sha256.json` で検証する。大きな元画像ZIPはこのGitHub向け小容量ZIPには再収録しない。
2. **Primary ledgers:** `primary_ledgers/` に19回分を原文のまま収録。ただし台帳は図の逐語転記ではなく過去のAI監査記録である。記述に争いがあればPNGが優先する。
3. **Supplementary audits:** `cross_audits/` — これまでの監査の範囲・暫定判定を保存。ソースと判定を混同しない。
4. **Five-area index:** `metadata/five_areas_index.json` — 初期の ① ② ⑤ ⑥ ⑦ の検索用索引であり、完全な概念一覧でも理論統合でもない。索引の英語の区別は案内用注釈で、原文の代替ではない。

## No-reduction policy / 非縮約規則

- 前表象・未捕捉・抑圧・復元不能を同一のResidual値に変換しない。
- 更新単位・Agency・主体・主権・責任を同一の識別子にしない。
- 関係軌道を個別軌道の和として定義しない。
- Reality、表象、参照系改訂、新参照系生成、測定可能性の成立を混同しない。
- 個人の経験→記録→組織への継承を情報コピーと定義しない。
- 未観測を不存在とみなさない。計測不能を実装失敗とみなさない。
- 初期図の仮説・規範・未解決問いを実証済み事実に格上げしない。
- 原図を更新せず、派生解釈・機能試験・コード案は別ファイル・別履歴で管理する。

## Integrity verification

```bash
python -c "import sys; sys.path.insert(0,'src'); from preservation_registry import validate_primary_image_zip; print(validate_primary_image_zip('path/to/IDOS_183図_原図と非圧縮横断監査_保存一式.zip'))"
```

空リストは画像のチェックサム一致を意味するだけで、思想全体の自動検証完了を意味しない。

## Installation

このZIPをリポジトリの `preservation/five_areas_primary_sources/` に展開。既存 `src/idos_reference_v1_1.py` は変更しない。元画像ZIPは容量を考慮し、別途GitHub Releases、Zenodo等で永続保存し、保存場所とSHA256をこのREADMEに追記する。画像の無断圧縮は行わない。

## Status

Source-preservation tooling only. **No empirical validation, no claim of complete semantic formalization or implementation.**
