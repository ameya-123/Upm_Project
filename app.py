from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Secret key for session management
app.secret_key = 'your_secret_key'

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'minor_project'

# Initialize MySQL
mysql = MySQL(app)

# Route for Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Route for Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form fields
        email = request.form['email']
        password = request.form['password']

        # Validate inputs for patient login
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM patient_details WHERE P_mail = %s AND password = %s', (email, password))
        patient_account = cursor.fetchone()

        # Check if the user is a patient
        if patient_account:
            session['loggedin'] = True
            session['email'] = patient_account['P_mail']
            session['full_name'] = f"{patient_account['Fname']} {patient_account['Lname']}"
            session['age'] = patient_account['age']  # Store other details as needed
            session['weight'] = patient_account['weight']
            flash('Login successful!')
            return redirect(url_for('patient_dashboard'))

        # If not found in patient_details, check doctor_details
        cursor.execute('SELECT * FROM doctor_details WHERE D_mail = %s AND password = %s', (email, password))
        doctor_account = cursor.fetchone()

        # Check if the user is a doctor
        if doctor_account:
            session['loggedin'] = True
            session['email'] = doctor_account['D_mail']
            session['full_name'] = f"{doctor_account['Fname']} {doctor_account['Lname']}" 
            flash('Login successful!')
            return redirect(url_for('doctor_dashboard'))

        # Invalid credentials
        flash('Invalid login credentials. Please try again.')
    
    return render_template('login.html')


# Route for Registration
#1 @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         # Get form data from the registration form
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         email = request.form['email']
#         age = request.form['age']
#         weight = request.form['weight']
#         password = request.form['password']
#        # role = request.form['role']

#         # Insert the form data into the users table
#         cursor = mysql.connection.cursor()
#         query = '''
#             INSERT INTO patient_details(fname, lname, p_mail, age, weight, password)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         '''
#         cursor.execute(query, (first_name, last_name, email, age, weight, password))
#         # Commit the transaction and close the cursor
#         mysql.connection.commit()
#         cursor.close()

#         # Redirect the user to the login page after successful registration
#         return redirect(url_for('login'))
    
#     return render_template('register.html')

# @2app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         # Get form data
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         email = request.form['email']
#         age = request.form['age']
#         weight = request.form['weight']
#         password = request.form['password']
#         role = request.form['role']

#         cursor = mysql.connection.cursor()

#         if role == 'Patient':
#             # Insert patient data into patient_details table
#             query = '''
#                 INSERT INTO patient_details(fname, lname, p_mail, age, weight, password)
#                 VALUES (%s, %s, %s, %s, %s, %s)
#             '''
#             cursor.execute(query, (first_name, last_name, email, age, weight, password))
        
#         elif role == 'Doctor':
#             # Insert doctor data into doctor_details table
#             query = '''
#                 INSERT INTO doctor_details(fname, lname, d_mail, password)
#                 VALUES (%s, %s, %s, %s)
#             '''
#             cursor.execute(query, (first_name, last_name, email, password))

#         # Commit the transaction and close the cursor
#         mysql.connection.commit()
#         cursor.close()

#         flash(f'{role} registered successfully!')
#         return redirect(url_for('login'))
    
#     return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        specialization = request.form['specialization']

        cursor = mysql.connection.cursor()

        if role == 'Patient':
            # Insert patient data into patient_details table
            age = request.form['age']
            weight = request.form['weight']
            query = '''
                INSERT INTO patient_details(fname, lname, p_mail, age, weight, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(query, (first_name, last_name, email, age, weight, password))
        
        elif role == 'Doctor':
            # Insert doctor data into doctor_details table
            query = '''
                INSERT INTO doctor_details(fname, lname, d_mail, password,speciality)
                VALUES (%s, %s, %s, %s,%s)
            '''
            cursor.execute(query, (first_name, last_name, email, password,specialization))

        # Commit the transaction and close the cursor
        mysql.connection.commit()
        cursor.close()

        flash(f'{role} registered successfully!')
        return redirect(url_for('login'))
    
    return render_template('register.html')




# @app.route('/patient_dashboard')
# def patient_dashboard():
#     # Check if the user is logged in
#     if 'loggedin' in session:
#         # Since we're not using a role, just ensure the user exists in the patient_details table
#         full_name = session.get('full_name')
#         email = session.get('email')
#         age = session.get('age')
#         weight = session.get('weight')

#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM patient_details WHERE P_mail = %s', (session['email'],))
#         patient_account = cursor.fetchone()

#         if patient_account:
#             # Render patient dashboard if the account exists
#             return render_template('patient_dashboard.html', full_name=full_name, email=email, age=age, weight=weight)

#         else:
#             # If not found, redirect to login
#             flash('Patient account not found.')
#             return redirect(url_for('login'))
    
#     # If the user is not logged in, redirect to login page
#     return redirect(url_for('login'))

@app.route('/patient_dashboard')
def patient_dashboard():
    # Check if the user is logged in
    if 'loggedin' in session:
        # Retrieve patient session details
        full_name = session.get('full_name')
        email = session.get('email')
        age = session.get('age')
        weight = session.get('weight')

        # Query the patient details
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM patient_details WHERE P_mail = %s', (email,))
        patient_account = cursor.fetchone()

        if patient_account:
            # Fetch patient's appointments
            cursor.execute('SELECT * FROM appointment_details WHERE P_mail = %s', (email,))
            appointments = cursor.fetchall()

            # Render patient dashboard if the account exists, with appointments
            return render_template('patient_dashboard.html', full_name=full_name, email=email, age=age, weight=weight, appointments=appointments)

        else:
            # If not found, redirect to login
            flash('Patient account not found.')
            return redirect(url_for('login'))
    
    # If the user is not logged in, redirect to login page
    return redirect(url_for('login'))


@app.route('/update_appointment_status/<int:appointment_id>', methods=['POST'])
def update_appointment_status(appointment_id):
    if 'loggedin' in session:
        # Get the status from the form submission
        new_status = request.form['status']

        # Update the appointment status in the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE appointment_details SET status = %s WHERE Ap_ID = %s', (new_status, appointment_id))
        mysql.connection.commit()

        # Flash message based on action
        if new_status == 'Approved':
            flash('Appointment has been approved.')
        else:
            flash('Appointment has been declined.')

        # Redirect back to the doctor dashboard
        return redirect(url_for('doctor_dashboard'))
    
    # If the user is not logged in, redirect to the login page
    return redirect(url_for('login'))



# Route for Doctor Dashboard
# @app.route('/doctor_dashboard')
# def doctor_dashboard():
#     # Check if the user is logged in
#     if 'loggedin' in session:
#         # Query the doctor_details table to verify the account
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM doctor_details WHERE D_mail = %s', (session['email'],))
#         doctor_account = cursor.fetchone()

#         if doctor_account:
#             # Render the doctor dashboard if the account exists
#             return render_template('doctor_dashboard.html', full_name=session['full_name'])
#         else:
#             # If the account is not found, redirect to login
#             flash('Doctor account not found.')
#             return redirect(url_for('login'))
    
#     # If the user is not logged in, redirect to login page
#     return redirect(url_for('login'))

@app.route('/doctor_dashboard')
def doctor_dashboard():
    # Check if the user is logged in
    if 'loggedin' in session:
        # Query the doctor_details table to verify the account
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doctor_details WHERE D_mail = %s', (session['email'],))
        doctor_account = cursor.fetchone()

        if doctor_account:
            # Query to fetch upcoming appointments for the doctor
            cursor.execute('''
                SELECT * FROM appointment_details
                WHERE D_mail = %s
                ORDER BY booking_details
            ''', (session['email'],))
            upcoming_appointments = cursor.fetchall()

            # Query to fetch the patient list for the doctor
            cursor.execute('''
                SELECT DISTINCT P_mail FROM appointment_details
                WHERE D_mail = %s
            ''', (session['email'],))
            patient_list = cursor.fetchall()

            # Render the doctor dashboard with necessary data
            return render_template('doctor_dashboard.html', 
                                   full_name=session['full_name'],
                                   upcoming_appointments=upcoming_appointments,
                                   patient_list=patient_list)
        else:
            # If the doctor account is not found, redirect to login
            flash('Doctor account not found.')
            return redirect(url_for('login'))
    
    # If the user is not logged in, redirect to login page
    return redirect(url_for('login'))


@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if 'loggedin' not in session:
        return redirect(url_for('login'))  # Ensure the user is logged in

    if request.method == 'POST':
        # Get the form data
        doctor_email = request.form['doctor_email']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        #symptoms = request.form['symptoms']
        payment_method = request.form['payment_method']
        reason = request.form['reason']
        #amount = request.form['amount']
        
        # Get patient details from session
        patient_email = session['email']
        
        # Insert the appointment into the database
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO appointment_details (P_mail, D_mail, booking_details, payment_method, reason)
            VALUES (%s, %s, %s, %s, %s)
        ''', (patient_email, doctor_email, appointment_date, payment_method, reason))
        mysql.connection.commit()
        
        flash('Appointment booked successfully!')
        return redirect(url_for('patient_dashboard'))  # Redirect to the patient dashboard after booking

    # Fetch doctors for selection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM doctor_details')
    doctors = cursor.fetchall()
    
    return render_template('book_appointment.html', doctors=doctors)

@app.route('/create_prescription/<appointment_id>', methods=['GET', 'POST'])
def create_prescription(appointment_id):
    if request.method == 'GET':
        # Fetch appointment details and reason from the appointment table
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM appointment_details WHERE Ap_ID = %s', (appointment_id,))
        appointment = cursor.fetchone()

        # Pass the reason for the visit to the form
        if appointment:
            return render_template('prescription_form.html', appointment=appointment)
        else:
            flash('Appointment not found.')
            return redirect(url_for('doctor_dashboard'))

    if request.method == 'POST':
        # Get the logged-in doctor's email from the session
        D_mail = session['email']  # Doctor's email (from session)
        P_mail = request.form['P_mail']  # Patient's email (can also be fetched from session if logged-in)
        prescription_details = request.form['prescription_details']
        issued_date = request.form['issued_date']
        reason = request.form['reason']  # This is the reason passed from the appointment

        # Insert the prescription details into the prescriptions table
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO prescriptions (P_mail, D_mail, prescription_details, issued_date, reason)
            VALUES (%s, %s, %s, %s, %s)
        """, (P_mail, D_mail, prescription_details, issued_date, reason))
        
        # Update the appointment status to 'Prescribed'
        cursor.execute("""
            UPDATE appointment_details SET status = 'Prescribed' WHERE Ap_ID = %s
        """, (appointment_id,))
        
        mysql.connection.commit()
        flash('Prescription created successfully!')
        return redirect(url_for('doctor_dashboard'))
    
    @app.route('/real_time_monitoring', methods=['GET', 'POST'])
    def real_time_monitoring():
        if 'loggedin' in session:
        # Assume the user is logged in as a patient
        # Fetch list of doctors for the dropdown (this is just an example)
         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT full_name, D_mail FROM doctor_details')
        doctors = cursor.fetchall()

        if request.method == 'POST':
            # Get the form data
            disease = request.form['disease']
            doctor_email = request.form['doctor']
            document = request.files['document']

            # Validate if a document is selected and has the correct file type
            if document and allowed_file(document.filename):
                filename = secure_filename(document.filename)
                document_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                document.save(document_path)  # Save document

                # Insert real-time monitoring data into the database (for demonstration)
                cursor.execute('''
                    INSERT INTO monitoring_reports (P_mail, D_mail, disease, document_path, status)
                    VALUES (%s, %s, %s, %s, 'Pending')
                ''', (session['email'], doctor_email, disease, document_path))
                mysql.connection.commit()

                # Notify the doctor by email or dashboard notification (implement this as needed)
                flash('Your report has been submitted successfully!')

                return redirect(url_for('patient_dashboard'))
            else:
                flash('Please upload a valid document!')

        return render_template('real_time_monitoring.html', doctors=doctors)

    # If the user is not logged in, redirect to the login page
    return redirect(url_for('login'))

@app.route('/download_report/<int:report_id>')
def download_report(report_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Fetch the report details by its ID
    cursor.execute('SELECT * FROM patient_reports WHERE report_id = %s', (report_id,))
    report = cursor.fetchone()

    if report:
        file_path = report['file_path']
        return send_file(file_path, as_attachment=True)
    else:
        flash('Report not found.')
        return redirect(url_for('doctor_dashboard'))






# Route for Admin Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    # Check if the user is logged in
    if 'loggedin' in session:
        # Query the admin_details table to verify the account
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin_details WHERE email = %s', (session['email'],))
        admin_account = cursor.fetchone()

        if admin_account:
            # Render the admin dashboard if the account exists
            return render_template('admin_dashboard.html', email=session['email'])
        else:
            # If the account is not found, redirect to login
            flash('Admin account not found.')
            return redirect(url_for('login'))

    # If the user is not logged in, redirect to login page
    return redirect(url_for('login'))


# Route for Logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    #session.pop('role', None)
    flash('You have successfully logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
