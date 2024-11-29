// Select elements
const chatbotIcon = document.getElementById("chatbot-icon");
const chatbotPopup = document.getElementById("chatbot-popup");
const closeChatbotButton = document.getElementById("close-chatbot");
const userMessageInput = document.getElementById("user-message");
const chatbotMessages = document.getElementById("chatbot-messages");

// Add event listener to chatbot icon
chatbotIcon.addEventListener("click", () => {
  chatbotPopup.classList.toggle("hidden");
});

// Add event listener to close button
closeChatbotButton.addEventListener("click", () => {
  chatbotPopup.classList.add("hidden");
});

// Send message to backend when user hits Enter
userMessageInput.addEventListener("keypress", async (event) => {
  if (event.key === "Enter" && userMessageInput.value.trim() !== "") {
    const userMessage = userMessageInput.value;
    displayUserMessage(userMessage);  // Display user message in the chat
    
    // Send the message to the Flask backend (API call to OpenAI)
    const response = await sendMessageToBackend(userMessage);
    
    // Display the bot response in the chat
    displayBotResponse(response);
    userMessageInput.value = "";  // Clear input after sending message
  }
});

// Function to send message to Flask backend
async function sendMessageToBackend(message) {
  try {
    const response = await fetch("http://localhost:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });
    
    const data = await response.json();
    return data.response;  // Return the chatbot's response
  } catch (error) {
    console.error("Error:", error);
    return "Lo siento, hubo un problema con la conexión.";
  }
}

// Function to display user message in the chatbot
function displayUserMessage(message) {
  const messageElement = document.createElement("div");
  messageElement.classList.add("bg-blue-600", "text-white", "p-2", "rounded-lg", "my-2", "max-w-xs");
  messageElement.textContent = message;
  chatbotMessages.appendChild(messageElement);
  chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}

// Function to display bot response in the chatbot
function displayBotResponse(response) {
  const messageElement = document.createElement("div");
  messageElement.classList.add("bg-gray-200", "text-black", "p-2", "rounded-lg", "my-2", "max-w-xs");
  messageElement.textContent = response;
  chatbotMessages.appendChild(messageElement);
  chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}
