/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: 'var(--color-primary, #3498db)',
        secondary: 'var(--color-secondary, #2ecc71)',
        background: 'var(--color-background, #ffffff)',
        text: 'var(--color-text, #333333)',
        accent: 'var(--color-accent, #f39c12)',
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            color: theme('colors.text'),
            a: {
              color: theme('colors.primary'),
              '&:hover': {
                color: theme('colors.accent'),
              },
            },
            h1: {
              color: theme('colors.text'),
              fontWeight: '700',
            },
            h2: {
              color: theme('colors.text'),
              fontWeight: '600',
            },
            h3: {
              color: theme('colors.text'),
              fontWeight: '600',
            },
          },
        },
      }),
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};
