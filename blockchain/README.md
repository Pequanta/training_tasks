### **Blockchain Application**  

This application is a Python-based blockchain system built with **FastAPI** and **Pydantic**, enabling users to create and manage transactions, mine blocks, and interact with a decentralized ledger.

---

### **Features**  

- View the blockchain and its state.  
- Create and validate transactions.  
- Mine blocks and add them to the blockchain.  
- Manage unspent transaction outputs (UTXOs).  

---

### **Getting Started**  

#### **Prerequisites**  
- Python 3.8 or higher  
- Virtual environment (recommended)  
- Dependencies in `requirements.txt`  

#### **Installation**  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/your-repo/blockchain-app.git  
   cd blockchain-app  
   ```  

2. Create and activate a virtual environment:  
   ```bash  
   python -m venv venv  
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`  
   ```  

3. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

#### **Run the Application**  
1. Start the server:  
   ```bash  
   python3 main.py # On windows, use 'python  main.py' 
   ```  

2. Access the API:  
   - Swagger Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
   - ReDoc Docs: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

---

### **API Endpoints**  

- **GET `/chain`**: Retrieve the blockchain.  
- **POST `/mine-block`**: Mine a new block.  
  - Input: `Block` object  
- **POST `/new-transaction`**: Add a new transaction.  
  - Input: Sender, receiver, amount, and UTXOs.  
- **POST `/add-block`**: Add a mined block to the blockchain.  

---

### **Project Structure**  

```plaintext  
blockchain-app/  
├── main.py           # Application entry point  
├── models.py           # Blockchain, Block, Transaction, Wallet, UTXO models  
├── utils/            # Cryptographic and helper functions  
├── requirements.txt  # Dependencies  
└── README.md         # Documentation  
```  

---

### **License**  

This project is licensed under the MIT License.  

---

### **Acknowledgments**  

Thanks to the open-source community for tools like FastAPI and Pydantic.