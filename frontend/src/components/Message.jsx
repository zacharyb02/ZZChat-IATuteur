import React, { useEffect } from 'react'
import { assets } from '../assets/assets'
import Markdown from "react-markdown";
import Prism from 'prismjs';

const Message = ({message}) => {

  useEffect(() => {
    Prism.highlightAll();
  }, [message.content])
  
  return (
    <div>
      {message.role === 'user' ? (
        <div className='flex items-start justify-end my-4 gap-2 '>
          <div className='flex flex-col gap-1 p-2 px-4 bg-slate-50 dark:bg-[#57317C]/30 border border-[#80609F]/30 rounded-md max-w-2xl' >
            <p className='text-sm dark:text-primary'>{message.content}</p>
          </div>
        </div>
      ) 
      : 
      (
        <div className='inline-flex flex-col gap-2 p-2 px-4 max-w-2xl bg-primary/20 dark:bg-[#57317C]/30 border border-[#80609F]/30 rounded-md my-4 '>
          {message.isImage ? (
            <img src={message.content} alt="message_icon" className='w-full max-w-md mt-2 rounded-md'/>
          ) 
          :
          (
            <div className='text-sm dark:text-primary reset-tw'>
              <Markdown>
                {message.content}
              </Markdown>
            </div>
          )}

        </div>
      )}
    </div>
  )
}

export default Message