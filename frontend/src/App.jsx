import React from 'react'
import SideBar from './components/SideBar'
import { Route, Routes, useLocation } from 'react-router-dom'
import ChatBox from './components/ChatBox'
import Login from './pages/Login'
import Loading from './pages/Loading'
import './assets/prism.css'
import { useAppContext } from './context/AppContext'

const App = () => {

  const {pathname} = useLocation();
  const {user} = useAppContext();

  if(pathname === '/loading') return <Loading />
  return (
    <>
    {user ? (
      <div className='dark:bg-linear-to-b from-[#242124] to-[#000000] dark:text-white'>
        <div className='flex h-screen w-screen'>
          <SideBar />

          <Routes>
            <Route path="/" element={<ChatBox />} />          
            <Route path="/login" element={<ChatBox />} />          
          </Routes>
        </div>

      </div>
    ) : (
      <div className='w-full min-h-screen flex justify-center items-center dark:bg-linear-to-b from-[#242124] to-[#000000] dark:text-white '>
        <Login />
      </div>
    )}
      
    </>
  )
}

export default App