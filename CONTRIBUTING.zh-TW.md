# 貢獻指南

這個 repo 有兩種貢獻方式，請根據你的目的閱讀對應的章節。

---

## Track 1 — 提交官方 testcase 的系統輸出

這是主要的使用場景。你將 40 個官方 Cadence testcase 跑過自己的 ICCAD 2026 系統，然後把輸出結果提交到這個 repo，讓大家可以交叉比對結果。

### 前置條件

- 一個 GitHub 帳號。
- 你的 ICCAD 2026 系統已經可以執行（`$BENCH_SYSTEM_CMD`）。
- 對 git 和 GitHub 有基本認識。

### Step 1：Fork 並 clone

1. 在這個 repo 的 GitHub 頁面右上角點擊 **Fork**。
2. 將你的 fork clone 到本機：

   ```bash
   git clone https://github.com/<your-github-username>/ICCAD2026_Problem-A_Benchmark.git
   cd ICCAD2026_Problem-A_Benchmark
   ```

### Step 2：建立 branch

```bash
git checkout -b submission/<your-github-username>
```

### Step 3：執行 benchmark runner

```bash
export BENCH_SYSTEM_CMD="./your_system --config llm_config.yaml"

# 執行單一 testcase
python3 runner/run_bench.py --source official --cases test01

# 或是執行全部 40 個官方 testcase
python3 runner/run_bench.py --source official
```

Runner 會把輸出寫到 `results/run_<timestamp>/testNN/system.log`。  
`results/` 資料夾已加入 `.gitignore`，只會留在你的本機，不會被 push 到 repo。

### Step 4：將 log 複製到你的 submission 資料夾

```bash
# 把 test01 和 <your-github-username> 換成實際的值
CASE=test01
USER=<your-github-username>
RUN_DIR=$(ls -dt results/run_*/ | head -1)   # 最新的執行結果

mkdir -p official_testcase/${CASE}/${USER}

cp ${RUN_DIR}/${CASE}/system.log \
   official_testcase/${CASE}/${USER}/${CASE}.log
```

你也可以選擇加入執行資訊：

```bash
cat > official_testcase/${CASE}/${USER}/submission.yaml << 'EOF'
system_name: cada0001_alpha
version: v0.3.2
commit_hash: abcdef0
run_timestamp: 2026-05-25T14:30:00+08:00
notes: |
  對這次執行的補充說明（選填）。
EOF
```

如果你的系統有輸出 Verilog 檔案（任何檔名的 `*.v`），也可以一起放進去 — 這是選填的，CI 不會驗證其內容。

### Step 5：Commit 並 push

```bash
git add official_testcase/${CASE}/${USER}/
git commit -m "submission: ${USER} ${CASE}"
git push origin submission/${USER}
```

### Step 6：開 pull request

1. 到你的 fork 的 GitHub 頁面。
2. 點擊 **Compare & pull request**。
3. 填寫 PR template 的 checklist 後送出。

CI 會自動驗證 submission 格式，如果有錯誤請修正後再請 maintainer review。

### Submission 規則（CI 自動執行）

| 規則 | 說明 |
|------|------|
| 資料夾名稱 | 必須與你的 GitHub 帳號完全一致（大小寫敏感）。 |
| 必填檔案 | `official_testcase/testNN/<your-username>/testNN.log` |
| Log 格式 | `#RESPONSE N` / `#END N` block，ID 從 1 開始遞增到 K；K = `requests.txt` 中的題目數。 |
| 選填檔案 | 任意 `*.v` 檔案（任意檔名）；`submission.yaml`。CI 不驗證其內容。 |
| 禁止修改 | 不可更動任何 `official_testcase/testNN/` 下的 `testNN.v`、`requests.txt`、`README.md`、`meta.yaml`，CI 會拒絕這類 PR。 |

---

## Track 2 — 新增社群 testcase 到 `tests/`

如果你想貢獻新的 testcase 設計和題目讓大家使用：

### 資料夾結構

每個 testcase 放在 `tests/case_<unique_name>/`，必須包含以下四個檔案：

```
tests/case_<unique_name>/
├── design.v          # Gate-level Verilog（必填）
├── requests.txt      # NL 題目，每行一題（必填）
├── golden.log        # 參考答案（必填）
└── README.md         # 電路說明 + 題目說明（必填）
```

### `design.v` 要求

- 單一 top module（不允許階層式架構）。
- 只能使用 primitive gate：`and`、`or`、`not`、`nand`、`nor`、`xor`、`xnor`、`buf`、`dff`。
- Gate 為 2-input，`buf` / `not` 為 1-input。
- DFF positional port 順序：`dff inst (q, d, clk, rst_n)`。
- 必須可以被 [pyverilog](https://github.com/PyHDI/Pyverilog) parse。

### `requests.txt` 要求

每行一個自然語言題目，`#` 開頭的行視為注釋並跳過。

**第一行必須是：**

```
This is the beginning of testcase <case_name>. Please output a copy of the log into <case_name>.log.
```

### `golden.log` 格式

```
#RESPONSE 1
<題目 1 的參考答案>
#END 1
#RESPONSE 2
<題目 2 的參考答案>
#END 2
```

- ID 從 1 開始遞增。
- `#RESPONSE` block 數量必須與 `requests.txt` 中非注釋行數一致。

### PR 流程

1. Fork → 建 branch → 新增 `tests/case_<name>/`（含四個檔案）。
2. 開 PR。Maintainer 會 review golden answer 的正確性。
3. Merge 後，testcase 正式加入公開 benchmark。

### 好的 community testcase 應該具備

- 至少一個非 trivial 的 query（路徑查詢、cone 分析、clock domain 確認）。
- 歡迎設計刁鑽的測試：dangling gate、constant output、多個 clock domain。
- 避免超過約 1000 個 gate 的大型設計，除非「規模本身」就是測試重點。
- 每個 golden answer 都必須可以逐步推導出來。

## 授權

提交貢獻即表示你同意將你的內容以 repo 的 MIT license 公開發布。
