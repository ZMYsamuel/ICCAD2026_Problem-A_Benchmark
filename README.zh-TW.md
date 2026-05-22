# ICCAD 2026 Problem A — Benchmark

這是 **ICCAD 2026 Problem A: LLM-Assisted Netlist Exploration and Transformation** 的社群 submission 存檔。

每位參賽者將 testcase 跑過自己的系統，然後把輸出結果提交到這個 repo。大家可以透過比對彼此的 submission，在沒有單一 golden answer 的情況下，交叉參照來推斷答案是否正確。

## 設計目標

1. **降低單一隊伍 eval set 的過擬合風險。** 來自多位貢獻者的對抗性測資，能覆蓋任何單一隊伍想不到的邊界情況。
2. **精確對應比賽的 I/O 格式**（見題目說明書 §3）。任何能通過這些 testcase 的系統，代表已正確接上比賽的評分系統。
3. **足夠開放，歡迎所有隊伍與指導老師加入。** 公開授權（MIT），無 NDA，不限隊伍。

## Repo 結構

```
ICCAD2026_Problem-A_Benchmark/
├── official_testcase/          # 40 個官方 Cadence testcase（由 maintainer 鎖定）
│   └── testNN/
│       ├── testNN.v            # Gate-level Verilog netlist
│       ├── requests.txt        # 官方題目（每行一題）
│       ├── meta.yaml           # task_type + expected.kind 分類資訊
│       ├── README.md           # Testcase 簡介
│       └── <github-username>/ # 你的 submission 資料夾
│           ├── testNN.log      # 必填 — 系統輸出
│           ├── *.v             # 選填 — 輸出 Verilog
│           └── submission.yaml # 選填 — 執行資訊
├── community_testcase/         # 社群自製 testcase（任何人都可新增/編輯）
│   └── <case_name>/
│       ├── <case_name>.v       # netlist（檔名不限，至少要有一個 .v）
│       ├── requests.txt        # 題目；第一行宣告 case_name
│       ├── README.md           # 選填
│       └── <github-username>/<case_name>.log + 選填 *.v + submission.yaml
├── runner/run_bench.py         # Submission runner
├── .github/
│   ├── scripts/validate_submission.py
│   └── workflows/submission-validate.yml
├── CONTRIBUTING.md
└── LICENSE
```

## 與比賽規格書的格式對應

| 比賽規格（題目說明書 §3）| 本 repo 對應 |
|---|---|
| 系統從 **stdin** 逐行讀取 NL 題目 | 每個 testcase 的 `requests.txt` 就是這個輸入串流 |
| 系統將回應輸出到 **stdout**，以 `#RESPONSE <id>` / `#END <id>` 分隔 | Submission log（`testNN.log` / `<case_name>.log`）必須符合此格式 |
| 每題限時：basic 操作 60 秒，其他 300 秒 | `runner/run_bench.py` 強制執行，並標記 `status: timeout` |
| Testcase 以 `This is the beginning of testcase <name>. …` 開頭 | 每個 `requests.txt` 的第一行皆遵循此格式 |

## 快速開始 — 在本機執行 benchmark

```bash
# 1. 設定你的系統指令（或使用 BENCH_SYSTEM_CMD 環境變數）
export BENCH_SYSTEM_CMD="./your_system --config llm_config.yaml"

# 2. 執行 runner
python3 runner/run_bench.py --source official --cases test01      # 單一官方 testcase
python3 runner/run_bench.py --source community --cases demo01     # 單一社群 testcase
python3 runner/run_bench.py --source all                          # 全部

# 輸出會寫到：results/run_<timestamp>/<case>/system.log
# （results/ 已加入 .gitignore，不會被 push 到 repo）

# 3. 把 log 複製到你的 submission 資料夾，然後開 PR
#    完整流程請參考 CONTRIBUTING.md
```

## `runner/run_bench.py` — CLI 參數說明

| 參數 | 預設值 | 說明 |
|---|---|---|
| `--system-cmd <str>` | `$BENCH_SYSTEM_CMD` 環境變數，或 `./your_team_alpha -config llm_config.yaml` | 呼叫受測系統的 shell 指令。Runner 對每個 testcase 建立獨立工作目錄，把 `requests.txt` 餵入 stdin，再從 stdout 讀取 `#RESPONSE`/`#END` 行。 |
| `--source <enum>` | `all` | 要執行的 testcase 集合：`official` → `official_testcase/test*/`；`community` → `community_testcase/*/`；`all` → 兩者都跑。 |
| `--cases <csv>` | （無，執行全部）| 要執行的 case 名稱（逗號分隔），例如 `test01,test10,demo01`。 |
| `--output-dir <path>` | `results/run_<timestamp>/` | 指定結果書和 per-case artifact 的輸出路徑。 |
| `--list-only` | 關閉 | 只印出找到的 case 目錄後離開，不實際執行。方便確認 selector 設定正確。 |

Runner 會繼承 shell 的環境變數。請在呼叫 runner 前，確保系統所需的 API key 和 `LD_LIBRARY_PATH` 都已經 export。

## 提交你的結果

完整的逐步說明（包含如何 fork 這個 repo 和開 pull request）請見 [CONTRIBUTING.md](CONTRIBUTING.md)。

開 PR 後，GitHub Actions CI 會自動檢查 submission 格式是否正確。CI 只驗證結構（資料夾名稱、必要檔案、log 格式），**不是正確性的判斷**。

## English

[English README](README.md)
