# Net Worth Dashboard

A private, fully offline net worth tracker. All data stays on your machine — no accounts, no cloud, no external network requests.

![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)

---

## Features

- Track assets across retirement accounts, investments, cash, and real estate
- Track liabilities (mortgage, loans)
- Month-over-month net worth chart with KPIs
- Investments vs Cash comparison chart
- Stacked asset allocation chart
- Per-account breakdown charts
- Add, edit, and delete monthly snapshots
- Manage and reclassify accounts at any time
- Investment accounts support an equity/cash split for mixed portfolios
- Light and dark mode
- Export and import your data as JSON

---

## Requirements

- Python 3.8+
- pip

---

## Setup

```bash
git clone https://github.com/archmuon/networth-dashboard.git
cd networth-dashboard
pip install -r requirements.txt
python3 server.py
```

Open **http://127.0.0.1:5001** in your browser.

---

## First-time use

1. Click **⚙ Accounts** in the header to set up your account categories (retirement, investments, cash, liabilities).
2. Click **+ Add Month** to enter your first month of data.
3. Repeat monthly to build your history.

### Try it with sample data

A sample file with dummy data is included. To load it:

1. Click **↑ Import** in the header (or the Import button on the empty state screen).
2. Select `data/networth_sample.json`.
3. Explore the dashboard, then clear it and set up your own accounts.

> Your real data file (`data/networth.json`) is gitignored and will never be committed to version control.

---

## Adding a month

Click **+ Add Month**, enter the label (e.g. `May '26`), fill in balances for each account, and click **Save**. Investment accounts with a cash split show separate Equity and Cash rows.

## Editing a month

Click **✎ Edit Month**, select the month from the dropdown, adjust any values, and save.

## Managing accounts

Click **⚙ Accounts** to add, rename, delete, or reclassify accounts. Use the group dropdown on each row to move an account between Retirement, Investment, Cash/Savings, and Liability. Historical data moves with the account automatically.

### Investment cash split

For brokerage accounts that hold both equities and a cash/money-market position, enable **Cash Split** in the Accounts panel. This adds separate Equity and Cash input rows and correctly counts the cash portion on the Cash & Savings side of the comparison chart.

## Exporting your data

Click **↓ Export** to download `networth.json` as a backup. Import it on another machine to restore your dashboard.

---

## Data privacy

- The server binds to `127.0.0.1` only — it is never reachable from the network.
- `data/networth.json` is gitignored. It will never be committed or pushed.
- No analytics, no telemetry, no external fonts, no CDN dependencies.
- Chart.js is bundled locally in `static/`.

---

## Changing the port

If port 5001 conflicts with another application:

```bash
PORT=8080 python3 server.py
```

---

## License

GNU Affero General Public License v3.0 — see [LICENSE](LICENSE).

Free to use, modify, and distribute for personal, educational, and non-commercial purposes. Modifications must be distributed under the same license. Contact the author for commercial licensing.
