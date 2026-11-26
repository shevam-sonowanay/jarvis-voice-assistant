#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <iomanip>

using namespace std;

struct Expense
{
    int id;
    string category;
    string description;
    double amount;
};

const string DATA_FILE = "expenses.csv";

vector<Expense> loadExpenses()
{
    vector<Expense> expenses;
    ifstream file(DATA_FILE);
    if (!file.is_open())
        return expenses;

    string line;
    while (getline(file, line))
    {
        if (line.empty())
            continue;
        stringstream ss(line);
        string idStr, category, desc, amountStr;

        getline(ss, idStr, ',');
        getline(ss, category, ',');
        getline(ss, desc, ',');
        getline(ss, amountStr, ',');

        Expense e;
        e.id = stoi(idStr);
        e.category = category;
        e.description = desc;
        e.amount = stod(amountStr);
        expenses.push_back(e);
    }
    file.close();
    return expenses;
}

void saveExpenses(const vector<Expense> &expenses)
{
    ofstream file(DATA_FILE);
    for (const auto &e : expenses)
    {
        file << e.id << "," << e.category << "," << e.description << "," << e.amount << "\n";
    }
    file.close();
}

void addExpense(vector<Expense> &expenses)
{
    Expense e;
    e.id = expenses.empty() ? 1 : expenses.back().id + 1;

    cin.ignore();
    cout << "Enter category (e.g., Food, Travel, Books): ";
    getline(cin, e.category);

    cout << "Enter description: ";
    getline(cin, e.description);

    cout << "Enter amount (INR): ";
    while (!(cin >> e.amount) || e.amount < 0)
    {
        cin.clear();
        cin.ignore(10000, '\n');
        cout << "Invalid amount. Enter a positive number: ";
    }

    expenses.push_back(e);
    saveExpenses(expenses);
    cout << "Expense added and saved!\n";
}

void viewExpenses(const vector<Expense> &expenses)
{
    if (expenses.empty())
    {
        cout << "\nNo expenses recorded yet.\n";
        return;
    }

    double total = 0;
    cout << "\n------------------------------------------------------------\n";
    cout << left << setw(6) << "ID" << setw(15) << "Category" << setw(25) << "Description" << "Amount (INR)\n";
    cout << "------------------------------------------------------------\n";

    for (const auto &e : expenses)
    {
        cout << left << setw(6) << e.id
             << setw(15) << e.category
             << setw(25) << e.description
             << fixed << setprecision(2) << e.amount << "\n";
        total += e.amount;
    }
    cout << "------------------------------------------------------------\n";
    cout << "Total Spent: INR " << fixed << setprecision(2) << total << "\n";
}

void deleteExpense(vector<Expense> &expenses)
{
    int targetId;
    cout << "Enter Expense ID to delete: ";
    cin >> targetId;

    for (size_t i = 0; i < expenses.size(); ++i)
    {
        if (expenses[i].id == targetId)
        {
            expenses.erase(expenses.begin() + i);
            saveExpenses(expenses);
            cout << "Expense #" << targetId << " deleted.\n";
            return;
        }
    }
    cout << "Expense ID not found.\n";
}

int main()
{
    vector<Expense> expenses = loadExpenses();
    int choice;

    while (true)
    {
        cout << "\n=== CLI Expense Tracker ===\n";
        cout << "1. Add Expense\n";
        cout << "2. View All Expenses\n";
        cout << "3. Delete Expense\n";
        cout << "4. Exit\n";
        cout << "Choose an option: ";

        if (!(cin >> choice))
        {
            cin.clear();
            cin.ignore(10000, '\n');
            cout << "Please enter a valid number.\n";
            continue;
        }

        switch (choice)
        {
        case 1:
            addExpense(expenses);
            break;
        case 2:
            viewExpenses(expenses);
            break;
        case 3:
            deleteExpense(expenses);
            break;
        case 4:
            cout << "Goodbye!\n";
            return 0;
        default:
            cout << "Invalid choice. Try 1-4.\n";
        }
    }
}
