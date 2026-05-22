# ICCAD 2026 Problem A — Benchmark

這是 **ICCAD 2026 Problem A: LLM-Assisted Netlist Exploration and Transformation** 的社群 submission 存檔。

每位參賽者將 40 個官方 Cadence testcase 跑過自己的系統，然後把輸出結果提交到這個 repo。大家可以透過比對彼此的 submission，在沒有單一 golden answer 的情況下，交叉參照來推斷答案是否正確。

## Repo 結構

```
ICCAD2026_Problem-A_Benchmark/
├── official_testcase/          # 40 個官方 Cadence testcase（公開）
│   └── testNN/
│       ├── testNN.v            # Gate-level Verilog netlist
│       ├── requests.txt        # 官方題目（每行一題）
│       ├── meta.yaml           # task_type + expected.kind 分類資訊
│       ├── README.md           # Testcase 簡介
│       └── <github-username>/ # 你的 submission 資料夾
│           ├── testNN.log      # 必填 — 系統輸出
│           ├── *.v             # 選填 — 輸出 Verilog
│           └── submission.yaml # 選填 — 執行資訊
├── tests/                      # 社群自製 testcase
├── runner/run_bench.py         # Submission runner
├── .github/
│   ├── scripts/validate_submission.py
│   └── workflows/submission-validate.yml
├── CONTRIBUTING.md
└── LICENSE
```

## 快速開始 — 在本機執行 benchmark

```bash
# 1. 設定你的系統指令
export BENCH_SYSTEM_CMD="./your_system --config llm_config.yaml"

# 2. 對一個或全部官方 testcase 執行 runner
python3 runner/run_bench.py --source official --cases test01
# 輸出會寫到：results/run_<timestamp>/test01/system.log
# （results/ 已加入 .gitignore，不會被 push 到 repo）

# 3. 把 log 複製到你的 submission 資料夾，然後開 PR
#    完整流程請參考 CONTRIBUTING.md
```

Runner 會讀取 `official_testcase/testNN/meta.yaml` 來設定正確的工作目錄，然後依序以 `requests.txt` 裡的每一題呼叫 `$BENCH_SYSTEM_CMD`。

## 提交你的結果

完整的逐步說明（包含如何 fork 這個 repo 和開 pull request）請見 [CONTRIBUTING.md](CONTRIBUTING.md)。

開 PR 後，GitHub Actions CI 會自動檢查 submission 格式是否正確。

## English

[English README](README.md)
