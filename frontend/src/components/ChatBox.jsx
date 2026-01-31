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
  const [mode, setMode] = useState('Text');
  
  const onSubmit = async (e) => {
    e.preventDefault();
    if (!prompt) return;

    setLoading(true);
    const currentPrompt = prompt;
    setPrompt("");

    try {
      let chatId = selectedChat?.id;

      // If no chat is selected, create a new one automatically
      if (!chatId) {
        const data = await createChat(); // call your API to create chat
        const newChat = { ...data.chat, messages: [] };
        setChats((prev) => [newChat, ...prev]);
        setSelectedChat(newChat);
        chatId = newChat.id;
      }

      // Send the message
      await sendMessage(currentPrompt, chatId);

      // Refetch messages
      const updatedMessages = await fetchMessages(chatId);
      setMessages(updatedMessages);

      // Update chat title if it's still "New Chat"
      if (selectedChat?.title === "New Chat" && updatedMessages.length > 0) {
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

  // if (!selectedChat) {
  //   return (
  //     <div className="flex-1 flex flex-col items-center justify-center text-primary">
  //       <img
  //         src={theme === "dark" ? assets.logo_full : assets.logo_full_dark}
  //         alt="logo"
  //         className="w-full max-w-56"
  //       />
  //       <p className="mt-5 text-4xl sm:text-6xl text-center text-gray-400 dark:text-white">
  //         Ask me anything.
  //       </p>
  //     </div>
  //   );
  // }

  
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
          Ask me anything.
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
    <select onChange={(e) => setMode(e.target.value)} value={mode} className='text-sm pl-3 pr-2 outline-none'>
      <option className='dark:bg-purple-900' value="Text">Text</option>
      <option className='dark:bg-purple-900' value="Image">Image</option>
    </select>

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