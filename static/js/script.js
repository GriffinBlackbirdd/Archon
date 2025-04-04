// DOM Elements
document.addEventListener("DOMContentLoaded", function () {
  // Navigation elements
  const navItems = document.querySelectorAll(".navigation ul li");
  const sendBtn = document.querySelector(".send-btn");
  const chatInput = document.querySelector(".chat-input");
  const chatMessages = document.querySelector(".chat-messages");
  const toolBtns = document.querySelectorAll(".tool-btn");
  const newAnalysisBtn = document.querySelector(".btn-primary");

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

      // Add transition effect
      document.querySelector(".current-tool").classList.add("tool-change");
      setTimeout(() => {
        document.querySelector(".current-tool").classList.remove("tool-change");
      }, 500);

      // Keep "New Analysis" text consistent for all tools
      document.querySelector(".btn-primary span").textContent = "New Analysis";
    });
  });

  // Send message functionality
  sendBtn.addEventListener("click", sendMessage);
  chatInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  function sendMessage() {
    const message = chatInput.value.trim();
    if (message) {
      // Add user message to chat
      addMessage("user", message);
      // Clear input
      chatInput.value = "";
      // Simulate AI response
      setTimeout(() => {
        simulateTyping();
        setTimeout(() => {
          const currentTool =
            document.querySelector(".current-tool h1").textContent;
          let response;

          if (currentTool === "Legal Analysis") {
            response =
              "Based on my analysis, the indemnification clause as written provides inadequate protection. I recommend adding specific liability caps and clarifying the triggering conditions.";
          } else if (currentTool === "Document Review") {
            response =
              "I've reviewed the contract terms and found that several provisions may be unenforceable under state law. Let me highlight the specific sections that need revision.";
          } else if (currentTool === "Case Evaluation") {
            response =
              "Your case presents interesting challenges regarding jurisdictional issues. I'll need to reference Smith v. Johnson (2022) to provide a comprehensive assessment.";
          } else if (currentTool === "Quick Summary (Experimental)") {
            response =
              "Quick Summary: This contract contains 15 sections, with potentially problematic clauses in sections 4.2 (Indemnification), 7.3 (Limitation of Liability), and 12.1 (Term and Termination). Recommend legal review of these sections.";
          }

          addMessage("ai", response);
        }, 2000);
      }, 1000);
    }
  }

  function addMessage(type, content) {
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
      messageDiv.innerHTML = `
              <div class="message-avatar">
                  <i class="fas fa-scale-balanced"></i>
              </div>
              <div class="message-content">
                  <p>${content}</p>
              </div>
              <div class="message-time">${timeString}</div>
              <div class="message-actions">
                  <button class="action-btn"><i class="fas fa-copy"></i></button>
                  <button class="action-btn"><i class="fas fa-bookmark"></i></button>
                  <button class="action-btn"><i class="fas fa-thumbs-up"></i></button>
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

    // Remove typing indicator after response is ready
    setTimeout(() => {
      chatMessages.removeChild(typingDiv);
    }, 2000);
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

// Copy message functionality
function initCopyFunctionality() {
  document.addEventListener("click", function (e) {
    if (
      e.target.classList.contains("fa-copy") ||
      e.target.parentElement.classList.contains("fa-copy")
    ) {
      const btn = e.target.closest(".action-btn");
      const message = btn.closest(".message");
      const messageText =
        message.querySelector(".message-content p").textContent;

      // Copy to clipboard
      navigator.clipboard.writeText(messageText).then(() => {
        // Show copy feedback
        const originalClass = btn.className;
        const originalInnerHTML = btn.innerHTML;

        btn.className = "action-btn copied";
        btn.innerHTML = '<i class="fas fa-check"></i>';

        setTimeout(() => {
          btn.className = originalClass;
          btn.innerHTML = originalInnerHTML;
        }, 2000);
      });
    }
  });
}

// Add CSS animation class
document.addEventListener("DOMContentLoaded", function () {
  // Add tool-change animation to CSS
  const style = document.createElement("style");
  style.textContent = `
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

  // Add show class to existing messages
  document.querySelectorAll(".message").forEach((msg) => {
    msg.classList.add("show");
  });
});

// Function to start a new chat
function startNewChat() {
  const chatMessages = document.querySelector(".chat-messages");

  // Clear all existing messages
  chatMessages.innerHTML = "";

  // Add welcome message
  const currentTool = document.querySelector(".current-tool h1").textContent;
  let welcomeMsg = `Welcome to Archon AI ${currentTool}. How can I help you today?`;

  const messageDiv = document.createElement("div");
  messageDiv.className = "message system";

  const currentTime = new Date();
  const timeString = currentTime.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  messageDiv.innerHTML = `
      <div class="message-content">
          <p>${welcomeMsg}</p>
      </div>
      <div class="message-time">${timeString}</div>
  `;

  chatMessages.appendChild(messageDiv);

  // Add animation to new message
  setTimeout(() => {
    messageDiv.classList.add("show");
  }, 100);

  // Add slight bounce animation to the button
  const btn = document.querySelector(".btn-primary");
  btn.classList.add("btn-clicked");

  setTimeout(() => {
    btn.classList.remove("btn-clicked");
  }, 300);
}
