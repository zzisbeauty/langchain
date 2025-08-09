import time
timestamp = str(int(time.time() * 1000))

import hashlib

def generate_authentication(username: str, timestamp: str) -> str:
    # 第一步：生成盐值
    salt_input = f"{username}{timestamp}"
    salt = hashlib.sha256(salt_input.encode('utf-8')).hexdigest()

    # 第二步：生成 Authentication
    auth_input = f"{username}{timestamp}{salt}"
    authentication = hashlib.sha256(auth_input.encode('utf-8')).hexdigest()

    return authentication

# 示例
username = "fanzhimin10-41"
username = "Y0126"
timestamp = timestamp
auth_token = generate_authentication(username, timestamp)

print("Authentication:", auth_token)



"""
// java key generate
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public static void main(String[] args) {
    try {
        long timestamp = System.currentTimeMillis();
        String userName = "test_user";
        String salt= encryptToSHA256(userName + timestamp );
        String tmpToken = Sha256Util.encryptToSHA256(userName + timestamp + salt);
        System.out.println("Authentication: " + tmpToken);
        System.out.println("Timestamp: " + timestamp);
        System.out.println("UserName: " + userName);
    } catch (Throwable e) {
        e.printStackTrace();
    }
}

public static String encryptToSHA256(String message) throws NoSuchAlgorithmException{
    MessageDigest digest = MessageDigest.getInstance("SHA-256");
    byte[] encodedhash = digest.digest(message.getBytes(StandardCharsets.UTF_8));
    StringBuilder hexString = new StringBuilder(2 * encodedhash.length);
    for (byte b : encodedhash) {
        String hex = Integer.toHexString(0xff & b);
        if(hex.length() == 1) hexString.append('0');
        hexString.append(hex);
    }
     return hexString.toString();
}
"""



# requests function - start requests
import requests

def call_workflow_api(auth_key: str, timestamp: str, authentication: str):
    url = "http://ailma.ai-test.xiangyuniot.com/ailma-gw/ailma-workflow/v1/workflows/run"

    headers = {
        "username": "H06529", # Y0126
        "timestamp": timestamp,
        "authentication": authentication,
        "Api-Key": "Bearer app-aj1uW0EZVQRJAyGt3F3bX8Qd",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": {"query": "支付途径"},
        "response_mode": "blocking",
        "user": "H06529"
    }

    response = requests.post(url, json=payload, headers=headers)

    try:
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e), "response": response.text}


auth_key = "Bearer app-aj1uW0EZVQRJAyGt3F3bX8Qd"
# timestamp = "YOUR_TIMESTAMP_HERE"
# authentication = "YOUR_AUTHENTICATION_HERE"

result = call_workflow_api(auth_key, timestamp, auth_token)
print(result)
