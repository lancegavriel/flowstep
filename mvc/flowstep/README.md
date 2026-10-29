# FlowStep
 
## Project Description
FlowStep is a Python OOP application that aids sari-sari store owners in recording, tracking, and managing customer credit (utang) balances, payments, and overdue accounts. Data is securely persisted locally using JSON storage. 

## High-Priority Features
1. Store owner authentication & cryptographic password hashing
2. Customer registration with custom credit limits
3. Credit purchase (*utang*) and payment recording
4. First in, first out balance tracking and overdue payment detection
5. Administrative dashboard overview and text statement export
 
## Technologies Used
- Python
- Tkinter
- JSON
 
## OOP Implementation
- Encapsulation: Transaction logic and customer balance updates are neatly encapsulated inside dedicated domain models.
- Inheritance: CreditPurchase and Payment extend the abstract Transaction base class
- Polymorphism: Distinct transaction types implement custom behavior for balance application (apply()) and description formatting (describe())
- Abstraction: Rules for giving credit are managed separately via the CreditPolicy class
 
## Project Structure
- models/: Application classes including (Customer, Transactions, CreditPolicy, OwnerAccount)
- views/: User interface components and dialog windows (Login, Dashboard, Customer view, Forms)
- `controllers/`: Application operations and navigation logic
- repositories/:Data access layers managing persistence and data retrieval
 
## Installation
1. Download or clone the repository.
2. Create and activate a Python environment.
3. Ensure Python and Tkinter are already installed in your device.
4. Configure the application settings.
5. Run the main Python file.
 
## Developers
- Lance Gavriel F. Aperocho
