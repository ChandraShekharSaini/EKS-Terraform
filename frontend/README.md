# Application Setup Guide

This guide provides step-by-step instructions to set up and run both the Backend (Java/Maven) and Frontend (Python/Streamlit) applications.

---

## Backend Setup

### 1. Create RDS Instance
Create an RDS database instance before proceeding with backend setup.


### 1. Install Dependencies
```bash
sudo yum install git -y
sudo yum install maven -y
```
### 3. Clone Repository
```bash
git clone https://github.com/CloudTechDevOps/Java-springboot-project.git
cd Java-springboot-project/backend
```
### 4. Configure RDS Details
Update the RDS connection details in:
```
/src/main/resources/application.properties
```
Ensure the database URL, username, and password match your RDS instance configuration.

### 5. Build Application
Run Maven build command from the backend directory:
```bash
mvn clean package -DskipTests=true
```

### 6. Navigate to Target Directory
```bash
cd target
```

### 7. Run JAR File
```bash
nohup java -jar datastore-0.0.7.jar > ~/datastore-nohup.out 2>&1 &  #if hard coded db crend
          or
nohup env \
  MYSQL_HOST=database-1.cxeakuo04ry1.us-east-1.rds.amazonaws.com \
  MYSQL_PORT=3306 \
  MYSQL_USERNAME=admin \
  MYSQL_PASSWORD=YOUR_PASSWORD_HERE \
  LOG_FILE_PATH=$LOG_DIR/datastore.log \
  java -jar target/datastore-0.0.7.jar \
  --server.port=8084 \
  > $LOG_DIR/nohup.out 2>&1 &
```
The backend application will now run on port **8084** (default configuration).
ps -ef | grep java #check process 


---

## Frontend Setup

### 1. Install Dependencies
```bash
sudo yum install git -y
sudo yum install python3-pip -y
```
### 2. Clone Repository
```bash
git clone https://github.com/CloudTechDevOps/Java-springboot-project.git
cd Java-springboot-project/frontend
```
### 3. Configure Backend API URL
Update the backend server IP in `app.py`:
```python
API_URL = os.environ.get("API_URL", "http://<BACKEND_PUBLIC_IP>:8084")
```
Replace `<BACKEND_PUBLIC_IP>` with the public IP address of your backend server. Keep the port as **8084**.

### 4. Install Python Dependencies
```bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Run Application
```bash
streamlit run app.py
     or run using pm2
pm2 start /root/myapp/venv/bin/streamlit \
  --name streamlit-app \
  --interpreter none \
  -- run /root/myapp/app.py --server.address=0.0.0.0 --server.port=8501
```
The frontend application will start on port **8501**.

streamlit is an open-source Python framework that lets you quickly build and share interactive web apps—especially for data science, machine learning, and analytics—without needing front-end skills like HTML, CSS, or JavaScript.

---

## Access the Application

Once both services are running fine

2. **Frontend Application**: `http://<FRONTEND_PUBLIC_IP>:8501`

Open your browser and navigate to the frontend URL using the public IP and port 8501.

---

