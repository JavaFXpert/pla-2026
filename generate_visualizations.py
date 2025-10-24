#!/usr/bin/env python3
"""
Generate interactive visualization HTML files for all music theory concepts.
"""

import json
import os

# Read concepts data
with open('music-theory-concepts.json', 'r') as f:
    data = json.load(f)

output_dir = 'canvas_music_theory_course/wiki_content'

# Common HTML template parts
def get_base_html(concept_name, content):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{concept_name} - Interactive Visualization</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 30px;
            background-color: #f9f9f9;
            line-height: 1.6;
        }}

        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}

        .visualization-container {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}

        .controls {{
            margin: 20px 0;
            padding: 20px;
            background: #ecf0f1;
            border-radius: 8px;
        }}

        button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
            transition: all 0.3s ease;
        }}

        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}

        button:active {{
            transform: translateY(0);
        }}

        .piano-keyboard {{
            display: flex;
            margin: 30px 0;
            position: relative;
            height: 200px;
        }}

        .white-key {{
            width: 50px;
            height: 200px;
            background: white;
            border: 2px solid #333;
            cursor: pointer;
            position: relative;
            transition: all 0.1s ease;
        }}

        .white-key:hover {{
            background: #f0f0f0;
        }}

        .white-key.active {{
            background: #667eea;
            color: white;
        }}

        .black-key {{
            width: 30px;
            height: 120px;
            background: #333;
            border: 2px solid #000;
            cursor: pointer;
            position: absolute;
            z-index: 2;
            transition: all 0.1s ease;
            color: white;
            font-size: 10px;
        }}

        .black-key:hover {{
            background: #555;
        }}

        .black-key.active {{
            background: #764ba2;
        }}

        .key-label {{
            position: absolute;
            bottom: 10px;
            width: 100%;
            text-align: center;
            font-size: 12px;
            font-weight: bold;
        }}

        .staff-container {{
            margin: 30px 0;
            position: relative;
        }}

        .staff-line {{
            height: 2px;
            background: #333;
            margin: 18px 0;
        }}

        .note-dot {{
            width: 24px;
            height: 24px;
            background: #667eea;
            border-radius: 50%;
            position: absolute;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .note-dot:hover {{
            transform: scale(1.2);
            background: #764ba2;
        }}

        .waveform {{
            width: 100%;
            height: 200px;
            background: #000;
            border-radius: 8px;
        }}

        .slider-container {{
            margin: 20px 0;
        }}

        .slider {{
            width: 100%;
            height: 8px;
            border-radius: 4px;
            background: #ddd;
            outline: none;
            opacity: 0.7;
            transition: opacity 0.2s;
        }}

        .slider:hover {{
            opacity: 1;
        }}

        .value-display {{
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
            text-align: center;
            margin: 20px 0;
        }}

        .chord-builder {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}

        .note-button {{
            padding: 15px;
            background: white;
            border: 2px solid #667eea;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
            font-weight: 500;
        }}

        .note-button:hover {{
            background: #f8f9ff;
            transform: translateY(-2px);
        }}

        .note-button.selected {{
            background: #667eea;
            color: white;
        }}

        .info-box {{
            background: #e8f4f8;
            border-left: 4px solid #3498db;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }}

        .rhythm-grid {{
            display: grid;
            grid-template-columns: repeat(16, 1fr);
            gap: 5px;
            margin: 20px 0;
        }}

        .beat-cell {{
            aspect-ratio: 1;
            background: white;
            border: 2px solid #667eea;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .beat-cell:hover {{
            background: #f8f9ff;
        }}

        .beat-cell.active {{
            background: #667eea;
        }}

        .beat-cell.playing {{
            background: #4caf50;
            transform: scale(1.1);
        }}
    </style>
</head>
<body>
    <h1>{concept_name} - Interactive Visualization</h1>
    {content}
</body>
</html>"""

# Visualization generators for different concept types

def generate_piano_keyboard_viz(concept):
    """Generate interactive piano keyboard visualization"""
    content = f"""
    <div class="visualization-container">
        <div class="info-box">
            <strong>Interactive Piano Keyboard</strong><br>
            Click on the keys to hear the notes and see their names. White keys are natural notes (C, D, E, F, G, A, B), and black keys are sharps/flats.
        </div>

        <div class="piano-keyboard" id="keyboard">
            <!-- Will be generated by JavaScript -->
        </div>

        <div class="value-display" id="noteDisplay">Click a key to play</div>

        <div class="controls">
            <button onclick="playScale()">Play C Major Scale</button>
            <button onclick="highlightOctaves()">Highlight C Notes</button>
            <button onclick="resetKeyboard()">Reset</button>
        </div>
    </div>

    <script>
        const whiteNotes = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'A', 'B'];
        const blackNotePositions = [1, 2, 4, 5, 6, 8, 9, 11, 12, 13]; // Positions where black keys appear
        const blackNotes = ['C#', 'D#', 'F#', 'G#', 'A#', 'C#', 'D#', 'F#', 'G#', 'A#'];

        const keyboard = document.getElementById('keyboard');
        const noteDisplay = document.getElementById('noteDisplay');

        // Audio context for playing notes
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();

        function playNote(frequency, duration = 0.5) {
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.value = frequency;
            oscillator.type = 'sine';

            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + duration);
        }

        function getNoteFrequency(note, octave = 4) {
            const noteFrequencies = {{
                'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
                'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
                'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
            }};
            return noteFrequencies[note] || 440;
        }

        // Create white keys
        whiteNotes.forEach((note, index) => {{
            const key = document.createElement('div');
            key.className = 'white-key';
            key.innerHTML = `<div class="key-label">${{note}}</div>`;
            key.onclick = () => {{
                playNote(getNoteFrequency(note));
                noteDisplay.textContent = note;
                key.classList.add('active');
                setTimeout(() => key.classList.remove('active'), 300);
            }};
            keyboard.appendChild(key);
        }});

        // Create black keys
        blackNotePositions.forEach((pos, index) => {{
            const key = document.createElement('div');
            key.className = 'black-key';
            key.style.left = (pos * 50 - 15) + 'px';
            key.innerHTML = `<div class="key-label">${{blackNotes[index]}}</div>`;
            key.onclick = (e) => {{
                e.stopPropagation();
                playNote(getNoteFrequency(blackNotes[index]));
                noteDisplay.textContent = blackNotes[index];
                key.classList.add('active');
                setTimeout(() => key.classList.remove('active'), 300);
            }};
            keyboard.appendChild(key);
        }});

        function playScale() {{
            const scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C'];
            scale.forEach((note, i) => {{
                setTimeout(() => {{
                    playNote(getNoteFrequency(note));
                    noteDisplay.textContent = note;
                }}, i * 500);
            }});
        }}

        function highlightOctaves() {{
            document.querySelectorAll('.white-key').forEach((key, index) => {{
                if (whiteNotes[index] === 'C') {{
                    key.classList.add('active');
                    setTimeout(() => key.classList.remove('active'), 2000);
                }}
            }});
        }}

        function resetKeyboard() {{
            document.querySelectorAll('.white-key, .black-key').forEach(key => {{
                key.classList.remove('active');
            }});
            noteDisplay.textContent = 'Click a key to play';
        }}
    </script>
    """
    return get_base_html(concept['name'], content)

def generate_staff_viz(concept):
    """Generate interactive staff notation visualization"""
    content = f"""
    <div class="visualization-container">
        <div class="info-box">
            <strong>Interactive Musical Staff</strong><br>
            The staff consists of five horizontal lines and four spaces. Each line and space represents a different pitch. Click to place notes!
        </div>

        <svg width="800" height="300" id="staffSvg" style="background: white; border-radius: 8px;">
            <!-- Staff lines -->
            <line x1="50" y1="80" x2="750" y2="80" stroke="#333" stroke-width="2"/>
            <line x1="50" y1="110" x2="750" y2="110" stroke="#333" stroke-width="2"/>
            <line x1="50" y1="140" x2="750" y2="140" stroke="#333" stroke-width="2"/>
            <line x1="50" y1="170" x2="750" y2="170" stroke="#333" stroke-width="2"/>
            <line x1="50" y1="200" x2="750" y2="200" stroke="#333" stroke-width="2"/>

            <!-- Treble clef -->
            <text x="60" y="160" font-size="80" fill="#667eea">𝄞</text>
        </svg>

        <div class="controls">
            <button onclick="clearStaff()">Clear Staff</button>
            <button onclick="playNotes()">Play Notes</button>
        </div>

        <div class="value-display" id="noteInfo">Click on the staff to add notes</div>
    </div>

    <script>
        const svg = document.getElementById('staffSvg');
        const noteInfo = document.getElementById('noteInfo');
        const notes = [];

        const staffPositions = [
            {{y: 50, note: 'A', freq: 440}},
            {{y: 65, note: 'G', freq: 392}},
            {{y: 80, note: 'F', freq: 349.23}},
            {{y: 95, note: 'E', freq: 329.63}},
            {{y: 110, note: 'D', freq: 293.66}},
            {{y: 125, note: 'C', freq: 261.63}},
            {{y: 140, note: 'B', freq: 246.94}},
            {{y: 155, note: 'A', freq: 220}},
            {{y: 170, note: 'G', freq: 196}},
            {{y: 185, note: 'F', freq: 174.61}},
            {{y: 200, note: 'E', freq: 164.81}},
            {{y: 215, note: 'D', freq: 146.83}}
        ];

        const audioContext = new (window.AudioContext || window.webkitAudioContext)();

        function playNote(frequency, startTime, duration = 0.5) {{
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.value = frequency;
            oscillator.type = 'sine';

            gainNode.gain.setValueAtTime(0.3, startTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + duration);

            oscillator.start(startTime);
            oscillator.stop(startTime + duration);
        }}

        svg.addEventListener('click', (e) => {{
            const rect = svg.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            if (x < 150 || x > 750) return;

            // Find closest staff position
            let closest = staffPositions[0];
            let minDist = Math.abs(y - closest.y);

            staffPositions.forEach(pos => {{
                const dist = Math.abs(y - pos.y);
                if (dist < minDist) {{
                    minDist = dist;
                    closest = pos;
                }}
            }});

            // Add note
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'ellipse');
            circle.setAttribute('cx', x);
            circle.setAttribute('cy', closest.y);
            circle.setAttribute('rx', 12);
            circle.setAttribute('ry', 10);
            circle.setAttribute('fill', '#667eea');
            circle.setAttribute('stroke', '#333');
            circle.setAttribute('stroke-width', '2');
            svg.appendChild(circle);

            notes.push({{x: x, note: closest.note, freq: closest.freq}});
            notes.sort((a, b) => a.x - b.x);

            noteInfo.textContent = `Note: ${{closest.note}}`;
            playNote(closest.freq, audioContext.currentTime, 0.5);
        }});

        function clearStaff() {{
            while (svg.children.length > 6) {{
                svg.removeChild(svg.lastChild);
            }}
            notes.length = 0;
            noteInfo.textContent = 'Click on the staff to add notes';
        }}

        function playNotes() {{
            if (notes.length === 0) return;
            notes.forEach((note, i) => {{
                playNote(note.freq, audioContext.currentTime + i * 0.5, 0.5);
            }});
        }}
    </script>
    """
    return get_base_html(concept['name'], content)

def generate_rhythm_viz(concept):
    """Generate interactive rhythm visualization"""
    content = f"""
    <div class="visualization-container">
        <div class="info-box">
            <strong>Interactive Rhythm Sequencer</strong><br>
            Click on the grid to create your own rhythm pattern. Press Play to hear it!
        </div>

        <div class="rhythm-grid" id="rhythmGrid"></div>

        <div class="controls">
            <button onclick="togglePlay()">▶ Play / ⏸ Pause</button>
            <button onclick="clearPattern()">Clear</button>
            <label>
                Tempo: <input type="range" min="60" max="180" value="120" id="tempoSlider" onchange="updateTempo(this.value)">
                <span id="tempoValue">120</span> BPM
            </label>
        </div>
    </div>

    <script>
        const grid = document.getElementById('rhythmGrid');
        const tempoValue = document.getElementById('tempoValue');
        const beats = 16;
        const pattern = new Array(beats).fill(false);
        let isPlaying = false;
        let currentBeat = 0;
        let tempo = 120;
        let intervalId = null;

        const audioContext = new (window.AudioContext || window.webkitAudioContext)();

        // Create grid
        for (let i = 0; i < beats; i++) {{
            const cell = document.createElement('div');
            cell.className = 'beat-cell';
            cell.dataset.beat = i;
            cell.onclick = () => toggleBeat(i);
            grid.appendChild(cell);
        }}

        function toggleBeat(index) {{
            pattern[index] = !pattern[index];
            updateGrid();
        }}

        function updateGrid() {{
            const cells = grid.children;
            for (let i = 0; i < beats; i++) {{
                if (pattern[i]) {{
                    cells[i].classList.add('active');
                }} else {{
                    cells[i].classList.remove('active');
                }}
            }}
        }}

        function playBeat() {{
            const cells = grid.children;

            // Remove playing class from all
            for (let cell of cells) {{
                cell.classList.remove('playing');
            }}

            // Add to current
            cells[currentBeat].classList.add('playing');

            // Play sound if beat is active
            if (pattern[currentBeat]) {{
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();

                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);

                oscillator.frequency.value = 800;
                oscillator.type = 'square';

                gainNode.gain.setValueAtTime(0.2, audioContext.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);

                oscillator.start(audioContext.currentTime);
                oscillator.stop(audioContext.currentTime + 0.1);
            }}

            currentBeat = (currentBeat + 1) % beats;
        }}

        function togglePlay() {{
            isPlaying = !isPlaying;

            if (isPlaying) {{
                const interval = 60000 / tempo / 4; // Quarter note duration
                intervalId = setInterval(playBeat, interval);
            }} else {{
                clearInterval(intervalId);
                const cells = grid.children;
                for (let cell of cells) {{
                    cell.classList.remove('playing');
                }}
            }}
        }}

        function clearPattern() {{
            pattern.fill(false);
            currentBeat = 0;
            updateGrid();
        }}

        function updateTempo(value) {{
            tempo = parseInt(value);
            tempoValue.textContent = tempo;

            if (isPlaying) {{
                clearInterval(intervalId);
                const interval = 60000 / tempo / 4;
                intervalId = setInterval(playBeat, interval);
            }}
        }}
    </script>
    """
    return get_base_html(concept['name'], content)

def generate_interval_viz(concept):
    """Generate interactive interval calculator"""
    content = f"""
    <div class="visualization-container">
        <div class="info-box">
            <strong>Interactive Interval Calculator</strong><br>
            Select two notes to see and hear the interval between them.
        </div>

        <div class="piano-keyboard" id="keyboard"></div>

        <div class="value-display" id="intervalDisplay">Select two notes to calculate interval</div>

        <div class="controls">
            <button onclick="resetInterval()">Reset</button>
            <button onclick="playInterval()">Play Interval</button>
        </div>

        <div class="info-box" style="margin-top: 20px;">
            <h3>Common Intervals:</h3>
            <ul>
                <li><strong>Unison:</strong> Same note (0 half steps)</li>
                <li><strong>Minor 2nd:</strong> 1 half step</li>
                <li><strong>Major 2nd:</strong> 2 half steps</li>
                <li><strong>Minor 3rd:</strong> 3 half steps</li>
                <li><strong>Major 3rd:</strong> 4 half steps</li>
                <li><strong>Perfect 4th:</strong> 5 half steps</li>
                <li><strong>Perfect 5th:</strong> 7 half steps</li>
                <li><strong>Octave:</strong> 12 half steps</li>
            </ul>
        </div>
    </div>

    <script>
        const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
        const selectedNotes = [];
        const keyboard = document.getElementById('keyboard');
        const intervalDisplay = document.getElementById('intervalDisplay');
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();

        const intervalNames = [
            'Unison', 'Minor 2nd', 'Major 2nd', 'Minor 3rd', 'Major 3rd',
            'Perfect 4th', 'Tritone', 'Perfect 5th', 'Minor 6th', 'Major 6th',
            'Minor 7th', 'Major 7th', 'Octave'
        ];

        function getNoteFrequency(noteIndex) {{
            return 261.63 * Math.pow(2, noteIndex / 12); // C4 = 261.63 Hz
        }}

        // Create keyboard
        notes.forEach((note, index) => {{
            const isBlack = note.includes('#');
            const key = document.createElement('div');
            key.className = isBlack ? 'black-key' : 'white-key';
            key.innerHTML = `<div class="key-label">${{note}}</div>`;
            key.dataset.noteIndex = index;

            if (isBlack) {{
                const whiteKeyIndex = notes.slice(0, index).filter(n => !n.includes('#')).length;
                key.style.left = (whiteKeyIndex * 50 - 15) + 'px';
            }}

            key.onclick = (e) => {{
                if (isBlack) e.stopPropagation();
                selectNote(index, key);
            }};

            keyboard.appendChild(key);
        }});

        function selectNote(index, keyElement) {{
            if (selectedNotes.length >= 2) {{
                resetInterval();
            }}

            selectedNotes.push(index);
            keyElement.classList.add('active');

            const freq = getNoteFrequency(index);
            playNote(freq, audioContext.currentTime, 0.5);

            if (selectedNotes.length === 2) {{
                calculateInterval();
            }} else {{
                intervalDisplay.textContent = `First note: ${{notes[index]}}. Select second note...`;
            }}
        }}

        function calculateInterval() {{
            const diff = Math.abs(selectedNotes[1] - selectedNotes[0]);
            const intervalName = intervalNames[diff] || `${{diff}} half steps`;
            intervalDisplay.textContent = `Interval: ${{intervalName}} (${{diff}} half steps)`;
        }}

        function playNote(frequency, startTime, duration) {{
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.value = frequency;
            oscillator.type = 'sine';

            gainNode.gain.setValueAtTime(0.3, startTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + duration);

            oscillator.start(startTime);
            oscillator.stop(startTime + duration);
        }}

        function playInterval() {{
            if (selectedNotes.length === 2) {{
                playNote(getNoteFrequency(selectedNotes[0]), audioContext.currentTime, 0.5);
                playNote(getNoteFrequency(selectedNotes[1]), audioContext.currentTime + 0.6, 0.5);
            }}
        }}

        function resetInterval() {{
            selectedNotes.length = 0;
            document.querySelectorAll('.white-key, .black-key').forEach(key => {{
                key.classList.remove('active');
            }});
            intervalDisplay.textContent = 'Select two notes to calculate interval';
        }}
    </script>
    """
    return get_base_html(concept['name'], content)

def generate_chord_builder_viz(concept):
    """Generate interactive chord builder"""
    content = f"""
    <div class="visualization-container">
        <div class="info-box">
            <strong>Interactive Chord Builder</strong><br>
            Select notes to build chords and hear how they sound together.
        </div>

        <div class="piano-keyboard" id="keyboard"></div>

        <div class="value-display" id="chordDisplay">Select notes to build a chord</div>

        <div class="controls">
            <button onclick="playChord()">Play Chord</button>
            <button onclick="clearChord()">Clear</button>
            <button onclick="buildChord('major')">C Major</button>
            <button onclick="buildChord('minor')">C Minor</button>
            <button onclick="buildChord('dim')">C Diminished</button>
            <button onclick="buildChord('aug')">C Augmented</button>
        </div>

        <div class="info-box" style="margin-top: 20px;">
            <h3>Common Chord Types:</h3>
            <ul>
                <li><strong>Major Triad:</strong> Root + Major 3rd + Perfect 5th (e.g., C-E-G)</li>
                <li><strong>Minor Triad:</strong> Root + Minor 3rd + Perfect 5th (e.g., C-Eb-G)</li>
                <li><strong>Diminished Triad:</strong> Root + Minor 3rd + Diminished 5th (e.g., C-Eb-Gb)</li>
                <li><strong>Augmented Triad:</strong> Root + Major 3rd + Augmented 5th (e.g., C-E-G#)</li>
            </ul>
        </div>
    </div>

    <script>
        const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
        const selectedNotes = new Set();
        const keyboard = document.getElementById('keyboard');
        const chordDisplay = document.getElementById('chordDisplay');
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const keyElements = [];

        function getNoteFrequency(noteIndex) {{
            return 261.63 * Math.pow(2, noteIndex / 12);
        }}

        // Create keyboard
        notes.forEach((note, index) => {{
            const isBlack = note.includes('#');
            const key = document.createElement('div');
            key.className = isBlack ? 'black-key' : 'white-key';
            key.innerHTML = `<div class="key-label">${{note}}</div>`;
            key.dataset.noteIndex = index;
            keyElements[index] = key;

            if (isBlack) {{
                const whiteKeyIndex = notes.slice(0, index).filter(n => !n.includes('#')).length;
                key.style.left = (whiteKeyIndex * 50 - 15) + 'px';
            }}

            key.onclick = (e) => {{
                if (isBlack) e.stopPropagation();
                toggleNote(index);
            }};

            keyboard.appendChild(key);
        }});

        function toggleNote(index) {{
            if (selectedNotes.has(index)) {{
                selectedNotes.delete(index);
                keyElements[index].classList.remove('active');
            }} else {{
                selectedNotes.add(index);
                keyElements[index].classList.add('active');
                playNote(getNoteFrequency(index), audioContext.currentTime, 0.3);
            }}
            updateChordDisplay();
        }}

        function updateChordDisplay() {{
            if (selectedNotes.size === 0) {{
                chordDisplay.textContent = 'Select notes to build a chord';
            }} else {{
                const noteNames = Array.from(selectedNotes).map(i => notes[i]).join(' - ');
                chordDisplay.textContent = `Selected notes: ${{noteNames}}`;
            }}
        }}

        function playNote(frequency, startTime, duration) {{
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.value = frequency;
            oscillator.type = 'sine';

            gainNode.gain.setValueAtTime(0.2, startTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + duration);

            oscillator.start(startTime);
            oscillator.stop(startTime + duration);
        }}

        function playChord() {{
            const now = audioContext.currentTime;
            selectedNotes.forEach(index => {{
                playNote(getNoteFrequency(index), now, 1.5);
            }});
        }}

        function clearChord() {{
            selectedNotes.clear();
            keyElements.forEach(key => key.classList.remove('active'));
            updateChordDisplay();
        }}

        function buildChord(type) {{
            clearChord();
            const root = 0; // C
            let intervals = [];

            switch(type) {{
                case 'major':
                    intervals = [0, 4, 7]; // Root, Major 3rd, Perfect 5th
                    break;
                case 'minor':
                    intervals = [0, 3, 7]; // Root, Minor 3rd, Perfect 5th
                    break;
                case 'dim':
                    intervals = [0, 3, 6]; // Root, Minor 3rd, Diminished 5th
                    break;
                case 'aug':
                    intervals = [0, 4, 8]; // Root, Major 3rd, Augmented 5th
                    break;
            }}

            intervals.forEach(interval => {{
                const noteIndex = (root + interval) % 12;
                selectedNotes.add(noteIndex);
                keyElements[noteIndex].classList.add('active');
            }});

            updateChordDisplay();
            playChord();
        }}
    </script>
    """
    return get_base_html(concept['name'], content)

def generate_scale_viz(concept):
    """Generate interactive scale visualization"""
    content = f"""
    <div class="visualization-container">
        <div class="info-box">
            <strong>Interactive Scale Builder</strong><br>
            Explore different musical scales and hear how they sound.
        </div>

        <div class="piano-keyboard" id="keyboard"></div>

        <div class="value-display" id="scaleDisplay">Select a scale to visualize</div>

        <div class="controls">
            <button onclick="buildScale('major')">Major Scale</button>
            <button onclick="buildScale('minor')">Natural Minor</button>
            <button onclick="buildScale('harmonic')">Harmonic Minor</button>
            <button onclick="buildScale('melodic')">Melodic Minor</button>
            <button onclick="buildScale('pentatonic')">Pentatonic</button>
            <button onclick="playScale()">Play Scale</button>
            <button onclick="clearScale()">Clear</button>
        </div>

        <div class="info-box" style="margin-top: 20px;">
            <h3>Scale Patterns (in half steps):</h3>
            <ul>
                <li><strong>Major:</strong> W-W-H-W-W-W-H (2-2-1-2-2-2-1)</li>
                <li><strong>Natural Minor:</strong> W-H-W-W-H-W-W (2-1-2-2-1-2-2)</li>
                <li><strong>Harmonic Minor:</strong> W-H-W-W-H-WH-H (2-1-2-2-1-3-1)</li>
                <li><strong>Pentatonic Major:</strong> W-W-WH-W-WH (2-2-3-2-3)</li>
            </ul>
            <p><em>W = Whole step (2 half steps), H = Half step (1 half step)</em></p>
        </div>
    </div>

    <script>
        const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
        const scaleNotes = [];
        const keyboard = document.getElementById('keyboard');
        const scaleDisplay = document.getElementById('scaleDisplay');
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const keyElements = [];

        const scalePatterns = {{
            major: [0, 2, 4, 5, 7, 9, 11, 12],
            minor: [0, 2, 3, 5, 7, 8, 10, 12],
            harmonic: [0, 2, 3, 5, 7, 8, 11, 12],
            melodic: [0, 2, 3, 5, 7, 9, 11, 12],
            pentatonic: [0, 2, 4, 7, 9, 12]
        }};

        function getNoteFrequency(noteIndex) {{
            return 261.63 * Math.pow(2, noteIndex / 12);
        }}

        // Create keyboard
        for (let i = 0; i < 13; i++) {{
            const noteIndex = i % 12;
            const note = notes[noteIndex];
            const isBlack = note.includes('#');
            const key = document.createElement('div');
            key.className = isBlack ? 'black-key' : 'white-key';
            key.innerHTML = `<div class="key-label">${{note}}</div>`;
            key.dataset.noteIndex = i;
            keyElements[i] = key;

            if (isBlack) {{
                const whiteCount = notes.slice(0, noteIndex).filter(n => !n.includes('#')).length;
                const octaveOffset = Math.floor(i / 12) * 7;
                key.style.left = ((whiteCount + octaveOffset) * 50 - 15) + 'px';
            }}

            keyboard.appendChild(key);
        }}

        function buildScale(type) {{
            clearScale();
            const pattern = scalePatterns[type];

            pattern.forEach(interval => {{
                scaleNotes.push(interval);
                keyElements[interval].classList.add('active');
            }});

            const scaleNames = {{
                major: 'C Major Scale',
                minor: 'C Natural Minor Scale',
                harmonic: 'C Harmonic Minor Scale',
                melodic: 'C Melodic Minor Scale',
                pentatonic: 'C Pentatonic Scale'
            }};

            scaleDisplay.textContent = scaleNames[type];
        }}

        function playScale() {{
            if (scaleNotes.length === 0) return;

            scaleNotes.forEach((noteIndex, i) => {{
                setTimeout(() => {{
                    const freq = getNoteFrequency(noteIndex);
                    playNote(freq, audioContext.currentTime, 0.5);
                }}, i * 400);
            }});
        }}

        function playNote(frequency, startTime, duration) {{
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.value = frequency;
            oscillator.type = 'sine';

            gainNode.gain.setValueAtTime(0.3, startTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + duration);

            oscillator.start(startTime);
            oscillator.stop(startTime + duration);
        }}

        function clearScale() {{
            scaleNotes.length = 0;
            keyElements.forEach(key => key.classList.remove('active'));
            scaleDisplay.textContent = 'Select a scale to visualize';
        }}
    </script>
    """
    return get_base_html(concept['name'], content)

def generate_waveform_viz(concept):
    """Generate waveform visualization for sound/acoustics concepts"""
    content = f"""
    <div class="visualization-container">
        <div class="info-box">
            <strong>Interactive Waveform Visualizer</strong><br>
            Explore how sound waves look and sound. Adjust frequency and amplitude to see and hear the changes.
        </div>

        <canvas id="waveformCanvas" width="800" height="200" style="background: #000; border-radius: 8px;"></canvas>

        <div class="slider-container">
            <label>
                Frequency: <input type="range" min="100" max="1000" value="440" id="freqSlider" onchange="updateWaveform()">
                <span id="freqValue">440</span> Hz
            </label>
        </div>

        <div class="slider-container">
            <label>
                Amplitude: <input type="range" min="0" max="100" value="50" id="ampSlider" onchange="updateWaveform()">
                <span id="ampValue">50</span>%
            </label>
        </div>

        <div class="controls">
            <button onclick="playTone()">Play Tone</button>
            <button onclick="stopTone()">Stop</button>
            <label>
                Wave Type:
                <select id="waveType" onchange="updateWaveform()">
                    <option value="sine">Sine</option>
                    <option value="square">Square</option>
                    <option value="sawtooth">Sawtooth</option>
                    <option value="triangle">Triangle</option>
                </select>
            </label>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('waveformCanvas');
        const ctx = canvas.getContext('2d');
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        let oscillator = null;
        let gainNode = null;

        function drawWaveform() {{
            const freq = parseInt(document.getElementById('freqSlider').value);
            const amp = parseInt(document.getElementById('ampSlider').value) / 100;
            const waveType = document.getElementById('waveType').value;

            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.strokeStyle = '#00ff00';
            ctx.lineWidth = 2;
            ctx.beginPath();

            const cycles = 3;
            const points = canvas.width;

            for (let x = 0; x < points; x++) {{
                const t = (x / points) * cycles;
                let y;

                switch(waveType) {{
                    case 'sine':
                        y = Math.sin(t * 2 * Math.PI);
                        break;
                    case 'square':
                        y = Math.sin(t * 2 * Math.PI) > 0 ? 1 : -1;
                        break;
                    case 'sawtooth':
                        y = 2 * (t % 1) - 1;
                        break;
                    case 'triangle':
                        const m = t % 1;
                        y = m < 0.5 ? 4 * m - 1 : 3 - 4 * m;
                        break;
                }}

                const py = canvas.height / 2 - (y * amp * canvas.height / 2.5);

                if (x === 0) {{
                    ctx.moveTo(x, py);
                }} else {{
                    ctx.lineTo(x, py);
                }}
            }}

            ctx.stroke();

            // Draw center line
            ctx.strokeStyle = '#333';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(0, canvas.height / 2);
            ctx.lineTo(canvas.width, canvas.height / 2);
            ctx.stroke();
        }}

        function updateWaveform() {{
            const freq = parseInt(document.getElementById('freqSlider').value);
            const amp = parseInt(document.getElementById('ampSlider').value);

            document.getElementById('freqValue').textContent = freq;
            document.getElementById('ampValue').textContent = amp;

            drawWaveform();

            if (oscillator) {{
                oscillator.frequency.value = freq;
                gainNode.gain.value = amp / 100 * 0.3;
            }}
        }}

        function playTone() {{
            stopTone();

            const freq = parseInt(document.getElementById('freqSlider').value);
            const amp = parseInt(document.getElementById('ampSlider').value) / 100;
            const waveType = document.getElementById('waveType').value;

            oscillator = audioContext.createOscillator();
            gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.value = freq;
            oscillator.type = waveType;
            gainNode.gain.value = amp * 0.3;

            oscillator.start();
        }}

        function stopTone() {{
            if (oscillator) {{
                oscillator.stop();
                oscillator = null;
                gainNode = null;
            }}
        }}

        drawWaveform();
    </script>
    """
    return get_base_html(concept['name'], content)

def generate_circle_of_fifths_viz(concept):
    """Generate circle of fifths visualization"""
    content = f"""
    <div class="visualization-container">
        <div class="info-box">
            <strong>Circle of Fifths</strong><br>
            The Circle of Fifths shows the relationship between the 12 tones of the chromatic scale,
            their corresponding key signatures, and the associated major and minor keys.
        </div>

        <svg width="600" height="600" id="circleOfFifths" style="display: block; margin: 20px auto;">
            <!-- Will be drawn by JavaScript -->
        </svg>

        <div class="value-display" id="keyInfo">Click on a key to see its information</div>

        <div class="controls">
            <button onclick="playKey()">Play Key</button>
        </div>
    </div>

    <script>
        const svg = document.getElementById('circleOfFifths');
        const keyInfo = document.getElementById('keyInfo');

        const majorKeys = ['C', 'G', 'D', 'A', 'E', 'B', 'F#/Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F'];
        const minorKeys = ['Am', 'Em', 'Bm', 'F#m', 'C#m', 'G#m', 'D#m/Ebm', 'Bbm', 'Fm', 'Cm', 'Gm', 'Dm'];
        const sharpsFlats = ['0', '1#', '2#', '3#', '4#', '5#', '6#/6♭', '5♭', '4♭', '3♭', '2♭', '1♭'];

        let selectedKey = null;
        const centerX = 300;
        const centerY = 300;
        const outerRadius = 220;
        const middleRadius = 170;
        const innerRadius = 120;

        // Draw circles
        for (let r of [outerRadius, middleRadius, innerRadius]) {{
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', centerX);
            circle.setAttribute('cy', centerY);
            circle.setAttribute('r', r);
            circle.setAttribute('fill', 'none');
            circle.setAttribute('stroke', '#667eea');
            circle.setAttribute('stroke-width', '2');
            svg.appendChild(circle);
        }}

        // Draw key segments
        for (let i = 0; i < 12; i++) {{
            const angle = (i * 30 - 90) * Math.PI / 180;
            const nextAngle = ((i + 1) * 30 - 90) * Math.PI / 180;

            // Outer label (Major keys)
            const majorX = centerX + Math.cos(angle + Math.PI / 12) * (outerRadius + 30);
            const majorY = centerY + Math.sin(angle + Math.PI / 12) * (outerRadius + 30);
            const majorText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            majorText.setAttribute('x', majorX);
            majorText.setAttribute('y', majorY);
            majorText.setAttribute('text-anchor', 'middle');
            majorText.setAttribute('dominant-baseline', 'middle');
            majorText.setAttribute('font-size', '16');
            majorText.setAttribute('font-weight', 'bold');
            majorText.setAttribute('fill', '#667eea');
            majorText.textContent = majorKeys[i];
            svg.appendChild(majorText);

            // Middle label (Sharps/Flats)
            const midX = centerX + Math.cos(angle + Math.PI / 12) * middleRadius;
            const midY = centerY + Math.sin(angle + Math.PI / 12) * middleRadius;
            const midText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            midText.setAttribute('x', midX);
            midText.setAttribute('y', midY);
            midText.setAttribute('text-anchor', 'middle');
            midText.setAttribute('dominant-baseline', 'middle');
            midText.setAttribute('font-size', '14');
            midText.setAttribute('fill', '#764ba2');
            midText.textContent = sharpsFlats[i];
            svg.appendChild(midText);

            // Inner label (Minor keys)
            const minorX = centerX + Math.cos(angle + Math.PI / 12) * innerRadius;
            const minorY = centerY + Math.sin(angle + Math.PI / 12) * innerRadius;
            const minorText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            minorText.setAttribute('x', minorX);
            minorText.setAttribute('y', minorY);
            minorText.setAttribute('text-anchor', 'middle');
            minorText.setAttribute('dominant-baseline', 'middle');
            minorText.setAttribute('font-size', '14');
            minorText.setAttribute('fill', '#667eea');
            minorText.textContent = minorKeys[i];
            svg.appendChild(minorText);

            // Draw separator lines
            const lineX = centerX + Math.cos(angle) * (innerRadius - 20);
            const lineY = centerY + Math.sin(angle) * (innerRadius - 20);
            const lineEndX = centerX + Math.cos(angle) * (outerRadius + 10);
            const lineEndY = centerY + Math.sin(angle) * (outerRadius + 10);

            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', lineX);
            line.setAttribute('y1', lineY);
            line.setAttribute('x2', lineEndX);
            line.setAttribute('y2', lineEndY);
            line.setAttribute('stroke', '#ddd');
            line.setAttribute('stroke-width', '1');
            svg.appendChild(line);
        }}

        // Center label
        const centerText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        centerText.setAttribute('x', centerX);
        centerText.setAttribute('y', centerY);
        centerText.setAttribute('text-anchor', 'middle');
        centerText.setAttribute('dominant-baseline', 'middle');
        centerText.setAttribute('font-size', '18');
        centerText.setAttribute('font-weight', 'bold');
        centerText.setAttribute('fill', '#667eea');
        centerText.textContent = 'Circle of Fifths';
        svg.appendChild(centerText);

        keyInfo.textContent = 'The outer ring shows major keys, the inner ring shows relative minor keys, and the middle ring shows the number of sharps or flats in each key signature.';
    </script>
    """
    return get_base_html(concept['name'], content)

# Map concepts to appropriate visualization generators
def get_visualization(concept):
    """Select appropriate visualization based on concept type"""
    concept_id = concept['id']
    name = concept['name'].lower()

    # Keyboard-based visualizations
    keyboard_concepts = ['note', 'note-name', 'octave', 'pitch', 'sharp', 'flat', 'natural',
                         'accidental', 'half-step', 'whole-step', 'enharmonic']

    # Staff-based visualizations
    staff_concepts = ['staff', 'clef', 'treble-clef', 'bass-clef', 'ledger-lines']

    # Rhythm-based visualizations
    rhythm_concepts = ['rhythm', 'beat', 'tempo', 'meter', 'time-signature', 'measure',
                      'note-value', 'rest', 'dot', 'tie', 'duration']

    # Interval concepts
    interval_concepts = ['interval', 'interval-number', 'interval-quality', 'perfect-interval',
                        'major-interval', 'minor-interval', 'consonance', 'dissonance']

    # Chord concepts
    chord_concepts = ['chord', 'triad', 'major-triad', 'minor-triad', 'diminished-triad',
                     'augmented-triad', 'seventh-chord', 'chord-inversion', 'harmony']

    # Scale concepts
    scale_concepts = ['scale', 'major-scale', 'minor-scale', 'scale-degree', 'tonic',
                     'dominant', 'chromatic', 'diatonic']

    # Sound/waveform concepts
    sound_concepts = ['sound', 'volume', 'timbre']

    # Theory concepts
    theory_concepts = ['key', 'key-signature', 'transposition', 'modulation', 'voice-leading',
                      'roman-numeral-analysis', 'cadence', 'chord-progression']

    if concept_id in keyboard_concepts:
        return generate_piano_keyboard_viz(concept)
    elif concept_id in staff_concepts:
        return generate_staff_viz(concept)
    elif concept_id in rhythm_concepts:
        return generate_rhythm_viz(concept)
    elif concept_id in interval_concepts:
        return generate_interval_viz(concept)
    elif concept_id in chord_concepts:
        return generate_chord_builder_viz(concept)
    elif concept_id in scale_concepts:
        return generate_scale_viz(concept)
    elif concept_id in sound_concepts:
        return generate_waveform_viz(concept)
    elif concept_id == 'key' or concept_id == 'key-signature':
        return generate_circle_of_fifths_viz(concept)
    else:
        # Default to a combination visualization
        return generate_piano_keyboard_viz(concept)

# Generate all visualization files
print(f"Generating {len(data['concepts'])} visualization files...")
for i, concept in enumerate(data['concepts'], 1):
    filename = f"{output_dir}/{concept['id']}-visualization.html"
    html_content = get_visualization(concept)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"{i}. Generated: {filename}")

print("\nAll visualization files generated successfully!")
