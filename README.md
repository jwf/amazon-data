# Amazon Purchase Analytics

A web-based visualization system for analyzing your Amazon order data. This application helps you understand your purchasing habits over time with interactive charts and statistics.

## Features

- **Summary Dashboard**: Overview of total spending, order counts, and average order values
- **Spending Over Time**: Track your spending trends monthly or yearly
- **Top Products**: See your most purchased items by quantity or spending
- **Category Breakdown**: Visualize spending by product categories
- **Payment Methods**: Analyze spending by payment type
- **Return Statistics**: Track return rates and return trends over time
- **Digital vs Retail**: Compare digital and retail order patterns

## Setup

### Prerequisites

- Python 3.8+
- Node.js 16+ and npm
- Your Amazon order data extracted in the `data/` directory

### Initial Setup

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Import data into database:**
```bash
cd backend
python import_data.py
```

This will create a SQLite database (`amazon_data.db`) and import all CSV data. This only needs to be done once, or when you add new data files.

3. **Start the backend server:**
```bash
cd backend
python app.py
```

The backend will run on `http://localhost:5001` (locally) and will also be accessible on your local network at `http://<your-ip>:5001`

### Frontend Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Start the development server:**
```bash
npm start
```

The frontend will run on `http://localhost:3000`

### Adding New Data

If you receive new Amazon order data files:

1. Extract them to the `data/` directory (maintaining the same folder structure)
2. Run the import script again:
```bash
cd backend
python import_data.py
```

The script will clear existing data and re-import everything. For incremental updates, you could modify the script to handle updates.

### Production Build

To build the frontend for production:

```bash
cd frontend
npm run build
```

The built files will be in `frontend/build/`. The Flask backend is configured to serve these files in production mode.

## Project Structure

```
amazon-data/
├── backend/
│   ├── app.py              # Flask application entry point
│   ├── database.py         # Database schema and connection management
│   ├── import_data.py      # Script to import CSV data into SQLite
│   ├── data_processor.py   # Data querying logic (uses database)
│   └── api/
│       ├── __init__.py
│       └── routes.py       # API endpoints
├── frontend/
│   ├── src/
│   │   ├── App.tsx         # Main application component
│   │   ├── api.ts          # API client functions
│   │   └── components/     # React visualization components
│   └── package.json
├── data/                   # Your Amazon order data CSV files
├── amazon_data.db          # SQLite database (created after import)
└── requirements.txt        # Python dependencies
```

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/stats/summary` - Overall statistics
- `GET /api/stats/spending-over-time?period=monthly|yearly` - Spending trends
- `GET /api/stats/top-products?limit=20&by=quantity|spending` - Top products
- `GET /api/stats/categories` - Category breakdown
- `GET /api/stats/payment-methods` - Payment method breakdown
- `GET /api/stats/returns` - Return statistics
- `GET /api/stats/digital-vs-retail` - Digital vs retail comparison
- `GET /api/orders?page=1&limit=50` - Paginated order list

## Technologies Used

- **Backend**: Python, Flask, SQLite, pandas (for CSV import only)
- **Frontend**: React, TypeScript, Tailwind CSS, Recharts
- **Database**: SQLite (for portability and simplicity)

## Database

The application uses SQLite for data storage. The database file (`amazon_data.db`) is created in the project root after running the import script. The database includes:

- `retail_orders` - All retail order items
- `digital_items` - Digital order items
- `returns` - Return records
- `cart_items` - Items added to cart (but not necessarily purchased)

Indexes are created on frequently queried columns (order_id, order_date, etc.) for optimal performance.

## Notes

- The database file (`.db`) is excluded from git by default (see `.gitignore`)
- Category detection uses keyword matching on product names
- All monetary values are displayed in the currency from your data (typically CAD for Amazon.ca)
- The application handles missing or malformed data gracefully
