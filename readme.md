# Receipt & Warranty Analyzer

An AI-powered application that extracts product information, warranty details, and contact information from receipts and bills using the Gemma 3 vision model.

## Features

- Extract product details (name, model, price, specifications)
- Identify warranty information and duration
- Capture store and contact details
- Export results in JSON or formatted text
- User-friendly web interface

## Sample Test Case

The repository includes a test bill in the `assets` folder. Here's an example of the application's output for this test bill:

```json
{
  "product": {
    "name": "Laptop",
    "model": null,
    "price": "42000",
    "quantity": "1",
    "specifications": null,
    "serial_number": null
  },
  "purchase": {
    "date": "2024-01-16",
    "store_name": "Gaurav Computers",
    "store_location": "B-15, Vishwanath Marg, Jaipur",
    "transaction_id": null
  },
  "warranty": {
    "duration": null,
    "expiry_date": null,
    "terms": null,
    "extended_warranty": null
  },
  "contact": {
    "store_phone": "0141-400227",
    "customer_service": null,
    "website": null,
    "email": "g.sharma@gmail.com",
    "service_centers": []
  }
}
```

This demonstrates the application's ability to extract:

- Basic product information (name, price, quantity)
- Store details and location
- Purchase date
- Contact information (phone and email)

## Prerequisites

1. **Python 3.8+**
2. **Ollama** - For running the Gemma 3 model locally
3. **VS Code** (recommended) - For better development experience
4. **Git** (optional) - For cloning the repository

## Installation

1. **Install Ollama**

   - Windows (WSL2 required):
     ```bash
     curl -fsSL https://ollama.com/install.sh | sh
     ```
   - MacOS:
     ```bash
     curl -fsSL https://ollama.com/install.sh | sh
     ```
   - Linux:
     ```bash
     curl -fsSL https://ollama.com/install.sh | sh
     ```

2. **Install Gemma 3 Model**

   ```bash
   ollama pull gemma3:12b
   ```

3. **Clone the repository** (or download the code)

   ```bash
   git clone <repository-url>
   cd ocr_be
   ```

4. **Environment Setup** (choose one method)

   ### Method 1: Using VS Code (Recommended)
   1. Open the project in VS Code:
      ```bash
      code .
      ```
   2. Install recommended VS Code extensions when prompted:
      - Python
      - Pylance
      - Python Environment Manager
   3. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
   4. Type "Python: Create Environment" and select it
   5. Choose "Venv" → "requirements.txt"
   6. Select a Python interpreter (3.8 or higher)
   7. VS Code will automatically:
      - Create a virtual environment
      - Install dependencies from requirements.txt
      - Configure the Python interpreter

   ### Method 2: Manual Setup
   1. Create and activate a virtual environment:
      ```bash
      # Windows
      python -m venv .venv
      .venv\Scripts\activate

      # Linux/MacOS
      python -m venv .venv
      source .venv/bin/activate
      ```
   2. Install dependencies:
      ```bash
      pip install -r requirements.txt
      ```

## Running the Application

1. **Start Ollama Server**

   ```bash
   ollama serve
   ```

2. **Run the Streamlit app** (in a new terminal)
   - VS Code: 
     1. Open a new terminal in VS Code (`Ctrl+` `)
     2. The virtual environment should activate automatically
     3. Run: `streamlit run app.py`
   
   - Manual:
     ```bash
     streamlit run app.py
     ```

3. The application will open in your default web browser at `http://localhost:8501`

## Usage

1. Upload a receipt or bill image (supported formats: PNG, JPG, JPEG)
2. Click "Analyze Receipt"
3. View the extracted information
4. Download results in JSON or text format

## Troubleshooting

1. **Ollama Connection Issues**

   - Ensure Ollama is running (`ollama serve`)
   - Check if the Gemma 3 model is installed (`ollama list`)
   - Verify no firewall is blocking port 11434

2. **Image Processing Errors**

   - Ensure the image is clear and readable
   - Supported formats: PNG, JPG, JPEG
   - Maximum file size: 10MB

3. **JSON Parsing Errors**
   - Try processing the image again
   - Ensure the receipt is clearly visible
   - Check if the image is properly oriented
