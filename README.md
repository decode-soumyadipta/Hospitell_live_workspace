
          
# 🏥 HOSPITELL: Effortless Bed & OPD Management

![Hospitell Logo](https://github.com/user-attachments/assets/b67f4445-039a-4831-8710-85fbf63cebdc)

## 📋 Overview

Hospitell is a comprehensive healthcare management platform that bridges the gap between patients and healthcare providers. The platform offers seamless bed and OPD management, enabling instant availability information for patients while providing streamlined control for hospitals, all enhanced by AI/LLM -powered features like chatbot based appointment booking.

## ✨ Key Features

### 👨‍👩‍👧‍👦 For Patients

- **🛏️ Bed Booking System**: Search and book hospital beds based on location, availability, and bed type (ICU, General, OPD)
- **🗓️ OPD Appointment Management**: Schedule, reschedule, and track outpatient appointments
- **🔬 Lab Test Booking**: Book diagnostic tests and receive results securely
- **🔐 Medical Records on Blockchain**: Store medical records securely using blockchain technology and IPFS
- **🚑 Ambulance Services**: Request and track ambulance services in real-time
- **🤖 AI-Powered Chatbot (ResQ)**: Get instant assistance and information
- **⏱️ Virtual Queue Management**: Join virtual queues to reduce waiting time at hospitals

### 🏢 For Hospitals

- **📊 Comprehensive Dashboard**: Monitor and manage all hospital resources in real-time
- **🏥 Ward & Bed Management**: Track and update bed availability across different wards
- **👨‍⚕️ Staff Management**: Manage doctors, nurses, and other staff efficiently
- **🏬 Department Administration**: Organize hospital departments and diagnostic services
- **💊 Medicine Inventory**: Track and manage medicine inventory and batches
- **🧍‍♂️ Queue Management**: Manage both physical and virtual patient queues
- **🔔 Notification System**: Automated notifications for appointments, bed availability, and more

### 🔧 Advanced Technology Features

- **⛓️ Blockchain Integration**: Secure storage of medical records using Ethereum smart contracts
- **📂 IPFS Storage**: Decentralized storage for medical documents and test results
- **📍 Geolocation Services**: Find nearby hospitals and services based on user location
- **⚡ Real-time Updates**: Live updates on bed availability and queue status
- **🔒 Multi-factor Authentication**: Secure login and data protection

## 🏗️ Technical Architecture

### 🖥️ Backend
- **🛠️ Framework**: Flask (Python)
- **🗄️ Database**: SQLAlchemy ORM with support for MySQL
- **🔑 Authentication**: Flask-Login with OAuth support (Google, Facebook)
- **⛓️ Blockchain**: Web3.py for Ethereum integration via Kaleido
- **📁 File Storage**: IPFS via Kaleido's IPFS service
- **📧 Notifications**: Email (Flask-Mail) and SMS integration

### 🎨 Frontend
- **📄 Templates**: Jinja2 with Bootstrap
- **⚙️ JavaScript**: jQuery, AJAX for dynamic content
- **🗺️ Maps Integration**: Geolocation services for hospital finding
- **📱 Responsive Design**: Mobile-friendly interface

### 🔐 Security Features
- **🔒 Password Hashing**: Secure password storage
- **🛡️ CSRF Protection**: Protection against cross-site request forgery
- **📤 Secure File Uploads**: Validation and sanitization of uploaded files
- **👮 Role-based Access Control**: Different permissions for patients, hospital admins, and staff

## 📥 Installation

### 📋 Prerequisites
- Python 3.8+
- MySQL Database
- Node.js and npm (for frontend dependencies)
- Ethereum account and Kaleido subscription (for blockchain features)

### 🔧 Setup

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/hospitell.git
   cd hospitell
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv hospi_venv
   source hospi_venv/bin/activate  # On Windows: hospi_venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables
   Create a `.env` file with the following variables:
   ```
   KALEIDO_RPC_URL=your_kaleido_rpc_url
   CONTRACT_ADDRESS=your_deployed_contract_address
   PRIVATE_KEY=your_ethereum_private_key
   KALEIDO_IPFS_URL=your_kaleido_ipfs_url
   KALEIDO_APP_ID=your_kaleido_app_id
   KALEIDO_APP_PASSWORD=your_kaleido_app_password
   ```

5. Initialize the database
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the application
   ```bash
   python app.py
   ```

## 📱 Usage

### 👨‍👩‍👧‍👦 Patient Portal
1. 🔐 Register/Login to the patient portal
2. 🔍 Search for hospitals based on location and bed availability
3. 📝 Book appointments or beds as needed
4. 📤 Upload and manage medical records securely on the blockchain
5. 📅 View booking history and upcoming appointments

### 🏢 Hospital Admin Portal
1. 🔐 Register/Login to the hospital admin portal
2. ⚙️ Manage hospital details, departments, and staff
3. 🔄 Update bed availability in real-time
4. 📊 Manage patient queues and appointments
5. 📈 View analytics and reports

## 🚀 Future Enhancements

- **👨‍⚕️ Telemedicine Integration**: Virtual consultations with doctors
- **💰 Health Insurance Integration**: Direct billing to insurance providers
- **📊 Advanced Analytics**: Predictive analytics for bed management and patient flow
- **📱 Mobile Applications**: Native mobile apps for Android and iOS
- **🔄 Interoperability**: Integration with other healthcare systems and EHRs

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. 🍴 Fork the repository
2. 🌿 Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🔍 Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

Project Link: [https://github.com/decode-soumyadipta/Hospitell_live_workspace](https://github.com/decode-soumyadipta/Hospitell_live_workspace)

---

*🏥 Hospitell - Revolutionizing healthcare management with technology*
        