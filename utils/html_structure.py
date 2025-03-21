def html_structure(json_object):
    html = f"""
            <!DOCTYPE html>
        <html lang="{json_object["language_code"]}" dir="{json_object["text_direction"]}">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{json_object["title_text"]}</title>
            <style>
                /* CSS Variables for Light/Dark Mode */
                :root {{
                    --bg-color: #f9f9f9;
                    --container-bg: #fff;
                    --text-color: #333;
                    --heading-color: #2e7d32;
                    --section-bg: #f5f5f5;
                    --box-shadow-color: rgba(0, 0, 0, 0.1);
                    --border-color: #ccc;
                    --analysis-bg: #e8f5e9;
                    --read-more-color: #2e7d32;
                }}

                [data-theme="dark"] {{
                    --bg-color: #121212;
                    --container-bg: #1e1e1e;
                    --text-color: #eee;
                    --heading-color: #64b5f6;
                    --section-bg: #4a4a4a;
                    --box-shadow-color: rgba(255, 255, 255, 0.05);
                    --border-color: #666;
                    --analysis-bg: #555;
                    --read-more-color: #64b5f6;
                }}

                /* General Styles */
                body {{
                    font-family: 'Cairo', sans-serif;
                    background: var(--bg-color);
                    margin: 0;
                    padding: 0;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    min-height: 100vh;
                    color: var(--text-color);
                    line-height: 1.6;
                    transition: background 0.3s, color 0.3s;
                }}

                .container {{
                    max-width: 900px;
                    width: 95%;
                    background: var(--container-bg);
                    padding: 40px;
                    border-radius: 15px;
                    box-shadow: 0 12px 30px var(--box-shadow-color);
                    margin: 20px 0;
                    transition: all 0.3s ease;
                }}

                h1 {{
                    text-align: center;
                    color: var(--heading-color);
                    margin-bottom: 20px;
                    font-weight: 700;
                    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.08);
                    font-size: 2.5em;
                }}

                h2 {{
                    color: var(--heading-color);
                    border-bottom: 2px solid var(--border-color);
                    padding-bottom: 8px;
                    margin-top: 25px;
                    font-weight: 600;
                    font-size: 1.8em;
                    transition: color 0.3s, border-color 0.3s;
                }}

                p {{
                    font-size: 16px;
                    line-height: 1.7;
                    color: var(--text-color);
                    margin-bottom: 20px;
                    transition: color 0.3s;
                }}

                .section {{
                    background-color: var(--section-bg);
                    border-radius: 12px;
                    padding: 25px;
                    margin-bottom: 20px;
                    box-shadow: 0 4px 12px var(--box-shadow-color);
                    transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s;
                }}

                .section:hover {{
                    transform: translateY(-5px);
                    box-shadow: 0 6px 15px var(--box-shadow-color);
                }}

                strong {{
                    color: var(--text-color);
                    font-weight: 600;
                    transition: color 0.3s;
                }}

                .container[dir="rtl"] {{
                    direction: rtl;
                }}

                .theme-switch-wrapper {{
                    display: flex;
                    align-items: center;
                    justify-content: flex-end;
                    margin-bottom: 20px;
                }}

                .theme-switch {{
                    position: relative;
                    display: inline-block;
                    width: 60px;
                    height: 34px;
                    margin-left: 10px;
                }}

                .theme-switch input {{
                    opacity: 0;
                    width: 0;
                    height: 0;
                }}

                .slider {{
                    position: absolute;
                    cursor: pointer;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background-color: #ccc;
                    transition: .4s;
                    border-radius: 34px;
                }}

                .slider:before {{
                    position: absolute;
                    content: "";
                    height: 26px;
                    width: 26px;
                    left: 4px;
                    bottom: 4px;
                    background-color: white;
                    transition: .4s;
                    border-radius: 50%;
                }}

                input:checked + .slider {{
                    background-color: #2979ff;
                }}

                input:focus + .slider {{
                    box-shadow: 0 0 1px #2979ff;
                }}

                input:checked + .slider:before {{
                    transform: translateX(26px);
                }}

                /* Style adjustments specific to analysis */
                .voice-analysis-container {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 15px;
                }}

                .voice-analysis-item {{
                    padding: 15px;
                    border-radius: 8px;
                    background: var(--analysis-bg);
                    box-shadow: 0 2px 6px var(--box-shadow-color);
                    transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s;
                }}

                .voice-analysis-item h3 {{
                    color: var(--heading-color);
                    font-size: 1.1em;
                    margin-bottom: 5px;
                }}

                .voice-analysis-item p {{
                    margin: 0;
                    font-size: 0.95em;
                    line-height: 1.5;
                }}

                .analysis-icon {{
                    font-size: 1.2em;
                    margin-right: 8px;
                    color: var(--heading-color);
                    display: inline-block;
                }}

                /* Read More/Less Styles */
                #transcriptionText {{
                    display: -webkit-box;
                    -webkit-box-orient: vertical;
                    overflow: hidden;
                }}

                .read-more-less-container {{
                    text-align: right; /* Align to right for RTL */
                    margin-top: 10px; /* Add margin for spacing */
                }}

                .read-more-trigger {{
                    cursor: pointer;
                    color: var(--read-more-color);
                    font-weight: 600;
                    text-decoration: none;
                    display: flex;
                    align-items: center;
                    transition: color 0.3s;
                }}

                .read-more-trigger:hover {{
                    color: darken(var(--read-more-color), 10%);
                    text-decoration: underline;
                }}

                .read-more-trigger::before {{
                    content: "◄";
                    font-size: 1.2em;
                    margin-left: 5px;
                    transform: rotate(180deg);
                    transition: transform 0.3s;
                }}

                .read-more-trigger.open::before {{
                    transform: rotate(90deg);
                    content: "▼";
                }}

                .read-more-content {{
                    display: none;
                    margin-top: 10px;
                    padding: 10px;
                    border: 1px solid var(--border-color);
                    border-radius: 5px;
                    background-color: var(--section-bg);
                }}

                .read-more-content.show {{
                    display: block;
                }}

                .summary {{
                    margin-bottom: 10px;
                }}
            </style>
            <!-- Load Elegant Font from Google Fonts -->
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
        </head>

        <body data-theme="light">
            <div class="container" dir="{json_object["text_direction"]}">
                <div class="theme-switch-wrapper">
                    <em id="darkModeLabel">"{json_object["dark_mode_text"]}"</em>
                    <label class="theme-switch" for="checkbox">
                        <input type="checkbox" id="checkbox" />
                        <span class="slider round"></span>
                    </label>
                </div>
                <h1>{json_object["main_heading"]}</h1>
                <div class="section">
                    <h2>1. {json_object["transcription_heading"]}</h2>
                    <p id="transcriptionText">{json_object["transcription"]}</p>

                    <div class="read-more-less-container">
                        <a id="readMoreBtn" class="read-more-trigger" onclick="toggleTranscription()">{json_object["read_more_text"]}</a>
                        <a id="readLessBtn" class="read-more-trigger" onclick="toggleTranscription()">{json_object["read_less_text"]}</a>
                    </div>
                </div>
                <div class="section">
                    <h2>2. {json_object["voice_analysis"]["voice_analysis_heading"]}</h2>
                    <div class="voice-analysis-container">
                        <div class="voice-analysis-item">
                            <h3><span class="analysis-icon">🔊</span> {json_object["voice_analysis"]["voice_speed"]["voice_speed_heading"]}</h3>
                            <p><strong>{json_object["voice_analysis"]["voice_speed"]["assessment_label"]}:</strong> {json_object["voice_analysis"]["voice_speed"]["voice_speed"]}</p>
                            <p><strong>{json_object["voice_analysis"]["voice_speed"]["notes_label"]}:</strong> {json_object["voice_analysis"]["voice_speed"]["voice_speed_notes"]}</p>
                        </div>
                        <div class="voice-analysis-item">
                            <h3><span class="analysis-icon">🗣️</span> {json_object["voice_analysis"]["voice_volume"]["voice_volume_heading"]}</h3>
                            <p><strong>{json_object["voice_analysis"]["voice_volume"]["assessment_label"]}:</strong> {json_object["voice_analysis"]["voice_volume"]["voice_volume"]}</p>
                            <p><strong>{json_object["voice_analysis"]["voice_volume"]["notes_label"]}:</strong> {json_object["voice_analysis"]["voice_volume"]["voice_volume_notes"]}</p>
                        </div>
                        <div class="voice-analysis-item">
                            <h3><span class="analysis-icon">🎵</span> {json_object["voice_analysis"]["voice_tone"]["voice_tone_heading"]}</h3>
                            <p><strong>{json_object["voice_analysis"]["voice_tone"]["assessment_label"]}:</strong> {json_object["voice_analysis"]["voice_tone"]["voice_tone"]}</p>
                            <p><strong>{json_object["voice_analysis"]["voice_tone"]["notes_label"]}:</strong> {json_object["voice_analysis"]["voice_tone"]["voice_tone_notes"]}</p>
                        </div>
                        <div class="voice-analysis-item">
                            <h3><span class="analysis-icon">😊</span> {json_object["voice_analysis"]["emotions"]["emotions_heading"]}</h3>
                            <p><strong>{json_object["voice_analysis"]["emotions"]["assessment_label"]}:</strong> {json_object["voice_analysis"]["emotions"]["emotions"]}</p>
                            <p><strong>{json_object["voice_analysis"]["emotions"]["notes_label"]}:</strong> {json_object["voice_analysis"]["emotions"]["emotions_notes"]}</p>
                        </div>
                        <div class="voice-analysis-item">
                            <h3><span class="analysis-icon">💬</span> {json_object["voice_analysis"]["pauses_filler"]["pauses_filler_heading"]}</h3>
                            <p><strong>{json_object["voice_analysis"]["pauses_filler"]["assessment_label"]}:</strong> {json_object["voice_analysis"]["pauses_filler"]["pauses_filler"]}</p>
                            <p><strong>{json_object["voice_analysis"]["pauses_filler"]["notes_label"]}:</strong> {json_object["voice_analysis"]["pauses_filler"]["pauses_filler_notes"]}</p>
                        </div>
                        <div class="voice-analysis-item">
                            <h3><span class="analysis-icon">📈</span> {json_object["voice_analysis"]["pitch_engagement"]["pitch_engagement_heading"]}</h3>
                            <p><strong>{json_object["voice_analysis"]["pitch_engagement"]["assessment_label"]}:</strong> {json_object["voice_analysis"]["pitch_engagement"]["pitch_engagement"]}</p>
                            <p><strong>{json_object["voice_analysis"]["pitch_engagement"]["notes_label"]}:</strong> {json_object["voice_analysis"]["pitch_engagement"]["pitch_engagement_notes"]}</p>
                        </div>
                    </div>
                </div>
                <div class="section">
                    <h2>3. {json_object["content_structure"]["content_structure_heading"]}</h2>
                    <p class="summary">{json_object["content_structure"]["content_structure_summary"]}</p>
                    <div class="read-more-less-container">
                        <a class="read-more-trigger" onclick="toggleReadMore('contentStructure')">{json_object["read_more_text"]} ({json_object["detailed_analysis_text"]})</a>
                        <div id="contentStructure" class="read-more-content">
                            {json_object["content_structure"]["content_structure_detailed"]}
                        </div>
                    </div>
                </div>
                <div class="section">
                    <h2>4. {json_object["strengths_weaknesses"]["strengths_weaknesses_heading"]}</h2>
                    <div style="display: flex; flex-direction: column;">
                        <div>
                            <h3>{json_object["strengths_weaknesses"]["strengths"]["strengths_heading"]}</h3>
                            <p class="summary">{json_object["strengths_weaknesses"]["strengths"]["strengths_summary"]}</p>
                            <div class="read-more-less-container">
                                <a class="read-more-trigger" onclick="toggleReadMore('strengths')">{json_object["read_more_text"]} ({json_object["detailed_analysis_text"]})</a>
                                <div id="strengths" class="read-more-content">
                                    {json_object["strengths_weaknesses"]["strengths"]["strengths_detailed"]}
                                </div>
                            </div>
                        </div>
                        <div>
                            <h3>{json_object["strengths_weaknesses"]["weaknesses"]["weaknesses_heading"]}</h3>
                            <p class="summary">{json_object["strengths_weaknesses"]["weaknesses"]["weaknesses_summary"]}</p>
                            <div class="read-more-less-container">
                                <a class="read-more-trigger" onclick="toggleReadMore('weaknesses')">{json_object["read_more_text"]} ({json_object["detailed_analysis_text"]})</a>
                                <div id="weaknesses" class="read-more-content">
                                    {json_object["strengths_weaknesses"]["weaknesses"]["weaknesses_detailed"]}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="section">
                    <h2>5. {json_object["fluency"]["fluency_heading"]}</h2>
                    <p class="summary">{json_object["fluency"]["fluency_summary"]}</p>
                    <div class="read-more-less-container">
                        <a class="read-more-trigger" onclick="toggleReadMore('fluency')">{json_object["read_more_text"]} ({json_object["detailed_analysis_text"]})</a>
                        <div id="fluency" class="read-more-content">
                            {json_object["fluency"]["fluency_detailed"]}
                        </div>
                    </div>
                </div>
                <div class="section">
                    <h2>6. {json_object["improvement"]["improvement_heading"]}</h2>
                    <p class="summary">{json_object["improvement"]["improvement_summary"]}</p>
                    <div class="read-more-less-container">
                        <a class="read-more-trigger" onclick="toggleReadMore('improvement')">{json_object["read_more_text"]} ({json_object["detailed_analysis_text"]})</a>
                        <div id="improvement" class="read-more-content">
                            {json_object["improvement"]["improvement_detailed"]}
                        </div>
                    </div>
                </div>
                <div class="section">
                    <h2>7. {json_object["recommendation"]["recommendation_heading"]}</h2>
                    <p class="summary">{json_object["recommendation"]["recommendation_summary"]}</p>
                    <div class="read-more-less-container">
                        <a class="read-more-trigger" onclick="toggleReadMore('recommendation')">{json_object["read_more_text"]} ({json_object["detailed_analysis_text"]})</a>
                        <div id="recommendation" class="read-more-content">
                            {json_object["recommendation"]["recommendation_detailed"]}
                        </div>
                    </div>
                </div>
            </div>
            <script>
                function toggleReadMore(elementId) {{
                    const element = document.getElementById(elementId);
                    const trigger = element.parentElement.querySelector('.read-more-trigger');
                    element.classList.toggle('show');
                    trigger.classList.toggle('open');
                }}

                function toggleTranscription() {{
                    var transcriptionText = document.getElementById("transcriptionText");
                    var readMoreBtn = document.getElementById("readMoreBtn");
                    var readLessBtn = document.getElementById("readLessBtn");

                    if (transcriptionText.classList.contains('truncated')) {{
                        transcriptionText.classList.remove('truncated');
                        transcriptionText.style.webkitLineClamp = 'unset';
                        readMoreBtn.style.display = "none";
                        readLessBtn.style.display = "flex";
                        readLessBtn.style.alignItems = "center";
                    }} else {{
                        transcriptionText.classList.add('truncated');
                        transcriptionText.style.webkitLineClamp = '5';
                        readMoreBtn.style.display = "flex";
                        readMoreBtn.style.alignItems = "center";
                        readLessBtn.style.display = "none";
                    }}
                }}

                document.addEventListener('DOMContentLoaded', function () {{
                    const checkbox = document.getElementById('checkbox');
                    const darkModeLabel = document.getElementById("darkModeLabel");

                    checkbox.addEventListener('change', () => {{
                        document.body.dataset.theme = document.body.dataset.theme === "light" ? "dark" : "light";
                        darkModeLabel.textContent = document.body.dataset.theme === "light" ? "{json_object["dark_mode_enable_text"]}" : "{json_object["dark_mode_disable_text"]}";
                        localStorage.setItem('theme', document.body.dataset.theme);
                    }});

                    const savedTheme = localStorage.getItem('theme');
                    if (savedTheme) {{
                        document.body.dataset.theme = savedTheme;
                        checkbox.checked = (savedTheme === "dark");
                        darkModeLabel.textContent = (savedTheme === "dark") ? "{json_object["dark_mode_enable_text"]}" : "{json_object["dark_mode_disable_text"]}";
                    }}

                    var transcriptionText = document.getElementById("transcriptionText");
                    var readMoreBtn = document.getElementById("readMoreBtn");
                    var readLessBtn = document.getElementById("readLessBtn");

                    const lineHeight = parseFloat(window.getComputedStyle(transcriptionText).lineHeight);
                    const maxHeight = lineHeight * 5;

                    if (transcriptionText.scrollHeight > maxHeight) {{
                        transcriptionText.classList.add('truncated');
                        transcriptionText.style.webkitLineClamp = '5';
                        readMoreBtn.style.display = "flex";
                        readMoreBtn.style.alignItems = "center";
                    }} else {{
                        readMoreBtn.style.display = "none";
                        readLessBtn.style.display = "none";
                    }}
                }});
            </script>

            <style>
                #transcriptionText.truncated {{
                    -webkit-line-clamp: 5;
                    display: -webkit-box;
                    -webkit-box-orient: vertical;
                    overflow: hidden;
                }}
            </style>
        </body>

        </html>
    """
    return html
