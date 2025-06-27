# 🧾 Sales Tracker Application

A simple desktop-based Sales Tracker built with **Python**, **Tkinter**, **SQLite**, and **TkCalendar**. This application helps users manage and analyze sales, cost, and profit/loss data through an intuitive graphical interface.

---

## ✨ Features

- 📆 Select and save sales data with date, sales amount, and cost.
- 📈 Automatically calculate profit or loss per entry.
- 📊 View all records in a sortable TreeView table.
- 🧮 Display overall totals, profit percentage, and status (Profit / Loss / Break-Even).
- 🔍 Filter records by:
  - **Year (YYYY)**
  - **Month (MM)**
  - **Profit**, **Loss**, or show **All**
- ✏️ Edit existing entries with a single click.
- ✅ Clean and minimalistic user interface.

---

## 🖥️ Tech Stack

- **Python 3**
- **Tkinter** (for GUI)
- **SQLite3** (for local database)
- **tkcalendar** (for date selection)

---

## 📦 Installation

1. Clone or download this repository.

2. Install the required dependency:

```bash
pip install tkcalendar
Run the application:

bash
Copy
Edit
python sales_tracker.py
🗃️ Database Structure
The application uses a local SQLite database named sales_tracker.db.

Table: sales

Column	Type	Description
id	INTEGER	Primary Key
date	TEXT	Date of the sale
sales_amount	REAL	Sales amount (in ₹)
cost	REAL	Cost of goods sold (in ₹)
profit_loss	REAL	Calculated profit/loss

📸 UI Preview (optional)
(Add screenshots or GIF demos of the app interface here)

🔧 Project Structure
bash
Copy
Edit
sales-tracker/
│
├── sales_tracker.py         # Main application script
├── sales_tracker.db         # Created automatically at runtime
└── README.md                # Project documentation
🚀 Future Enhancements
Export records to Excel/CSV

Graphs for monthly/yearly analysis

User authentication for multi-user support

Data backup and restore

🤝 Contributing
Contributions, suggestions, and improvements are welcome!
Feel free to fork this project or raise an issue.

📄 License
This project is open source and free to use under the MIT License.

🙌 Acknowledgments
Thanks to:

Python Community

Open-source modules: tkinter, sqlite3, and tkcalendar

vbnet
Copy
Edit

Let me know if you'd like a badge section (e.g., Python version, license), or want to include export features or setup instructions for Windows `.exe` packaging.









