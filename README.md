UltraVision AI – An AI-powered Ultrasound Assistant that helps healthcare professionals by:

Enhancing ultrasound image quality.
Detecting breast tumors (Normal / Benign / Malignant).
Segmenting (highlighting) suspicious regions.
Assessing image quality.
Generating an AI-assisted medical report.
Assisting doctors, not replacing them.

## Backend

A complete, modular FastAPI backend now lives in [`backend/`](backend/README.md) —
authentication, image upload/enhancement, pluggable disease classification
(breast/lung/skin/retina), Grad-CAM, a chatbot, PDF/HTML reports, and patient
history, with Docker, Alembic, and a passing pytest suite. AI inference points
are placeholder interfaces ready for real models. See `backend/README.md` for
architecture, diagrams, and full endpoint documentation.

