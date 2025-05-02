
# 🎙️ Vocalis

**Vocalis** is an AI-powered presentation assistant integrated into a Discord bot. It provides users with detailed feedback on their presentations, including voice analysis (speed, volume, tone, pitch, emotions, filler words, and pauses), content structure, strengths and weaknesses, fluency, and personalized improvement recommendations.

---

## 📑 Features

- **Easy Command to Call the Bot:** A simple command to activate the assistant.
- **Voice Analysis:** Evaluates voice speed, volume, tone, and pitch, along with detecting emotions, filler words, and pauses.
- **Content Structure Feedback:** Assesses the overall organization and flow of the presentation.
- **Strengths and Weaknesses Identification:** Highlights areas of strength and potential improvement.
- **Fluency Check:** Analyzes the smoothness of the presentation delivery.
- **Personalized Improvement Recommendations:** Provides tailored suggestions to enhance the presentation.

---

## 🛠 Tech Stack

- **Language:** Python
- **Bot Framework:** Pycord
- **AI Integration:** Google Gemini

---

## 🚀 Getting Started

### 1. Create a Discord Bot
- Go to the [Discord Developer Portal](https://discord.com/developers/applications)
- Create a new application and add a bot to it
- Copy the bot token

### 2. Clone the Repository
```bash
https://github.com/amjadAwad95/Vocalis.git
cd vocalis
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory and add:
```env
DISCORD_TOKEN=your_discord_token_here
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

---

## ▶️ How to Use Vocalis

1. **Add the Bot to Your Discord Server** using the OAuth2 URL from the Developer Portal.
2. **Start Your Presentation**  
   Type:
   ```
   /record
   ```
3. **Stop Your Presentation**  
   Type:
   ```
   /stop_recording
   ```
4. **Receive Feedback**  
   After a short wait, you’ll receive a feedback report as an HTML file.

---

## 📝 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
