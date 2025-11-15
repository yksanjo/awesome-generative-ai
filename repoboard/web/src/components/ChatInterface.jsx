import React, { useState, useRef, useEffect } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { sendMessage, getConversationHistory } from '../api'
import './ChatInterface.css'

function ChatInterface() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "👋 Hi! I'm RepoBoard AI. I can help you discover GitHub repositories!\n\nTry asking me:\n• \"Find Python libraries\"\n• \"Show me trending repos\"\n• \"What machine learning tools are there?\"\n• \"Search for React frameworks\""
    }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = input.trim()
    setInput('')
    
    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setIsLoading(true)

    try {
      // Send to API
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
      })

      const data = await response.json()
      
      // Add assistant response
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.response,
        repos: data.repos || null
      }])
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try again or use the search feature.',
        error: true
      }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>💬 Chat with RepoBoard AI</h2>
        <p>Ask me anything about GitHub repositories!</p>
      </div>

      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="message-content">
              {msg.content.split('\n').map((line, i) => (
                <p key={i}>{line}</p>
              ))}
              
              {msg.repos && msg.repos.length > 0 && (
                <div className="repo-results">
                  <h4>Found Repositories:</h4>
                  {msg.repos.map((item, i) => {
                    const repo = item.repo
                    const summary = item.summary
                    return (
                      <div key={i} className="repo-card">
                        <h5>
                          <a href={repo.url} target="_blank" rel="noopener noreferrer">
                            {repo.full_name}
                          </a>
                        </h5>
                        {summary && <p>{summary.summary}</p>}
                        <div className="repo-stats">
                          <span>⭐ {repo.stars}</span>
                          {summary && <span>{summary.category}</span>}
                        </div>
                      </div>
                    )
                  })}
                </div>
              )}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message assistant">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={handleSend}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me about repositories... (e.g., 'Find Python libraries')"
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  )
}

export default ChatInterface


