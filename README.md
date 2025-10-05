# Re:Member: Emotional Question Generation from Personal Memories

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)  
[![arXiv](https://img.shields.io/badge/arXiv-Preprint-red.svg)](https://arxiv.org/abs/XXXX.XXXXX)

**Re:Member** is an open-source system that explores how emotionally expressive, memory-grounded interaction can support more engaging second language (L2) learning.  
By drawing on users’ **personal videos** and generating **stylized spoken questions** in the target language, Re:Member encourages affective recall and conversational engagement.

> 🧠🎙️📹 Combining **WhisperX**, **vision-language processing**, and **Style-BERT-VITS2**, Re:Member aligns emotional tone with visual context to generate emotionally expressive, context-sensitive spoken questions.

---

## ✨ Features

- 🖼️ Visual grounding: Samples three sequential video frames for each utterance.  
- 📝 Precise transcripts: Uses WhisperX for time-aligned speech transcripts.  
- 🤖 Multimodal question generation: GPT-4o produces natural Japanese-language questions grounded in the transcript + frames.  
- 🎭 Emotion style selection: Automatically selects from 5 Japanese emotional TTS styles (e.g., whispered, cheerful, late-night).  
- 🗣️ Expressive speech synthesis: Style-BERT-VITS2 generates emotionally voiced audio questions.  
- 🖥️ Interactive Gradio UI: Browse and play back synchronized frames, text, and speech.

---

## 🏗️ System Overview

1. Segment video with Silero VAD + WhisperX transcription  
2. Extract visual frames before, during, and after each utterance  
3. Generate Japanese questions using GPT-4o conditioned on transcript and frames  
4. Select emotion labels from 5 predefined styles  
5. Synthesize emotional speech using Style-BERT-VITS2  
6. Display all elements in a Gradio web interface

---

## 📊 Example Output

**Video**: Walking along Tokyo’s Sumida River  
**Generated Question**:  
> 東京スカイツリーの高さはどのくらいですか？  
> *Translation: How tall is Tokyo Sky Tree?*  
**Emotion Style**: るんるん (Cheerful)

---

## 🧪 Installation

### 1. Clone Repository
git clone https://github.com/yourusername/Re-Member.git  
cd Re-Member

### 2. Install Dependencies
pip install -r requirements.txt

💡 Make sure you have Python ≥ 3.9 and ffmpeg installed.

### 3. Download Models
- WhisperX models download automatically on first use  
- Download and configure Style-BERT-VITS2 (Japanese voice model: Ami Koharune)

### 4. Run the App
python app_gradio.py  
Visit http://localhost:7860 in your browser. Optional args include --share, which creates a public link.

---

## 🧰 Configuration

| Component            | Description                                                  |
|----------------------|--------------------------------------------------------------|
| Silero VAD           | Voice activity detection to segment speech                   |
| WhisperX             | Accurate speech transcription with timing alignment          |
| OpenCV               | Frame extraction and formatting                              |
| GPT-4o               | Multimodal Japanese question generation                      |
| Style-BERT-VITS2     | Emotionally expressive Japanese TTS                          |
| Gradio               | Interactive front-end interface for playback                 |

---

## 🌐 Emotion Styles

| Japanese Label         | English Meaning          | Description                                 |
|------------------------|--------------------------|---------------------------------------------|
| るんるん               | Cheerful                 | Playful, bubbly tone                        |
| ささやきA（無声）      | Whisper A (voiceless)    | Gentle, breathy whisper                     |
| ささやきB（有声）      | Whisper B (voiced)       | Soft, intimate voice                        |
| ノーマル              | Neutral                  | Standard voice                              |
| よふかし              | Late-night relaxed       | Sleepy, relaxed nighttime tone              |

---

## 🧠 Research Context

Re:Member contributes to work in:
- Emotionally intelligent educational technologies  
- Memory-grounded human–AI interaction  
- Multimodal question generation  
- Stylized TTS for affective engagement

### 📄 Citation

If you use this system in your research:

@inproceedings{rackauckas2025remember,  
  title={Re:Member: Emotional Question Generation from Personal Memories},  
  author={Rackauckas, Zackary and Minematsu, Nobuaki and Hirschberg, Julia},  
  booktitle={Proceedings of the Fourth Workshop on Bridging Human–Computer Interaction
  and Natural Language Processing},  
  year={2025}  
}

---

## ⚠️ Limitations

- Assumes clean, monolingual speech  
- Emotion classification is prompt-based, not perception-based  
- Consider privacy and emotional safety in personal media usage

---

## 🤝 Contributing

Pull requests are welcome.  
Open an issue to discuss changes or ideas.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- WhisperX: https://github.com/m-bain/whisperX  
- Style-BERT-VITS2: https://github.com/litagin02/Style-Bert-VITS2  
- OpenCV: https://github.com/opencv/opencv  
- Gradio: https://gradio.app  
- Developed at Columbia University & The University of Tokyo
