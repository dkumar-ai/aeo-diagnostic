# AEO Diagnostic — AI Visibility Checker

## 📋 Overview

**AEO Diagnostic** is an intelligent tool that measures your brand's visibility across three leading AI models: Groq, Google Gemini, and Cohere. By querying these AI engines simultaneously, it provides a comprehensive visibility score, competitive analysis, and actionable recommendations to improve your product's ranking in AI-driven search results.

### Key Features

- **Multi-Model Analysis**: Query 3 AI engines in parallel for comprehensive insights
- **Visibility Scoring**: Get a 0-10 score with letter grades (A-F) based on brand ranking
- **Competitive Intelligence**: Identify and track your top competitors
- **Actionable Recommendations**: Receive personalized suggestions based on your visibility score
- **Beautiful UI**: Streamlit-powered interface with intuitive visualizations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- API keys for:
  - [Groq API](https://console.groq.com)
  - [Google Gemini API](https://makersuite.google.com/app/apikey)
  - [Cohere API](https://dashboard.cohere.com)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/aeo-diagnostic.git
   cd aeo-diagnostic
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   COHERE_API_KEY=your_cohere_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

   The app will open in your browser at `http://localhost:8501`

## 📊 How It Works

### 1. Query Input
Enter a product category query (e.g., "best magnesium supplement for seniors") and optionally specify your brand name.

### 2. Multi-Model Analysis
The tool simultaneously queries:
- **Groq** (via Mixtral 8x7B)
- **Google Gemini** (via Gemini Pro)
- **Cohere** (via Command R)

### 3. Response Parsing
Each LLM returns a ranked list of brands. The parser extracts:
- Brand names
- Rankings (1st, 2nd, 3rd, etc.)
- Your brand's position (if specified)

### 4. Scoring & Grading
- **#1 ranking** → 10 points
- **#2 ranking** → 8 points
- **#3 ranking** → 6 points
- **#4 ranking** → 4 points
- **#5 ranking** → 2 points
- **Not mentioned** → 0 points

**Overall Score** = Average of all 3 LLM scores

**Grades:**
| Score | Grade | Visibility |
|-------|-------|------------|
| 9-10  | A     | Excellent  |
| 7-8   | B     | Good       |
| 5-6   | C     | Moderate   |
| 3-4   | D     | Poor       |
| 0-2   | F     | Not visible|

### 5. Competitive Analysis
The tool identifies competitors by:
- Collecting all brands mentioned across all 3 LLMs
- Removing your target brand
- Ranking by frequency of mentions

### 6. Recommendations
Based on your score, the tool generates specific recommendations:
- **Low score (<5)**: Focus on keyword optimization and review volume
- **Moderate score (5-7)**: Improve review recency and content quality
- **High score (>7)**: Monitor competitors and maintain position

## 📁 Project Structure

```
aeo-diagnostic/
├── app.py                 # Main Streamlit application
├── llm_client.py          # LLM API clients (Groq, Gemini, Cohere)
├── parser.py              # Response parsing logic
├── scorer.py              # Scoring and grading logic
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🔧 Module Descriptions

### `app.py`
Main Streamlit application with:
- Input fields for product query and brand name
- Real-time diagnostic execution
- Results visualization with tables and metrics
- Competitor analysis display
- Raw response viewer

### `llm_client.py`
Handles API communication with:
- `GroqClient`: Queries Groq API (Mixtral 8x7B)
- `GeminiClient`: Queries Google Gemini API
- `CohereClient`: Queries Cohere API
- `query_all_llms()`: Parallel query function

### `parser.py`
Extracts structured data from LLM responses:
- `parse_response()`: Extracts numbered brand list
- `find_target_brand()`: Locates your brand in results
- `extract_competitors()`: Ranks competitors by frequency

### `scorer.py`
Calculates visibility metrics:
- `score_brand_position()`: Converts rank to score
- `calculate_overall_score()`: Averages LLM scores
- `score_to_grade()`: Converts score to letter grade
- `generate_recommendation()`: Creates personalized advice

## 🌐 Deployment

### Deploy on Streamlit Cloud (Recommended)

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select the repository and branch
   - Set the main file path to `app.py`

3. **Add API Keys as Secrets**
   - In Streamlit Cloud dashboard, go to App settings → Secrets
   - Add the same environment variables:
     ```
     GROQ_API_KEY = "your_key_here"
     GOOGLE_API_KEY = "your_key_here"
     COHERE_API_KEY = "your_key_here"
     ```

4. **Deploy** → Get your public URL

### Local Deployment

For local testing and development:
```bash
streamlit run app.py --logger.level=debug
```

## 📈 Example Usage

**Query:** "best magnesium supplement for seniors"  
**Target Brand:** "Nature Made"

**Results:**
- Groq ranks Nature Made #2 → 8 points
- Gemini ranks Nature Made #4 → 4 points
- Cohere doesn't mention Nature Made → 0 points
- **Overall Score:** (8 + 4 + 0) / 3 = **4.0/10**
- **Grade:** D (Poor visibility)
- **Recommendation:** "Your brand has low AI visibility. Consider optimizing product descriptions with keywords that match how customers search for this category."

## 🔮 Future Enhancements

- Historical tracking of visibility scores over time
- SEO keyword suggestions based on competitor analysis
- PDF export of diagnostic reports
- Batch analysis for multiple products
- Integration with e-commerce platforms
- Custom LLM model selection
- A/B testing for product description optimization

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Support

For issues, questions, or feedback, please open an issue on GitHub.

---

**Built with ❤️ using Streamlit, Groq, Google Gemini, and Cohere**
