// Function to create a room and capture the default daily configuration
export const fetch_create_room = async (serverUrl: string) => {
  const req = await fetch(serverUrl + "create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

  const data = await req.json();

  if (!req.ok) {
    return { error: true, detail: data.detail };
  }
  return data;
};

// Function to start the agent with the provided room URL and token
export const fetch_start_agent = async (
  roomUrl: string,
  token: string,
  serverUrl: string,
  selectedPrompt: string
) => {
  const req = await fetch(serverUrl + "start", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ room_url: roomUrl, token: token, selected_prompt: selectedPrompt }),
  });

  const data = await req.json();

  if (!req.ok) {
    return { error: true, detail: data.detail };
  }
  return data;
};
