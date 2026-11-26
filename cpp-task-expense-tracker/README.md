# 💰 CLI Expense Tracker (C++)

A fast command-line personal expense tracker built in **C++** using STL containers and persistent CSV file storage.

## ✨ Features
- **Add, View & Delete Expenses:** Track spending by category, description, and amount (INR).
- **Persistent CSV Storage:** Automatically saves and reloads records from `expenses.csv` across sessions using `fstream`.
- **Input Validation:** Handles invalid menu or numeric inputs cleanly without crashing.

## 🚀 How to Compile & Run
1. Compile the program: `g++ -std=c++17 main.cpp -o tracker`
2. Run the executable: `./tracker`
