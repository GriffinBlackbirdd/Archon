// DOM Elements
document.addEventListener("DOMContentLoaded", function () {
  // Navigation elements
  const navItems = document.querySelectorAll(".navigation ul li");
  const rightPanel = document.querySelector(".right-panel");
  const panelCloseBtn = document.querySelector(".panel-close");
  const sendBtn = document.querySelector(".send-btn");
  const chatInput = document.querySelector(".chat-input");
  const chatMessages = document.querySelector(".chat-messages");
  const toolCards = document.querySelectorAll(".tool-card");

  // Navigation functionality
  navItems.forEach((item) => {
    item.addEventListener("click", function () {
      // Remove active class from all items
      navItems.forEach((nav) => nav.classList.remove("active"));
      // Add active class to clicked item
      this.classList.add("active");

      // Update header title
      const toolName = this.querySelector("span").textContent;
      const toolIcon = this.querySelector("i").className;
      document.querySelector(".current-tool h1").textContent = toolName;
      document.querySelector(".current-tool i").className = toolIcon;
    });
  });

  // Right panel toggle
  panelCloseBtn.addEventListener("click", function () {
    rightPanel.classList.toggle("active");
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
      // Simulate AI response (in a real app, this would be an API call)
      setTimeout(() => {
        simulateTyping();
        setTimeout(() => {
          const responses = [
            "Based on my analysis, the indemnification clause as written provides inadequate protection. I recommend adding specific liability caps and clarifying the triggering conditions.",
            "I've reviewed the contract terms and found that several provisions may be unenforceable under state law. Let me highlight the specific sections that need revision.",
            "Your case presents interesting challenges regarding jurisdictional issues. I'll need to reference Smith v. Johnson (2022) to provide a comprehensive assessment.",
          ];
          const randomResponse =
            responses[Math.floor(Math.random() * responses.length)];
          addMessage("ai", randomResponse);
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
    }

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
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

  // Tool cards functionality
  toolCards.forEach((card) => {
    card.addEventListener("click", function () {
      // In a real app, this would trigger specific tool functionality
      const toolName = this.querySelector("span").textContent;
      addMessage("system", `Launching ${toolName} tool...`);

      // Simulate tool response
      setTimeout(() => {
        if (toolName === "Risk Assessment") {
          addMessage(
            "ai",
            "Risk Assessment complete. The indemnification clause has a risk score of 7.8/10 (High Risk). Primary concerns: unlimited liability, no carve-outs for indirect damages, and lack of proportionality requirements."
          );
        } else if (toolName === "Draft Amendment") {
          addMessage(
            "ai",
            'Amendment Draft Generated: "The Indemnifying Party shall indemnify and hold harmless the Indemnified Party from and against any and all direct damages, liabilities, costs, and expenses arising from the Indemnifying Party\'s breach of this Agreement, provided that such liability shall be capped at the total value of fees paid under this Agreement."'
          );
        } else {
          addMessage(
            "ai",
            `${toolName} analysis complete. I've identified 3 key relationships and dependencies in this contract structure. Would you like me to elaborate on any specific aspect?`
          );
        }
      }, 2000);
    });
  });

  // Animated Background with Square Net
  createAnimatedBackground();
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

  // Add floating element animation to the stylesheet
  const style = document.createElement("style");
  style.textContent = `
      @keyframes floatAnimation {
          0%, 100% {
              transform: translate(0, 0) rotate(0deg);
          }
          25% {
              transform: translate(50px, 50px) rotate(5deg);
          }
          50% {
              transform: translate(0, 100px) rotate(10deg);
          }
          75% {
              transform: translate(-50px, 50px) rotate(5deg);
          }
      }
  `;
  document.head.appendChild(style);
}

// Copy message functionality
document.addEventListener("click", function (e) {
  if (
    e.target.classList.contains("fa-copy") ||
    e.target.parentElement.classList.contains("fa-copy")
  ) {
    const btn = e.target.closest(".action-btn");
    const message = btn.closest(".message");
    const messageText = message.querySelector(".message-content p").textContent;

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
