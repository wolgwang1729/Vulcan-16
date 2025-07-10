import { createBrowserRouter, RouterProvider, createRoutesFromElements, Route } from 'react-router-dom';
import { createRoot } from 'react-dom/client'
import { StrictMode } from 'react';
import './index.css'
import Layout from './Layout';
import Home from './components/Home';
import HardwareSimulator from './components/HardwareSimulator';

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<Layout />}>
      <Route index element={<Home />} />
      <Route path="hardware-simulator" element={<HardwareSimulator />} />
    </Route>
  )
);


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
