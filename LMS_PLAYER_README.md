# Music Theory Mini-LMS Player

A standalone, interactive learning management system (LMS) player for exploring the comprehensive Music Theory course.

## Features

### 🎯 Core Functionality
- **91 Music Theory Concepts**: Browse through all concepts from basic sound properties to advanced harmonic analysis
- **Organized by Difficulty**: Concepts grouped into 6 difficulty levels for progressive learning
- **Interactive Navigation**: Click any concept to view its detailed content
- **Prerequisites Tracking**: See required prerequisite concepts before studying advanced topics

### 📊 Progress Tracking
- **Automatic Progress Saving**: Your progress is automatically saved to browser localStorage
- **Visual Progress Bar**: See your completion percentage at a glance
- **Completion Checkmarks**: Completed concepts are marked with a checkmark
- **Progress Statistics**: View total concepts, completed count, and difficulty levels

### 🔍 Search & Discovery
- **Real-time Search**: Find concepts by name, description, or tags
- **Keyboard Shortcut**: Press `Ctrl+K` (or `Cmd+K` on Mac) to quickly focus the search box
- **Smart Filtering**: Search results update instantly as you type

### 🎨 User Experience
- **Clean, Modern Design**: Professional gradient header and card-based layout
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Smooth Animations**: Elegant transitions and hover effects
- **Custom Scrollbars**: Styled scrollbars for a polished look

### 📚 Content Display
- **Rich HTML Content**: Each concept includes:
  - Definition and description
  - Difficulty level indicator
  - Learning objectives
  - Real-world examples
  - Related concepts
  - Study tips
  - Tags for categorization

## How to Use

### Getting Started
1. Open `index.html` in any modern web browser (Chrome, Firefox, Safari, Edge)
2. No server required - it runs entirely in your browser
3. The welcome screen shows course statistics and your progress

### Navigating the Course
1. **Browse Concepts**: Scroll through the sidebar to see all concepts organized by difficulty level
2. **Select a Concept**: Click any concept to view its detailed content
3. **Follow Prerequisites**: Yellow prerequisite badges show what you should learn first - click them to navigate
4. **Search**: Use the search box to find specific topics quickly
5. **Track Progress**: Concepts are automatically marked as completed when you view them

### Managing Progress
- **View Progress**: Check the progress bar in the header to see your completion percentage
- **Reset Progress**: Click the "Reset Progress" button on the welcome screen to start over
- **Persistent Storage**: Your progress is saved automatically and persists between browser sessions

### Navigation Tips
- Use the search box to quickly find topics (keyboard shortcut: `Ctrl+K` or `Cmd+K`)
- Completed concepts show a green checkmark
- The active concept is highlighted in purple
- Hover over concepts to see a preview with tags
- Click prerequisite badges to understand the learning path

## Technical Details

### Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Data Sources
- **Concepts**: `music-theory-concepts.json` (91 concepts with metadata)
- **Content**: `canvas_music_theory_course/wiki_content/*.html` (individual concept pages)
- **Progress**: Stored in browser's localStorage

### Features Overview
- Single-page application (SPA)
- No dependencies or frameworks required
- Vanilla JavaScript, HTML5, and CSS3
- localStorage for progress persistence
- Responsive flexbox layout
- CSS animations and transitions

## File Structure
```
index.html                              # The mini-LMS player
music-theory-concepts.json              # Concept metadata and relationships
canvas_music_theory_course/
  ├── wiki_content/                     # Individual concept HTML pages
  │   ├── sound.html
  │   ├── pitch.html
  │   ├── ... (89 more files)
  └── course_settings.json              # Course configuration
```

## Keyboard Shortcuts
- `Ctrl+K` or `Cmd+K` - Focus search box

## Privacy & Data
- All data is stored locally in your browser
- No data is sent to any server
- Clearing browser data will reset progress
- No tracking or analytics

## Tips for Best Learning Experience
1. Start with Level 1 concepts and work your way up
2. Review prerequisites before tackling advanced topics
3. Use the search function to find related concepts
4. Take notes outside the player for better retention
5. Review completed concepts periodically for reinforcement

## Support
For issues or questions about the course content, refer to the main repository documentation.

---

**Course**: Comprehensive Music Theory Course
**Concepts**: 91
**Difficulty Levels**: 1-6
**License**: MIT
