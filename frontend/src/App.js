import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import Board from './components/Board';
import ChatModal from './components/ChatModal';
import './styles.css';

const socket = io('http://localhost:5000');

function App() {
  const [conversations, setConversations] = useState({});
  const [activeChat, setActiveChat] = useState(null);

  useEffect(() => {
    socket.on('newMessage', data => {
      setConversations(prev => {
        const conv = prev[data.conv_id] || { messages: [], from: data.from };
        return {
          ...prev,
          [data.conv_id]: {
            ...conv,
            messages: [...conv.messages, { body: data.body, timestamp: data.timestamp, from: data.from }],
            lastMessage: data.body
          }
        };
      });
    });
    return () => socket.off('newMessage');
  }, []);

  const handleSendMessage = (conv_id, message) => {
    socket.emit('sendMessage', { conv_id, message });
    setConversations(prev => {
      const conv = prev[conv_id];
      return {
        ...prev,
        [conv_id]: {
          ...conv,
          messages: [...conv.messages, { body: message, timestamp: Date.now(), from: 'operator' }],
          lastMessage: message
        }
      };
    });
  };

  return (
    <div className="App">
      <Board conversations={conversations} setActiveChat={setActiveChat} />
      {activeChat && (
        <ChatModal
          conversation={conversations[activeChat]}
          conv_id={activeChat}
          onClose={() => setActiveChat(null)}
          onSend={handleSendMessage}
        />
      )}
    </div>
  );
}

export default App;
