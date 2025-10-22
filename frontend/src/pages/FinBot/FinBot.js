import React, { useState, useRef, useEffect } from 'react';
import { PaperPlaneIcon } from '@radix-ui/react-icons'; 
import api from '../../api'; 
import './FinBot.css';

const FinBot = () => {
  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: 'Hello! I am FinBot, your personal financial advisor. Ask me anything about your budget, spending habits, or how to save money.',
    },
  ]);

  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { sender: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Assuming your AI endpoint is at /ai/chat
      const response = await api.post('/ai/chat', { message: input });
      const botMessage = { sender: 'bot', text: response.data.reply };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {

      const errorMessage = { sender: 'bot', text: 'Sorry, I am having trouble connecting. Please try again later.' };
      setMessages((prev) => [...prev, errorMessage]);
      console.error('Error fetching AI response:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="finbot-container">
      <div className="finbot-card">
        <div className="finbot-header">
          <h3>FinBot: Your Financial Advisor</h3>
          <p>Ask for advice based on your transactions!</p>
        </div>
        <div className="chat-window">
          {messages.map((msg, index) => (
            <div key={index} className={`chat-message ${msg.sender}`}>
              <p>{msg.text}</p>
            </div>
          ))}
          {isLoading && (
            <div className="chat-message bot loading">
              <p><span>.</span><span>.</span><span>.</span></p>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        <form onSubmit={handleSend} className="chat-input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask FinBot for advice..."
            disabled={isLoading}
          />

          <button type="submit" disabled={isLoading}>
            <PaperPlaneIcon />
          </button>
        </form>
      </div>
    </div>
  );
};

export default FinBot;