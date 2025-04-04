/**
 * Markdown rendering for Archon AI using popular libraries
 * This uses Marked.js for parsing and Highlight.js for code highlighting
 */

// Wait for the libraries to load before initializing
document.addEventListener("DOMContentLoaded", function () {
  // Initialize once libraries are loaded
  initializeMarkdownRenderer();
});

function initializeMarkdownRenderer() {
  // Check if libraries are loaded
  if (typeof marked === "undefined") {
    console.error("Marked.js is not loaded. Please include the library.");
    return;
  }

  // Configure marked options
  marked.setOptions({
    renderer: new marked.Renderer(),
    highlight: function (code, lang) {
      if (typeof hljs !== "undefined") {
        const language = hljs.getLanguage(lang) ? lang : "plaintext";
        return hljs.highlight(code, { language }).value;
      }
      return code;
    },
    langPrefix: "hljs language-", // highlight.js css expects a language-* class
    pedantic: false,
    gfm: true,
    breaks: true,
    sanitize: false,
    smartypants: false,
    xhtml: false,
  });

  // Override the original formatMarkdown function
  window.formatMarkdown = function (text) {
    if (!text) return "";
    return marked.parse(text);
  };

  // Function to extract plain text (for copying)
  window.markdownToPlainText = function (text) {
    return text; // Just return the original markdown
  };

  console.log("Markdown renderer initialized successfully");
}

// Helper function to add code copy buttons
function addCodeCopyButtons() {
  document.querySelectorAll("pre code").forEach((block) => {
    const pre = block.parentNode;

    // Skip if already has a button
    if (pre.querySelector(".code-copy-btn")) return;

    // Create button
    const button = document.createElement("button");
    button.className = "code-copy-btn";
    button.innerHTML = '<i class="fas fa-copy"></i>';
    button.title = "Copy code";

    // Add click handler
    button.addEventListener("click", function () {
      const code = block.textContent;
      navigator.clipboard.writeText(code).then(() => {
        // Show feedback
        this.innerHTML = '<i class="fas fa-check"></i>';
        setTimeout(() => {
          this.innerHTML = '<i class="fas fa-copy"></i>';
        }, 2000);
      });
    });

    // Add to pre element
    pre.appendChild(button);
  });
}

// Handle rendering of markdown in messages
function renderMarkdownMessages() {
  // Observer for new messages
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.type === "childList" && mutation.addedNodes.length) {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === 1 && node.classList.contains("message")) {
            const content = node.querySelector(".message-content");
            if (content && content.classList.contains("markdown-content")) {
              // Add copy buttons to code blocks
              setTimeout(() => {
                addCodeCopyButtons();
              }, 100);
            }
          }
        });
      }
    });
  });

  // Start observing
  observer.observe(document.querySelector(".chat-messages"), {
    childList: true,
    subtree: true,
  });
}

// Initialize once DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
  if (document.querySelector(".chat-messages")) {
    renderMarkdownMessages();
  }
});
