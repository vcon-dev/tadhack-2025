import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="vCon 2026 Viewer", page_icon="📞", layout="wide")

st.title("vCon 2026 Conversation Viewer")
st.markdown("Browse and explore vCon conversation data from vCon 2026")

@st.cache_data
def load_vcon_files():
    """Load all vCon files from 911_calls and numbered day directories"""
    vcon_data = []
    base_path = Path(".")
    # 911_calls + any numbered directories (18, 19, ...)
    dirs_to_scan = []
    if (base_path / "911_calls").is_dir():
        dirs_to_scan.append(base_path / "911_calls")
    for d in sorted(base_path.glob("[0-9]*")):
        if d.is_dir():
            dirs_to_scan.append(d)
    for day_dir in dirs_to_scan:
        for vcon_file in sorted(day_dir.glob("*.vcon.json")):
            try:
                with open(vcon_file, 'r') as f:
                    data = json.load(f)
                    data['file_path'] = str(vcon_file)
                    data['day'] = day_dir.name
                    vcon_data.append(data)
            except Exception as e:
                st.error(f"Error loading {vcon_file}: {e}")
    return vcon_data

# Load all vCon files
vcon_files = load_vcon_files()

if not vcon_files:
    st.warning("No vCon files found in the current directory")
else:
    # Sidebar for filtering
    st.sidebar.header("Filters")
    
    # Get unique days
    days = sorted(set(vcon['day'] for vcon in vcon_files))
    selected_days = st.sidebar.multiselect("Select Days", days, default=days)
    
    # Filter by selected days
    filtered_vcons = [vcon for vcon in vcon_files if vcon['day'] in selected_days]
    
    # Main content area
    st.subheader(f"Found {len(filtered_vcons)} conversations")
    
    # Create overview dataframe
    overview_data = []
    for vcon in filtered_vcons:
        created_at = datetime.fromisoformat(vcon['created_at'].replace('Z', '+00:00'))
        duration = vcon['dialog'][0]['duration'] if vcon.get('dialog') else 0
        num_parties = len(vcon.get('parties', []))
        
        overview_data.append({
            'Day': vcon['day'],
            'UUID': vcon['uuid'],
            'Created': created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'Duration (s)': duration,
            'Parties': num_parties,
            'File': os.path.basename(vcon['file_path'])
        })
    
    df = pd.DataFrame(overview_data)
    
    # Display overview table
    st.dataframe(df, use_container_width=True)
    
    # Detailed view
    st.subheader("Conversation Details")
    
    # Let user select a conversation
    conversation_options = {f"Day {vcon['day']} - {vcon['uuid'][:8]}... ({datetime.fromisoformat(vcon['created_at'].replace('Z', '+00:00')).strftime('%H:%M:%S')})": idx 
                           for idx, vcon in enumerate(filtered_vcons)}
    
    if conversation_options:
        selected_conv = st.selectbox("Select a conversation to view details", 
                                    options=list(conversation_options.keys()))
        
        if selected_conv:
            selected_idx = conversation_options[selected_conv]
            vcon = filtered_vcons[selected_idx]
            
            # Display conversation details
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Metadata")
                st.json({
                    "UUID": vcon['uuid'],
                    "Version": vcon['vcon'],
                    "Created": vcon['created_at'],
                    "Day": vcon['day']
                })
                
                st.markdown("### Parties")
                for party in vcon.get('parties', []):
                    with st.expander(f"{party.get('name', 'Unknown')} ({party.get('role', 'Unknown')})"):
                        st.json(party)
            
            with col2:
                st.markdown("### Dialog")
                if vcon.get('dialog'):
                    dialog = vcon['dialog'][0]
                    st.write(f"**Duration:** {dialog['duration']} seconds")
                    st.write(f"**Start:** {dialog['start']}")
                    st.write(f"**Parties:** {', '.join(str(p) for p in dialog['parties'])}")
                    
                    # Audio player: .mp3 or .wav (same base name as vCon). Load as bytes so playback works reliably.
                    base = vcon['file_path'].replace('.vcon.json', '')
                    audio_path_mp3 = base + '.mp3'
                    audio_path_wav = base + '.wav'
                    audio_path = audio_path_mp3 if os.path.exists(audio_path_mp3) else (audio_path_wav if os.path.exists(audio_path_wav) else None)
                    if audio_path:
                        try:
                            with open(audio_path, 'rb') as f:
                                audio_bytes = f.read()
                            format = 'audio/mpeg' if audio_path.endswith('.mp3') else 'audio/wav'
                            st.audio(audio_bytes, format=format)
                            st.caption("If you hear nothing: generated placeholders are silent. Use real recordings or TTS to get speech.")
                        except Exception as e:
                            st.error(f"Could not load audio: {e}")
                    else:
                        st.info("Audio file not found locally (run scripts/generate_mp3_for_vcons.py to create silent .mp3 or .wav)")
            
            # Analysis section
            st.markdown("### Analysis")
            def _body_text(analysis_obj):
                """Extract display text from analysis body (string or object)."""
                body = analysis_obj.get('body', '')
                if isinstance(body, str):
                    return body
                if isinstance(body, dict):
                    return body.get('transcript', body.get('body', str(body)))
                return str(body) if body else ''

            if vcon.get('analysis'):
                for analysis in vcon['analysis']:
                    analysis_type = analysis.get('type', 'Unknown')
                    
                    if analysis_type == 'transcript':
                        with st.expander("Transcript", expanded=True):
                            st.text(_body_text(analysis) or 'No transcript available')
                    
                    elif analysis_type == 'summary':
                        with st.expander("Summary"):
                            st.write(_body_text(analysis) or 'No summary available')
                    
                    elif analysis_type == 'diarized':
                        with st.expander("Diarized Conversation"):
                            diarized_text = _body_text(analysis)
                            # Format diarized text for better readability
                            lines = diarized_text.split('\n')
                            for line in lines:
                                if line.strip():
                                    if line.startswith('Customer:') or line.startswith('Caller:'):
                                        st.markdown(f"**{line}**")
                                    elif line.startswith('Agent:') or line.startswith('AI:') or line.startswith('Dispatcher:'):
                                        st.markdown(f"*{line}*")
                                    else:
                                        st.write(line)
            
            # Raw JSON view
            with st.expander("Raw vCon JSON"):
                st.json(vcon)

# Add refresh button
if st.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()