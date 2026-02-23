# local-rag

Minimal local Retrieval-Augmented Generation (RAG) examples with LlamaIndex and Hugging Face models.

## Project Status

This repository is in archive mode.
It is kept as a reference implementation and is not under active feature development.

## Repository Contents

- `localRag.py`: terminal-based RAG example for local documents.
- `localRagChat.py`: Streamlit app for chatting with an uploaded PDF.
- `runmodel.py`: helper launcher for update/start flows.
- `run_linux.sh`: Linux wrapper for environments based on `text-generation-webui`.
- `config.py` + `.env_example`: runtime configuration via environment variables.
- `LocalRAGChatPdf_orig.py`: legacy reference version.

## Requirements

- Python 3.10+
- Hugging Face token for gated models (for example Llama 2)
- Optional GPU setup (CUDA/ROCm) depending on model size
- Optional local `text-generation-webui` checkout for `run_linux.sh`

Expected structure when using `run_linux.sh`:

```text
~/projects/
  local-rag/
  text-generation-webui/
```

## Quick Start

1. Create and activate a Python environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
cp .env_example .env
```

4. Optional sample data download:

```bash
./get_bitcoinbook_data.sh
```

## Run

Streamlit app:

```bash
streamlit run localRagChat.py
```

Linux wrapper:

```bash
./run_linux.sh --update
./run_linux.sh --script localRagChat.py
```

## Notes

- First model startup may take several minutes.
- Dependencies are intentionally lightweight in this repo, but model/runtime compatibility is environment-specific.
- For archival reproducibility, pin exact versions in your local environment before long-term reuse.

## License

MIT. See `LICENSE`.
