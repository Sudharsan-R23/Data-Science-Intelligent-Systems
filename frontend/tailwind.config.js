/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                brand: {
                    blue: '#2563eb', // Vibrant Blue
                    lightblue: '#dbeafe',
                    orange: '#ff6b35', // Vibrant Orange/Coral
                    lightorange: '#ffedd5',
                    navy: '#1e3a8a',
                    slate: '#f8fafc',
                }
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            },
            borderRadius: {
                '3xl': '1.5rem',
                '4xl': '2rem',
                '5xl': '2.5rem',
            },
            boxShadow: {
                'premium': '0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05)',
                'blue': '0 10px 15px -3px rgba(37, 99, 235, 0.2), 0 4px 6px -4px rgba(37, 99, 235, 0.2)',
                'orange': '0 10px 15px -3px rgba(255, 107, 53, 0.2), 0 4px 6px -4px rgba(255, 107, 53, 0.2)',
            },
            animation: {
                'bounce-subtle': 'bounceSubtle 2s infinite',
            },
            keyframes: {
                bounceSubtle: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-5px)' },
                }
            }
        },
    },
    plugins: [],
}
