import React, { useEffect, useRef, useState } from "react";
import { useAppContext } from "../context/AppContext";
import Message from "./Message";
import { assets } from "../assets/assets";
import { classifyImage } from "../api/chatApi";

const Classification = () => {
  const bottomRef = useRef(null);
  const { theme } = useAppContext();
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [imageFile, setImageFile] = useState(null);
  const [dragOver, setDragOver] = useState(false);

  // Scroll to bottom when messages change
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleFiles = (files) => {
    if (files && files[0]) setImageFile(files[0]);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    handleFiles(e.dataTransfer.files);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!imageFile) return;

    const imageUrl = URL.createObjectURL(imageFile);

    // Show user image
    setMessages((prev) => [
      ...prev,
      { id: Date.now(), role: "user", content: imageUrl, isImage: true },
    ]);

    setLoading(true);

    try {
      const res = await classifyImage(imageFile);

      // Show classification result
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          role: "assistant",
          content: `${res.label} (${res.confidence.toFixed(2)}%)`,
          isImage: false,
        },
      ]);
    } finally {
      setLoading(false);
      setImageFile(null);
    }
  };

  return (
    <div className="flex-1 flex flex-col justify-between m-5 md:m-10 xl-pr-40">
      {/* Chat messages */}
      <div className="flex-1 mb-5 overflow-y-scroll">
        {messages.length > 0 ? (
          messages.map((msg) => <Message key={msg.id} message={msg} />)
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center gap-2 text-primary">
            <img
              src={theme === "dark" ? assets.logo_full : assets.logo_full_dark}
              alt="logo"
              className="w-full max-w-56 sm:max-w-68"
            />
            <p className="mt-5 text-4xl sm:text-6xl text-center text-gray-400 dark:text-white">
              Upload an image here to classify.
            </p>
          </div>
        )}
        <div ref={bottomRef} />
        {loading && (
          <div className="loader flex items-center gap-1.5">
            <div className="w-1.5 h-1.5 rounded-full bg-gray-500 dark:bg-white animate-bounce"></div>
            <div className="w-1.5 h-1.5 rounded-full bg-gray-500 dark:bg-white animate-bounce"></div>
            <div className="w-1.5 h-1.5 rounded-full bg-gray-500 dark:bg-white animate-bounce"></div>
          </div>
        )}
      </div>

      {/* Drag & drop / file input */}
      <form
        onSubmit={handleSubmit}
        className="flex gap-4 items-center w-full border rounded-full border-primary dark:border-[#80609F]/30 max-w-2xl pl-4 mx-auto transition-all"
      >
        <input
          type="file"
          accept="image/*"
          onChange={(e) => handleFiles(e.target.files)}
          className="flex-1 cursor-pointer w-full text-sm outline-none"
        />
        <button disabled={loading || !imageFile}>
          <img
            src={loading ? assets.stop_icon : assets.send_icon}
            alt="send"
            className="cursor-pointer w-8 m-2"
          />
        </button>
      </form>
    </div>
  );
};

export default Classification;