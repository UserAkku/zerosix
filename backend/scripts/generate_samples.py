import os
import torch
from TTS.api import TTS

# Make sure output directories exist
os.makedirs("../data/fake/hindi", exist_ok=True)
os.makedirs("../data/fake/hinglish", exist_ok=True)
os.makedirs("../data/fake/english", exist_ok=True)

# Determine device
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {device}")

# Initialize TTS Model (this will download ~2-3GB on first run)
print("Loading XTTS v2 model... this may take a while to download.")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# We need a reference audio of a real person (10-15 seconds clear speech)
# IMPORTANT: Put a clean recording of yourself named "speaker_ref.wav" in the scripts folder!
ref_audio = "speaker_ref.wav"

if not os.path.exists(ref_audio):
    print(f"ERROR: You must provide a reference audio file named '{ref_audio}' in this folder.")
    print("Record 10 seconds of clear speech (Hindi or English) and try again.")
    exit(1)

# Scenarios to generate
hindi_texts = [
    "Namaste, main Rajesh Kumar, CFO bol raha hoon. Mujhe aapke saath ek important matter discuss karna hai.",
    "Main District Collector office se baat kar raha hoon. Aapko immediately report submit karni hogi."
]

hinglish_texts = [
    "Bhai suno, mujhe ek urgent transfer karna hai account me. Five lakh immediately daalo please.",
    "Listen yaar, client ko ye proposal immediately send kar do. Main travel me hoon, tum handle karo."
]

english_texts = [
    "Hello, this is the IT department. We need you to reset your password immediately for security reasons.",
    "Please process the invoice attached to my previous email as soon as possible."
]

print("Generating Hindi fake samples...")
for i, text in enumerate(hindi_texts):
    out_path = f"../data/fake/hindi/fake_hindi_xtts_{i+1}.wav"
    tts.tts_to_file(text=text, speaker_wav=ref_audio, language="hi", file_path=out_path)
    print(f"Saved: {out_path}")

print("Generating Hinglish fake samples...")
for i, text in enumerate(hinglish_texts):
    out_path = f"../data/fake/hinglish/fake_hinglish_xtts_{i+1}.wav"
    # For Hinglish, XTTS might struggle depending on language tag. We'll use "hi" as primary.
    tts.tts_to_file(text=text, speaker_wav=ref_audio, language="hi", file_path=out_path)
    print(f"Saved: {out_path}")

print("Generating English fake samples...")
for i, text in enumerate(english_texts):
    out_path = f"../data/fake/english/fake_english_xtts_{i+1}.wav"
    tts.tts_to_file(text=text, speaker_wav=ref_audio, language="en", file_path=out_path)
    print(f"Saved: {out_path}")

print("Done! All fake samples generated.")
