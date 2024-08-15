import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'static/dist/',
    manifest: true,
    rollupOptions: {
      input: [
        'languagecards/components/languagecards.jsx',
//      'languagecards/components/all.jsx',
// Also add to urls.py
      ]
    }
  }
})
