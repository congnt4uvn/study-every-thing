# AWS WebSocket APIs with API Gateway

## What is WebSocket?

WebSocket is a **two-way interactive communication** protocol between a user's browser and a server. Unlike traditional HTTP, the server can push information to the client without the client making a request.

### Key Characteristics
- **Bidirectional Communication**: Server can push data to clients proactively
- **Stateful**: Maintains persistent connections
- **Real-time**: Enables instant data transfer

## Common Use Cases

WebSocket APIs are commonly used in real-time applications:
- 💬 **Chat applications**
- 🤝 **Collaboration platforms**
- 🎮 **Multiplayer games**
- 📈 **Financial trading platforms**

## WebSocket API Architecture

### Connection Lifecycle

1. **Connection Establishment**
   - Client connects to WebSocket API on API Gateway
   - Establishes a **persistent connection** (not multiple connections)
   - `onConnect` Lambda function is invoked
   - Connection ID can be stored in DynamoDB for tracking

2. **Message Sending**
   - Client sends messages over the persistent connection
   - Messages are called **frames**
   - `sendMessage` Lambda function is invoked
   - Same connection ID is maintained throughout

3. **Disconnection**
   - Client sends disconnect signal
   - `onDisconnect` Lambda function is invoked
   - Connection is terminated

### Backend Integration Options

API Gateway WebSocket can integrate with:
- ⚡ Lambda functions
- 🗄️ DynamoDB tables
- 🌐 HTTP endpoints
- Other AWS services

## WebSocket URL Structure

```
wss://{unique-id}.execute-api.{region}.amazonaws.com/{stage-name}
```

- `wss://` - Encrypted WebSocket protocol
- Unique ID assigned to your API
- Deployed to specific AWS region
- Stage name (dev, prod, etc.)

## How WebSocket Works with API Gateway

### Client to Server Communication

1. Client connects using WebSocket URL
2. Persistent connection established
3. Connection ID assigned and persisted
4. Client sends frames (messages) through the same connection
5. Lambda functions process messages
6. Connection ID remains constant during the session

### Server to Client Communication (Callback)

To send data back to clients without a request:

**Connection URL Callback Format:**
```
wss://{api-url}/@connections/{connectionId}
```

- Lambda function makes an **HTTP POST** request
- Must be signed with **IAM SigV4**
- Targets specific connection ID
- Pushes data directly to the client

## Important Concepts for Exam

- ✅ WebSocket maintains **persistent connection** (not multiple)
- ✅ Messages sent over WebSocket are called **frames**
- ✅ **Connection ID** remains constant during the session
- ✅ Three main Lambda triggers: `onConnect`, `sendMessage`, `onDisconnect`
- ✅ Server push requires **connection URL callback** with IAM SigV4
- ✅ Connection metadata typically stored in **DynamoDB**

## Typical Architecture Pattern

```
Client (Browser)
    ↕️ (persistent connection)
API Gateway (WebSocket API)
    ↕️
Lambda Functions (onConnect, sendMessage, onDisconnect)
    ↕️
DynamoDB (Connection IDs, Messages, User Metadata)
```

## Key Takeaways

1. **WebSocket = Two-way communication** with persistent connections
2. **Real-time applications** are the primary use case
3. **Connection ID** is the key identifier throughout the session
4. **Callback URL** enables server-to-client push notifications
5. **IAM SigV4 signing** required for server-initiated messages
