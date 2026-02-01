const API_URL = "http://localhost:5000/api"; // mettre l’URL de votre back Flask

// --- Auth API ---
export const loginUser = async (email, password) => {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
    credentials: "include", // pour les cookies de session
  });
  return res.json();
};

export const registerUser = async (username, email, password) => {
  const res = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password }),
    credentials: "include",
  });
  return res.json();
};

export const logoutUser = async () => {
  try {
    const res = await fetch("http://localhost:5000/api/auth/logout", {
      method: "POST",
      credentials: "include",
    });
    
    if (!res.ok) {
      console.warn("Logout request failed", res.status);
      return { error: "Not logged in" };
    }

    return res.json();
  } catch (err) {
    console.error(err);
    return { error: "Network error" };
  }
};


export const getCurrentUser = async () => {
  const res = await fetch(`${API_URL}/auth/me`, {
    method: "GET",
    credentials: "include",
  });
  return res.json();
};
