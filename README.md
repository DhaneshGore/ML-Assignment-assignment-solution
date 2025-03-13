# MultiLLM Cost-Optimized API
## Features
- Routes requests to multiple LLM providers
- Tracks token usage and cost
- Implements automatic failover
- Exposes API for text generation

## Setup
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Set API keys in `.env` file.
3. Run ```python -m src.app ``` to start the service.

4. Run the service:
   ```
   chmod +x run.sh
   ./run.sh
   ```
