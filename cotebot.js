async function login() {
  const url = "https://faucetearner.org/api.php?act=login";
  const headers = { 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://faucetearner.org",
    "Dnt": "1",
    "Referer": "https://faucetearner.org/login.php",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=1",
    "Te": "trailers"
  };

  const data = JSON.stringify({
    "email": "rhsalisu", // Replace with your actual credentials
    "password": "Rhs2048@" // Replace with your actual credentials
  });

  const response = await fetch(url, {
    method: 'POST',
    headers,
    body: data,
  });

  if (!response.ok) {
    console.error("Failed to login:", response.status, response.statusText);
    return false;
  }

  const responseData = await response.json();
  if (responseData["code"] === 0) {
    console.log("Login successful");
    const cookieHeader = response.headers.get("Set-Cookie");
    await f8db3b815e7d4ac797b41c3c00bfe9e1.put("cookies", cookieHeader); // Store cookies in KV
    return true;
  } else {
    console.error("Login failed:", responseData["message"]);
    return false;
  }
}

async function faucet() {
  const url = "https://faucetearner.org/api.php?act=faucet";
  const headers = { 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://faucetearner.org",
    "Dnt": "1",
    "Referer": "https://faucetearner.org/faucet.php",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=1",
    "Te": "trailers"
  };

  const cookies = await MY_KV_NAMESPACE.get("cookies", "text");
  if (cookies) {
    headers["Cookie"] = cookies;
  } else {
    console.error("Cookies not found. Please login first.");
    return false; 
  }

  const data = JSON.stringify([]);

  const response = await fetch(url, {
    method: 'POST',
    headers,
    body: data,
  });

  if (!response.ok) {
    console.error("Failed to request:", response.status, response.statusText);
    return false;
  }

  const responseData = await response.json();
  console.log("Response:", responseData);
  
  if (responseData["code"] === 0) {
    const message = responseData["message"];
    const amountMatch = message.match(/<span translate=\'no\' class=\'text-info fs-2\'>(.+?)<\/span>/);
    const amount = amountMatch ? amountMatch[1] : "unknown amount";
    console.log(`Request successful: Received ${amount}`);
    return true;
  } else if (responseData["code"] === 2) {
    console.warn("Wave missed:", responseData["message"]);
    return false;
  } else {
    console.error("Unexpected response code:", responseData["code"]);
    return false;
  }
}

async function main() {
  while (true) {
    if (!(await login())) {
      console.error("Exiting due to failed login.");
      break;
    }
    while (true) {
      if (!(await faucet())) {
        break;
      }
      await new Promise(resolve => setTimeout(resolve, 60000)); // Sleep for 60 seconds
    }
  }
}

// Start the main loop
main().catch(console.error); // Handle errors
