import React from 'react'
import { useAppContext } from '../context/AppContext'
import { assets } from '../assets/assets';
import { useState } from 'react';
import moment from 'moment'; 
import { logoutUser } from '../api/userApi';
import { createChat, fetchMessages, deleteChat } from "../api/chatApi";
import { useNavigate } from 'react-router-dom';

const SideBar = () => {

  const {chats, selectedChat, setSelectedChat, theme, setTheme, user, setUser, navigate, setChats} = useAppContext();

  const [search, setSearch] = useState('');

  return (
    <div className='flex flex-col h-screen min-w-72 p-5 dark:bg-linear-to-b from-[#242124]/30 to-[#000000]/30 border-r border-[#80609F]/30 backdrop-blur-3xl transition-all duration-500 
    max-md:absolute left-0 z-1 '>
        {/* Logo */}
        <img onClick={() => navigate("/")} src={theme === 'dark' ? assets.logo_full : assets.logo_full_dark} alt="logo" className='cursor-pointer w-full max-w-48'/>
        
        {/* <button
          className='flex justify-center items-center w-full cursor-pointer py-2 mt-10 text-white bg-linear-to-r from-[#242a81] to-[#204AC2] text-sm border border-gray-400/30 rounded-md'
          onClick={async () => {
            try {
              const data = await createChat();

              const newChat = {
                ...data.chat,
                messages: []
              };

              setChats((prev) => [newChat, ...prev]);
              setSelectedChat(newChat);
            } catch (err) {
              console.error(err);
            }
          }}
        >
          <span className='mr-2 text-xl'>+</span> New Chat
        </button>
        {/* New Chat Button */}
        <button
          className="flex justify-center items-center w-full cursor-pointer py-2 mt-10 text-white bg-linear-to-r from-[#242a81] to-[#204AC2] text-sm border border-gray-400/30 rounded-md"
          onClick={async () => {
            try {
              const data = await createChat(); // normal backend call

              const newChat = {
                ...data.chat,
                messages: [],
                type: "chat", // normal chat
              };

              setChats((prev) => [newChat, ...prev]);
              setSelectedChat(newChat);
            } catch (err) {
              console.error(err);
            }
          }}
        >
          <span className="mr-2 text-xl">+</span> New Chat
        </button>

        {/* Image Classification Chat Button */}
        <button
          className="flex justify-center items-center w-full cursor-pointer py-2 mt-4 text-white bg-linear-to-r from-[#242a81] to-[#204AC2] text-sm border border-gray-400/30 rounded-md"
          onClick={() => {
            const newClassificationChat = {
              id: `classification-${Date.now()}`, // temporary ID
              title: "Image Classification",
              messages: [],
              type: "classification", // mark as image classification
            };

            setChats((prev) => [newClassificationChat, ...prev]);
            setSelectedChat(newClassificationChat);

            navigate("/classification");
          }}
        >
          <span className="mr-2 text-xl">🖼️</span> Image Classification
        </button>

        {/* Search Conversations */}
        <div className='flex items-center gap-2 p-3 mt-4 border border-gray-400 dark:border-white/20 rounded-md'>
          <img src={assets.search_icon} alt="search" className='w-4 not-dark:invert'/>
          <input onChange={(e) => {setSearch(e.target.value)}} value={search} type="text" placeholder='Search conversations ...' className='text-xs placeholder:text-gray-400 outline-none'/>
        </div> 

        {/* Recent chats */}
        {chats.length > 0 && <p className='mt-4 text-sm'>Recent chats</p>}
        <div className='flex-1 overflow-y-scroll mt-3 text-sm space-y-3'>
          {chats.map((chat) => (
            <div
              key={chat.id}
              className='p-1 px-4 border border-gray-300 rounded-md dark:border-[#80609F]/15 cursor-pointer flex justify-between group hover:bg-gray-100 hover:dark:bg-gray-900'
            >
              <div onClick={async () => {
                // Charger les messages du chat
                const messages = await fetchMessages(chat.id);
                setSelectedChat({ ...chat, messages });
                navigate("/");
              }}>
                <p className='truncate w-full'>{chat.title}</p>
                <p className='text-xs text-gray-400 dark:text-[#B1A6C0]'>
                  {chat.updated_at ? new Date(chat.updated_at).toLocaleString() : ""}
                </p>
              </div>

              <img 
                src={assets.bin_icon} 
                alt="bin" 
                className='w-4 hidden group-hover:block cursor-pointer not-dark:invert'
                onClick={async () => {
                  await deleteChat(chat.id);
                  setChats((prev) => prev.filter(c => c.id !== chat.id));
                  if (selectedChat?.id === chat.id) setSelectedChat(null);
                }}
              />
            </div>
          ))}
        </div>

        {/* Dark mode toggle */}
        <div className='flex items-center justify-between gap-2 p-2 mt-4 border border-gray-300 dark:border-white/15 rounded-md'>
          <div className='flex items-center gap-2 text-sm'>
            <img src={assets.theme_icon} alt="theme" className='not-dark:invert w-4' />
            <p>Dark Mode</p>
          </div>

          <label className='relative inline-flex cursor-pointer'>
            <input onChange={() => setTheme(theme==='dark' ? 'light' : 'dark')}
             type="checkbox" className='sr-only peer' checked={theme === 'dark'}
            />

            <div className='w-9 h-5 bg-gray-400 rounded-full peer-checked:bg-[#1E257D] transition-all'></div>
            <span className='absolute left-1 top-1 w-3 h-3 bg-white rounded-full transition-all peer-checked:translate-x-4 '></span>
          </label>
        </div>

        {/* User Account */}
        <div className='flex items-center justify-between mt-4 gap-3 p-2 border border-gray-300 rounded-md dark:border-white/15 group cursor-pointer'>
          <img src={assets.user_icon} alt="userIcon" className='w-8 rounded-full' />
          <p className='flex-1 text-sm truncate dark:text-primary'>{user ? user.username : 'Login to your account'}</p>
        
          {user && (
            <img 
              src={assets.logout_icon} 
              alt="logout" 
              className='h-5 hidden group-hover:block cursor-pointer not-dark:invert'
              onClick={async () => {
                try {
                  const data = await logoutUser();
                  if (data.message) {
                    setUser(null);
                    navigate("/login");
                  } else if (data.error) {
                    console.error(data.error);
                    alert("Logout failed");
                  }
                } catch (err) {
                  console.error(err);
                  alert("Logout failed");
                }
              }}
            />
          )}

        </div>

    </div>
  )
}

export default SideBar