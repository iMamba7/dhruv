from flask import Flask, render_template, request, redirect, url_for
from data_manager import data_manager
from datetime import datetime

app = Flask(__name__)
# temp = data_manager()

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
        data = data_manager.get_company_data(selection, company=company)
        # Check if data is returned
        if data:
            # Define the headers
            headers = ['Date', 'Name', 'Box', 'Dozen', 'Total Items', 'Weight', 'Total Weight','flag']
            column_name = ['Date', 'Name', 'Box', 'Dozen', 'Total Items', 'Weight', 'Total Weight','flag']

            if selection == 'paisa':
                column_name = ['Date', 'Name', 'Box', 'Dozen', 'Total Items', 'paisa', 'Total paisa','flag']

            # Convert to list of dictionaries
            data = [dict(zip(headers, row)) for row in data]
            
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
    data = data_manager.get_data()
    data = [{'id': t[0], 'name': t[1]} for t in data]
    if request.method == 'POST':
        name = request.form['name']
        return redirect(url_for('add_data',company = name))
    return render_template('get_company.html',data=data)

@app.route('/viewcompany', methods=['GET', 'POST'])
def viewcompany():
    data = data_manager.get_data()
    data = [{'id': t[0], 'name': t[1]} for t in data]
    if request.method == 'POST':
        name = request.form['name']
        return redirect(url_for('view_data',company = name))
    return render_template('viewcompany.html',data=data)

@app.route('/add-data/<company>', methods=['GET', 'POST'])
def add_data(company):
    if request.method == 'POST':
        date = request.form.get('date', '')
        name : str = request.form.get('name', '')
        box : int = request.form.get('box', '')
        total_items : int = request.form.get('totalItem', '')
        option_input : int  = request.form.get('input', '')
        option : str = request.form.get('option', '')
        count = request.form.get('agree','')
        both = request.form.get('both','')
        data_manager.add_data(data_manager,date=date,name= name,box= box,total_item= total_items,option_input= option_input,option= option,count=count,both=both, company=company)
        
        return redirect(url_for('add_data', company=company))
    return render_template('add_data.html', company=company)


if __name__ == '__main__':
    app.run(debug=True)
