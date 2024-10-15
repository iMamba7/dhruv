from flask import Flask, render_template, request, redirect, url_for, jsonify  # Add jsonify import
from data_manager import DataManager  # Ensure this is a class that can be instantiated
from datetime import datetime
import sqlite3 as sql  # Make sure to import sqlite3

app = Flask(__name__)

# Create an instance of the data manager
data_manager_instance = DataManager()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/view-data/<company>', methods=['GET', 'POST'])
def view_data(company):
    data = []
    column_name = []
    filtertitle = []

    if request.method == 'POST':
        selection = request.form.get('dropdown')  # Get dropdown value
        filterDateTo = request.form.get('filterDateTo')  # Get the filter date from the form
        filterDateFrom = request.form.get('filterDateFrom')  # Get the filter date from the form
        
        # Fetch data based on the selected option
        data = data_manager_instance.get_company_data(selection, company=company)  # Use the instance

        # Check if data is returned
        if data:
            # Define the headers
            headers = ['no','Date', 'Name', 'Box', 'Dozen', 'Total Items', 'Weight', 'Total Weight', 'flag']
            column_name = ['no','Date', 'Name', 'Box', 'Dozen', 'Total Items', 'Weight', 'Total Weight', 'flag']

            if selection == 'paisa':
                column_name = ['no','Date', 'Name', 'Box', 'Dozen', 'Total Items', 'paisa', 'Total paisa', 'flag']

            # Convert to list of dictionaries
            data = [dict(zip(headers, row)) for row in data]

            # Filter out entries where Weight and Total Weight are both None
            data = [
                entry for entry in data 
                if not (entry['Weight'] is None and entry['Total Weight'] is None)
            ]

            # Convert date strings to datetime objects for comparison
            if filterDateFrom:
                filterDateFrom = datetime.strptime(filterDateFrom, "%Y-%m-%d")
            if filterDateTo:
                filterDateTo = datetime.strptime(filterDateTo, "%Y-%m-%d")

            # Filter the data between dates
            if filterDateFrom and filterDateTo:
                data = [
                    entry for entry in data 
                    if filterDateFrom <= datetime.strptime(entry['Date'], "%Y-%m-%d") <= filterDateTo
                ]
                title = f"Filtered by {selection}, dates: {filterDateFrom.strftime('%d-%m-%Y')} to {filterDateTo.strftime('%d-%m-%Y')}"
                filtertitle = [title]
            elif filterDateFrom:
                data = [
                    entry for entry in data 
                    if datetime.strptime(entry['Date'], "%Y-%m-%d") >= filterDateFrom
                ]
                title = f"Filtered by {selection}, from date: {filterDateFrom.strftime('%d-%m-%Y')}"
                filtertitle = [title]
            elif filterDateTo:
                data = [
                    entry for entry in data 
                    if datetime.strptime(entry['Date'], "%Y-%m-%d") <= filterDateTo
                ]
                title = f"Filtered by {selection}, to date: {filterDateTo.strftime('%d-%m-%Y')}"
                filtertitle = [title]
            else:
                title = f"Filtered by {selection}"
                filtertitle = [title]

            # Sort the data by Date (ascending or descending based on requirement)
            data = sorted(data, key=lambda x: datetime.strptime(x['Date'], "%Y-%m-%d"), reverse=False)  # Change reverse=True for descending

            # Format the dates to dd-mm-yyyy in the sorted data
            for entry in data:
                entry['Date'] = datetime.strptime(entry['Date'], "%Y-%m-%d").strftime('%d-%m-%Y')

        else:
            print(f"No data returned for selection: {selection}")

    return render_template('view_data.html', data=data, headers=column_name, company=company, filtertitle=filtertitle)

@app.route('/company', methods=['GET', 'POST'])
def get_company():
    data = data_manager_instance.get_data()  # Use the instance
    data = [{'id': t[0], 'name': t[1]} for t in data]
    if request.method == 'POST':
        name = request.form['name']
        return redirect(url_for('add_data', company=name))
    return render_template('get_company.html', data=data)

@app.route('/viewcompany', methods=['GET', 'POST'])
def viewcompany():
    data = data_manager_instance.get_data()  # Use the instance
    data = [{'id': t[0], 'name': t[1]} for t in data]
    if request.method == 'POST':
        name = request.form['name']
        return redirect(url_for('view_data', company=name))
    return render_template('viewcompany.html', data=data)

@app.route('/delete/<no>', methods=['POST'])
def delete(no):
    with sql.connect('data.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM data WHERE no = ?", (no,))
            conn.commit()
            print(f"Deleted record with id: {no}")  # Log for confirmation
            return jsonify(success=True), 200
        except Exception as e:
            print(f"Error occurred: {e}")  # Log the error
            return jsonify(success=False, error=str(e)), 500

@app.route('/add-data/<company>', methods=['GET', 'POST'])
def add_data(company):
    if request.method == 'POST':
        date = request.form.get('date', '')
        name = request.form.get('name', '')
        try:
            box = request.form.get('box', '0')  # Default to 0 if not provided
            total_items = request.form.get('totalItem', '0')  # Default to 0 if not provided
        except ValueError:
            return "Invalid input. Please enter numeric values for box and total items.", 400  # Handle invalid input

        option_input = request.form.get('input', '0')  # Default to 0 if not provided
        option = request.form.get('option', '')
        count = request.form.get('agree', '')
        both = request.form.get('both', '')

        # Call data_manager's add_data method with correct parameters
        data_manager_instance.add_data(
            date=date, name=name, box=box, total_item=total_items,
            option_input=option_input, option=option, count=count, both=both, company=company
        )

        return redirect(url_for('add_data', company=company))
    
    return render_template('add_data.html', company=company)

if __name__ == '__main__':
    app.run(debug=True)
