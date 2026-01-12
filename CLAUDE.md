# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Chinese user comment analysis tool (评论分析智能体) that automatically categorizes user feedback, scores sentiment, determines urgency levels, and generates statistical reports. The application uses a **rule-based analysis engine** (no AI APIs) with a Streamlit web interface.

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the web app
streamlit run app.py

# Or use the helper script
bash run.sh
```

The app will open at `http://localhost:8501`.

## Architecture

### Two-Layer Structure

1. **Web Layer (`app.py`)**
   - Streamlit-based web interface with Apple-inspired minimalist design
   - Handles user input (direct text or sample data)
   - Displays results in two tables: summary statistics and detailed analysis
   - Provides markdown report download functionality

2. **Analysis Engine (`comment_analyzer.py`)**
   - `CommentAnalyzer` class: Core analysis logic
   - Rule-based classification using keyword matching
   - No external API calls - completely self-contained

### Analysis Pipeline

Comments flow through this pipeline:
1. **Classification** (`classify()`) - Categorizes into 5 types based on keyword matching
2. **Sentiment Scoring** (`score_sentiment()`) - Scores 1-5 based on emotional keywords
3. **Urgency Determination** (`determine_urgency()`) - Assigns P0/P1/P2 priority levels
4. **Core Issue Extraction** (`extract_core_issue()`) - Extracts 3-5 Chinese characters summarizing the issue
5. **Report Generation** (`generate_report()`) - Outputs two markdown tables

## Classification System

The analyzer categorizes comments into 5 predefined categories using keyword matching:

- **1-功能稳定性** (Functional Stability): crashes, freezes, playback failures, network errors
- **2-交互与体验UI/UX** (UI/UX): interface design, buttons, fonts, dark mode requests
- **3-商业化** (Monetization): pricing, ads, subscriptions, billing issues
- **4-内容版权** (Content/Copyright): song availability, audio quality, library completeness
- **5-其他** (Other): emotional venting, spam, praise, unrelated content

Each category has a predefined keyword list in `CATEGORY_KEYWORDS` dictionary.

## Sentiment & Urgency Scoring

**Sentiment Scale (1-5)**:
- 1分（愤怒）: Profanity, threats to uninstall, extreme disappointment
- 2分（不满）: Criticism with negative tone
- 3分（中立）: Suggestions or factual statements
- 4分（满意）: Positive with minor suggestions
- 5分（惊喜）: Pure praise

**Urgency Levels (P0/P1/P2)**:
- P0（高危）: Crashes, unusable features, payment issues (money deducted but service not delivered)
- P1（重要）: Poor experience but core features still work
- P2（一般）: Visual suggestions or feature requests

## Output Format

The analyzer generates two markdown tables:

1. **核心数据汇总表** (Summary Table): Category, count, average sentiment, highest urgency, typical issue
2. **全量评论分析明细表** (Detail Table): ID, category, sentiment score, urgency, core issue, original comment preview (first 10 chars)

## Key Implementation Details

### Keyword Matching Logic
- Classification uses keyword frequency scoring - the category with most keyword matches wins
- If tied, the category with lower number (higher priority) is selected
- If no keywords match, defaults to "5-其他" (Other)

### Core Issue Extraction
- Extracts 3-5 Chinese characters around matched keywords
- Falls back to category defaults if extraction fails
- Uses regex to count only Chinese characters: `[\u4e00-\u9fff]`

### Invalid Data Detection
- Empty comments or comments < 2 characters
- Comments with >70% non-Chinese characters (likely spam)
- Pure numbers or symbols

## File Structure

```
agents/
├── app.py                 # Streamlit web application (main entry point)
├── comment_analyzer.py    # Core analysis engine
├── example.py             # Usage examples (run standalone)
├── requirements.txt       # Python dependencies (only streamlit>=1.28.0)
├── run.sh                 # Launch script
├── README.md              # Project documentation (Chinese)
├── QUICKSTART.md          # Quick start guide (Chinese)
├── DEPLOYMENT.md          # Streamlit Cloud deployment guide
└── SECURITY_CHECK.md      # Security verification (confirms no hardcoded API keys)
```

## Development Notes

### Modifying Classification Rules
All classification logic is centralized in three dictionaries in `comment_analyzer.py`:
- `CATEGORY_KEYWORDS`: Add/modify keywords for each category
- `SENTIMENT_KEYWORDS`: Add/modify sentiment detection keywords
- `URGENCY_KEYWORDS`: Add/modify urgency level keywords

### Testing
Run `example.py` to test the analyzer with various scenarios:
```bash
python example.py
```

### Streamlit UI Customization
The UI uses extensive custom CSS (lines 20-379 in `app.py`) for Apple-inspired styling. Key CSS classes:
- `.main-stage-card`: Main content container
- `.stRadio`: Custom radio button styling
- `.stTextArea textarea`: Input field styling
- `.result-section table`: Markdown table styling

## Deployment

The app is designed for Streamlit Cloud deployment (free):
1. Push code to GitHub
2. Connect at https://streamlit.io/cloud
3. Select repository and set main file to `app.py`
4. No secrets or API keys needed (rule-based analysis only)

See `DEPLOYMENT.md` for detailed deployment instructions.
