# 📌 **Duplicate Image Finder Agent**
A **Node.js (TypeScript) & AI-powered tool** for finding duplicate images using **Puppeteer**, **CLIP**, and **YOLO**. This project scrapes **Google Photos**, extracts image metadata, and detects similar/duplicate images using machine learning.

---

## **🚀 Project Structure**
```
duplicate-image-finder/
│── backend/                   # Node.js backend (API + Puppeteer scraper)
│   ├── src/
│   │   ├── services/          # Business logic (Puppeteer scraping, AI processing)
│   │   ├── controllers/       # API endpoints
│   │   ├── models/            # Data models
│   │   ├── index.ts           # Entry point
│   ├── package.json
│   ├── tsconfig.json
│   ├── Dockerfile
│── ai-processing/             # Python-based image similarity & object detection
│   ├── models/                # Pretrained models & weights
│   ├── src/
│   │   ├── image_similarity.py # CLIP-based similarity detection
│   │   ├── object_detection.py # YOLO-based object detection
│   │   ├── pipeline.py         # Main processing pipeline
│   ├── requirements.txt
│   ├── Dockerfile
│── frontend/                   # Next.js + React UI
│   ├── pages/
│   ├── components/
│   ├── package.json
│   ├── tsconfig.json
│   ├── Dockerfile
│── scripts/                    # Automation scripts
│   ├── setup.sh                # Installs dependencies, builds & starts services
│   ├── run_scraper.sh          # Starts Puppeteer scraper
│   ├── process_images.sh       # Runs AI pipeline
│── docker-compose.yml          # Multi-container setup
│── .gitignore
│── README.md                   # Project documentation
```

---

## **🔧 Prerequisites**
Before running this project, ensure you have:
- **Node.js** (`v18+`)
- **Python** (`v3.10+`)
- **Docker & Docker Compose**
- **Git**

---

## **⚡ Setup & Run the Project**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-repo/duplicate-image-finder.git
cd duplicate-image-finder
```

### **2️⃣ Run Setup Script**
This script installs dependencies, builds Docker containers, and starts the project.
```bash
bash scripts/setup.sh
```

If on **Windows**, use PowerShell:
```powershell
./scripts/setup.ps1
```

### **3️⃣ Verify Running Containers**
Check that the **backend, AI processing, and frontend** are running:
```bash
docker ps
```

---

## **🛠 Troubleshooting Start-up Issues**
If you face issues during setup, try these fixes:

### **1️⃣ Node.js Dependencies Issues**
If `npm install` fails inside `backend/` or `frontend/`, run:
```bash
cd backend
rm -rf node_modules package-lock.json
npm install
cd ../frontend
rm -rf node_modules package-lock.json
npm install
```

---

### **2️⃣ Python Virtual Environment Issues**
If you see:
```
externally managed environment error
```
Fix it by setting up a **Python virtual environment**:
```bash
cd ai-processing
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### **3️⃣ Docker Issues**
#### 🛑 **Docker Compose Not Found**
If `docker-compose` command fails:
```bash
brew install docker-compose  # macOS
sudo apt install docker-compose  # Linux
```
or use:
```bash
docker compose up --build -d  # (without `-`)
```

#### 🛑 **Error: "Dockerfile Cannot Be Empty"**
Ensure `backend/`, `frontend/`, and `ai-processing/` each have a **Dockerfile**.  
If missing, recreate them and retry:
```bash
docker compose up --build -d
```

---

### **4️⃣ Fixing AI Processing Issues**
If `torch` or `torchvision` installation fails:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```
Update `requirements.txt` with the correct versions.

---

## **🎯 Next Steps**
1️⃣ Implement **Puppeteer scraper** for Google Photos.  
2️⃣ Enhance **AI image comparison** using CLIP & YOLO.  
3️⃣ Improve **UI & user experience** in Next.js.  

---

## **📜 License**
This project is licensed under **MIT License**.

---

### **🚀 Need Help?**
If you're stuck, open an **issue on GitHub** or reach out to the contributors.  
