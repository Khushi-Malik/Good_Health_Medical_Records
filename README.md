# Medicine Inventory Management System

A command-line based inventory management system for medical stores to manage medicine stock, track sales, handle returns, and monitor expiry dates.

## Features

- **Stock Management**
  - Add new medicines with detailed information
  - Update existing stock quantities
  - Delete medicines from inventory
  
- **Transaction Handling**
  - Sell medicines and automatically update inventory
  - Process returns for expired or damaged medicines
  - Maintain transaction history in separate files

- **Inventory Monitoring**
  - Search medicines by name
  - View complete inventory
  - Track medicines expiring within 30 days
  - Automatic expiry date validation

- **Data Persistence**
  - All data stored using Python pickle format
  - Separate files for inventory, sales, and returns

## Installation

### Prerequisites

- Python 3.7 or higher

### Setup

1. Clone or download this repository:
```bash
git clone <repository-url>
cd medicines
```

2. No additional dependencies required - uses only Python standard library

## Usage

### Running the Application

```bash
python main.py
```

### Main Menu Options

```
1. ADD STOCK           - Add new medicines to inventory
2. UPDATE STOCK        - Modify existing medicine quantities
3. DELETE MEDICINE     - Remove medicines from database
4. SELL MEDICINE       - Process medicine sales
5. RETURN MEDICINE     - Handle medicine returns
6. UPCOMING EXPIRY     - View medicines expiring soon (within 30 days)
7. SEARCH MEDICINE     - Find medicines by name
8. VIEW ALL MEDICINES  - Display complete inventory
0. EXIT                - Close the application
```

### Adding a New Medicine

When adding stock, you'll need to provide:
- Medicine name
- Brand name
- Manufacturing date (format: yyyy, mm, dd)
- Expiry date (format: yyyy, mm, dd)
- Type (0 for Syrup, 1 for Tablet)
- Price per unit (strip/bottle)
- Quantity

### Selling Medicine

1. Enter the medicine name
2. System displays available stock and price
3. Enter quantity to sell
4. Confirm the transaction
5. Sale is recorded and inventory updated automatically

### Managing Expiry

The system automatically:
- Validates expiry dates when adding medicines
- Warns about expired medicines
- Lists medicines expiring within 30 days
- Shows days remaining until expiry

## Data Format

### Medicine Record Structure

Each medicine is stored as a list with the following fields:
```python
[
    medicine_id,           # int: Unique identifier
    name,                  # str: Medicine name
    brand,                 # str: Brand name
    manufacturing_date,    # str: Format "yyyy, mm, dd"
    expiry_date,          # str: Format "yyyy, mm, dd"
    type,                 # int: 0=Syrup, 1=Tablet
    quantity,             # int: Number of units in stock
    price,                # float: Price per unit
    amount                # float: Total value (quantity × price)
]
```

## Important Notes

### Date Format
All dates must be entered in the format: `yyyy, mm, dd` (with commas and spaces)
- Example: `2024, 12, 31`

### Medicine Types
- `0` = Syrup (sold in bottles)
- `1` = Tablet (sold in strips)

### Data Files
- The system uses Python's pickle format for data storage
- **Warning**: Pickle files are not human-readable and not secure for untrusted data
- Consider migrating to JSON or a database for production use

## Known Issues & Limitations

1. **Pickle Format**: Not recommended for production due to security concerns
2. **No User Authentication**: Anyone with access can modify inventory
3. **Limited Search**: Only searches by medicine name (case-insensitive partial match)
4. **No Backup System**: Manual backups recommended
5. **Transaction History**: Sales and returns stored separately but not easily queryable
6. **No Reporting**: No built-in reports for sales analysis or inventory valuation

## Recent Improvements in `main.py`

### Bug Fixes
- Fixed ID generation to handle empty databases
- Added proper input validation for all numeric inputs
- Fixed expiry date validation logic
- Added checks for negative quantities

### Enhanced Features
- Added "View All Medicines" option
- Better error handling and user feedback
- Currency symbol (₹) for amounts
- Improved table formatting with proper column alignment
- Transaction confirmations before sales/returns
- Better date validation with meaningful error messages
- Screen clearing for better UX (cross-platform)

### Code Quality
- Added docstrings to all functions
- Better type hints
- Created helper functions for common operations
- Added Medicine class (prepared for future OOP refactoring)
- Consistent error messages
- Better separation of concerns

## Future Enhancements

Potential improvements for future versions:

1. **Database Migration**: Replace pickle with SQLite or PostgreSQL
2. **User Authentication**: Add login system with role-based access
3. **GUI Interface**: Create a graphical interface using Tkinter or PyQt
4. **Reports & Analytics**: 
   - Daily/monthly sales reports
   - Low stock alerts
   - Profit/loss calculations
   - Popular medicines tracking
5. **Advanced Search**: Filter by brand, type, expiry date range
6. **Barcode Support**: Scan medicines for quick entry
7. **Export Features**: Generate CSV/PDF reports
8. **Automated Alerts**: Email notifications for low stock or expiring medicines
9. **Multi-store Support**: Manage multiple store locations
10. **Supplier Management**: Track suppliers and purchase orders

## Contributing

Contributions are welcome! Areas that need improvement:
- Input validation
- Error handling
- Unit tests
- Documentation
- UI/UX improvements

## License

This project is open source and available under the [MIT License](LICENSE).
