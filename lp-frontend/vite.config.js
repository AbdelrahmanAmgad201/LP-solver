import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: './', // Ensures correct file paths
  server: {
    port: 3000,
    host: "0.0.0.0"
  }
})
