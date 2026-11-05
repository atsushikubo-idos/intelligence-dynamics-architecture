# IDOS Inverse Observability v0.1–v0.8 統合監査

監査日: 2026-11-05  
対象: この会話にアップロードされた `intelligence-dynamics-architecture-main (18)(1).zip`、および別途生成された v0.1–v0.8 の各フォルダ／ZIP。**GitHubの最新コミットを取得した監査ではない。**

## 結論

**判定: 独立した探索・検証実験として保持。MASTER_MAPへの昇格・「未知構造を発見するエンジン」の対外的主張は保留。**

8バージョンを再テストし、合計92/92件成功。ただしテスト通過は指定されたコードの性質の確認であり、独立の理論実証、12PDMの妥当性、モデル間の一貫したエンドツーエンド実証ではない。

## 1. 12PDM / 12CDP 定義監査

- `architecture/MASTER_MAP_v1.1.md` §9 は12PDMを **Dynamic Observation / Description Protocol** と位置づけ、Coreの必要要素とはしない。
- 12プロセスの歴史的配列は Reality → Difference → Representation → Residual → Holding → Update → Possibility Space → Trajectory → Limit → Enactment → Reality′ → Reopening。
- `measurement/MEASUREMENT_OBSERVABILITY_PROTOCOL_v0.3.md` は12CDP表記も用い、evidence-first、観測可能性区分 O/P/I/U、参照系・境界・測定・provenance の記録を要求する。
- 順序固定、12本の独立センサー、12数値スコアと解してはならない。統計的な予測残差≠IDOSのResidual、観測された待ち時間≠Holding、予測精度の改善≠Future Updateability。
- `src/idos_reference_v1_1.py` の `CommonDynamicsProtocol` / `CDPDescription` は12CDPの12項目と同一視しない（略称の意味が異なる可能性を明示）。

## 2. 機能・証拠・未達の一覧

|版|実装して確認したもの|検証データ|証明していないこと|既存IDOSとの境界|
|---|---|---|---|---|
|v0.1|既知A,Cの可観測性ランク|人工2次元系|未知のAや内部変数の存在|数学的可観測性とO/P/I/Uは別|
|v0.2|2つの指定モデルの有限時間の区別|人工・無雑音|任意モデルの発見や因果特定|介入の実行・権限は別|
|v0.3|未知初期水準・ドリフトを消す2階差分、ノイズ判定|人工・既知σ|一般的な未知状態復元|参照系変化は拒否のみ|
|v0.4|0〜3ラグ候補を残差から選択|人工イベント|候補集合外の規則発見|統計残差≠Residual|
|v0.5|AR(4)対選択ラグの未使用時点評価|実マクロ系列|潜在変数・12PDM妥当性・因果|経済変数は既観測|
|v0.6|業務イベントCSV分析器と時系列分割|人工イベントログ|実企業ログへの外的妥当性|12PDMへの証拠マッピングなし|
|v0.7|既定仮説の期待情報利得・観測案選択|人工尤度モデル|未知仮説生成・実データでの尤度較正|Discoveryによる概念提案とは別|
|v0.8|既定仮説集合の不適合テスト・比較停止|人工正規モデル|不適合の原因特定・参照系生成|Discoveryの遷移は呼び出さず|

**実行記録:** `python -m unittest discover -p 'test*.py' -q` を各フォルダで実行し、それぞれ 7, 9, 18, 12, 8, 9, 14, 15件で成功、計92件。

## 3. 既存コードとの重複と不足

- `implementation/discovery_architecture/discovery_architecture.py` の `DiscoveryCycle` は、差異の記録、参照系候補の提案、recontact、条件修正を担う。
- `implementation/discovery_architecture/intervention_design.py` は介入仕様と実行記録を扱う。
- `implementation/discovery_architecture/emergent_engine/engine.py` には `ResidualGenerator`、`InterventionPlanner`、`Engine` がある。候補生成の概念・試行は既存。
- `src/idos_reference_v1_1.py` は `ReferenceFrame`、`MeasurementSystem`、`Trajectory`、`ProvenanceEvent` 等を保有する。
- 新モジュール固有の**限定的な**数値役割は、可観測性／仮説区別／追加観測の情報利得／開集合監査。既存コードとの直接接続は未検証で、同一記録を往復させたパイプラインは存在しない。
- とくに **v0.6が出力する変数からv0.7の尤度を推定していない**。v0.8の仮説集合とノイズもv0.6の実ログから学習していない。したがって「v0.6→v0.7→v0.8」が実データで接続できたとは主張できない。

## 4. 研究上の弱点（優先度順）

1. **実務の一次証拠の不在:** 企業・組織でのケースID、日時、担当、行動と結果、参照系・装置バージョン、変更証拠が揃った検証がない。BPI2012の元ログは未取得。
2. **同一データでの一貫したモデル学習なし:** v0.7の確率分布は研究者が与え、v0.8のモデル・σも既知とする。独立評価での較正・外部妥当性が未確認。
3. **比較対照不足:** AR/線形回帰・一般的なイベントログ分析との部分比較に留まる。HMM、状態空間、変化点検知、プロセスマイニング、従来のactive learning/optimal experiment designとの公平比較が必要。
4. **数理的同定可能性≠現実の構造の存在証明:** 等価なモデル、隠れ交絡、選択バイアス、情報漏洩、観測者影響を十分には排除していない。
5. **IDOS固有の出力定義不足:** 「どの情報が新たに得られたら従来法より良いか」「新しい測定で旧参照系から何が失われるか」「更新可能性がどう保持されたか」を、成果指標と証拠リンクに落とし込む必要がある。
6. **現実との接触:** 12PDMラベルを付ける前に記録の根拠を確認し、未観測・推測・競合解釈を分離する必要がある。

## 5. 統合する場合の最小限のインターフェース（提案、未実装）

`EvidenceRecord -> ObservationContext -> CandidateSet -> TestReport -> ObservationProposal -> RecontactRecord`

- **EvidenceRecord:** `evidence_id`, `source`, `timestamp`, `observed_or_inferred`, `case_id`, `actor_id`、同意・利用許可など。
- **ObservationContext:** `updating_unit_id`, `boundary_version`, `reference_frame_version`, `measurement_version`, `observer_id`, `time_basis`, `provenance_ids`。
- **CandidateSet:** 固定した候補集合、学習済みモデルのバージョン、仮説の生成元と除外理由。
- **TestReport:** 学習/評価期間の区別、外部検証結果、曖昧・棄却・比較不能の区別、比較ベースライン。
- **ObservationProposal:** 予測される情報増分、費用、権限、可逆性、個人情報影響、棄却理由。**これは実行命令でない。**
- **RecontactRecord:** 実行の有無、事後の一次証拠、旧・新参照系のブリッジ、否定的証拠、未解決の残差。

この型は12項目を必須値にしない。12PDMタグは一次証拠に明示的リンクを持つ**任意の記述注釈**とし、統計特徴を機械的に変換しない。Frozen Core変更なし。Discoveryへの提案は`propose_frame`に相当する非自動・審査付き手続きが必要。

## 6. 次の実証を始めるための合否基準

**実証前のゲート:**

- 事前に仮説・対象イベント・観測窓・欠測の扱い・分析単位・エンドポイントを確定する。
- 少なくとも1種の一次イベントログを合法・適正に取得する（なければ外的妥当性を主張しない）。
- 同じ過去データから候補・尤度・ノイズを推定し、完全に未使用の時期または組織で予測と識別改善を測る。
- 追加観測「なし」、標準的なプロセスマイニング、標準的な変化点検知／アクティブ実験計画を比較対象にする。
- 予想された情報利得と、実際に取得した追加証拠による仮説区別の改善を照合する。
- 新参照系を提案した場合、旧基準で失われた観測も保存する。
- 不確実なときは、候補の採用を保留し、記録を残す。

**IDO​​S特有の追加価値を認める基準:** ①既存法が区別できない実際の関係候補を、独立証拠によって区別できるようにする、または②参照系変更の損失・provenance・更新の再可能性を、通常の代替法より明確に保持して判断の質を改善する。どちらも効果量・コスト・誤判定・失敗例とともに記載する。なお、これは研究の評価基準案であり達成済みの成果ではない。

## 7. 判断

- **保存:** v0.1–0.8を改変せず、履歴として保持。別の統合READMEまたは監査ノートだけを追加。
- **統合:** Coreに吸収しない。数値的な逆問題診断はDiscoveryから呼び出せる独立の実験アダプター候補として扱う。
- **次の実務:** v0.9を急がず、まず元ログ取得、12PDMエビデンス対応表、統一データ仕様、ベースライン比較計画を確定。
- **研究上の主張:** 「12PDMから未知の構造を解析的に導出した」はまだ不可。「限定モデルの可観測性、候補比較、追加観測設計、不適合監査を実装し、独立テストが通過」は可。
