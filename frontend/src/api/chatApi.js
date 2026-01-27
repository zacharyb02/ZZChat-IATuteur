const API_URL = "http://localhost:5000/api"; // Backend Flask

// Chats 
export const fetchChats = async () => {
  const res = await fetch(`${API_URL}/chats/`, {
    method: "GET",
    credentials: "include",
  });
  return res.json();
};

export const createChat = async () => {
  const res = await fetch("http://localhost:5000/api/chats/", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!res.ok) throw new Error("Failed to create chat");
  return res.json();
};

export const deleteChat = async (chatId) => {
  const res = await fetch(`${API_URL}/chats/${chatId}`, {
    method: "DELETE",
    credentials: "include",
  });
  return res.json();
};

// Messages
export const fetchMessages = async (chatId) => {
  const res = await fetch(`${API_URL}/chats/${chatId}/messages/`, {
    method: "GET",
    credentials: "include",
  });
  return res.json();
};

export const sendMessage = async (content, chatId) => {
  const res = await fetch(`${API_URL}/chats/${chatId}/messages/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ content }),
  });
  return res.json();
};
