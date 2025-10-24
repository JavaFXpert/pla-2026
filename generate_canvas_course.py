#!/usr/bin/env python3
"""
Canvas LMS Course Generator for Music Theory
Generates an IMS Common Cartridge package from music-theory-concepts.json
"""

import json
import os
import uuid
import shutil
import zipfile
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Load the concepts
with open('music-theory-concepts.json', 'r') as f:
    data = json.load(f)

concepts = {c['id']: c for c in data['concepts']}

# YouTube video mapping for Brad Harrison videos
# Each concept maps to a search query or topic for Brad Harrison's channel
brad_harrison_videos = {
    "sound": "music fundamentals sound",
    "pitch": "pitch music theory",
    "duration": "rhythm duration music",
    "volume": "dynamics volume music",
    "timbre": "tone color timbre",
    "note": "musical notes basics",
    "note-name": "note names music theory",
    "beat": "beat pulse music",
    "staff": "staff notation music",
    "clef": "clef music theory",
    "treble-clef": "treble clef",
    "bass-clef": "bass clef",
    "ledger-lines": "ledger lines",
    "accidental": "accidentals music theory",
    "sharp": "sharps music",
    "flat": "flats music",
    "natural": "natural signs music",
    "half-step": "half step semitone",
    "whole-step": "whole step tone",
    "interval": "intervals music theory",
    "octave": "octave music",
    "interval-number": "interval numbers",
    "interval-quality": "interval quality",
    "perfect-interval": "perfect intervals",
    "major-interval": "major intervals",
    "minor-interval": "minor intervals",
    "rhythm": "rhythm music theory",
    "tempo": "tempo music",
    "meter": "meter time signature",
    "time-signature": "time signatures",
    "measure": "measures bars music",
    "note-value": "note values duration",
    "rest": "rests music notation",
    "dot": "dotted notes",
    "tie": "ties music notation",
    "scale": "scales music theory",
    "major-scale": "major scale",
    "minor-scale": "minor scale",
    "scale-degree": "scale degrees",
    "tonic": "tonic music theory",
    "dominant": "dominant chord",
    "key": "key music theory",
    "key-signature": "key signatures",
    "enharmonic": "enharmonic equivalents",
    "diatonic": "diatonic music",
    "chromatic": "chromatic scale",
    "harmony": "harmony music theory",
    "chord": "chords music theory",
    "triad": "triads music",
    "major-triad": "major chords triads",
    "minor-triad": "minor chords triads",
    "diminished-triad": "diminished chords",
    "augmented-triad": "augmented chords",
    "seventh-chord": "seventh chords",
    "chord-inversion": "chord inversions",
    "consonance": "consonance music",
    "dissonance": "dissonance music",
    "chord-progression": "chord progressions",
    "cadence": "cadences music theory",
    "melody": "melody music theory",
    "phrase": "musical phrases",
    "motif": "motif motive music",
    "dynamics": "dynamics music",
    "articulation": "articulation music",
    "form": "musical form",
    "texture": "musical texture",
    "transposition": "transposition music",
    "modulation": "modulation music theory",
    "voice-leading": "voice leading",
    "roman-numeral-analysis": "roman numeral analysis"
}

# Organize concepts by difficulty for learning progression
# Each concept becomes its own section/module
concept_order = [
    "sound", "pitch", "duration", "volume", "timbre", "note", "note-name", "beat",
    "staff", "clef", "treble-clef", "bass-clef", "ledger-lines",
    "rhythm", "tempo", "meter", "time-signature", "measure", "note-value", "rest", "dot", "tie",
    "accidental", "sharp", "flat", "natural", "half-step", "whole-step",
    "interval", "octave", "interval-number",
    "interval-quality", "perfect-interval", "major-interval", "minor-interval",
    "scale", "major-scale", "minor-scale", "scale-degree", "tonic", "dominant",
    "key", "key-signature", "enharmonic", "diatonic", "chromatic",
    "harmony", "chord", "triad", "major-triad", "minor-triad",
    "diminished-triad", "augmented-triad", "seventh-chord", "chord-inversion",
    "consonance", "dissonance", "chord-progression", "cadence",
    "melody", "phrase", "motif",
    "dynamics", "articulation",
    "form", "texture",
    "transposition", "modulation", "voice-leading", "roman-numeral-analysis"
]

# Create output directory structure
output_dir = "canvas_music_theory_course"
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

os.makedirs(output_dir)
os.makedirs(f"{output_dir}/wiki_content")
os.makedirs(f"{output_dir}/assessment_questions")

# Generate unique identifiers
def generate_id():
    return f"i{uuid.uuid4().hex}"

# Store IDs for manifest
resource_ids = {}
module_ids = {}
item_ids = {}

def create_html_page(concept):
    """Create an HTML page for a concept"""
    c = concepts[concept]

    # Build prerequisites section
    prereq_html = ""
    if c['prerequisites']:
        prereq_list = [f"<li><strong>{concepts[p]['name']}</strong></li>" for p in c['prerequisites']]
        prereq_html = f"""
        <div class="prerequisites" style="background-color: #f0f8ff; padding: 15px; border-left: 4px solid #4CAF50; margin: 20px 0;">
            <h3>Prerequisites</h3>
            <p>Before studying this concept, make sure you understand:</p>
            <ul>
                {''.join(prereq_list)}
            </ul>
        </div>
        """

    # Build examples section
    examples_html = ""
    if c['examples']:
        example_items = [f"<li>{ex}</li>" for ex in c['examples']]
        examples_html = f"""
        <div class="examples" style="background-color: #fff9e6; padding: 15px; border-left: 4px solid #ff9800; margin: 20px 0;">
            <h3>Examples</h3>
            <ul>
                {''.join(example_items)}
            </ul>
        </div>
        """

    # Build learning objectives section
    objectives_html = ""
    if c['learning_objectives']:
        obj_items = [f"<li>{obj}</li>" for obj in c['learning_objectives']]
        objectives_html = f"""
        <div class="learning-objectives" style="background-color: #e8f5e9; padding: 15px; border-left: 4px solid #2196F3; margin: 20px 0;">
            <h3>Learning Objectives</h3>
            <p>By the end of this lesson, you should be able to:</p>
            <ul>
                {''.join(obj_items)}
            </ul>
        </div>
        """

    # Build related concepts section
    related_html = ""
    if c['related_concepts']:
        related_list = [f"<li>{concepts.get(r, {}).get('name', r)}</li>" for r in c['related_concepts']]
        related_html = f"""
        <div class="related-concepts" style="background-color: #f3e5f5; padding: 15px; border-left: 4px solid #9c27b0; margin: 20px 0;">
            <h3>Related Concepts</h3>
            <ul>
                {''.join(related_list)}
            </ul>
        </div>
        """

    # Build tags section
    tags_html = ""
    if c['tags']:
        tag_badges = [f'<span style="background-color: #607d8b; color: white; padding: 5px 10px; border-radius: 3px; margin-right: 5px; display: inline-block; margin-bottom: 5px;">{tag}</span>'
                      for tag in c['tags']]
        tags_html = f"""
        <div class="tags" style="margin: 20px 0;">
            {''.join(tag_badges)}
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{c['name']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2, h3 {{
            color: #34495e;
        }}
        .description {{
            font-size: 1.2em;
            color: #555;
            margin: 20px 0;
            padding: 20px;
            background-color: #ecf0f1;
            border-radius: 5px;
        }}
        .difficulty {{
            display: inline-block;
            padding: 8px 15px;
            background-color: #3498db;
            color: white;
            border-radius: 20px;
            font-weight: bold;
            margin: 10px 0;
        }}
        ul {{
            line-height: 1.8;
        }}
        li {{
            margin-bottom: 8px;
        }}
    </style>
</head>
<body>
    <h1>{c['name']}</h1>

    <div class="difficulty">Difficulty Level: {c['difficulty']}/6</div>

    {tags_html}

    <div class="description">
        <strong>Definition:</strong> {c['description']}
    </div>

    {prereq_html}

    {objectives_html}

    {examples_html}

    {related_html}

    <div style="margin-top: 40px; padding: 20px; background-color: #e3f2fd; border-radius: 5px;">
        <h3>Study Tips</h3>
        <ul>
            <li>Review this concept multiple times until you feel confident</li>
            <li>Try to create your own examples beyond those provided</li>
            <li>Connect this concept to music you already know and enjoy</li>
            <li>Practice identifying this concept in real musical examples</li>
        </ul>
    </div>
</body>
</html>"""

    return html

def create_video_page(concept_id):
    """Create an HTML page with embedded Brad Harrison YouTube video"""
    c = concepts[concept_id]
    search_query = brad_harrison_videos.get(concept_id, c['name'])

    # YouTube channel URL for Brad Harrison
    channel_url = "https://www.youtube.com/@BradHarrison"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{c['name']} - Video Lesson</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #e74c3c;
            padding-bottom: 10px;
        }}
        .video-container {{
            position: relative;
            padding-bottom: 56.25%; /* 16:9 aspect ratio */
            height: 0;
            overflow: hidden;
            max-width: 100%;
            background: #000;
            margin: 30px 0;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .video-container iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 0;
        }}
        .instructor-info {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .instructor-info h2 {{
            color: #e74c3c;
            margin-top: 0;
        }}
        .channel-link {{
            display: inline-block;
            background-color: #e74c3c;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 5px;
            margin: 15px 0;
            font-weight: bold;
            transition: background-color 0.3s;
        }}
        .channel-link:hover {{
            background-color: #c0392b;
        }}
        .note {{
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <h1>{c['name']} - Video Lesson</h1>

    <div class="instructor-info">
        <h2>Learn from Brad Harrison</h2>
        <p>Brad Harrison is a Toronto-based trumpet player, composer, and music educator with over 214K YouTube subscribers. His channel focuses on music theory, practice techniques, and other musical topics.</p>
        <a href="{channel_url}" target="_blank" class="channel-link">Visit Brad Harrison's YouTube Channel</a>
    </div>

    <div class="note">
        <strong>Video Lesson:</strong> Watch this video from Brad Harrison to deepen your understanding of <strong>{c['name']}</strong>.
    </div>

    <div class="video-container">
        <!-- Embedded YouTube Search Results for Brad Harrison + topic -->
        <iframe
            src="https://www.youtube.com/embed?listType=search&list=Brad+Harrison+{search_query.replace(' ', '+')}"
            allowfullscreen
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture">
        </iframe>
    </div>

    <div style="background-color: white; padding: 20px; border-radius: 8px; margin-top: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h3>After Watching</h3>
        <ul>
            <li>Take notes on key concepts explained in the video</li>
            <li>Try the practice exercises if any are demonstrated</li>
            <li>Re-watch sections that need clarification</li>
            <li>Explore more of Brad Harrison's videos on related topics</li>
            <li>Apply what you learned to your own musical practice</li>
        </ul>
    </div>

    <div style="background-color: #e3f2fd; padding: 15px; border-radius: 8px; margin-top: 20px;">
        <p><em>Note: This embedded search shows videos from Brad Harrison's channel related to "{search_query}".
        If the video player doesn't load automatically, you can visit <a href="{channel_url}" target="_blank">Brad Harrison's YouTube channel</a>
        and search for videos about "{c['name']}".</em></p>
    </div>
</body>
</html>"""

    return html

def create_quiz_for_module(module_num, module_data):
    """Create quiz questions for a module"""
    questions = []

    for concept_id in module_data['concepts']:
        c = concepts[concept_id]
        q_id = generate_id()

        # Create a multiple choice question based on the concept
        question = {
            'id': q_id,
            'type': 'multiple_choice',
            'title': f"Understanding {c['name']}",
            'text': f"Which of the following best describes {c['name']}?",
            'correct_answer': c['description'],
            'distractors': generate_distractors(c)
        }
        questions.append(question)

        # Create additional questions based on learning objectives
        if c['learning_objectives'] and len(c['learning_objectives']) > 0:
            obj = c['learning_objectives'][0]
            q_id2 = generate_id()
            question2 = {
                'id': q_id2,
                'type': 'essay',
                'title': f"Application: {c['name']}",
                'text': f"Explain in your own words: {obj}"
            }
            questions.append(question2)

    return questions

def generate_distractors(concept):
    """Generate plausible wrong answers"""
    # This is simplified - in a real implementation, you'd want more sophisticated distractor generation
    return [
        "A musical term for tempo variations",
        "A type of musical instrument",
        "A performance technique"
    ]

def create_quiz_xml(module_num, questions):
    """Create QTI XML for a quiz"""
    assessment = Element('questestinterop')
    assessment.set('xmlns', 'http://www.imsglobal.org/xsd/ims_qtiasiv1p2')

    for q in questions:
        item = SubElement(assessment, 'item')
        item.set('ident', q['id'])
        item.set('title', q['title'])

        presentation = SubElement(item, 'presentation')
        material = SubElement(presentation, 'material')
        mattext = SubElement(material, 'mattext')
        mattext.set('texttype', 'text/html')
        mattext.text = q['text']

        if q['type'] == 'multiple_choice':
            response = SubElement(presentation, 'response_lid')
            response.set('ident', 'response1')
            response.set('rcardinality', 'Single')

            render = SubElement(response, 'render_choice')

            # Correct answer
            choice1 = SubElement(render, 'response_label')
            choice1.set('ident', 'correct')
            mat1 = SubElement(choice1, 'material')
            text1 = SubElement(mat1, 'mattext')
            text1.text = q['correct_answer']

            # Distractors
            for i, dist in enumerate(q['distractors'], 1):
                choice = SubElement(render, 'response_label')
                choice.set('ident', f'distractor{i}')
                mat = SubElement(choice, 'material')
                text = SubElement(mat, 'mattext')
                text.text = dist

        elif q['type'] == 'essay':
            response = SubElement(presentation, 'response_str')
            response.set('ident', 'response1')
            response.set('rcardinality', 'Single')

    return minidom.parseString(tostring(assessment)).toprettyxml(indent="  ")

# Generate all content
print("Generating Canvas course package...")
print(f"Total concepts: {len(concepts)}")
print(f"Each concept will be its own section with 2 pages")

# Store video page resource IDs
video_resource_ids = {}

# Create pages and video pages for each concept
for concept_id in concept_order:
    if concept_id in concepts:
        concept_name = concepts[concept_id]['name']
        print(f"\nProcessing section: {concept_name}")

        # Create concept page (Page 1)
        print(f"  - Creating concept page")
        html_content = create_html_page(concept_id)
        page_id = generate_id()
        resource_ids[concept_id] = page_id
        filename = f"{concept_id}.html"

        with open(f"{output_dir}/wiki_content/{filename}", 'w') as f:
            f.write(html_content)

        # Create video page (Page 2)
        print(f"  - Creating video page with Brad Harrison content")
        video_content = create_video_page(concept_id)
        video_page_id = generate_id()
        video_resource_ids[concept_id] = video_page_id
        video_filename = f"{concept_id}-video.html"

        with open(f"{output_dir}/wiki_content/{video_filename}", 'w') as f:
            f.write(video_content)

# Create manifest XML
print("\nGenerating imsmanifest.xml...")

manifest = Element('manifest')
manifest.set('identifier', generate_id())
manifest.set('xmlns', 'http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1')
manifest.set('xmlns:lom', 'http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource')
manifest.set('xmlns:lomimscc', 'http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest')
manifest.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')

# Metadata
metadata = SubElement(manifest, 'metadata')
schema = SubElement(metadata, 'schema')
schema.text = 'IMS Common Cartridge'
schemaversion = SubElement(metadata, 'schemaversion')
schemaversion.text = '1.1.0'

lom_meta = SubElement(metadata, 'lom:lom')
general = SubElement(lom_meta, 'lom:general')
title_elem = SubElement(general, 'lom:title')
title_string = SubElement(title_elem, 'lom:string')
title_string.text = 'Comprehensive Music Theory Course'

# Organizations (module structure)
organizations = SubElement(manifest, 'organizations')
org = SubElement(organizations, 'organization')
org.set('identifier', 'org_1')
org.set('structure', 'rooted-hierarchy')

org_title = SubElement(org, 'title')
org_title.text = 'Comprehensive Music Theory Course'

# Add each concept as its own section/module with 2 pages
for concept_id in concept_order:
    if concept_id in concepts and concept_id in resource_ids:
        # Create a section/module for this concept
        section = SubElement(org, 'item')
        section.set('identifier', generate_id())

        section_title = SubElement(section, 'title')
        section_title.text = concepts[concept_id]['name']

        # Add Page 1: Concept explanation
        page1 = SubElement(section, 'item')
        page1.set('identifier', generate_id())
        page1.set('identifierref', resource_ids[concept_id])

        page1_title = SubElement(page1, 'title')
        page1_title.text = f"Lesson: {concepts[concept_id]['name']}"

        # Add Page 2: Video from Brad Harrison
        page2 = SubElement(section, 'item')
        page2.set('identifier', generate_id())
        page2.set('identifierref', video_resource_ids[concept_id])

        page2_title = SubElement(page2, 'title')
        page2_title.text = f"Video: {concepts[concept_id]['name']}"

# Resources section
resources = SubElement(manifest, 'resources')

# Add concept page resources
for concept_id, page_id in resource_ids.items():
    resource = SubElement(resources, 'resource')
    resource.set('identifier', page_id)
    resource.set('type', 'webcontent')

    file_elem = SubElement(resource, 'file')
    file_elem.set('href', f"wiki_content/{concept_id}.html")

# Add video page resources
for concept_id, video_page_id in video_resource_ids.items():
    resource = SubElement(resources, 'resource')
    resource.set('identifier', video_page_id)
    resource.set('type', 'webcontent')

    file_elem = SubElement(resource, 'file')
    file_elem.set('href', f"wiki_content/{concept_id}-video.html")

# Write manifest
manifest_xml = minidom.parseString(tostring(manifest)).toprettyxml(indent="  ")
with open(f"{output_dir}/imsmanifest.xml", 'w') as f:
    f.write(manifest_xml)

# Create course settings file
course_settings = {
    "course_name": "Comprehensive Music Theory Course",
    "course_code": "MUSIC-THEORY-101",
    "start_date": datetime.now().isoformat(),
    "conclude_date": None,
    "is_public": False,
    "syllabus_body": "<h2>Welcome to Comprehensive Music Theory!</h2><p>This course covers all fundamental and advanced concepts in music theory, from basic sound properties to advanced harmonic analysis.</p>",
    "grading_standard_enabled": True,
    "course_format": "online"
}

with open(f"{output_dir}/course_settings.json", 'w') as f:
    json.dump(course_settings, f, indent=2)

# Create the .imscc package (ZIP file)
print("\nCreating .imscc package...")
package_name = "music_theory_course.imscc"

with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, output_dir)
            zipf.write(file_path, arcname)

print(f"\n{'='*60}")
print(f"SUCCESS! Course package created: {package_name}")
print(f"{'='*60}")
print(f"\nCourse Statistics:")
print(f"  - Total Sections (one per concept): {len(concept_order)}")
print(f"  - Total Concept Pages: {len(resource_ids)}")
print(f"  - Total Video Pages: {len(video_resource_ids)}")
print(f"  - Total Pages: {len(resource_ids) + len(video_resource_ids)}")
print(f"\nCourse Structure:")
print(f"  Each atomic concept is now its own section with:")
print(f"    • Page 1: Detailed lesson content")
print(f"    • Page 2: Brad Harrison YouTube video")
print(f"\nTo import into Canvas:")
print(f"  1. Log into Canvas")
print(f"  2. Go to your course")
print(f"  3. Navigate to Settings > Import Course Content")
print(f"  4. Select 'Common Cartridge 1.x Package'")
print(f"  5. Upload the file: {package_name}")
print(f"  6. Click 'Import'")
print(f"\nPackage location: {os.path.abspath(package_name)}")
