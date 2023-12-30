/**
 * Initializes character and word counters for all richtext fields on the page.
 */
function initializeCharacterCounters() {
  // Locate all main editor containers
  const editorWrappers = document.querySelectorAll('.w-field--draftail_rich_text_area');

  // If no editor containers exist, exit the function.
  if (!editorWrappers.length) {
    return;
  }

  // Iterate over each editor container
  editorWrappers.forEach((editorWrapper, index) => {
    // Create an element for the character counter
    const charCounter = document.createElement('div');
    charCounter.className = `char-counter-${index}`;

    // Create an element for the word counter
    const wordCounter = document.createElement('div');
    wordCounter.className = `word-counter-${index}`;

    // Append the counters directly below the editor container
    editorWrapper.parentNode.insertBefore(charCounter, editorWrapper.nextSibling);
    editorWrapper.parentNode.insertBefore(wordCounter, charCounter.nextSibling);

    // Locate the contenteditable element
    const textField = editorWrapper.querySelector('.DraftEditor-editorContainer [contenteditable="true"]');

    // Function to update the character and word count
    const updateCounter = () => {
      const textContent = textField.textContent || "";
      const wordCount = textContent.split(/\s+/).filter(Boolean).length;
      charCounter.innerText = `Characters: ${textContent.length}`;
      wordCounter.innerText = `Words: ${wordCount}`;
    };

    // Attach event listeners
    textField.addEventListener('input', updateCounter);
    textField.addEventListener('keydown', (event) => {
      if (event.keyCode === 8 || event.keyCode === 46) {
        setTimeout(updateCounter, 50);
      }
    });
    textField.addEventListener('paste', () => setTimeout(updateCounter, 50));

    // Set initial values
    updateCounter();
  });
}

/**
 * Initializes the mutation observer to monitor for added richtext fields.
 */
function initObserver() {
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.addedNodes && mutation.addedNodes.length > 0) {
        for (const node of mutation.addedNodes) {
          if (node.querySelector && node.querySelector('.w-field--draftail_rich_text_area')) {
            initializeCharacterCounters();
          }
        }
      }
    });
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });
}

// Initialize on page load and DOMContentLoaded
window.addEventListener('load', initObserver);
document.addEventListener('DOMContentLoaded', initializeCharacterCounters);