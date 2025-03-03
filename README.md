# duplicate-image-finder

duplicate-image-finder/
│── backend/                   # Node.js (TypeScript) backend
│   ├── src/
│   │   ├── services/          # Business logic (e.g., image processing, Puppeteer scraping)
│   │   ├── controllers/       # API endpoints
│   │   ├── models/            # Data models (if needed)
│   │   ├── utils/             # Helper functions
│   │   ├── index.ts           # Entry point
│   ├── tests/                 # Unit tests
│   ├── package.json
│   ├── tsconfig.json
│   ├── Dockerfile
│   ├── .env.example
│   ├── scripts/               # Bash/PowerShell scripts for setup & automation
│── ai-processing/             # CLIP & YOLO-based image analysis
│   ├── models/                # Pretrained models & weights
│   ├── src/
│   │   ├── image_similarity.py # CLIP-based similarity detection
│   │   ├── object_detection.py # YOLO-based object detection
│   │   ├── pipeline.py         # Main processing pipeline
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile
│── frontend/                   # Next.js + React UI
│   ├── pages/
│   ├── components/
│   ├── public/
│   ├── styles/
│   ├── package.json
│   ├── tsconfig.json
│   ├── Dockerfile
│── docker-compose.yml          # Multi-container setup
│── .gitignore
│── README.md
