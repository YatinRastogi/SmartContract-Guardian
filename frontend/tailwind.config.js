/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                background: '#0d1117',
                surface: '#161b22',
                border: '#30363d',
                primary: '#238636', // Security Green
                alert: '#da3633',   // Alert Red
                secondary: '#1f6feb', // Blue accent
                text: '#c9d1d9',
                muted: '#8b949e',
            },
            fontFamily: {
                mono: ['ui-monospace', 'SFMono-Regular', 'SF Mono', 'Menlo', 'Consolas', 'Liberation Mono', 'monospace'],
                sans: ['Inter', 'system-ui', 'sans-serif'],
            }
        },
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
}
