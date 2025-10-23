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

# Define module structure based on difficulty and topics
modules = [
    {
        "title": "Module 1: Foundations of Sound and Music",
        "concepts": ["sound", "pitch", "duration", "volume", "timbre", "note", "note-name", "beat"]
    },
    {
        "title": "Module 2: Musical Notation Basics",
        "concepts": ["staff", "clef", "treble-clef", "bass-clef", "ledger-lines"]
    },
    {
        "title": "Module 3: Rhythm and Time",
        "concepts": ["rhythm", "tempo", "meter", "time-signature", "measure", "note-value", "rest", "dot", "tie"]
    },
    {
        "title": "Module 4: Accidentals and Steps",
        "concepts": ["accidental", "sharp", "flat", "natural", "half-step", "whole-step"]
    },
    {
        "title": "Module 5: Intervals Foundation",
        "concepts": ["interval", "octave", "interval-number"]
    },
    {
        "title": "Module 6: Interval Quality",
        "concepts": ["interval-quality", "perfect-interval", "major-interval", "minor-interval"]
    },
    {
        "title": "Module 7: Scales",
        "concepts": ["scale", "major-scale", "minor-scale", "scale-degree", "tonic", "dominant"]
    },
    {
        "title": "Module 8: Keys and Key Signatures",
        "concepts": ["key", "key-signature", "enharmonic", "diatonic", "chromatic"]
    },
    {
        "title": "Module 9: Chords and Triads",
        "concepts": ["harmony", "chord", "triad", "major-triad", "minor-triad"]
    },
    {
        "title": "Module 10: Advanced Chords",
        "concepts": ["diminished-triad", "augmented-triad", "seventh-chord", "chord-inversion"]
    },
    {
        "title": "Module 11: Harmony and Progressions",
        "concepts": ["consonance", "dissonance", "chord-progression", "cadence"]
    },
    {
        "title": "Module 12: Melody and Structure",
        "concepts": ["melody", "phrase", "motif"]
    },
    {
        "title": "Module 13: Musical Expression",
        "concepts": ["dynamics", "articulation"]
    },
    {
        "title": "Module 14: Form and Texture",
        "concepts": ["form", "texture"]
    },
    {
        "title": "Module 15: Advanced Theory",
        "concepts": ["transposition", "modulation", "voice-leading", "roman-numeral-analysis"]
    }
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
print(f"Total modules: {len(modules)}")

# Create pages and quizzes for each module
for module_num, module_data in enumerate(modules, 1):
    print(f"\nProcessing {module_data['title']}...")

    module_id = generate_id()
    module_ids[module_num] = module_id

    # Create pages for each concept in the module
    for concept_id in module_data['concepts']:
        if concept_id in concepts:
            print(f"  - Creating page for {concepts[concept_id]['name']}")

            # Generate HTML
            html_content = create_html_page(concept_id)

            # Save HTML file
            page_id = generate_id()
            resource_ids[concept_id] = page_id
            filename = f"{concept_id}.html"

            with open(f"{output_dir}/wiki_content/{filename}", 'w') as f:
                f.write(html_content)

    # Create quiz for the module
    print(f"  - Creating quiz for module {module_num}")
    questions = create_quiz_for_module(module_num, module_data)
    quiz_xml = create_quiz_xml(module_num, questions)
    quiz_id = generate_id()

    with open(f"{output_dir}/assessment_questions/quiz_module_{module_num}.xml", 'w') as f:
        f.write(quiz_xml)

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

# Add modules to organization
for module_num, module_data in enumerate(modules, 1):
    item = SubElement(org, 'item')
    item.set('identifier', module_ids[module_num])

    item_title = SubElement(item, 'title')
    item_title.text = module_data['title']

    # Add concept pages as sub-items
    for concept_id in module_data['concepts']:
        if concept_id in resource_ids:
            subitem = SubElement(item, 'item')
            subitem.set('identifier', generate_id())
            subitem.set('identifierref', resource_ids[concept_id])

            subitem_title = SubElement(subitem, 'title')
            subitem_title.text = concepts[concept_id]['name']

# Resources section
resources = SubElement(manifest, 'resources')

# Add wiki page resources
for concept_id, page_id in resource_ids.items():
    resource = SubElement(resources, 'resource')
    resource.set('identifier', page_id)
    resource.set('type', 'webcontent')

    file_elem = SubElement(resource, 'file')
    file_elem.set('href', f"wiki_content/{concept_id}.html")

# Add quiz resources
for module_num in range(1, len(modules) + 1):
    resource = SubElement(resources, 'resource')
    resource.set('identifier', generate_id())
    resource.set('type', 'imsqti_xmlv1p2/imscc_xmlv1p1/assessment')

    file_elem = SubElement(resource, 'file')
    file_elem.set('href', f"assessment_questions/quiz_module_{module_num}.xml")

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
print(f"  - Total Modules: {len(modules)}")
print(f"  - Total Concepts: {len(concepts)}")
print(f"  - Total Pages: {len(resource_ids)}")
print(f"  - Total Quizzes: {len(modules)}")
print(f"\nTo import into Canvas:")
print(f"  1. Log into Canvas")
print(f"  2. Go to your course")
print(f"  3. Navigate to Settings > Import Course Content")
print(f"  4. Select 'Common Cartridge 1.x Package'")
print(f"  5. Upload the file: {package_name}")
print(f"  6. Click 'Import'")
print(f"\nPackage location: {os.path.abspath(package_name)}")
