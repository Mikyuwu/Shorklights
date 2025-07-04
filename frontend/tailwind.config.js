module.exports = {
    content: [
        './src/**/*.{html,js,svelte,ts}',
    ],
    theme: {
        extend: {},
    },
    plugins: [
        function ({ addVariant }) {
            addVariant('tall', '@media (min-height: 850px)');
        },
        function ({ addBase, theme }) {
            addBase({
                '--tw-color-green-500': theme('colors.green.500'),
                '--tw-color-pink-500': theme('colors.pink.500'),
                '--tw-color-blue-500': theme('colors.blue.500')
            });
        }
    ],
};