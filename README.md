SAMAKSH - Assistive Vision Agent for Visually Impaired Indians

Team Elite Achievers
Lead: Dhruv Gupta
WHAT WE'RE BUILDING

SAMAKSH is a wearable AI device that helps blind people read text and understand their surroundings through voice interaction in Hindi and English. It costs ₹4,880 - which is 95% cheaper than existing solutions like OrCam MyEye (₹1,00,000+).
The device is a camera + speaker system you can wear or hold. Press a button, it captures what's in front of you, reads the text aloud in the detected language, and then you can ask follow-up questions through voice.

WHO IS THIS FOR

Primary users: Visually impaired individuals in tier 2/3 cities and rural India who:
- Can't afford expensive assistive devices (₹50,000 - ₹1,00,000)
- Don't have or struggle with smartphones
- Need independence in daily tasks like reading bills, medicine labels, books, signboards
- Prefer voice interaction in Hindi or regional languages

Target market: 8 million visually impaired people in India. We're aiming for 100,000 users in the first year through NGO partnerships.

THE CORE PROBLEM WE'RE SOLVING

Right now, blind people depend on others to read everyday things - medicine bottles, electricity bills, bank statements, letters, signboards. Existing assistive devices are prohibitively expensive. Smartphone apps exist but require significant tech literacy and screen navigation.

Our job-to-be-done: Enable independent reading of printed text and basic scene understanding through a simple, affordable, hands-free device with voice interaction.

Success metric: Reduce dependency on sighted assistance for reading daily documents from 100% to under 20%.

HOW IT WORKS (THE AGENT ACTIONS)

This isn't just OCR. SAMAKSH is an autonomous agent that takes actions:

1. Vision-to-Action Pipeline
   Button press → Captures image → Extracts text via OCR → Detects language (Hindi/English) → Reads aloud in that language → Stores in memory

2. Conversational Context Agent
   Maintains conversation history. User can ask "repeat that paragraph" or "what was the expiry date" and it retrieves from memory and responds.

3. Scene Understanding
   When no text is found, offers to describe the environment using GPT-4 Vision. "I see a room with a desk on the left, bookshelf on the right..."

4. Language Auto-Switching
   Automatically detects Devanagari script vs Latin and switches TTS language. Mixed Hindi-English documents are handled naturally.

5. Voice Command Router
   Routes spoken queries to correct function - whether it's re-reading text, explaining something, or describing a scene.

Example workflow:
User presses capture button → Device reads medicine label in Hindi → User asks "खुराक फिर से बताओ" (tell me dosage again) → Device retrieves that specific info from context → Responds in Hindi

Another workflow:
User captures government form → Device reads all sections → User asks "form ki deadline kya hai?" → Device extracts deadline from stored context → Responds conversationally

This is repeatable, autonomous, and doesn't require user to understand the system - just press button and ask.

WHY THIS CAN REACH 1 BILLION (OR BE ON PATH TO IT)

Cost Economics:
Current hardware cost: ₹4,880
At 1,000 units: ₹3,340 per device
At 10,000 units: ₹2,530 per device

Operational cost per user: ₹170/month (includes API costs, support, infrastructure)

Why it scales:
- Qualifies for government ADIP subsidy (₹50,000 available for assistive tech - we're 90% under that limit, making approval easy)
- Open-source hardware means local repair shops can fix it, NGOs can manufacture it
- No smartphone required, works for feature phone users
- Single API call per interaction, not streaming (low token costs)

Distribution strategy:
Phase 1: Partner with National Association for the Blind, Sightsavers India, Blind Relief Association for initial 500 units
Phase 2: Apply for government procurement under accessibility initiatives
Phase 3: Bulk orders to 250+ blind schools across India
Phase 4: E-commerce with EMI options for direct consumers

The path to scale is through institutional partnerships first, then individual sales. Government subsidy makes it free for economically weaker sections.

---

ACCESSIBILITY BARRIERS WE ADDRESS

Connectivity: Core features (OCR + text reading) work completely offline. Only conversational AI needs internet, and that's optional.

Cost: 95% cheaper than alternatives. At scale, under ₹3,000.

Device constraints: Standalone hardware. No smartphone needed. No app downloads. No updates.

Language: Hindi + English with auto-detection. Expandable to Tamil, Telugu, Bengali, Marathi, Gujarati post-hackathon.

Literacy: Zero reading or typing required. 100% voice interaction. Physical buttons, no screen navigation.

Disability: Built specifically for blind users, not adapted from sighted-user products.

Trust: All text processing happens on-device. Cloud AI only called when user explicitly asks questions. No data collection.

Graceful degradation:
- No internet: Text reading still works fully
- Slow 2G: Works but conversational AI takes 20-30 seconds
- No API credits: Basic OCR + TTS continues, AI features disabled with notification

---

TECHNICAL IMPLEMENTATION

Hardware:
- Raspberry Pi Zero 2W (₹1,500)
- Pi Camera Module v2 (₹1,200)
- USB Microphone (₹300)
- USB Audio adapter + Earphone (₹200)
- 2 GPIO buttons for capture and voice mode (₹20)
- Power bank 10,000mAh (₹800)
- MicroSD card 32GB (₹400)
- Enclosure and wiring (₹460)
Total: ₹4,880

Software stack:
- EasyOCR for text extraction (supports Hindi + English + 78 other languages, runs on-device)
- gTTS for text-to-speech with offline pyttsx3 fallback
- Google Speech Recognition for voice input
- OpenAI GPT-4o-mini for conversational AI (₹0.01 per query)
- picamera2 for image capture
- Python 3.11 running on Raspberry Pi OS

Architecture:
Button press → Camera captures image → EasyOCR extracts text (5-8 seconds on device) → Language detection (checks for Devanagari script) → gTTS converts to speech → Audio plays through speaker → Text stored in context → User presses voice button → Mic captures speech → Google STT converts to text → GPT-4 processes with context → Response synthesized to speech → Audio output

Performance:
- Text reading: 8-13 seconds total (fully offline possible)
- Voice interaction: 13-21 seconds (requires internet for AI)
- Battery life: 8-10 hours continuous use

What we're NOT building (to stay focused):
- No medical diagnosis or health advice
- No navigation/obstacle detection (separate product)
- No form submission (only reads forms)
- No social media integration
- No mobile app companion
- No cloud storage of personal data

---

DEMO SCENARIOS

Scenario 1: Reading Hindi medicine label
User points device at medicine bottle, presses button
Device: "छवि कैप्चर कर रहा हूं... पाठ पढ़ रहा हूं... सिट्राजिन टैबलेट। एक गोली दिन में दो बार। भोजन के बाद लें।"
User presses voice button: "खुराक फिर से बताओ"
Device: "एक गोली दिन में दो बार"

Scenario 2: Reading electricity bill
User captures bill
Device: "Consumer number 123456789. Current bill amount: Rupees 850. Due date: 25th March 2025."
User: "What happens if I pay late?"
Device analyzes stored text: "Late payment will incur a charge of 50 rupees after due date."

Scenario 3: Understanding unfamiliar room
User enters room, presses capture button
Device: "No text found. Would you like me to describe the scene?"
User presses voice: "Yes, describe what you see"
Device: "I see a living room. There's a sofa on the left side, a coffee table in the center, and a TV mounted on the wall ahead."

---

WHY THIS IS DIFFERENT

Compared to OrCam MyEye (₹1,00,000):
- 95% cheaper
- Has conversational AI, not just command-based
- Supports Hindi and regional languages (OrCam is English only)
- Open-source and repairable

Compared to smartphone apps:
- Hands-free wearable, no phone fumbling
- Single-purpose device is more reliable
- Works for people without smartphones
- Physical buttons, no screen navigation

Compared to other hackathon projects:
- Actual hardware integration, not just software
- Production-ready cost model, not ₹50,000 prototype
- True agentic actions with context management
- Multilingual from day one

Fresh angles:
- Conversational memory - remembers what it read, answers follow-ups
- Code-switching support for Hindi-English mix (natural Indian usage)
- Community manufacturing model through open-source
- Priced specifically to qualify for government subsidy

---

VALIDATION SO FAR

User research: Interviewed 12 visually impaired individuals at NAB Delhi
Key findings:
- 9 out of 12 use smartphones but struggle with screen readers
- 11 out of 12 prefer voice in Hindi over English
- 8 out of 12 need help reading bills/medicines daily
- All expressed strong desire for reading independence

Beta testing: 5 users tested prototype
- 85% text recognition accuracy on printed text
- 92% satisfaction with voice interaction
- Average 3.2 uses per day per user
- Main feedback: wants more languages, better battery life

Cost validation: Received quotes from 3 manufacturers
- At 1,000 units: ₹3,340 per device confirmed
- At 10,000 units: ₹2,530 per device confirmed
- Breakeven at 500 units per month

---

ROADMAP

Hackathon (current):
Text reading in English and Hindi, scene understanding, voice Q&A, conversational context

Post-hackathon (Month 1-3):
Add Tamil, Telugu, Bengali, Marathi, Gujarati
Currency recognition for Indian notes
Offline LLM (Phi-2) for conversational features
Battery optimization to 12+ hours
User testing with 50 blind individuals

Pilot phase (Month 4-6):
Partnership with NAB, Sightsavers, Blind Relief Association
Deploy 100 devices
Collect usage data
Apply for ADIP subsidy approval

Scale phase (Month 7-12):
Manufacturing partnership for 1,000 units/month
E-commerce launch
Government procurement participation
Expand to 10 Indian languages

---

MEASURABLE SUCCESS

Primary metric: Daily Active Usage Rate
Target: 70% of users use the device at least once daily within 30 days of receiving it
Current baseline: 0% (no device exists)
Industry comparison: OrCam users report 3-5 uses per day

Secondary metrics:
- Task completion rate above 80% (successful text readings)
- User satisfaction NPS above 50
- Independence score: self-reported reduction in sighted assistance

Tracking: Anonymous usage logs (button presses, session duration, no personal data)

---

WHAT WE'RE NOT INCLUDING

We explicitly decided NOT to build:
- Medical diagnosis features (only reads labels, no health advice)
- Navigation system (different product category)
- Form filling and submission (compliance and liability)
- Social media integration (privacy-first approach)
- Currency identification (planned for v2)
- Cloud storage (all local processing)

This keeps the product focused, safe, and achievable in hackathon timeline.

---

FILES AND CODE

Project structure:
samaksh/
├── main.py (orchestrates everything)
├── config.py (all settings)
├── modules/
│   ├── camera.py (image capture)
│   ├── ocr.py (text extraction)
│   ├── tts.py (speech synthesis)
│   ├── stt.py (speech recognition)
│   ├── ai.py (LLM agent)
│   └── gpio_control.py (button handling)
├── data/
│   ├── captured_images/ (temp storage)
│   ├── audio_cache/ (TTS cache)
│   └── context.json (conversation memory)

Setup: Flash Raspberry Pi OS on SD card, install dependencies (EasyOCR, gTTS, speech_recognition, RPi.GPIO, picamera2, openai), wire up buttons and camera, configure API keys, run main.py

Testing: Individual module tests, then full integration test with real-world documents
We split work as:
- Hardware integration (Pi, camera, audio setup, enclosure)
- AI/ML pipeline (OCR, speech recognition, LLM)
- Software orchestration (main logic, context management, APIs)
- UX/Voice design (interaction flows, multilingual TTS, error handling)
