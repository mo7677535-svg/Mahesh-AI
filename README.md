# Mini AI Chatbot (FREE - Google Gemini)
Made by Mahesh Oli. Ask any question and get a simple answer.

## Easy run (Windows)
1. Extract this zip (right-click > Extract All).
2. Open the extracted folder and double-click run.bat
3. Paste your Gemini key when asked (get a free key at https://aistudio.google.com > Get API key).
4. Your browser opens at http://localhost:8000. Keep the black window open while you chat.

## Run in VS Code
File > Open Folder > select this folder, then in the terminal:
    pip install -r requirements.txt
    python web_chatbot.py
Press F5 to run the browser version (choose "Run Browser Chatbot").

## Save your key (optional)
Open the .env file, write GEMINI_API_KEY=your-key on one line, press Ctrl+S.
Never share your key with anyone.
