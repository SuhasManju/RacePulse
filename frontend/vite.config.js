import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig(({ mode }) => ({
    base: mode === 'development' ? '/' : '/static/',
    build: {
        outDir: '../static/dist',
        emptyOutDir: true,
        manifest: true,
        rollupOptions: {
            input: {
                main: resolve(__dirname, 'src/main.js'),
            },
        },
    },
    server: {
        origin: 'http://localhost:5173',
        port: 5173,
        strictPort: true,
        watch: {
            usePolling: true,
        },
    },
}));
