const toastElList = document.querySelectorAll('.toast')
const toastList = [...toastElList].map(toastEl => new bootstrap.Toast(toastEl))

// Count characters of textarea in Notes form 
const noteTextarea = document.getElementById("note-textarea");
const countSpan = document.getElementById("note-chars-count");

// Check if noteTextarea present on page
// if (typeof (noteTextarea) != 'undefined' && noteTextarea != null) {
if (noteTextarea) {
    // Update counter with existed text on edit page
    countSpan.textContent = noteTextarea.value.length;

    // Add an event listener for input events
    noteTextarea.addEventListener("input", function() {
        const characterCount = noteTextarea.value.length;
        countSpan.textContent = characterCount;
    });
}
