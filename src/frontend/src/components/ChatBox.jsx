import React, { useEffect, useRef, useState } from 'react'
import { useAppContext } from '../context/AppContext'
import { assets } from '../assets/assets';
import Message from './Message';
import { sendMessage, fetchMessages, createChat } from "../api/chatApi";


const ChatBox = () => {
  const containerRef = useRef(null);  
  const bottomRef = useRef(null);
  

  const {selectedChat, theme, setSelectedChat, setChats} = useAppContext();
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [prompt, setPrompt] = useState('');
  
  const onSubmit = async (e) => {
    e.preventDefault();
    if (!prompt) return;

    const currentPrompt = prompt;
    setPrompt("");

    let chatId = selectedChat?.id;

    
    const userMessage = {
      id: `temp-${Date.now()}`, // temporary ID for rendering
      role: "user",
      content: currentPrompt,
    };
    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);

    try {
      // If no chat exists, create one
      if (!chatId) {
        const data = await createChat();
        const newChat = { ...data.chat, messages: [userMessage] };
        setChats((prev) => [newChat, ...prev]);
        setSelectedChat(newChat);
        chatId = newChat.id;
      }

      // Send message to backend
      const response = await sendMessage(currentPrompt, chatId);

      // Append AI response
      const aiMessage = response.messages.find((m) => m.role === "assistant");
      if (aiMessage) {
        setMessages((prev) => [...prev, aiMessage]);
      }

      // Update chat title if it's still "New Chat"
      if (selectedChat?.title === "New Chat") {
        const newTitle = currentPrompt.split(" ").slice(0, 5).join(" ");
        setSelectedChat((prev) => ({ ...prev, title: newTitle }));
        setChats((prev) =>
          prev.map((chat) =>
            chat.id === chatId ? { ...chat, title: newTitle } : chat
          )
        );
      }

    } catch (err) {
      console.error(err);
      setMessages((prev) => prev.filter((m) => m.id !== userMessage.id));
    } finally {
      setLoading(false);
    }
  };


  useEffect(() => {
    if (!selectedChat?.id) {
      setMessages([]);
      return;
    }

    const loadMessages = async () => {
      const msgs = await fetchMessages(selectedChat.id);
      setMessages(msgs);
    };

    loadMessages();
  }, [selectedChat?.id])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);
  
  return (
    <div className='flex-1 flex flex-col justify-between m-5 md:m-10 xl-pr-40'>
      {/* Chat messages / placeholder */}
      <div ref={containerRef} className='flex-1 mb-5 overflow-y-scroll'>
        {selectedChat && messages.length > 0 ? (
          messages.map((message, index) => <Message key={index} message={message} />)
        ) : (
          <div className='flex-1 flex flex-col items-center justify-center gap-2 text-primary'>
            <img
              src={theme === "dark" ? assets.logo_full : assets.logo_full_dark}
              alt="logo"
              className="w-full max-w-56 sm:max-w-68"
            />
            <p className='mt-5 text-4xl sm:text-6xl text-center text-gray-400 dark:text-white'>
              Ask me anything about CNN.
            </p>
          </div>
        )}
        <div ref={bottomRef} />

        {loading && <div className='loader flex items-center gap-1.5'>
            <div className='w-1.5 h-1.5 rounded-full bg-gray-500 dark:bg-white animate-bounce'></div>
            <div className='w-1.5 h-1.5 rounded-full bg-gray-500 dark:bg-white animate-bounce'></div>
            <div className='w-1.5 h-1.5 rounded-full bg-gray-500 dark:bg-white animate-bounce'></div>
          </div>}
      </div>

      {/* Prompt input box — always visible */}
      <form onSubmit={onSubmit} className='flex gap-4 items-center w-full border rounded-full border-primary dark:border-[#80609F]/30 max-w-2xl pl-4 mx-auto'>
        <input 
          onChange={(e) => setPrompt(e.target.value)}
          value={prompt}
          type="text"
          placeholder="How can I help you ..."
          className="flex-1 w-full text-sm outline-none"
        />

        <button disabled={loading}>
          <img src={loading ? assets.stop_icon : assets.send_icon} alt="prompt" className='cursor-pointer w-8 m-2'/>
        </button>
      </form>
    </div>
  )
}

export default ChatBox