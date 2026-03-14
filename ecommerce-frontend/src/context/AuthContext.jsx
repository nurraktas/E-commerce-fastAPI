import { createContext , useContext, useState } from "react";

const AutContext = createContext();

export function AuthProvider({ children }) {
    const [token, setToken] = useState(localStorage.getItem("token") || null);

    const login = (newToken) => {
        localStorage.setItem("token", newToken);
        setToken(newToken);
    };

    const logout = () => {
        localStorage.removeItem("token");
        setToken(null);
    };

    return (
        <AutContext.Provider value={{ token, login, logout, isLoggedIn : !!token }}>
            {children}
        </AutContext.Provider>
    );
}
    export function useAuth() {
    return useContext(AutContext);
}