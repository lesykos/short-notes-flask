// Count characters of textarea in Notes form 
const noteTextarea = document.getElementById("note-textarea");
const countSpan = document.getElementById("note-chars-count");

// Check if noteTextarea present on page
// if (typeof (noteTextarea) != 'undefined' && noteTextarea != null) {
if (noteTextarea) {
    // Add an event listener for input events
    noteTextarea.addEventListener("input", function() {
        const characterCount = noteTextarea.value.length;
        countSpan.textContent = characterCount;
    });
}
