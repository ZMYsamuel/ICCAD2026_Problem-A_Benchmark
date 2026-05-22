# 貢獻指南

這個 repo 可以貢獻三種內容，流程都一樣 — fork、branch、push、PR — 差別只在你新增的檔案放在哪裡。

| 你要做的事 | 檔案放在哪 |
|---|---|
| 提交 **官方** testcase 的系統輸出 | `official_testcase/testNN/<your-github-username>/` |
| 提交 **社群** testcase 的系統輸出 | `community_testcase/<case_name>/<your-github-username>/` |
| 新增一個社群 testcase | `community_testcase/<case_name>/`（直接放在資料夾下） |

這三種可以在同一個 PR 裡混合提交。各自獨立 — 上傳 testcase 不用同時附答案，反之亦然。

---

## 資料夾規則

### 官方 testcase 資料夾 — `official_testcase/testNN/`

由 maintainer 持有。netlist、`requests.txt`、`meta.yaml`、`README.md` 都是鎖死的。投稿者只在裡面新增自己的答案子資料夾。

### 社群 testcase 資料夾 — `community_testcase/<case_name>/`

任何人都可以新增、任何人都可以編輯。資料夾裡必須包含：

- 至少一個 `*.v` netlist 檔（檔名不限）。
- `requests.txt` — 你的 prompt，一行一題。內容自訂（比賽規則允許 prompt 引用任意的檔名）。
- `README.md` — 選填。

資料夾名自訂。建議使用簡短、有描述性的名稱（例如 `my_dff_test`、`alu_fanout`）。

### 答案子資料夾 — `<root>/<case>/<your-github-username>/`

- 資料夾名必須與你的 GitHub 帳號完全一致。CI 用 PR author 的 GitHub login 作為基準。
- 必填檔案：`<case_name>.log` — 你的系統輸出，格式為 `#RESPONSE N` / `#END N` block。
- 選填：任何輸出的 `*.v` 檔、任何 `submission.yaml`（執行資訊）。

預期的 log 檔名等於上層 case 資料夾名：
- `official_testcase/test01/` → `test01.log`
- `community_testcase/demo01/` → `demo01.log`

---

## 完整流程

下面每一步都有 **CLI 形式**（已列出）和 **GitHub-UI 形式** 兩種選擇。指令只是其中一種便利的方式，並非必須 — 用你最習慣的方法即可。真正重要的只有最終的資料夾結構與 log 格式。

### Step 1 — Fork 並 clone

在 GitHub UI 上 fork 這個 repo，然後可以選擇 clone 到本機，或直接在瀏覽器裡編輯檔案：

```bash
git clone https://github.com/<your-github-username>/ICCAD2026_Problem-A_Benchmark.git
cd ICCAD2026_Problem-A_Benchmark
git checkout -b submission/<your-github-username>
```

### Step 2 — 產生你的輸出 _(選填)_

你可以用任何習慣的方式產生 `.log` — 手動跑你的系統、用自己的 harness 餵 prompt、都沒問題。唯一的要求是輸出的 log 檔需要使用 `#RESPONSE N` / `#END N` block 格式，且 block 數量等於 `requests.txt` 中非註解行的數量。

若想直接用現成的 runner，這個 repo 也有附：

```bash
export BENCH_SYSTEM_CMD="./your_system --config llm_config.yaml"

# 單一官方 testcase
python3 runner/run_bench.py --source official --cases test01

# 全部官方 testcase
python3 runner/run_bench.py --source official

# 社群 testcase
python3 runner/run_bench.py --source community --cases demo01
```

Runner 會把輸出寫到 `results/run_<timestamp>/<case>/system.log`。`results/` 資料夾只留在你的本機 — 已在 `.gitignore` 裡。

若是新增 testcase 投稿，直接寫檔案就好。

### Step 3 — 把檔案放到對的位置

你可以在 GitHub 網頁 UI 上直接拖拉上傳（在你的 fork 點 `Add file → Upload files`），或在本機操作：

```bash
# 答案投稿（以官方 testcase 為例）
CASE=test01
USER=<your-github-username>
RUN_DIR=$(ls -dt results/run_*/ | head -1)

mkdir -p official_testcase/${CASE}/${USER}
cp ${RUN_DIR}/${CASE}/system.log \
   official_testcase/${CASE}/${USER}/${CASE}.log
```

社群答案就把 root 換成 `community_testcase/`，加上對應的 case 資料夾名。

新增社群 testcase 則直接在 `community_testcase/<case_name>/` 下建立 `.v` 和 `requests.txt`。

可選擇在你的答案資料夾裡加入 `submission.yaml`，記錄執行資訊：

```yaml
system_name: cada0001_alpha
version: v0.3.2
commit_hash: abcdef0
run_timestamp: 2026-05-25T14:30:00+08:00
notes: |
  對這次執行的補充說明（選填）。
```

### Step 4 — Commit 並 push

如果在 Step 3 是透過瀏覽器上傳，GitHub 已經自動幫你 commit 了，可直接跳到下一步。若是在本機操作：

```bash
git add <你新增的檔案>
git commit -m "submission: <your-github-username> test01"
git push origin submission/<your-github-username>
```

### Step 5 — 開 pull request

在你的 fork GitHub 頁面點擊 **Compare & pull request**，填好 PR template 後送出。（這一步只能透過 GitHub UI，除非你有安裝 `gh` CLI。）

### Step 6 — 若 CI 失敗

CI 對你的 PR 做結構檢查（資料夾名、必要檔案、log 格式），不是正確性檢查。

若 check fail 了，先讀錯誤訊息嘗試在本機修正。大多數錯誤都很單純：

- 資料夾名與你的 GitHub login 不符 → 改名。
- Log 檔名與預期不符 → 改名為 `<case_name>.log`（必須等於 case 資料夾名，例如 `community_testcase/demo01/` 的 log 必須叫 `demo01.log`）。
- Log block ID 數量與 prompt 數量不符 → 重跑系統。

如果你嘗試過了，覺得問題出在 benchmark 端，請在 PR comment 裡 tag `@ZMYsamuel`。

---

## 授權

提交貢獻即表示你同意將內容以 repo 的 MIT license 公開發布。
