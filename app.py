import gradio as gr
import pretty_midi
import numpy as np
import soundfile as sf
import tempfile
import os

def midi_to_audio(midi_file, sf2_file):
    """
    Convert MIDI file to audio using a SoundFont file
    """
    try:
        # Load MIDI file
        midi_data = pretty_midi.PrettyMIDI(midi_file.name)
        
        # Synthesize audio using the SoundFont
        audio_data = midi_data.fluidsynth(fs=44100, sf2_path=sf2_file.name)
        
        # Convert to mono if stereo (take just one channel)
        if len(audio_data.shape) > 1:
            audio_data = audio_data.mean(axis=1)
        
        # Normalize audio
        audio_data = audio_data / np.max(np.abs(audio_data)) if np.max(np.abs(audio_data)) > 0 else audio_data
        
        # Save to temporary WAV file
        temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        sf.write(temp_wav.name, audio_data, 44100)
        
        return temp_wav.name
        
    except Exception as e:
        raise gr.Error(f"Error converting MIDI: {str(e)}")

# Create Gradio interface
with gr.Blocks(title="MIDI to Audio Converter") as demo:
    gr.Markdown("# 🎹 MIDI to Audio Converter")
    gr.Markdown("Upload a MIDI file and a SoundFont (.sf2) file to convert MIDI to audio")
    
    with gr.Row():
        midi_input = gr.File(
            label="MIDI File",
            file_types=[".mid", ".midi"],
            type="filepath"
        )
        sf2_input = gr.File(
            label="SoundFont File (.sf2)",
            file_types=[".sf2"],
            type="filepath"
        )
    
    convert_button = gr.Button("Convert to Audio", variant="primary")
    audio_output = gr.Audio(label="Generated Audio", type="filepath")
    
    # Example usage
    gr.Markdown("""
    ### Instructions:
    1. Upload a MIDI file (.mid or .midi)
    2. Upload a SoundFont file (.sf2) - you can find free ones online
    3. Click "Convert to Audio"
    4. Play or download the generated audio
    
    ### Popular free SoundFonts:
    - [FluidR3_GM.sf2](https://member.keymusician.com/Member/FluidR3_GM/index.html)
    - [TimGM6mb.sf2](https://sourceforge.net/projects/timgm6mb-soundfont/)
    """)
    
    convert_button.click(
        fn=midi_to_audio,
        inputs=[midi_input, sf2_input],
        outputs=audio_output
    )

if __name__ == "__main__":
    demo.launch()
