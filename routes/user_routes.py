from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import json
from flask_login import login_required, current_user
from models import Hospital, Booking, Rating, Bed, Ward, db, Department, Doctor, OPDAppointment, LabTestBooking, Hospital, Queue, DiagnosticDepartment, DiagnosticTest
from sqlalchemy.orm import aliased
from geopy.distance import great_circle
import random
from werkzeug.utils import secure_filename
import messagebird
from flask_mail import Mail, Message  # Import Message here
import os
from datetime import datetime, timedelta
from routes.hospital_routes import hospital_bp
# Initialize Flask Blueprint
user_bp = Blueprint('user_bp', __name__)
# Initialize Flask-Mail
mail = Mail()
# Your MessageBird API key
MESSAGEBIRD_API_KEY = '8XOUzqZZ0uxGo4GSKYkTMSFQCSvxQW0JoqtB'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
UPLOAD_FOLDER = 'static/images/'
# Initialize the MessageBird client
client = messagebird.Client(MESSAGEBIRD_API_KEY)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load configuration from config.json
with open('config.json') as config_file:
    config = json.load(config_file)
hospital_bp = Blueprint('hospital_bp', __name__)

# Lab test booking page
# Function for booking a lab test
# Function for booking a lab test
@user_bp.route('/book_lab_test', methods=['GET', 'POST'])
@login_required
def book_lab_test():
    if request.method == 'POST':
        department_id = request.form.get('department')
        test_id = request.form.get('test')
        hospital_id = request.form.get('hospital')
        price = request.form.get('price')
        booking_date = request.form.get('booking_date')  # Get the booking date

        if not booking_date:
            flash('Booking date is required.', 'danger')
            return redirect(url_for('user_bp.book_lab_test'))



        # Handle file upload for prescription
        if 'prescription' not in request.files or request.files['prescription'].filename == '':
            flash('No prescription file selected.', 'danger')
            return redirect(url_for('user_bp.book_lab_test'))

        file = request.files['prescription']

        # Validate the file type
        if not allowed_file(file.filename):
            flash('Invalid file format. Only PDF, JPG, and PNG are allowed.', 'danger')
            return redirect(url_for('user_bp.book_lab_test'))

        # Secure filename and save the file using the path from config.json
        filename = secure_filename(file.filename)
        upload_folder = config['params']['upload_location']  # Fetch from config.json

        # Ensure the directory exists
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Save the file in the UPLOAD_FOLDER and construct the relative path
        file.save(os.path.join(upload_folder, filename))

        # Store the relative path to be saved in the database
        prescription_path = "images/" + filename  # This is the path relative to the static folder

        # Generate a unique 4-digit booking code
        booking_code = str(random.randint(1000, 9999))

        # Save the booking in the database
        booking = LabTestBooking(
            user_id=current_user.id,
            test_category=DiagnosticDepartment.query.get(department_id).name,
            test_name=DiagnosticTest.query.get(test_id).name,
            hospital_id=hospital_id,
            booking_date=booking_date,  # Save the booking date
            prescription=prescription_path,  # Save the relative path to the prescription
            booking_code=booking_code,
            status='Pending'
        )
        db.session.add(booking)
        db.session.commit()

        # Send a confirmation email
        hospital = Hospital.query.get(hospital_id)
        test = DiagnosticTest.query.get(test_id)
        msg = Message('Lab Test Booking Confirmation', recipients=[current_user.email])
        msg.body = f"""
        Dear {current_user.name},

        Your lab test booking has been confirmed:
        Test: {test.name}
        Price: ₹{price}
        Hospital: {hospital.name}
        Booking Code: {booking_code}

        Please show this code at the hospital on arrival.

        Best regards,
        Hospital Management System
        """
        mail.send(msg)

        flash('Lab test booked successfully! Confirmation email sent.', 'success')
        return redirect(url_for('user_bp.lab_test_booking_history'))

    # Fetch available departments, tests, and hospitals for form selection
    departments = DiagnosticDepartment.query.all()
    return render_template('user_dashboard/book_lab_test.html', departments=departments)

# Lab test booking history
@user_bp.route('/lab_test_booking_history')
@login_required
def lab_test_booking_history():
    # Fetch the current user's lab test bookings
    bookings = LabTestBooking.query.filter_by(user_id=current_user.id).all()
    return render_template('user_dashboard/lab_test_booking_history.html', bookings=bookings)
@user_bp.route('/view_check_ins', methods=['GET'])
@login_required
def view_check_ins():
    test_id = request.args.get('test_id')
    booking_date = request.args.get('booking_date')

    # Fetch bookings for the specific date and test
    bookings = LabTestBooking.query.filter_by(test_id=test_id, booking_date=booking_date, status='Verified').all()

    return render_template('user_dashboard/view_check_ins.html', bookings=bookings)

# Fetch tests based on selected department
@user_bp.route('/get_tests_by_department/<int:department_id>')
@login_required
def get_tests_by_department(department_id):
    tests = DiagnosticTest.query.filter_by(department_id=department_id).all()
    return jsonify({'tests': [{'id': test.id, 'name': test.name, 'price': test.price} for test in tests]})

# Fetch hospitals offering the selected test
@user_bp.route('/get_hospitals_by_test/<int:test_id>')
@login_required
def get_hospitals_by_test(test_id):
    # Fetch the test and join it with DiagnosticDepartment to get the hospital
    hospitals = Hospital.query.join(DiagnosticDepartment, Hospital.id == DiagnosticDepartment.hospital_id) \
                              .join(DiagnosticTest, DiagnosticTest.department_id == DiagnosticDepartment.id) \
                              .filter(DiagnosticTest.id == test_id).all()
    
    # Fetch the test to get the price
    test = DiagnosticTest.query.get(test_id)
    
    return jsonify({
        'hospitals': [{'id': hospital.id, 'name': hospital.name} for hospital in hospitals],
        'price': test.price
    })






@user_bp.route('/dashboard')
@login_required
def dashboard():
    
    current_bookings = Booking.query.filter_by(user_id=current_user.id, status='Confirmed').all()
    return render_template('user_dashboard/index.html', current_bookings=current_bookings)

@user_bp.route('/book_bed', methods=['POST'])
@login_required
def book_bed():
    if Booking.query.filter_by(user_id=current_user.id, status='Confirmed').count() > 0:
        return jsonify({'success': False, 'message': 'You already have a confirmed booking.'}), 400

    data = request.json
    hospital_id = data.get('hospital_id')
    ambulance_required = data.get('ambulance_required')
    hospital = Hospital.query.get(hospital_id)

    if not hospital:
        return jsonify({'success': False, 'message': 'Hospital not found.'}), 404

    if hospital.vacant_general_beds <= 0:
        return jsonify({'success': False, 'message': 'No General beds available.'}), 400

    # Check user location and address
    if not current_user.location or not current_user.address:
        return jsonify({'success': False, 'message': 'User location or address not set.'}), 400

    # Calculate distance and generate admission code
    user_lat, user_lng = map(float, current_user.location.split(','))
    distance = great_circle((user_lat, user_lng), (hospital.latitude, hospital.longitude)).kilometers
    admission_code = str(random.randint(1000, 9999))

    # Create a new booking
    booking = Booking(
        user_id=current_user.id,
        hospital_id=hospital_id,
        bed_type='General',
        distance=distance,
        status='Confirmed',
        admission_code=admission_code
    )
    db.session.add(booking)
    db.session.commit()

    if ambulance_required:
        # Fetch a random ambulance from the hospital
        ambulance = Ambulance.query.filter_by(hospital_id=hospital_id).first()

        if not ambulance:
            return jsonify({'success': False, 'message': 'No ambulance available.'}), 400

        # Send email with ambulance details
        msg = Message('Booking Confirmation with Ambulance Service',
                      sender=os.environ.get('SENDER_EMAIL'),
                      recipients=[current_user.email])
        msg.body = f"""
        Dear {current_user.name},

        Your booking for a General bed at {hospital.name} has been confirmed.
        Your admission code is {admission_code}.

        Ambulance Driver: {ambulance.driver_name}
        Driver Phone: {ambulance.driver_phone}
        Vehicle Number: {ambulance.vehicle_number}

        Best regards,
        Hospital Management System
        """
        mail.send(msg)
    else:
        # Send normal email confirmation
        msg = Message('Booking Confirmation',
                      sender=os.environ.get('SENDER_EMAIL'),
                      recipients=[current_user.email])
        msg.body = f"""
        Dear {current_user.name},

        Your booking for a General bed at {hospital.name} has been confirmed.
        Your admission code is {admission_code}.

        Best regards,
        Hospital Management System
        """
        mail.send(msg)

    return jsonify({'success': True, 'message': 'Bed booked successfully.'}), 200






@user_bp.route('/rate_service', methods=['POST'])
@login_required
def rate_service():
    rating = Rating(user_id=current_user.id, hospital_id=request.form.get('hospital_id'), driver_id=request.form.get('driver_id'), rating=request.form.get('rating'), feedback=request.form.get('feedback'))
    db.session.add(rating)
    db.session.commit()
    flash("Thank you for your feedback!", "success")
    return redirect(url_for('user_bp.dashboard'))

@user_bp.route('/nearby_hospitals', methods=['POST'])
@login_required
def nearby_hospitals():
    user_lat = request.json.get('latitude')
    user_lng = request.json.get('longitude')
    bed_type = request.json.get('bed_type')

    if not user_lat or not user_lng:
        return jsonify({'error': 'Missing latitude or longitude'}), 400

    hospitals = Hospital.query.all()
    nearby_hospitals = []
    for hospital in hospitals:
        hospital_location = (hospital.latitude, hospital.longitude)
        user_location = (float(user_lat), float(user_lng))
        distance = great_circle(user_location, hospital_location).kilometers

        if distance <= 5:
            # Sum all ready beds across all wards for this hospital
            icu_beds_ready = Bed.query.join(Ward).filter(
                Bed.bed_type == 'ICU',
                Bed.status == 'ready',
                Ward.hospital_id == hospital.id
            ).count()

            opd_beds_ready = Bed.query.join(Ward).filter(
                Bed.bed_type == 'OPD',
                Bed.status == 'ready',
                Ward.hospital_id == hospital.id
            ).count()

            general_beds_ready = Bed.query.join(Ward).filter(
                Bed.bed_type == 'General',
                Bed.status == 'ready',
                Ward.hospital_id == hospital.id
            ).count()

            nearby_hospitals.append({
                'id': hospital.id,
                'name': hospital.name,
                'address': hospital.address,
                'distance': round(distance, 2),
                'vacant_icu_beds': icu_beds_ready,
                'vacant_opd_beds': opd_beds_ready,
                'vacant_general_beds': general_beds_ready,
                'contact_info': hospital.contact_info,
                'latitude': hospital.latitude,
                'longitude': hospital.longitude,
            })

    return jsonify(nearby_hospitals), 200


@user_bp.route('/save_phone_number', methods=['POST'])
@login_required
def save_phone_number():
    data = request.json
    phone = data.get('phone')

    if phone:
        current_user.phone = phone
        db.session.commit()
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'message': 'Phone number is required.'}), 400

def is_whatsapp_number(phone_number):
    try:
        lookup = client.lookup(phone_number, {'type': 'whatsapp'})
        return lookup and lookup.whatsapp
    except messagebird.client.ErrorException as e:
        print(f"Error checking WhatsApp number: {e}")
        return False

def send_whatsapp_message(phone_number, message):
    try:
        msg = client.message_create(
            originator='918240575718',
            recipients=[phone_number],
            body=message,
            messaging_type='whatsapp'
        )
        print(f"WhatsApp message sent successfully: {msg.id}")
        return msg.id
    except messagebird.client.ErrorException as e:
        print(f"Failed to send WhatsApp message: {e}")
        return None


@user_bp.route('/update_whatsapp_number', methods=['POST'])
@login_required
def update_whatsapp_number():
    new_whatsapp_number = request.form.get('whatsapp_number')
    if not new_whatsapp_number:
        return jsonify({'success': False, 'message': 'Please enter a valid WhatsApp number.'}), 400

    if not is_whatsapp_number(new_whatsapp_number):
        return jsonify({'success': False, 'message': 'The entered number is not registered with WhatsApp.'}), 400

    current_user.phone = new_whatsapp_number
    db.session.commit()
    return jsonify({'success': True, 'message': 'WhatsApp number updated successfully.'}), 200


@user_bp.route('/booking_history')
@login_required
def booking_history():
    past_bookings = Booking.query.filter(
        Booking.user_id == current_user.id,
        Booking.created_at < datetime.utcnow() - timedelta(hours=24)
    ).all()
    return render_template('user_dashboard/booking_history.html', bookings=past_bookings)

@user_bp.route('/save_address', methods=['POST'])
@login_required
def save_address():
    data = request.json
    location = data.get('location')
    address = data.get('address')

    if location and address:
        current_user.location = location
        current_user.address = address
        db.session.commit()
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid data.'}), 400

@user_bp.route('/cancel_booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking or booking.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Booking not found or access denied.'}), 404
    
    booking.status = 'Cancelled'
    db.session.commit()
    
    return jsonify({'success': True}), 200


@user_bp.route('/book_opd', methods=['GET', 'POST'])
@login_required
def book_opd():
    if request.method == 'POST':
        appointment_date = request.form.get('appointment_date')
        doctor_id = request.form.get('doctor_id')
        time_slot = request.form.get('time_slot')
        hospital_id = request.form.get('hospital_id')  # Capture the hospital_id from the form
        appointment_code = str(random.randint(1000, 9999))

        # Ensure the current user hasn't already booked this slot
        existing_appointment = OPDAppointment.query.filter_by(
            user_id=current_user.id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            time_slot=time_slot
        ).first()

        if existing_appointment:
            flash('You have already booked this time slot.', 'warning')
            return redirect(url_for('user_bp.view_appointments'))

        # Update user details if provided
        current_user.phone = request.form.get('phone') or current_user.phone
        current_user.age = request.form.get('age') or current_user.age
        current_user.address = request.form.get('address') or current_user.address

        # Create the OPDAppointment with the hospital_id
        appointment = OPDAppointment(
            user_id=current_user.id,
            doctor_id=doctor_id,
            hospital_id=hospital_id,  # Ensure hospital_id is saved
            appointment_date=appointment_date,
            time_slot=time_slot,
            appointment_code=appointment_code
        )
        db.session.add(appointment)
        db.session.commit()

        # Send confirmation email
        doctor = Doctor.query.get(doctor_id)
        hospital = Hospital.query.get(hospital_id)
        msg = Message('Your OPD Appointment Details', recipients=[current_user.email])
        msg.body = f"""
        Dear {current_user.name},

        Your appointment is confirmed with Dr. {doctor.name} at {hospital.name} on {appointment_date} at {time_slot}.
        Appointment Code: {appointment_code}

        Thank you for choosing our hospital.
        """
        mail.send(msg)

        flash('Appointment booked successfully', 'success')
        return redirect(url_for('user_bp.view_appointments'))

    hospitals = Hospital.query.all()
    return render_template('user_dashboard/book_opd.html', hospitals=hospitals)



@user_bp.route('/view_appointments', methods=['GET'])
@login_required
def view_appointments():
    today = datetime.today().date()
    end_date = today + timedelta(days=10)
    appointments = OPDAppointment.query.filter(
        OPDAppointment.user_id == current_user.id,
        OPDAppointment.appointment_date.between(today, end_date)
    ).all()
    return render_template('user_dashboard/view_appointments.html', appointments=appointments)



@user_bp.route('/get_doctors/<int:department_id>', methods=['GET'])
def get_doctors(department_id):
    appointment_date = request.args.get('date')
    
    if not appointment_date:
        return jsonify({'doctors': []})

    date_obj = datetime.strptime(appointment_date, '%Y-%m-%d')
    weekday_name = date_obj.strftime('%A')

    doctors = Doctor.query.filter_by(department_id=department_id).all()
    available_doctors = []

    for doctor in doctors:
        availability_days = [day.strip().capitalize() for day in doctor.availability_days.split(',')]
        if weekday_name in availability_days:
            available_doctors.append({
                'id': doctor.id,
                'name': doctor.name
            })

    return jsonify({'doctors': available_doctors})

@user_bp.route('/get_time_slots/<int:doctor_id>/<string:appointment_date>', methods=['GET'])
@login_required
def get_time_slots(doctor_id, appointment_date):
    appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()

    # Fetch all appointments for the selected doctor and date
    existing_appointments = OPDAppointment.query.filter_by(
        doctor_id=doctor_id, 
        appointment_date=appointment_date
    ).all()

    occupied_slots = set(appointment.time_slot for appointment in existing_appointments if appointment.user_id == current_user.id)
    
    all_slots = Doctor.query.get(doctor_id).chamber_timings.split(',')
    available_slots = [slot for slot in all_slots if slot not in occupied_slots]

    return jsonify({'time_slots': available_slots})



@user_bp.route('/get_departments/<int:hospital_id>', methods=['GET'])
def get_departments(hospital_id):
    departments = Department.query.filter_by(hospital_id=hospital_id).all()
    return jsonify({'departments': [{'id': dept.id, 'name': dept.name} for dept in departments]})

@user_bp.route('/doctor_details/<int:doctor_id>', methods=['GET'])
@login_required
def doctor_details(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    return render_template('user_dashboard/doctor_details.html', doctor=doctor)