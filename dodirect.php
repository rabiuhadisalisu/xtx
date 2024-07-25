<?php

// Function to perform login and save cookies
function login() {
    $url = "https://faucetearner.org/api.php?act=login";
    $headers = [
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept: application/json, text/javascript, */*; q=0.01",
        "Accept-Language: en-US,en;q=0.5",
        "Accept-Encoding: gzip, deflate, br",
        "Content-Type: application/json",
        "X-Requested-With: XMLHttpRequest",
        "Origin: https://faucetearner.org",
        "Dnt: 1",
        "Referer: https://faucetearner.org/login.php",
        "Sec-Fetch-Dest: empty",
        "Sec-Fetch-Mode: cors",
        "Sec-Fetch-Site: same-origin",
        "Priority: u=1",
        "Te: trailers"
    ];

    $data = json_encode([
        "email" => "rhsalisu",
        "password" => "Rhs2048@"
    ]);

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_COOKIEJAR, 'cookies.txt');
    curl_setopt($ch, CURLOPT_COOKIEFILE, 'cookies.txt');

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

    if ($httpCode == 200) {
        $response_data = json_decode($response, true);
        if ($response_data["code"] == 0) {
            echo "Login successful\n";
            curl_close($ch);
            return true;
        } else {
            echo "Login failed: " . $response_data["message"] . "\n";
            curl_close($ch);
            return false;
        }
    } else {
        echo "Failed to login: HTTP " . $httpCode . " - " . $response . "\n";
        curl_close($ch);
        return false;
    }
}

// Function to perform faucet request using saved cookies
function faucet() {
    $url = "https://faucetearner.org/api.php?act=faucet";
    $headers = [
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept: application/json, text/javascript, */*; q=0.01",
        "Accept-Language: en-US,en;q=0.5",
        "Accept-Encoding: gzip, deflate, br",
        "Content-Type: application/json",
        "X-Requested-With: XMLHttpRequest",
        "Origin: https://faucetearner.org",
        "Dnt: 1",
        "Referer: https://faucetearner.org/faucet.php",
        "Sec-Fetch-Dest: empty",
        "Sec-Fetch-Mode: cors",
        "Sec-Fetch-Site: same-origin",
        "Priority: u=1",
        "Te: trailers"
    ];

    $data = json_encode([]);

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_COOKIEFILE, 'cookies.txt');

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

    if ($httpCode == 200) {
        $response_data = json_decode($response, true);
        echo "Response: " . json_encode($response_data) . "\n"; // Expose entire response message
        if ($response_data["code"] == 0) {
            $message = $response_data["message"];
            preg_match('/<span translate=\'no\' class=\'text-info fs-2\'>(.+?)<\/span>/', $message, $matches);
            $amount = $matches[1] ?? "unknown amount";
            echo "Request successful: Received $amount\n";
            curl_close($ch);
            return true;
        } elseif ($response_data["code"] == 2) {
            echo "Wave missed: " . $response_data["message"] . "\n";
            curl_close($ch);
            return false;
        }
    } else {
        echo "Failed to request: HTTP " . $httpCode . " - " . $response . "\n";
        curl_close($ch);
        return false;
    }
}

// Main loop
while (true) {
    if (!login()) {
        echo "Exiting due to failed login.\n";
        break;
    }

    while (true) {
        if (!faucet()) {
            break;
        }
        sleep(60);
    }
}
?>
