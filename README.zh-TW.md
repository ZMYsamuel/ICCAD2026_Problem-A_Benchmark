# ICCAD 2026 Problem A — 公開題庫

社群協作的 **ICCAD Contest 2026 Problem A: LLM-Assisted Netlist Exploration and Transformation** benchmark 題庫。

題目要求參賽隊伍打造一個系統，能接收自然語言請求、理解之後對 gate-level Verilog netlist 進行分析或轉換操作。這個 repo 蒐集 testcase（design + NL request 序列 + 參考答案），讓任何隊伍都能拿來評估自己的系統。

> English version: [README.md](README.md).

## 目標

1. **避免單一隊伍 over-fit 自己的 eval set。** 多個 contributor 出題的 adversarial testcase 能覆蓋單隊伍想不到的 corner case。
2. **完全對齊 contest I/O 格式**（problem statement §3）。只要能通過本 repo 的 testcase，就能在正式評測環境直接接上。
3. **完全開放給所有隊伍 / 指導老師。** Public、MIT 授權、無 NDA、不限隊伍。

## Repo 結構

```
ICCAD2026_Problem-A_Benchmark/
├── README.md                       # 英文版說明
├── README.zh-TW.md                 # 本檔案（繁體中文台灣版）
├── CONTRIBUTING.md                 # 貢獻新 testcase 的格式規範
├── TODO.md                         # 已知待辦 / coverage 缺口
├── LICENSE                         # MIT
├── docs/
│   ├── META_SCHEMA.md              # 選用的 per-case meta.yaml schema
│   └── MANUAL_REVIEW_WORKFLOW.md   # 撰寫 golden 答案的人工驗證流程
├── tests/
│   └── case_<name>/
│       ├── design.v                # gate-level Verilog（單一 top module、primitive gates）
│       ├── requests.txt            # NL request 一行一條,直接餵到系統 stdin
│       ├── golden.log              # 參考輸出,#RESPONSE/#END 格式（contest §3.3）
│       ├── meta.yaml               # 選用:每條 prompt 的 task_type + expected.kind
│       └── README.md               # design 說明 + 題意
├── runner/
│   ├── run_bench.py                # Python runner（推薦）── 含 selector / timeout / result book
│   └── run_bench.sh                # legacy shell runner（單 case,保留向後相容）
├── tools/
│   ├── convert_official.py         # 把官方 release 轉成本 repo schema
│   └── render_diff.py              # golden 對 actual 並排 Markdown diff
└── results/                        # 每次跑的輸出（gitignored,不會 commit）
    └── run_<timestamp>/
        ├── result_book.md
        ├── run_meta.json
        └── <case>/{system.log, system.stderr, artifacts/*.v, ...}
```

## 與 contest 規格的對應

| Contest 規格（problem statement §3）| 本 repo 怎麼對應 |
|---|---|
| 系統從 **stdin** 讀 NL request,一行一條 | `tests/<case>/requests.txt` 就是這個串流 |
| 系統往 **stdout** 寫 `#RESPONSE <id>` / `#END <id>` 包裝的回應 | `tests/<case>/golden.log` 是這個格式的參考答案 |
| 系統還要寫一份到 `<case_name>.log` | Runner 會把系統實際寫的 log 存到 `results/<run>/<case>/system.log` |
| 第一條 prompt 一定是 `This is the beginning of testcase <name>. ...` | `requests.txt` 第一行就是這個格式 |
| 每條 prompt 的 timeout:basic op 60s、其他 300s | `runner/run_bench.py` 兩個都會強制執行,超時標 `status: timeout` |

## 快速開始

```bash
# 1. clone & 進到目錄
git clone https://github.com/ZMYsamuel/ICCAD2026_Problem-A_Benchmark.git
cd ICCAD2026_Problem-A_Benchmark

# 2. 裝 runner 相依套件(只需要 PyYAML)
python3 -m pip install pyyaml

# 3. 設定 runner 指向你的系統 binary（contest §3.1 規定要叫 cada<隊伍編號>_alpha）
#    最方便的做法:在 shell rc 設好 env var,之後 runner 就不用每次指路徑
export BENCH_SYSTEM_CMD="/abs/path/to/your_team_alpha -config /abs/path/to/llm_config.yaml"

# 4. 跑單一 case
python3 runner/run_bench.py --source community --cases case_demo01

# 5. 跑全部 community case
python3 runner/run_bench.py --source community

# 6. 看 result book
ls results/run_*/result_book.md
```

Runner 每次跑會產一份 `result_book.md`,裡面有每個 case 的時間、每條 prompt 的 request + 系統回答 + 參考答案（如果 `meta.yaml` 有寫的話）、總體通過率統計。

## `runner/run_bench.py` ── CLI 完整參考

```
python3 runner/run_bench.py [flags]
```

| Flag | 預設值 | 說明 |
|---|---|---|
| `--system-cmd <字串>` | 讀 `$BENCH_SYSTEM_CMD` env var,沒設的話用 `./your_team_alpha -config llm_config.yaml` | 啟動「被測系統」的 shell 命令。**必填** ── runner 沒有真實 binary 路徑無法工作。Runner 會每個 case 開一個 temp workdir 執行這個命令、把 `requests.txt` pipe 到它的 stdin、從 stdout 讀 `#RESPONSE/#END`。 |
| `--source <enum>` | `all` | 要跑哪一批 case。`community` → `tests/case_*/`（公開,本 repo）。`official` → `private/official_0510/test*/`（gitignored,本地專用,見下）。`personal` → 保留。`all` → 全部。 |
| `--cases <csv>` | _(無)_ | 用 comma 分隔指定 case 名（例如 `test01,test10,case_demo01`）。可加可不加 `case_` 前綴。 |
| `--output-dir <路徑>` | `results/run_<timestamp>/` | 自訂 result book + 每個 case 的 artifact 寫去哪。 |
| `--list-only` | off | 列出符合 selector 的 case 目錄,**不執行**。檢查 selector 設對了沒很好用。 |

Runner 會繼承呼叫者的 **環境變數**,所以系統啟動時要讀的東西（API key、`LD_LIBRARY_PATH`、shell wrapper 裡的 config 路徑）都直接從 shell 來。Runner 只額外注入 `LD_LIBRARY_PATH=/lib64/:$LD_LIBRARY_PATH`,確保 NTHU 工作站上 PyYAML 能 import。

### 切換 LLM provider（OpenAI ↔ Claude）

Runner 本身**不管 provider**,完全 provider-agnostic。要切的話:

1. 編輯你系統的 config 檔（就是 `--system-cmd` 裡 `-config <path>` 指的那個檔）,把裡面的 `provider: "openai"` 改成 `"anthropic"`(或反之)。
2. 確認對應的 API key 有 export(`OPENAI_API_KEY` 或 `ANTHROPIC_API_KEY`)。
3. 直接重跑 runner ── 完全不用改 flag。

Contest §6.2 規定 `gpt-4o-mini` 和 `claude-haiku-4-5` 兩個 provider 都要支援,所以兩個都測過比較保險。

### 公開 / 私有 corpus 混用

Runner 支援兩個平行的 testcase 來源:

- `tests/case_<name>/` ── 公開、MIT 授權、本 repo。任何人都能貢獻。
- `private/official_0510/test<NN>/` ── **gitignored**。Cadence 在 2026-05-10 釋出的 40 個官方 testcase。**不要** commit,因為 redistribution 權利狀態不明。用 `tools/convert_official.py` 把官方原始 release 轉成本 repo schema、放進 `private/`。

```bash
# 轉換官方 0510 release(預設找 ~/official_docs/A_release\ testcase_0510/)
python3 tools/convert_official.py            # 全 40 個
python3 tools/convert_official.py --cases test01,test10  # 部分

# 跑 private corpus(轉換完才能跑,永遠不會被 push 上 GitHub)
python3 runner/run_bench.py --source official
```

## 貢獻 testcase

詳細格式規範看 [CONTRIBUTING.md](CONTRIBUTING.md)。簡版:

1. 在 `tests/case_<你的名字>/` 開新目錄,放 `design.v`、`requests.txt`、`golden.log`、`README.md`。
2. （推薦但可選）加 `meta.yaml`,格式看 [docs/META_SCHEMA.md](docs/META_SCHEMA.md) ── 有這個未來才能接自動 grader。
3. 開 PR。CI 會驗格式、Verilog 可解析性、`#RESPONSE` 數量是否對得上。
4. Maintainer 會看 **design、題目、golden 答案** ── golden 一定要能證明是對的,如果有不直觀的計算要 walkthrough 給 reviewer 看。

## 授權

[MIT](LICENSE) ── 自由 copy / modify / redistribute。若用在 paper 請註明出處。

## 進度

- 2026-05-07:Initial scaffold + 6 個 sample testcase（contest §4 例子 + 小型 Week-4 demo design）。
- 2026-05-14:Python runner + meta.yaml schema + `case_c17`(ISCAS85)+ `case_spec_gaps`(spec §4.3 transformation pattern coverage)。
- 待辦項目在 [TODO.md](TODO.md)(CI 驗證、LLM-judge 自動評分、dual-provider 並排執行)。
