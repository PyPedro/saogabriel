import React, { useState, useRef, useEffect } from 'react';

function ChatModal({ conversation, conv_id, onClose, onSend }) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [conversation]);

  const handleSend = () => {
    if (input.trim()) {
      onSend(conv_id, input);
      setInput('');
    }
  };

  return (
    <div className="chat-modal" onClick={onClose}>
      <div className="chat-box" onClick={e => e.stopPropagation()}>
        <div className="chat-header">{conv_id}</div>
        <div className="chat-messages">
          {conversation.messages.map((msg, i) => (
            <div key={i} className={"chat-message" + (msg.from === 'operator' ? ' me' : '')}>
              {msg.body}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        <div className="chat-input">
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
            placeholder="Digite uma mensagem..."
          />
          <button onClick={handleSend}>Enviar</button>
        </div>
      </div>
    </div>
  );
}

export default ChatModal;
