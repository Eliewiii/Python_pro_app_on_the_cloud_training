# Gradual Algorithmic Productionization

![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-v0.110-05998b)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-orange)
![Deployment](https://img.shields.io/badge/AWS-App%20Runner-232F3E)

## 🎯 Project Mission
Mastering the transition from R&D scripts to professional software architecture. This project follows a 4-stage integration strategy to move a Python/C++ engine into a deployed cloud service.

---

## 🏗️ Directory Structure
```text
project-root/
├── app/                # FastAPI interface layer
│   └── main.py
├── benchmarks/         # Dedicated Profiling Suite
│   ├── README.md           <-- "How to run the performance tests"
│   ├── suite_test.py       <-- The high-level Benchmarking script
│   └── scripts/            
│       └── profile_logic.py <-- The low-level Profiling script 'core/'
│   └── outputs/        # Stores Flame Graphs and .prof files
├── core/               # Algorithmic engine (Modular Logic)
│   ├── __init__.py
│   └── processor.py
├── tests/              # Pytest suite
│   ├── fixtures/       # For files used for testing only.
│   ├── __init__.py
│   └── test_processor.py
├── .github/workflows/  # CI/CD Automation
├── requirements/       # Split requirements
│    ├── base.txt        # Production (FastAPI, NumPy)
│    └── dev.txt         # Benchmarking/Testing (Pytest, line_profiler, Py-Spy)
└── Dockerfile          # Phase 2: Containerization

