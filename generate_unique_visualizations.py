#!/usr/bin/env python3
"""
Generate unique, concept-specific HTML visualizations for music theory concepts.
"""

import json
import os


def load_concepts(filepath):
    """Load concepts from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def get_base_html(title, instructions, content, script):
    """Generate base HTML template."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 900px;
            width: 100%;
        }}
        h1 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 28px;
        }}
        .instructions {{
            color: #666;
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f9ff;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        .controls {{
            margin: 20px 0;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
        }}
        button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: transform 0.2s, box-shadow 0.2s;
            font-weight: 600;
        }}
        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        button:active {{
            transform: translateY(0);
        }}
        button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        input[type="range"] {{
            flex: 1;
            min-width: 150px;
        }}
        label {{
            color: #333;
            font-weight: 600;
            margin-right: 10px;
        }}
        select {{
            padding: 8px 12px;
            border: 2px solid #667eea;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
        }}
        canvas {{
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            margin: 20px 0;
            display: block;
            width: 100%;
            background: white;
        }}
        .value-display {{
            color: #667eea;
            font-weight: bold;
            min-width: 60px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="instructions">{instructions}</div>
        {content}
    </div>
    <script>
        {script}
    </script>
</body>
</html>"""


def generate_waveform_visualization(concept):
    """Generate waveform visualization for sound/acoustics concepts."""
    title = f"Interactive Waveform: {concept['name']}"
    instructions = f"<strong>{concept['name']}:</strong> {concept['description']}<br><br>Adjust the frequency and amplitude sliders, select different wave types, and click Play to hear the sound."

    content = """
        <canvas id="waveCanvas" width="800" height="300"></canvas>
        <div class="controls">
            <label>Frequency:</label>
            <input type="range" id="freqSlider" min="100" max="2000" value="440">
            <span class="value-display" id="freqValue">440 Hz</span>
        </div>
        <div class="controls">
            <label>Amplitude:</label>
            <input type="range" id="ampSlider" min="0" max="100" value="50">
            <span class="value-display" id="ampValue">50%</span>
        </div>
        <div class="controls">
            <label>Wave Type:</label>
            <select id="waveType">
                <option value="sine">Sine</option>
                <option value="square">Square</option>
                <option value="sawtooth">Sawtooth</option>
                <option value="triangle">Triangle</option>
            </select>
        </div>
        <div class="controls">
            <button id="playBtn">Play Sound</button>
            <button id="stopBtn">Stop</button>
        </div>
    """

    script = """
        const canvas = document.getElementById('waveCanvas');
        const ctx = canvas.getContext('2d');
        const freqSlider = document.getElementById('freqSlider');
        const ampSlider = document.getElementById('ampSlider');
        const freqValue = document.getElementById('freqValue');
        const ampValue = document.getElementById('ampValue');
        const waveType = document.getElementById('waveType');
        const playBtn = document.getElementById('playBtn');
        const stopBtn = document.getElementById('stopBtn');

        let audioContext = null;
        let oscillator = null;
        let gainNode = null;

        function drawWaveform() {
            const freq = parseFloat(freqSlider.value);
            const amp = parseFloat(ampSlider.value) / 100;
            const type = waveType.value;

            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.beginPath();
            ctx.strokeStyle = '#667eea';
            ctx.lineWidth = 3;

            const centerY = canvas.height / 2;
            const wavelength = canvas.width / 3;

            for (let x = 0; x < canvas.width; x++) {
                let y;
                const t = x / wavelength * Math.PI * 2;

                switch(type) {
                    case 'sine':
                        y = Math.sin(t);
                        break;
                    case 'square':
                        y = Math.sign(Math.sin(t));
                        break;
                    case 'sawtooth':
                        y = 2 * (t / (Math.PI * 2) % 1) - 1;
                        break;
                    case 'triangle':
                        y = 2 * Math.abs(2 * (t / (Math.PI * 2) % 1) - 1) - 1;
                        break;
                }

                y = centerY - (y * amp * (canvas.height / 3));

                if (x === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            }

            ctx.stroke();

            ctx.strokeStyle = '#ccc';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(0, centerY);
            ctx.lineTo(canvas.width, centerY);
            ctx.stroke();
        }

        function updateDisplay() {
            freqValue.textContent = freqSlider.value + ' Hz';
            ampValue.textContent = ampSlider.value + '%';
            drawWaveform();
        }

        freqSlider.addEventListener('input', updateDisplay);
        ampSlider.addEventListener('input', updateDisplay);
        waveType.addEventListener('change', updateDisplay);

        playBtn.addEventListener('click', () => {
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }

            if (oscillator) {
                oscillator.stop();
            }

            oscillator = audioContext.createOscillator();
            gainNode = audioContext.createGain();

            oscillator.type = waveType.value;
            oscillator.frequency.value = parseFloat(freqSlider.value);
            gainNode.gain.value = parseFloat(ampSlider.value) / 200;

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            oscillator.start();
        });

        stopBtn.addEventListener('click', () => {
            if (oscillator) {
                oscillator.stop();
                oscillator = null;
            }
        });

        drawWaveform();
    """

    return get_base_html(title, instructions, content, script)


def generate_piano_keyboard_visualization(concept):
    """Generate piano keyboard visualization."""
    title = f"Interactive Piano: {concept['name']}"
    instructions = f"<strong>{concept['name']}:</strong> {concept['description']}<br><br>Click on the piano keys to play notes and explore the keyboard."

    content = """
        <canvas id="pianoCanvas" width="800" height="250"></canvas>
        <div class="controls">
            <button id="showLabels">Toggle Note Labels</button>
            <button id="highlightPattern">Highlight C Major Scale</button>
        </div>
    """

    script = """
        const canvas = document.getElementById('pianoCanvas');
        const ctx = canvas.getContext('2d');
        const showLabelsBtn = document.getElementById('showLabels');
        const highlightBtn = document.getElementById('highlightPattern');

        let audioContext = null;
        let showLabels = true;
        let highlightKeys = [];

        const whiteKeys = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'A', 'B'];
        const blackKeys = [1, 2, null, 4, 5, 6, null, 1, 2, null, 4, 5, 6];
        const whiteKeyWidth = canvas.width / 14;
        const whiteKeyHeight = 200;
        const blackKeyWidth = whiteKeyWidth * 0.6;
        const blackKeyHeight = 120;

        const frequencies = [261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25, 554.37];

        function drawPiano() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (let i = 0; i < 14; i++) {
                const x = i * whiteKeyWidth;
                const isHighlighted = highlightKeys.includes(i);

                ctx.fillStyle = isHighlighted ? '#e0e7ff' : 'white';
                ctx.fillRect(x, 0, whiteKeyWidth, whiteKeyHeight);
                ctx.strokeStyle = '#333';
                ctx.lineWidth = 2;
                ctx.strokeRect(x, 0, whiteKeyWidth, whiteKeyHeight);

                if (showLabels) {
                    ctx.fillStyle = '#667eea';
                    ctx.font = 'bold 14px sans-serif';
                    ctx.textAlign = 'center';
                    ctx.fillText(whiteKeys[i], x + whiteKeyWidth / 2, whiteKeyHeight - 10);
                }
            }

            for (let i = 0; i < 13; i++) {
                if (blackKeys[i] !== null) {
                    const x = (i + 0.7) * whiteKeyWidth;
                    ctx.fillStyle = '#333';
                    ctx.fillRect(x, 0, blackKeyWidth, blackKeyHeight);
                    ctx.strokeStyle = '#000';
                    ctx.strokeRect(x, 0, blackKeyWidth, blackKeyHeight);
                }
            }
        }

        function playNote(freq) {
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }

            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.frequency.value = freq;
            oscillator.type = 'sine';
            gainNode.gain.value = 0.3;

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.start();
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
            oscillator.stop(audioContext.currentTime + 0.5);
        }

        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            for (let i = 0; i < 13; i++) {
                if (blackKeys[i] !== null) {
                    const blackX = (i + 0.7) * whiteKeyWidth;
                    if (x >= blackX && x <= blackX + blackKeyWidth && y <= blackKeyHeight) {
                        const blackFreq = frequencies[i] * Math.pow(2, 1/12);
                        playNote(blackFreq);
                        return;
                    }
                }
            }

            const whiteKeyIndex = Math.floor(x / whiteKeyWidth);
            if (whiteKeyIndex >= 0 && whiteKeyIndex < 14) {
                playNote(frequencies[whiteKeyIndex]);
            }
        });

        showLabelsBtn.addEventListener('click', () => {
            showLabels = !showLabels;
            drawPiano();
        });

        highlightBtn.addEventListener('click', () => {
            highlightKeys = highlightKeys.length > 0 ? [] : [0, 2, 4, 5, 7, 9, 11, 12];
            drawPiano();
        });

        drawPiano();
    """

    return get_base_html(title, instructions, content, script)


def generate_staff_visualization(concept):
    """Generate interactive staff notation visualization."""
    title = f"Interactive Staff: {concept['name']}"
    instructions = f"<strong>{concept['name']}:</strong> {concept['description']}<br><br>Click on the staff to place notes. Observe how notes are positioned on lines and spaces."

    content = """
        <canvas id="staffCanvas" width="800" height="300"></canvas>
        <div class="controls">
            <button id="clearNotes">Clear Notes</button>
            <button id="toggleClef">Switch Clef</button>
        </div>
    """

    script = """
        const canvas = document.getElementById('staffCanvas');
        const ctx = canvas.getContext('2d');
        const clearBtn = document.getElementById('clearNotes');
        const clefBtn = document.getElementById('toggleClef');

        let notes = [];
        let clefType = 'treble';
        const staffY = 80;
        const lineSpacing = 20;

        function drawStaff() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (let i = 0; i < 5; i++) {
                const y = staffY + i * lineSpacing;
                ctx.strokeStyle = '#333';
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(50, y);
                ctx.lineTo(canvas.width - 50, y);
                ctx.stroke();
            }

            ctx.font = 'bold 80px serif';
            ctx.fillStyle = '#667eea';
            if (clefType === 'treble') {
                ctx.fillText('𝄞', 55, staffY + 70);
            } else {
                ctx.fillText('𝄢', 60, staffY + 35);
            }

            notes.forEach(note => {
                ctx.beginPath();
                ctx.arc(note.x, note.y, 8, 0, Math.PI * 2);
                ctx.fillStyle = '#764ba2';
                ctx.fill();
                ctx.strokeStyle = '#333';
                ctx.lineWidth = 2;
                ctx.stroke();
            });
        }

        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            if (x > 120 && x < canvas.width - 50) {
                const snappedY = Math.round((y - staffY + lineSpacing) / (lineSpacing / 2)) * (lineSpacing / 2) + staffY - lineSpacing;
                notes.push({ x, y: snappedY });
                drawStaff();
            }
        });

        clearBtn.addEventListener('click', () => {
            notes = [];
            drawStaff();
        });

        clefBtn.addEventListener('click', () => {
            clefType = clefType === 'treble' ? 'bass' : 'treble';
            drawStaff();
        });

        drawStaff();
    """

    return get_base_html(title, instructions, content, script)


def generate_interval_visualization(concept):
    """Generate interval calculator visualization."""
    title = f"Interval Calculator: {concept['name']}"
    instructions = f"<strong>{concept['name']}:</strong> {concept['description']}<br><br>Click two keys to hear the interval and see its name and distance in half steps."

    content = """
        <canvas id="intervalCanvas" width="800" height="200"></canvas>
        <div class="controls">
            <div id="intervalInfo" style="font-size: 18px; color: #667eea; font-weight: bold; min-height: 30px;"></div>
        </div>
        <div class="controls">
            <button id="playHarmonic">Play Harmonic</button>
            <button id="playMelodic">Play Melodic</button>
            <button id="reset">Reset</button>
        </div>
    """

    script = """
        const canvas = document.getElementById('intervalCanvas');
        const ctx = canvas.getContext('2d');
        const info = document.getElementById('intervalInfo');
        const harmonicBtn = document.getElementById('playHarmonic');
        const melodicBtn = document.getElementById('playMelodic');
        const resetBtn = document.getElementById('reset');

        let audioContext = null;
        let selectedNotes = [];

        const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
        const frequencies = [261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88];
        const intervalNames = ['Unison', 'Minor 2nd', 'Major 2nd', 'Minor 3rd', 'Major 3rd', 'Perfect 4th', 'Tritone', 'Perfect 5th', 'Minor 6th', 'Major 6th', 'Minor 7th', 'Major 7th'];

        const keyWidth = canvas.width / 12;

        function drawKeys() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (let i = 0; i < 12; i++) {
                const x = i * keyWidth;
                const isBlack = notes[i].includes('#');
                const isSelected = selectedNotes.some(n => n.index === i);

                if (isBlack) {
                    ctx.fillStyle = isSelected ? '#764ba2' : '#333';
                } else {
                    ctx.fillStyle = isSelected ? '#e0e7ff' : 'white';
                }

                ctx.fillRect(x, 0, keyWidth, 180);
                ctx.strokeStyle = '#333';
                ctx.lineWidth = 2;
                ctx.strokeRect(x, 0, keyWidth, 180);

                ctx.fillStyle = isBlack ? 'white' : '#667eea';
                ctx.font = 'bold 16px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(notes[i], x + keyWidth / 2, 160);
            }
        }

        function playNote(freq, delay = 0) {
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }

            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.frequency.value = freq;
            oscillator.type = 'sine';
            gainNode.gain.value = 0.3;

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.start(audioContext.currentTime + delay);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + delay + 0.8);
            oscillator.stop(audioContext.currentTime + delay + 0.8);
        }

        function updateInfo() {
            if (selectedNotes.length === 2) {
                const halfSteps = Math.abs(selectedNotes[1].index - selectedNotes[0].index);
                const intervalName = intervalNames[halfSteps] || 'Octave';
                info.textContent = `Interval: ${intervalName} (${halfSteps} half steps)`;
            } else if (selectedNotes.length === 1) {
                info.textContent = 'Select a second note...';
            } else {
                info.textContent = 'Click two keys to calculate interval';
            }
        }

        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const index = Math.floor(x / keyWidth);

            if (selectedNotes.length < 2) {
                selectedNotes.push({ index, freq: frequencies[index] });
                playNote(frequencies[index]);
            } else {
                selectedNotes = [{ index, freq: frequencies[index] }];
                playNote(frequencies[index]);
            }

            drawKeys();
            updateInfo();
        });

        harmonicBtn.addEventListener('click', () => {
            if (selectedNotes.length === 2) {
                playNote(selectedNotes[0].freq);
                playNote(selectedNotes[1].freq);
            }
        });

        melodicBtn.addEventListener('click', () => {
            if (selectedNotes.length === 2) {
                playNote(selectedNotes[0].freq, 0);
                playNote(selectedNotes[1].freq, 0.5);
            }
        });

        resetBtn.addEventListener('click', () => {
            selectedNotes = [];
            drawKeys();
            updateInfo();
        });

        drawKeys();
        updateInfo();
    """

    return get_base_html(title, instructions, content, script)


def generate_rhythm_visualization(concept):
    """Generate rhythm sequencer visualization."""
    title = f"Rhythm Sequencer: {concept['name']}"
    instructions = f"<strong>{concept['name']}:</strong> {concept['description']}<br><br>Click on the grid to toggle beats on/off, then press Play to hear your rhythm pattern."

    content = """
        <canvas id="rhythmCanvas" width="800" height="200"></canvas>
        <div class="controls">
            <button id="playRhythm">Play</button>
            <button id="stopRhythm">Stop</button>
            <button id="clearRhythm">Clear</button>
            <label>Tempo:</label>
            <input type="range" id="tempoSlider" min="60" max="180" value="120">
            <span class="value-display" id="tempoValue">120 BPM</span>
        </div>
    """

    script = """
        const canvas = document.getElementById('rhythmCanvas');
        const ctx = canvas.getContext('2d');
        const playBtn = document.getElementById('playRhythm');
        const stopBtn = document.getElementById('stopRhythm');
        const clearBtn = document.getElementById('clearRhythm');
        const tempoSlider = document.getElementById('tempoSlider');
        const tempoValue = document.getElementById('tempoValue');

        let audioContext = null;
        let beats = new Array(16).fill(false);
        let currentBeat = -1;
        let intervalId = null;

        const beatWidth = canvas.width / 16;
        const beatHeight = 150;

        function drawGrid() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (let i = 0; i < 16; i++) {
                const x = i * beatWidth;
                const isActive = beats[i];
                const isCurrent = i === currentBeat;

                if (isCurrent) {
                    ctx.fillStyle = '#fbbf24';
                } else if (isActive) {
                    ctx.fillStyle = '#667eea';
                } else {
                    ctx.fillStyle = '#f3f4f6';
                }

                ctx.fillRect(x + 2, 25, beatWidth - 4, beatHeight);
                ctx.strokeStyle = '#333';
                ctx.lineWidth = 2;
                ctx.strokeRect(x + 2, 25, beatWidth - 4, beatHeight);

                ctx.fillStyle = '#333';
                ctx.font = 'bold 12px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(i + 1, x + beatWidth / 2, 15);
            }
        }

        function playBeat() {
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }

            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.frequency.value = 800;
            oscillator.type = 'square';
            gainNode.gain.value = 0.2;

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.start();
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
            oscillator.stop(audioContext.currentTime + 0.1);
        }

        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const index = Math.floor(x / beatWidth);

            if (index >= 0 && index < 16) {
                beats[index] = !beats[index];
                drawGrid();
            }
        });

        playBtn.addEventListener('click', () => {
            if (intervalId) return;

            const tempo = parseInt(tempoSlider.value);
            const interval = 60000 / tempo / 4;
            currentBeat = 0;

            intervalId = setInterval(() => {
                if (beats[currentBeat]) {
                    playBeat();
                }

                currentBeat = (currentBeat + 1) % 16;
                drawGrid();
            }, interval);
        });

        stopBtn.addEventListener('click', () => {
            if (intervalId) {
                clearInterval(intervalId);
                intervalId = null;
                currentBeat = -1;
                drawGrid();
            }
        });

        clearBtn.addEventListener('click', () => {
            beats = new Array(16).fill(false);
            drawGrid();
        });

        tempoSlider.addEventListener('input', () => {
            tempoValue.textContent = tempoSlider.value + ' BPM';
        });

        drawGrid();
    """

    return get_base_html(title, instructions, content, script)


def generate_scale_visualization(concept):
    """Generate scale builder visualization."""
    title = f"Scale Builder: {concept['name']}"
    instructions = f"<strong>{concept['name']}:</strong> {concept['description']}<br><br>Select a scale type to see its pattern on the keyboard. Click Play to hear the scale."

    content = """
        <canvas id="scaleCanvas" width="800" height="200"></canvas>
        <div class="controls">
            <label>Scale Type:</label>
            <select id="scaleType">
                <option value="major">Major Scale (W-W-H-W-W-W-H)</option>
                <option value="minor">Natural Minor (W-H-W-W-H-W-W)</option>
                <option value="chromatic">Chromatic (All Half Steps)</option>
            </select>
        </div>
        <div class="controls">
            <button id="playScale">Play Ascending</button>
            <button id="playDescending">Play Descending</button>
        </div>
    """

    script = """
        const canvas = document.getElementById('scaleCanvas');
        const ctx = canvas.getContext('2d');
        const scaleType = document.getElementById('scaleType');
        const playBtn = document.getElementById('playScale');
        const descendBtn = document.getElementById('playDescending');

        let audioContext = null;

        const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C'];
        const frequencies = [261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25];

        const scalePatterns = {
            major: [0, 2, 4, 5, 7, 9, 11, 12],
            minor: [0, 2, 3, 5, 7, 8, 10, 12],
            chromatic: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        };

        const keyWidth = canvas.width / 13;

        function drawScale() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const pattern = scalePatterns[scaleType.value];

            for (let i = 0; i < 13; i++) {
                const x = i * keyWidth;
                const isBlack = notes[i].includes('#');
                const isInScale = pattern.includes(i);

                if (isBlack) {
                    ctx.fillStyle = isInScale ? '#764ba2' : '#333';
                } else {
                    ctx.fillStyle = isInScale ? '#e0e7ff' : 'white';
                }

                ctx.fillRect(x, 0, keyWidth, 180);
                ctx.strokeStyle = '#333';
                ctx.lineWidth = 2;
                ctx.strokeRect(x, 0, keyWidth, 180);

                ctx.fillStyle = isBlack ? 'white' : (isInScale ? '#667eea' : '#999');
                ctx.font = 'bold 14px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(notes[i], x + keyWidth / 2, 160);

                if (isInScale && !isBlack) {
                    ctx.fillStyle = '#667eea';
                    ctx.font = 'bold 20px sans-serif';
                    ctx.fillText('•', x + keyWidth / 2, 100);
                }
            }
        }

        function playNote(freq, delay) {
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }

            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.frequency.value = freq;
            oscillator.type = 'sine';
            gainNode.gain.value = 0.3;

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.start(audioContext.currentTime + delay);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + delay + 0.4);
            oscillator.stop(audioContext.currentTime + delay + 0.5);
        }

        playBtn.addEventListener('click', () => {
            const pattern = scalePatterns[scaleType.value];
            pattern.forEach((noteIndex, i) => {
                playNote(frequencies[noteIndex], i * 0.3);
            });
        });

        descendBtn.addEventListener('click', () => {
            const pattern = [...scalePatterns[scaleType.value]].reverse();
            pattern.forEach((noteIndex, i) => {
                playNote(frequencies[noteIndex], i * 0.3);
            });
        });

        scaleType.addEventListener('change', drawScale);

        drawScale();
    """

    return get_base_html(title, instructions, content, script)


def generate_chord_visualization(concept):
    """Generate chord builder visualization."""
    title = f"Chord Builder: {concept['name']}"
    instructions = f"<strong>{concept['name']}:</strong> {concept['description']}<br><br>Click on keys to build a chord, or use preset buttons. Click Play to hear the chord."

    content = """
        <canvas id="chordCanvas" width="800" height="200"></canvas>
        <div class="controls">
            <button onclick="buildChord([0, 4, 7])">C Major</button>
            <button onclick="buildChord([0, 3, 7])">C Minor</button>
            <button onclick="buildChord([0, 3, 6])">C Diminished</button>
            <button onclick="buildChord([0, 4, 8])">C Augmented</button>
            <button onclick="buildChord([0, 4, 7, 10])">C7</button>
        </div>
        <div class="controls">
            <button id="playChord">Play Chord</button>
            <button id="clearChord">Clear</button>
            <div id="chordFormula" style="margin-left: 20px; color: #667eea; font-weight: bold;"></div>
        </div>
    """

    script = """
        const canvas = document.getElementById('chordCanvas');
        const ctx = canvas.getContext('2d');
        const playBtn = document.getElementById('playChord');
        const clearBtn = document.getElementById('clearChord');
        const formula = document.getElementById('chordFormula');

        let audioContext = null;
        let selectedNotes = new Set();

        const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
        const frequencies = [261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88];
        const keyWidth = canvas.width / 12;

        function drawKeys() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (let i = 0; i < 12; i++) {
                const x = i * keyWidth;
                const isBlack = notes[i].includes('#');
                const isSelected = selectedNotes.has(i);

                if (isBlack) {
                    ctx.fillStyle = isSelected ? '#764ba2' : '#333';
                } else {
                    ctx.fillStyle = isSelected ? '#e0e7ff' : 'white';
                }

                ctx.fillRect(x, 0, keyWidth, 180);
                ctx.strokeStyle = '#333';
                ctx.lineWidth = 2;
                ctx.strokeRect(x, 0, keyWidth, 180);

                ctx.fillStyle = isBlack ? 'white' : '#667eea';
                ctx.font = 'bold 14px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(notes[i], x + keyWidth / 2, 160);
            }

            updateFormula();
        }

        function updateFormula() {
            const noteArray = Array.from(selectedNotes).sort((a, b) => a - b);
            if (noteArray.length === 0) {
                formula.textContent = '';
                return;
            }

            const intervals = noteArray.map(n => n);
            formula.textContent = 'Formula: ' + intervals.join('-');
        }

        function playNote(freq) {
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }

            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.frequency.value = freq;
            oscillator.type = 'sine';
            gainNode.gain.value = 0.2;

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.start();
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 1.5);
            oscillator.stop(audioContext.currentTime + 1.5);
        }

        window.buildChord = function(pattern) {
            selectedNotes = new Set(pattern);
            drawKeys();
        };

        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const index = Math.floor(x / keyWidth);

            if (selectedNotes.has(index)) {
                selectedNotes.delete(index);
            } else {
                selectedNotes.add(index);
            }

            drawKeys();
        });

        playBtn.addEventListener('click', () => {
            selectedNotes.forEach(noteIndex => {
                playNote(frequencies[noteIndex]);
            });
        });

        clearBtn.addEventListener('click', () => {
            selectedNotes.clear();
            drawKeys();
        });

        drawKeys();
    """

    return get_base_html(title, instructions, content, script)


def generate_circle_of_fifths_visualization(concept):
    """Generate circle of fifths visualization."""
    title = f"Circle of Fifths: {concept['name']}"
    instructions = f"<strong>{concept['name']}:</strong> {concept['description']}<br><br>Click on segments to explore different keys and see their sharps or flats."

    content = """
        <canvas id="circleCanvas" width="600" height="600"></canvas>
        <div class="controls">
            <div id="keyInfo" style="font-size: 18px; color: #667eea; font-weight: bold; min-height: 30px;"></div>
        </div>
    """

    script = """
        const canvas = document.getElementById('circleCanvas');
        const ctx = canvas.getContext('2d');
        const keyInfo = document.getElementById('keyInfo');

        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = 200;

        const majorKeys = ['C', 'G', 'D', 'A', 'E', 'B', 'F#/Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F'];
        const minorKeys = ['Am', 'Em', 'Bm', 'F#m', 'C#m', 'G#m', 'D#m/Ebm', 'Bbm', 'Fm', 'Cm', 'Gm', 'Dm'];
        const accidentals = ['0', '1#', '2#', '3#', '4#', '5#', '6#/6b', '5b', '4b', '3b', '2b', '1b'];

        let selectedSegment = -1;

        function drawCircle() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (let i = 0; i < 12; i++) {
                const startAngle = (i * Math.PI / 6) - Math.PI / 2;
                const endAngle = startAngle + Math.PI / 6;

                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.arc(centerX, centerY, radius, startAngle, endAngle);
                ctx.closePath();

                if (i === selectedSegment) {
                    ctx.fillStyle = '#764ba2';
                } else {
                    ctx.fillStyle = i % 2 === 0 ? '#e0e7ff' : '#f3f4f6';
                }
                ctx.fill();

                ctx.strokeStyle = '#667eea';
                ctx.lineWidth = 2;
                ctx.stroke();

                const angle = startAngle + Math.PI / 12;
                const textX = centerX + Math.cos(angle) * (radius * 0.7);
                const textY = centerY + Math.sin(angle) * (radius * 0.7);

                ctx.fillStyle = '#333';
                ctx.font = 'bold 16px sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(majorKeys[i], textX, textY - 10);

                ctx.font = '12px sans-serif';
                ctx.fillText(minorKeys[i], textX, textY + 10);

                const accX = centerX + Math.cos(angle) * (radius * 0.4);
                const accY = centerY + Math.sin(angle) * (radius * 0.4);
                ctx.font = 'bold 14px sans-serif';
                ctx.fillStyle = '#667eea';
                ctx.fillText(accidentals[i], accX, accY);
            }

            ctx.beginPath();
            ctx.arc(centerX, centerY, 60, 0, Math.PI * 2);
            ctx.fillStyle = 'white';
            ctx.fill();
            ctx.strokeStyle = '#667eea';
            ctx.lineWidth = 3;
            ctx.stroke();

            ctx.fillStyle = '#667eea';
            ctx.font = 'bold 18px sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText('Circle of', centerX, centerY - 10);
            ctx.fillText('Fifths', centerX, centerY + 10);
        }

        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left - centerX;
            const y = e.clientY - rect.top - centerY;

            const angle = Math.atan2(y, x) + Math.PI / 2;
            const normalizedAngle = (angle + Math.PI * 2) % (Math.PI * 2);
            const segment = Math.floor(normalizedAngle / (Math.PI / 6));

            const distance = Math.sqrt(x * x + y * y);
            if (distance <= radius && distance >= 60) {
                selectedSegment = segment;
                keyInfo.textContent = `${majorKeys[segment]} major / ${minorKeys[segment]} - ${accidentals[segment]}`;
                drawCircle();
            }
        });

        drawCircle();
        keyInfo.textContent = 'Click on a segment to explore keys';
    """

    return get_base_html(title, instructions, content, script)


def generate_progression_visualization(concept):
    """Generate chord progression builder visualization."""
    title = f"Chord Progression Builder: {concept['name']}"
    instructions = f"<strong>{concept['name']}:</strong> {concept['description']}<br><br>Click Roman numeral buttons to build a chord progression, then play it back."

    content = """
        <div class="controls">
            <button onclick="addChord('I')">I</button>
            <button onclick="addChord('ii')">ii</button>
            <button onclick="addChord('iii')">iii</button>
            <button onclick="addChord('IV')">IV</button>
            <button onclick="addChord('V')">V</button>
            <button onclick="addChord('vi')">vi</button>
            <button onclick="addChord('vii°')">vii°</button>
        </div>
        <div id="progression" style="min-height: 80px; background: #f3f4f6; border-radius: 10px; padding: 20px; margin: 20px 0; font-size: 24px; font-weight: bold; color: #667eea; text-align: center;">
            (Empty Progression)
        </div>
        <div class="controls">
            <button id="playProg">Play Progression</button>
            <button id="clearProg">Clear</button>
            <button onclick="setProgression(['I', 'IV', 'V', 'I'])">I-IV-V-I</button>
            <button onclick="setProgression(['I', 'V', 'vi', 'IV'])">I-V-vi-IV</button>
            <button onclick="setProgression(['ii', 'V', 'I'])">ii-V-I</button>
        </div>
    """

    script = """
        let audioContext = null;
        let progression = [];

        const chordMap = {
            'I': [261.63, 329.63, 392.00],
            'ii': [293.66, 349.23, 440.00],
            'iii': [329.63, 392.00, 493.88],
            'IV': [349.23, 440.00, 523.25],
            'V': [392.00, 493.88, 587.33],
            'vi': [440.00, 523.25, 659.25],
            'vii°': [493.88, 587.33, 698.46]
        };

        function updateDisplay() {
            const display = document.getElementById('progression');
            if (progression.length === 0) {
                display.textContent = '(Empty Progression)';
            } else {
                display.textContent = progression.join(' - ');
            }
        }

        window.addChord = function(chord) {
            progression.push(chord);
            updateDisplay();
        };

        window.setProgression = function(prog) {
            progression = prog;
            updateDisplay();
        };

        function playChord(frequencies, delay) {
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }

            frequencies.forEach(freq => {
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();

                oscillator.frequency.value = freq;
                oscillator.type = 'sine';
                gainNode.gain.value = 0.15;

                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);

                oscillator.start(audioContext.currentTime + delay);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + delay + 0.9);
                oscillator.stop(audioContext.currentTime + delay + 1);
            });
        }

        document.getElementById('playProg').addEventListener('click', () => {
            progression.forEach((chord, i) => {
                const frequencies = chordMap[chord];
                if (frequencies) {
                    playChord(frequencies, i * 1);
                }
            });
        });

        document.getElementById('clearProg').addEventListener('click', () => {
            progression = [];
            updateDisplay();
        });

        updateDisplay();
    """

    return get_base_html(title, instructions, content, script)


def generate_melody_builder_visualization(concept):
    """Generate melody/pattern builder visualization."""
    title = f"Melody Builder: {concept['name']}"
    instructions = f"<strong>{concept['name']}:</strong> {concept['description']}<br><br>Click on the grid to create a melodic pattern. Each column is a beat, each row is a note."

    content = """
        <canvas id="melodyCanvas" width="800" height="400"></canvas>
        <div class="controls">
            <button id="playMelody">Play Melody</button>
            <button id="clearMelody">Clear</button>
        </div>
    """

    script = """
        const canvas = document.getElementById('melodyCanvas');
        const ctx = canvas.getContext('2d');
        const playBtn = document.getElementById('playMelody');
        const clearBtn = document.getElementById('clearMelody');

        let audioContext = null;
        const cols = 16;
        const rows = 8;
        const cellWidth = canvas.width / cols;
        const cellHeight = canvas.height / rows;

        const notes = ['C5', 'B4', 'A4', 'G4', 'F4', 'E4', 'D4', 'C4'];
        const frequencies = [523.25, 493.88, 440.00, 392.00, 349.23, 329.63, 293.66, 261.63];

        let grid = Array(rows).fill().map(() => Array(cols).fill(false));

        function drawGrid() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (let row = 0; row < rows; row++) {
                for (let col = 0; col < cols; col++) {
                    const x = col * cellWidth;
                    const y = row * cellHeight;

                    ctx.fillStyle = grid[row][col] ? '#667eea' : '#f3f4f6';
                    ctx.fillRect(x + 1, y + 1, cellWidth - 2, cellHeight - 2);

                    ctx.strokeStyle = '#ddd';
                    ctx.lineWidth = 1;
                    ctx.strokeRect(x, y, cellWidth, cellHeight);
                }

                ctx.fillStyle = '#333';
                ctx.font = 'bold 12px sans-serif';
                ctx.textAlign = 'right';
                ctx.fillText(notes[row], canvas.width - 5, row * cellHeight + cellHeight / 2 + 4);
            }
        }

        canvas.addEventListener('click', (e) => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const col = Math.floor(x / cellWidth);
            const row = Math.floor(y / cellHeight);

            if (row >= 0 && row < rows && col >= 0 && col < cols) {
                grid[row][col] = !grid[row][col];
                drawGrid();
            }
        });

        playBtn.addEventListener('click', () => {
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }

            for (let col = 0; col < cols; col++) {
                for (let row = 0; row < rows; row++) {
                    if (grid[row][col]) {
                        const oscillator = audioContext.createOscillator();
                        const gainNode = audioContext.createGain();

                        oscillator.frequency.value = frequencies[row];
                        oscillator.type = 'sine';
                        gainNode.gain.value = 0.2;

                        oscillator.connect(gainNode);
                        gainNode.connect(audioContext.destination);

                        const delay = col * 0.25;
                        oscillator.start(audioContext.currentTime + delay);
                        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + delay + 0.2);
                        oscillator.stop(audioContext.currentTime + delay + 0.25);
                    }
                }
            }
        });

        clearBtn.addEventListener('click', () => {
            grid = Array(rows).fill().map(() => Array(cols).fill(false));
            drawGrid();
        });

        drawGrid();
    """

    return get_base_html(title, instructions, content, script)


def generate_dynamics_visualization(concept):
    """Generate dynamics visualizer."""
    title = f"Dynamics Visualizer: {concept['name']}"
    instructions = f"<strong>{concept['name']}:</strong> {concept['description']}<br><br>Select dynamic markings to hear and see the difference in volume levels."

    content = """
        <canvas id="dynamicsCanvas" width="800" height="300"></canvas>
        <div class="controls">
            <button onclick="setDynamic('pp', 0.1)">pp (pianissimo)</button>
            <button onclick="setDynamic('p', 0.25)">p (piano)</button>
            <button onclick="setDynamic('mp', 0.4)">mp (mezzo-piano)</button>
            <button onclick="setDynamic('mf', 0.6)">mf (mezzo-forte)</button>
            <button onclick="setDynamic('f', 0.8)">f (forte)</button>
            <button onclick="setDynamic('ff', 1.0)">ff (fortissimo)</button>
        </div>
    """

    script = """
        const canvas = document.getElementById('dynamicsCanvas');
        const ctx = canvas.getContext('2d');

        let audioContext = null;
        let currentDynamic = 'mf';
        let currentVolume = 0.6;

        const dynamics = [
            { name: 'pp', volume: 0.1, x: 100 },
            { name: 'p', volume: 0.25, x: 200 },
            { name: 'mp', volume: 0.4, x: 300 },
            { name: 'mf', volume: 0.6, x: 400 },
            { name: 'f', volume: 0.8, x: 500 },
            { name: 'ff', volume: 1.0, x: 600 }
        ];

        function drawDynamics() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            dynamics.forEach(dyn => {
                const barHeight = dyn.volume * 200;
                const y = canvas.height - 50 - barHeight;

                if (dyn.name === currentDynamic) {
                    ctx.fillStyle = '#764ba2';
                } else {
                    ctx.fillStyle = '#e0e7ff';
                }

                ctx.fillRect(dyn.x - 30, y, 60, barHeight);
                ctx.strokeStyle = '#667eea';
                ctx.lineWidth = 2;
                ctx.strokeRect(dyn.x - 30, y, 60, barHeight);

                ctx.fillStyle = '#333';
                ctx.font = 'bold 20px serif';
                ctx.textAlign = 'center';
                ctx.fillText(dyn.name, dyn.x, canvas.height - 20);
            });

            ctx.fillStyle = '#667eea';
            ctx.font = 'bold 18px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('Dynamic Levels (Loudness)', canvas.width / 2, 30);
        }

        window.setDynamic = function(name, volume) {
            currentDynamic = name;
            currentVolume = volume;
            drawDynamics();

            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }

            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.frequency.value = 440;
            oscillator.type = 'sine';
            gainNode.gain.value = volume * 0.3;

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.start();
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 1);
            oscillator.stop(audioContext.currentTime + 1);
        };

        drawDynamics();
    """

    return get_base_html(title, instructions, content, script)


def generate_transposition_visualization(concept):
    """Generate transposition tool visualization."""
    title = f"Transposition Tool: {concept['name']}"
    instructions = f"<strong>{concept['name']}:</strong> {concept['description']}<br><br>Create a simple melody, then transpose it to different keys while preserving intervals."

    content = """
        <canvas id="transposeCanvas" width="800" height="300"></canvas>
        <div class="controls">
            <label>Transpose by:</label>
            <select id="transposeInterval">
                <option value="0">0 (Original)</option>
                <option value="1">+1 half step</option>
                <option value="2">+2 half steps (Whole step)</option>
                <option value="3">+3 half steps</option>
                <option value="4">+4 half steps</option>
                <option value="5">+5 half steps</option>
                <option value="6">+6 half steps</option>
                <option value="-1">-1 half step</option>
                <option value="-2">-2 half steps</option>
            </select>
        </div>
        <div class="controls">
            <button id="playOriginal">Play Original</button>
            <button id="playTransposed">Play Transposed</button>
            <button id="clearTranspose">Clear</button>
        </div>
    """

    script = """
        const canvas = document.getElementById('transposeCanvas');
        const ctx = canvas.getContext('2d');
        const transposeSelect = document.getElementById('transposeInterval');
        const playOrigBtn = document.getElementById('playOriginal');
        const playTransBtn = document.getElementById('playTransposed');
        const clearBtn = document.getElementById('clearTranspose');

        let audioContext = null;
        let melody = [0, 2, 4, 5, 7];

        const baseFreq = 261.63;

        function getFrequency(halfSteps) {
            return baseFreq * Math.pow(2, halfSteps / 12);
        }

        function drawMelody() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const transpose = parseInt(transposeSelect.value);
            const spacing = canvas.width / (melody.length + 1);

            ctx.font = 'bold 16px sans-serif';
            ctx.fillStyle = '#333';
            ctx.textAlign = 'center';
            ctx.fillText('Original Melody', canvas.width / 2, 30);

            melody.forEach((note, i) => {
                const x = (i + 1) * spacing;
                const y = 150 - (note * 8);

                ctx.beginPath();
                ctx.arc(x, y, 15, 0, Math.PI * 2);
                ctx.fillStyle = '#667eea';
                ctx.fill();
                ctx.strokeStyle = '#333';
                ctx.lineWidth = 2;
                ctx.stroke();

                if (i > 0) {
                    const prevX = i * spacing;
                    const prevY = 150 - (melody[i - 1] * 8);
                    ctx.beginPath();
                    ctx.moveTo(prevX, prevY);
                    ctx.lineTo(x, y);
                    ctx.strokeStyle = '#667eea';
                    ctx.lineWidth = 3;
                    ctx.stroke();
                }
            });

            if (transpose !== 0) {
                ctx.fillStyle = '#764ba2';
                ctx.fillText(`Transposed by ${transpose} half steps`, canvas.width / 2, 180);

                const transposedMelody = melody.map(n => n + transpose);
                transposedMelody.forEach((note, i) => {
                    const x = (i + 1) * spacing;
                    const y = 250 - (note * 8);

                    ctx.beginPath();
                    ctx.arc(x, y, 15, 0, Math.PI * 2);
                    ctx.fillStyle = '#764ba2';
                    ctx.fill();
                    ctx.strokeStyle = '#333';
                    ctx.lineWidth = 2;
                    ctx.stroke();

                    if (i > 0) {
                        const prevX = i * spacing;
                        const prevY = 250 - (transposedMelody[i - 1] * 8);
                        ctx.beginPath();
                        ctx.moveTo(prevX, prevY);
                        ctx.lineTo(x, y);
                        ctx.strokeStyle = '#764ba2';
                        ctx.lineWidth = 3;
                        ctx.stroke();
                    }
                });
            }
        }

        function playMelodyNotes(notes, delay = 0) {
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }

            notes.forEach((note, i) => {
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();

                oscillator.frequency.value = getFrequency(note);
                oscillator.type = 'sine';
                gainNode.gain.value = 0.3;

                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);

                const noteDelay = delay + i * 0.4;
                oscillator.start(audioContext.currentTime + noteDelay);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + noteDelay + 0.3);
                oscillator.stop(audioContext.currentTime + noteDelay + 0.4);
            });
        }

        playOrigBtn.addEventListener('click', () => {
            playMelodyNotes(melody);
        });

        playTransBtn.addEventListener('click', () => {
            const transpose = parseInt(transposeSelect.value);
            const transposedMelody = melody.map(n => n + transpose);
            playMelodyNotes(transposedMelody);
        });

        clearBtn.addEventListener('click', () => {
            melody = [];
            drawMelody();
        });

        transposeSelect.addEventListener('change', drawMelody);

        drawMelody();
    """

    return get_base_html(title, instructions, content, script)


def categorize_concept(concept):
    """Determine which visualization type to use for a concept."""
    concept_id = concept['id']
    tags = concept.get('tags', [])

    # Sound/Acoustics concepts
    if concept_id in ['sound', 'pitch', 'volume', 'timbre']:
        return 'waveform'

    # Keyboard/Note concepts
    elif concept_id in ['note', 'note-name', 'octave', 'sharp', 'flat', 'natural',
                         'accidental', 'enharmonic', 'half-step', 'whole-step']:
        return 'keyboard'

    # Staff notation concepts
    elif concept_id in ['staff', 'clef', 'treble-clef', 'bass-clef', 'ledger-lines']:
        return 'staff'

    # Interval concepts
    elif concept_id in ['interval', 'interval-number', 'interval-quality',
                         'perfect-interval', 'major-interval', 'minor-interval',
                         'consonance', 'dissonance']:
        return 'interval'

    # Rhythm concepts
    elif concept_id in ['rhythm', 'beat', 'tempo', 'meter', 'time-signature',
                         'measure', 'note-value', 'rest', 'dot', 'tie', 'duration']:
        return 'rhythm'

    # Scale concepts
    elif concept_id in ['scale', 'major-scale', 'minor-scale', 'scale-degree',
                         'tonic', 'dominant', 'chromatic', 'diatonic']:
        return 'scale'

    # Chord concepts
    elif concept_id in ['chord', 'triad', 'major-triad', 'minor-triad',
                         'diminished-triad', 'augmented-triad', 'seventh-chord',
                         'chord-inversion', 'harmony']:
        return 'chord'

    # Key concepts
    elif concept_id in ['key', 'key-signature']:
        return 'circle'

    # Progression/Analysis concepts
    elif concept_id in ['chord-progression', 'cadence', 'roman-numeral-analysis', 'voice-leading']:
        return 'progression'

    # Structure/Form concepts
    elif concept_id in ['phrase', 'motif', 'melody', 'form', 'texture']:
        return 'melody'

    # Performance concepts
    elif concept_id in ['dynamics', 'articulation']:
        return 'dynamics'

    # Advanced concepts
    elif concept_id in ['transposition', 'modulation']:
        return 'transposition'

    # Default to keyboard for any others
    else:
        return 'keyboard'


def generate_visualization(concept):
    """Generate the appropriate visualization for a concept."""
    viz_type = categorize_concept(concept)

    generators = {
        'waveform': generate_waveform_visualization,
        'keyboard': generate_piano_keyboard_visualization,
        'staff': generate_staff_visualization,
        'interval': generate_interval_visualization,
        'rhythm': generate_rhythm_visualization,
        'scale': generate_scale_visualization,
        'chord': generate_chord_visualization,
        'circle': generate_circle_of_fifths_visualization,
        'progression': generate_progression_visualization,
        'melody': generate_melody_builder_visualization,
        'dynamics': generate_dynamics_visualization,
        'transposition': generate_transposition_visualization
    }

    generator = generators.get(viz_type, generate_piano_keyboard_visualization)
    return generator(concept)


def main():
    """Main function to generate all visualizations."""
    input_file = '/home/user/pla-2026/music-theory-concepts.json'
    output_dir = '/home/user/pla-2026/canvas_music_theory_course/wiki_content/'

    # Load concepts
    print(f"Loading concepts from {input_file}...")
    data = load_concepts(input_file)
    concepts = data['concepts']

    print(f"Found {len(concepts)} concepts")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate visualizations
    print(f"\nGenerating visualizations in {output_dir}...")
    for i, concept in enumerate(concepts, 1):
        concept_id = concept['id']
        filename = f"{concept_id}-visualization.html"
        filepath = os.path.join(output_dir, filename)

        html_content = generate_visualization(concept)

        with open(filepath, 'w') as f:
            f.write(html_content)

        print(f"  [{i}/{len(concepts)}] Generated {filename}")

    print(f"\nCompleted! Generated {len(concepts)} unique visualizations.")


if __name__ == '__main__':
    main()
