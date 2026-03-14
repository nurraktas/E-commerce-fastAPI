import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ProductsPage from "./pages/ProductsPage";
import CartPage from "./pages/CartPage";
import OrdersPage from "./pages/OrdersPage";
import PrivateRoute from "./components/PrivateRoute";

export default function App() {
    return (
        <AuthProvider>
            <BrowserRouter>
                <Navbar />
                <Routes>
                    <Route path="/" element={<ProductsPage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/cart" element={
                        <PrivateRoute>
                            <CartPage />
                        </PrivateRoute>
                    } />
                    <Route path="/orders" element={
                        <PrivateRoute>
                            <OrdersPage />
                        </PrivateRoute>
                    } />
                </Routes>
            </BrowserRouter>
        </AuthProvider>
    )
}