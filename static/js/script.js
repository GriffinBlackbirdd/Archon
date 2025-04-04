// DOM Elements
document.addEventListener("DOMContentLoaded", function () {
  // Navigation elements
  const navItems = document.querySelectorAll(".navigation ul li");
  const sendBtn = document.querySelector(".send-btn");
  const chatInput = document.querySelector(".chat-input");
  const chatMessages = document.querySelector(".chat-messages");
  const toolBtns = document.querySelectorAll(".tool-btn");
  const newAnalysisBtn = document.querySelector(".btn-primary");
  const attachBtn = document.querySelector(".tool-btn:nth-child(1)"); // Paperclip button
  const exportBtn = document.querySelector(".btn-secondary"); // Export button

  // File upload elements
  let fileInput = document.createElement("input");
  fileInput.type = "file";
  fileInput.multiple = true;
  fileInput.style.display = "none";
  fileInput.accept = ".pdf,.doc,.docx,.txt";
  document.body.appendChild(fileInput);

  // Create file display area above input bar
  let fileDisplayArea = document.createElement("div");
  fileDisplayArea.className = "file-display-area";
  document.querySelector(".chat-input-wrapper").before(fileDisplayArea);

  // Track selected files
  let selectedFiles = [];

  // Current active tool
  let currentTool = "Legal Analysis";

  // Navigation functionality
  navItems.forEach((item) => {
    item.addEventListener("click", function () {
      // Remove active class from all items
      navItems.forEach((nav) => nav.classList.remove("active"));
      // Add active class to clicked item
      this.classList.add("active");

      // Update header title and icon
      const toolName = this.querySelector("span").textContent;
      const toolIcon = this.querySelector("i").className;
      document.querySelector(".current-tool h1").textContent = toolName;
      document.querySelector(".current-tool i").className = toolIcon;

      // Update current tool
      currentTool = toolName;

      // Add transition effect
      document.querySelector(".current-tool").classList.add("tool-change");
      setTimeout(() => {
        document.querySelector(".current-tool").classList.remove("tool-change");
      }, 500);

      // Keep "New Analysis" text consistent for all tools
      document.querySelector(".btn-primary span").textContent = "New Analysis";

      // Start a new chat with the selected tool
      startNewChat();
    });
  });

  // File attachment button
  attachBtn.addEventListener("click", function () {
    fileInput.click();
  });

  // File input change handler
  fileInput.addEventListener("change", function (e) {
    selectedFiles = Array.from(e.target.files);

    if (selectedFiles.length > 0) {
      // Update file display area
      updateFileDisplay();

      // Add visual indication that files are selected
      attachBtn.classList.add("active-attachment");
      attachBtn.setAttribute("title", `${selectedFiles.length} files selected`);
    }
  });

  // Function to update file display
  function updateFileDisplay() {
    const fileDisplayArea = document.querySelector(".file-display-area");
    fileDisplayArea.innerHTML = "";

    if (selectedFiles.length === 0) {
      fileDisplayArea.style.display = "none";
      return;
    }

    fileDisplayArea.style.display = "flex";

    selectedFiles.forEach((file, index) => {
      const fileItem = document.createElement("div");
      fileItem.className = "file-item";

      // Determine file icon based on type
      let fileIcon = "fa-file";
      if (file.name.endsWith(".pdf")) {
        fileIcon = "fa-file-pdf";
      } else if (file.name.endsWith(".doc") || file.name.endsWith(".docx")) {
        fileIcon = "fa-file-word";
      } else if (file.name.endsWith(".txt")) {
        fileIcon = "fa-file-lines";
      }

      fileItem.innerHTML = `
        <i class="fas ${fileIcon}"></i>
        <span class="file-name">${file.name}</span>
        <button class="file-remove" data-index="${index}">
          <i class="fas fa-times"></i>
        </button>
      `;

      fileDisplayArea.appendChild(fileItem);
    });

    // Add event listeners to remove buttons
    document.querySelectorAll(".file-remove").forEach((btn) => {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        const index = parseInt(this.getAttribute("data-index"));
        removeFile(index);
      });
    });
  }

  // Function to remove a file
  function removeFile(index) {
    selectedFiles = selectedFiles.filter((_, i) => i !== index);
    updateFileDisplay();

    if (selectedFiles.length === 0) {
      // Remove visual indication
      attachBtn.classList.remove("active-attachment");
      attachBtn.removeAttribute("title");
    } else {
      // Update title
      attachBtn.setAttribute("title", `${selectedFiles.length} files selected`);
    }
  }

  // Export button functionality
  exportBtn.addEventListener("click", function () {
    exportChatHistory();
  });

  // Send message functionality
  sendBtn.addEventListener("click", sendMessage);
  chatInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message && selectedFiles.length === 0) return;

    // Add user message to chat
    addMessage("user", message);

    // Clear input
    chatInput.value = "";

    // Start typing indicator
    simulateTyping();

    try {
      let response;

      // If we have files, use the upload endpoint
      if (selectedFiles.length > 0) {
        const formData = new FormData();
        formData.append("message", message);
        formData.append("tool", currentTool);

        selectedFiles.forEach((file) => {
          formData.append("files", file);
        });

        // Send request to upload endpoint
        const uploadResponse = await fetch("/api/upload", {
          method: "POST",
          body: formData,
        });

        if (!uploadResponse.ok) {
          throw new Error(`Upload failed: ${uploadResponse.status}`);
        }

        response = await uploadResponse.json();

        // Clear selected files after uploading
        selectedFiles = [];
        fileInput.value = "";
        attachBtn.classList.remove("active-attachment");
        attachBtn.removeAttribute("title");
        updateFileDisplay();
      }
      // Otherwise use the regular chat endpoint
      else {
        const chatResponse = await fetch("/api/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: message,
            tool: currentTool,
          }),
        });

        if (!chatResponse.ok) {
          throw new Error(`Chat request failed: ${chatResponse.status}`);
        }

        response = await chatResponse.json();
      }

      // Remove typing indicator
      const typingElement = document.querySelector(".message.ai.typing");
      if (typingElement) {
        chatMessages.removeChild(typingElement);
      }

      // Display the response
      addMessage("ai", response.response);
    } catch (error) {
      console.error("Error:", error);

      // Remove typing indicator
      const typingElement = document.querySelector(".message.ai.typing");
      if (typingElement) {
        chatMessages.removeChild(typingElement);
      }

      // Display error message
      addMessage("system", `An error occurred: ${error.message}`);
    }
  }

  function addMessage(type, content) {
    if (!content) content = "";

    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${type}`;

    const currentTime = new Date();
    const timeString = currentTime.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    if (type === "user") {
      messageDiv.innerHTML = `
              <div class="message-content">
                  <p>${content}</p>
              </div>
              <div class="message-time">${timeString}</div>
          `;
    } else if (type === "ai") {
      // Store original content for copying
      messageDiv.dataset.originalContent = content;

      // Convert markdown to HTML using the marked library
      const formattedContent = window.marked ? marked.parse(content) : content;

      messageDiv.innerHTML = `
              <div class="message-avatar">
                  <i class="fas fa-scale-balanced"></i>
              </div>
              <div class="message-content prose prose-invert">
                  ${formattedContent}
              </div>
              <div class="message-time">${timeString}</div>
              <div class="message-actions">
                  <button class="action-btn" title="Copy to clipboard"><i class="fas fa-copy"></i></button>
              </div>
          `;
    } else if (type === "system") {
      messageDiv.innerHTML = `
              <div class="message-content">
                  <p>${content}</p>
              </div>
              <div class="message-time">${timeString}</div>
          `;
    }

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Add animation to new message
    setTimeout(() => {
      messageDiv.classList.add("show");
    }, 100);
  }

  function simulateTyping() {
    const typingDiv = document.createElement("div");
    typingDiv.className = "message ai typing";
    typingDiv.innerHTML = `
          <div class="message-avatar">
              <i class="fas fa-scale-balanced"></i>
          </div>
          <div class="message-content">
              <div class="message-typing">
                  <div class="dot"></div>
                  <div class="dot"></div>
                  <div class="dot"></div>
              </div>
          </div>
      `;

    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // Tool buttons hover effect
  toolBtns.forEach((btn) => {
    btn.addEventListener("mouseenter", function () {
      this.querySelector("i").classList.add("fa-bounce");
    });

    btn.addEventListener("mouseleave", function () {
      this.querySelector("i").classList.remove("fa-bounce");
    });
  });

  // New Analysis button functionality
  newAnalysisBtn.addEventListener("click", startNewChat);

  // Create animated background with floating elements
  createAnimatedBackground();

  // Initialize copy functionality
  initCopyFunctionality();

  // Export chat history functionality
  function exportChatHistory() {
    // Get all messages
    const messages = document.querySelectorAll(".message");
    let exportText = `# Archon AI Legal Assistant Chat - ${currentTool}\n`;
    exportText += `Exported on: ${new Date().toLocaleString()}\n\n`;

    messages.forEach((message) => {
      const time = message.querySelector(".message-time").textContent;
      let content = "";

      // Check if we have the original content stored for AI messages
      if (message.classList.contains("ai") && message.dataset.originalContent) {
        content = message.dataset.originalContent;
      } else {
        // Extract text content from regular messages
        const contentElement = message.querySelector(".message-content");
        content = contentElement.innerText || contentElement.textContent;
      }

      if (message.classList.contains("user")) {
        exportText += `[User] ${time}\n${content}\n\n`;
      } else if (message.classList.contains("ai")) {
        exportText += `[Archon AI] ${time}\n${content}\n\n`;
      } else if (message.classList.contains("system")) {
        exportText += `[System] ${time}\n${content}\n\n`;
      }
    });

    // Create and download file
    const blob = new Blob([exportText], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `archon-ai-chat-${new Date().toISOString().slice(0, 10)}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  // Add show class to existing messages
  document.querySelectorAll(".message").forEach((msg) => {
    msg.classList.add("show");
  });

  // Clear default conversation when page loads
  window.addEventListener("load", function () {
    startNewChat();
  });
});

function createAnimatedBackground() {
  const background = document.querySelector(".background");

  // Add floating elements for the background
  for (let i = 0; i < 10; i++) {
    const floatingElement = document.createElement("div");
    floatingElement.className = "floating-element";

    // Set random size, position, and animation
    const size = Math.random() * 300 + 100;
    const posX = Math.random() * window.innerWidth;
    const posY = Math.random() * window.innerHeight;
    const animDuration = Math.random() * 15 + 15;
    const animDelay = Math.random() * 5;
    const blurAmount = Math.random() * 50 + 30;
    const opacity = Math.random() * 0.05 + 0.02;

    // Create a gradient shape
    floatingElement.style.width = `${size}px`;
    floatingElement.style.height = `${size}px`;
    floatingElement.style.borderRadius = "50%";
    floatingElement.style.position = "absolute";
    floatingElement.style.left = `${posX}px`;
    floatingElement.style.top = `${posY}px`;
    floatingElement.style.background =
      Math.random() > 0.5
        ? "radial-gradient(circle, rgba(0, 229, 255, 0.3), rgba(0, 229, 255, 0) 70%)"
        : "radial-gradient(circle, rgba(114, 9, 183, 0.3), rgba(114, 9, 183, 0) 70%)";
    floatingElement.style.filter = `blur(${blurAmount}px)`;
    floatingElement.style.opacity = opacity;
    floatingElement.style.animation = `floatAnimation ${animDuration}s infinite ease-in-out ${animDelay}s`;

    background.appendChild(floatingElement);
  }
}

// Simple copy functionality
function initCopyFunctionality() {
  document.addEventListener("click", function (e) {
    if (
      e.target.classList.contains("fa-copy") ||
      e.target.parentElement.classList.contains("fa-copy")
    ) {
      const btn = e.target.closest(".action-btn");
      const message = btn.closest(".message");

      // Get the original content if available
      let textToCopy = "";

      if (message.dataset.originalContent) {
        // If we have the original markdown content, use it directly
        textToCopy = message.dataset.originalContent;
      } else {
        // Fallback to the rendered content
        const messageContent = message.querySelector(".message-content");
        textToCopy = messageContent.innerText || messageContent.textContent;
      }

      // Copy to clipboard
      navigator.clipboard
        .writeText(textToCopy.trim())
        .then(() => {
          // Show copy feedback
          const originalClass = btn.className;
          const originalInnerHTML = btn.innerHTML;

          btn.className = "action-btn copied";
          btn.innerHTML = '<i class="fas fa-check"></i>';

          setTimeout(() => {
            btn.className = originalClass;
            btn.innerHTML = originalInnerHTML;
          }, 2000);

          // Show a toast notification
          showToast("Content copied to clipboard");
        })
        .catch((err) => {
          console.error("Error copying text:", err);
          showToast("Failed to copy to clipboard", "error");
        });
    }
  });
}

// Toast notification system
function showToast(message, type = "success") {
  // Create toast container if it doesn't exist
  let toastContainer = document.querySelector(".toast-container");
  if (!toastContainer) {
    toastContainer = document.createElement("div");
    toastContainer.className = "toast-container";
    document.body.appendChild(toastContainer);
  }

  // Create toast
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;

  // Add to container
  toastContainer.appendChild(toast);

  // Animate
  setTimeout(() => {
    toast.classList.add("show");
  }, 10);

  // Remove after delay
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => {
      toastContainer.removeChild(toast);
    }, 300);
  }, 3000);
}

// Function to start a new chat
function startNewChat() {
  const chatMessages = document.querySelector(".chat-messages");

  // Clear all existing messages
  chatMessages.innerHTML = "";

  // Add slight bounce animation to the button
  const btn = document.querySelector(".btn-primary");
  btn.classList.add("btn-clicked");

  setTimeout(() => {
    btn.classList.remove("btn-clicked");
  }, 300);

  // Clear any selected files
  const fileInput = document.querySelector('input[type="file"]');
  if (fileInput) {
    fileInput.value = "";
  }

  // Reset attachment button
  const attachBtn = document.querySelector(".tool-btn:nth-child(1)");
  if (attachBtn) {
    attachBtn.classList.remove("active-attachment");
    attachBtn.removeAttribute("title");
  }

  // Clear selected files and update display
  selectedFiles = [];
  updateFileDisplay();
}

// Add CSS for file display and animations
document.addEventListener("DOMContentLoaded", function () {
  // Add styles for file display
  const style = document.createElement("style");
  style.textContent = `
    /* File display area */
    .file-display-area {
      display: none;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 10px;
      max-width: 100%;
      overflow-x: auto;
      padding: 5px 0;
    }

    .file-item {
      display: flex;
      align-items: center;
      padding: 6px 10px;
      background-color: rgba(0, 229, 255, 0.1);
      border-radius: 8px;
      border: 1px solid rgba(0, 229, 255, 0.2);
      max-width: 250px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .file-item i {
      color: var(--primary-neon);
      margin-right: 8px;
      font-size: 14px;
    }

    .file-item .file-name {
      font-size: 12px;
      color: var(--text-secondary);
      margin-right: 8px;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .file-item .file-remove {
      background: none;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      transition: color 0.2s ease;
      padding: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-left: auto;
    }

    .file-item .file-remove:hover {
      color: var(--primary-neon);
    }

    /* Chat input container modifications for file display */
    .chat-input-container {
      display: flex;
      flex-direction: column;
    }

    .chat-input-wrapper {
      position: relative;
    }

    /* Tool button active state for file attachment */
    .tool-btn.active-attachment {
      background-color: rgba(0, 229, 255, 0.2);
      color: var(--primary-neon);
      box-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
    }

    /* Toast notifications */
    .toast-container {
      position: fixed;
      bottom: 20px;
      right: 20px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 10px;
    }

    .toast {
      padding: 10px 20px;
      border-radius: 8px;
      color: var(--text-primary);
      font-size: 14px;
      opacity: 0;
      transform: translateY(20px);
      transition: all 0.3s ease;
      max-width: 300px;
    }

    .toast.show {
      opacity: 1;
      transform: translateY(0);
    }

    .toast.success {
      background-color: rgba(0, 229, 255, 0.2);
      border-left: 3px solid var(--primary-neon);
    }

    .toast.error {
      background-color: rgba(255, 50, 50, 0.2);
      border-left: 3px solid #ff5050;
    }

    /* Custom prose fixes for our dark theme */
    .prose {
      max-width: 100% !important; /* Override the default max-width */
      color: var(--text-primary) !important;
    }

    .prose code {
      font-family: 'Courier New', monospace !important;
    }

    /* Animations */
    .tool-change {
      animation: toolChange 0.5s ease-in-out;
    }

    @keyframes toolChange {
      0% {
        opacity: 0.5;
        transform: translateY(-10px);
      }
      100% {
        opacity: 1;
        transform: translateY(0);
      }
    }

    .message {
      opacity: 0;
      transform: translateY(20px);
      transition: opacity 0.3s ease, transform 0.3s ease;
    }

    .message.show {
      opacity: 1;
      transform: translateY(0);
    }

    .btn-clicked {
      animation: btnClick 0.3s ease;
    }

    @keyframes btnClick {
      0% {
        transform: scale(1);
      }
      50% {
        transform: scale(0.95);
      }
      100% {
        transform: scale(1);
      }
    }
  `;
  document.head.appendChild(style);
});
