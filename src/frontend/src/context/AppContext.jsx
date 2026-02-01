import { createContext, useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { dummyChats, dummyUserData } from "../assets/assets";
import { getCurrentUser } from "../api/userApi";
import { fetchChats } from "../api/chatApi";


const AppContext = createContext()

export const AppContextProvider = ({children}) => {
    const navigate = useNavigate();

    const [user, setUser] = useState(null);
    
    const [chats, setChats] = useState([]);

    const [selectedChat, setSelectedChat] = useState(null);

    const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light');

    const fetchUser = async () => {
    try {
        const data = await getCurrentUser();
        if (data.user) {
        setUser(data.user);
        } else {
        setUser(null);
        }
    } catch (err) {
        console.error(err);
        setUser(null);
    }
    };

    useEffect(() => {
        fetchUser()
    }, [] )
    
    const fetchUserChats = async () => {
        if (!user) return;

        try {
            const data = await fetchChats();
            setChats(data); 
            setSelectedChat(null); 
        } catch (err) {
            console.error("Error fetching chats", err);
        }
    };

    useEffect(() => {
        if (user) {
            fetchUserChats();
        } else {
            setChats([]);
            setSelectedChat(null);
        }
    }, [user])

    useEffect(() => {
        if(theme === 'dark') {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
        localStorage.setItem('theme', theme);
    }, [theme])
    
    const value = {navigate, user, setUser, fetchUser, chats, setChats, selectedChat, setSelectedChat, theme, setTheme}

    return (
        <AppContext.Provider value={value}>
            {children}
        </AppContext.Provider>
    )
}

export const useAppContext = () => useContext(AppContext)